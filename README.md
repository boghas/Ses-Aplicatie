- Full stack application with FastApi and PostgreSQL DB \*

** This application performs Read & Update Operations over a postgresql database.
** The use has the possibility to read all items from the database, update rows, upload and download files while
\*\* automatically updating the database.

** Installation **

1.  Clone this repository or download the archive:
    https://github.com/boghas/Ses-Aplicatie.git

- If you don't have git installed, you can get it from
  https://git-scm.com/downloads

2.  Install PostgreSQL & setup your database
    https://www.postgresql.org/download/

3.  Create a Python virtual environmnet. From the /backend direcory run:
    python -m venv env

4.  Start the environment:
    For Windows: /backend/env/Scripts/Activate.ps1

5.  Install dependencies. From the /backend direcory run:
    pip install -r

6.  Create the .env file and set your variables:
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_URL=your_db_url
    DB_PORT=yout_db_port

7.  Run the server. From the /backend direcory run:
    uvicorn main:app --reload

openssl rand -hex 32

React:

create new vite project
npm create vite@latest
npm i
npm run dev

npx create-react-app ses-app

cd /ses-app/
npm start

npm install axios

npm i react-data-table-component

npm install json-server
npm i react-router-dom
npm i file-saver
npm i jwt-decode
npm i bootstrap@5.3.3
npm i dotenv
npm start
json-server react-data-table-component react-router-dom file-saver jwt-decode bootstrap@5.3.3 dotenv

docker build -t my-vite-react-app .

docker run -p 8080:80 my-vite-react-app

docker build -t backend .

docker run -p 80:80 backend

docker-compose up --build

npm install --global serve
