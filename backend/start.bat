rem create virtual environment
python -m venv env
rem Copy the .env file to backend folder
cp .env backend\
rem acticate the env
env\Scripts\activate.bat && pip install -r requirements.txt && uvicorn main:app --reload --port=8000 --host=0.0.0.0 
