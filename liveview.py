import cv2
import time
from pytorch import analyze_plant_live_view, get_model

def processVideo():
    cap = cv2.VideoCapture(0)

    (success, image) = cap.read()

    startTime = 0

    while success:
        currentTime = time.time()
        fps = 1/(currentTime - startTime)
        startTime = currentTime
        plant = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        output = analyze_plant_live_view(plant)
        # print(f'Output : {output}')

        cv2.putText(image, "FPS: " + str(int(fps)), (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
        cv2.imshow('Custom ResNet18 Inference', image)
        (success, image) = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    processVideo()