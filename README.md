* Full stack application with FastApi and PostgreSQL DB *

** This application performs Read & Update Operations over a postgresql database.
**	The use has the possibility to read all items from the database, update rows, upload and download files while
**	automatically updating the database. 

** Installation **
 
 1. Clone this repository or download the archive: 
 https://github.com/boghas/Ses-Aplicatie.git
 
 * If you don't have git installed, you can get it from
 https://git-scm.com/downloads
 
 2. Install PostgreSQL & setup your database
 https://www.postgresql.org/download/
 
 3. Create a Python virtual environmnet. From the /backend direcory run:
 python -m venv env
 
 4. Start the environment:
For Windows: /backend/env/Scripts/Activate.ps1

5. Install dependencies. From the /backend direcory run:
pip install -r

6. Create the .env file and set your variables:
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_URL=your_db_url
DB_PORT=yout_db_port

7. Run the server. From the /backend direcory run:
uvicorn main:app --reload


React:


npx create-react-app ses-app

cd /ses-app/
npm start 


npm install axios

npm i react-data-table-component

npm install json-server
npm i react-router-dom
npm start