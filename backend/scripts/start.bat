rem create virtual environment
python -m venv env
rem install dependencies
pip install -r './requirements.txt'
rem run the server
main:app --reload --port=8000 --host=0.0.0.0