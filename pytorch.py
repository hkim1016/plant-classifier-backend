import torch
import torch.nn as nn
from torchvision import models, transforms

from PIL import Image

import os
import json
import pandas as pd
from http import HTTPStatus

class BadRequestException(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

def load_model(model, filename):
    if not os.path.exists(filename):
        raise FileNotFoundError
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    d = torch.load(filename, map_location=device)
    model.load_state_dict(d['model'])

def get_model():
    classes = 1081
    save_dir = os.path.join(os.getcwd(), 'model')
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, classes)
    load_model(model, os.path.join(save_dir, 'data01_weights_best_acc.tar'))

    return model

__classes_df = pd.read_csv('classes.csv')

__species_json_file = open('./plantnet300K_species_names.json', 'r')
__species_json = json.load(__species_json_file)

__device = (
    'cuda'
    if torch.cuda.is_available()
    else 'cpu'
)
__model = get_model()
__model.to(__device)
# __model.eval()

def analyze_plant(img):
    try:
        __model.eval()

        test_transform = transforms.Compose([
            transforms.Resize(224),
            # transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        img = Image.open(img).convert('RGB')
        img = test_transform(img)
        img = img.unsqueeze(0)

        with torch.no_grad():
            outputs = __model(img)
            _, preds = torch.max(outputs, 1)

            classID = str(__classes_df.loc[__classes_df['index'] == preds[0].item()].iloc[0]['class'])
            plantTypeList = __species_json[classID].split('_')
            plantType = plantTypeList[0] + ' ' + plantTypeList[1].capitalize()

            print(f'Predicted class ID : {classID}')
            print(f'Plant Species Name : {plantType}')
        
        return {
            'ClassID': classID,
            'PlantType': plantType
        }
    except Exception as e:
        print('Error', e)
        raise BadRequestException('Something went wrong', HTTPStatus.BAD_REQUEST)
    
def analyze_plant_live_view(img):
    try:
        __model.eval()

        test_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        img = test_transform(img)
        img = img.unsqueeze(0)

        with torch.no_grad():
            outputs = __model(img)
            _, preds = torch.max(outputs, 1)

            classID = str(__classes_df.loc[__classes_df['index'] == preds[0].item()].iloc[0]['class'])
            plantTypeList = __species_json[classID].split('_')
            plantType = plantTypeList[0] + ' ' + plantTypeList[1].capitalize()

            print(f'Predicted class ID : {classID}')
            print(f'Plant Species Name : {plantType}')
        
        return {
            'ClassID': classID,
            'PlantType': plantType
        }
    except Exception as e:
        print('Error', e)
        raise BadRequestException('Something went wrong', HTTPStatus.BAD_REQUEST)

if __name__ == '__main__':
    img = Image.open('./bitter_lettuce.jpeg')
    analyze_plant(img)