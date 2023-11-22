# Plant Classifier Backend API
To run the backend API, run the following commands: <br>
`pip install -r requirements.txt` <br><br>
`pip3 install torch torchvision` <br><br>
`python3 main.py` <br>
OR <br>
`gunicorn app:app --workers 2 --worker-class uvicorn.workers.UvicornWorker` <br><br>
Opens port 8000 <br>