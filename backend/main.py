from fastapi import FastAPI, HTTPException,  File, UploadFile, status, Form, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, text
from databases import Database
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import FileResponse
import models
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from typing import Annotated
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from urllib.parse import unquote
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from typing import Annotated, Union
from pydantic import BaseModel

ALGORITHM = "HS256"
Base = declarative_base()

app = FastAPI()

origins = [
    "*"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization"],
)

load_dotenv()
db_name=os.environ.get('DB_NAME')
db_user=os.environ.get('DB_USER')
db_password=os.environ.get('DB_PASSWORD')
db_url=os.environ.get('DB_URL')
db_port=os.environ.get('DB_PORT')
secret_key=os.environ.get('SECRET_KEY')
algorithm=os.environ.get('ALGORITHM'),
token_expiration_time=os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

database_url = f"postgresql://{db_user}:{db_password}@{db_url}:{db_port}/{db_name}"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Connect to the database
database = Database(database_url)
metadata = models.Base.metadata
engine = create_engine(database_url)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Users(Base):
    __tablename__ = "users"
    user_id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String)
    hashed_password: str = Column(String)
    disabled: bool = Column(Boolean)


class UserInDB(Users):
    Users.hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username):
    session = SessionLocal()
    try:
        with session.begin():
            user = session.query(Users).filter(Users.username == username).first()
            if user:
                user_dict = user.__dict__
                user_dict.pop('_sa_instance_state', None)
                return UserInDB(**user_dict)
    finally:
        session.close()


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=135)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.Users, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post('/create_user')
async def create_user(username: str, password: str):
    hashed_password = get_password_hash(password)
    user = Users(username=username, hashed_password=hashed_password)
    user.disabled = False

    async with database.transaction():
            with SessionLocal() as session:
                try:
                    session.add(user)
                    print('Client creat')
                except:
                    print('Failed to create user')
                
                session.commit()
                session.refresh(user)
    return user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user.username)
    access_token_expires = timedelta(minutes=int(token_expiration_time))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return ({"access_token": access_token, "token_type": "bearer"})


@app.get('/')
async def get_all_clients(current_user: Annotated[models.Users, Depends(get_current_active_user)]):
    query = models.Client.__table__.select()
    clients = {
        'clients': database.fetch_all(query)
    }
    return await database.fetch_all(query)

@app.get('/client/{client_id}')
async def get_client_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int):
    async with database.transaction():
        with SessionLocal() as session:
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
    
            return client

def create_user_folders(client_id):
    try:
        os.mkdir(f'./db/{client_id}')
        os.mkdir(f'./db/{client_id}/Contract_Anexa')
        os.mkdir(f'./db/{client_id}/Documente_Incarcate')
        os.mkdir(f'./db/{client_id}/Dosar_Prosumator')
        os.mkdir(f'./db/{client_id}/Factura_Avans')
        os.mkdir(f'./db/{client_id}/Garantii_Client')
        os.mkdir(f'./db/{client_id}/Serie_Inventor')
        os.mkdir(f'./db/{client_id}/Serie_Panouri')
        os.mkdir(f'./db/{client_id}/Serie_Smart_Meter')
        os.mkdir(f'./db/{client_id}/Certificat_Racordare')
        print('folders created')
    except:
        print('Folders already exists!')
        os.remove(f'./db/{client_id}')
        create_user_folders(client_id)


@app.post('/client/create_client/{client_name}', status_code=status.HTTP_201_CREATED)
async def create_new_client(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_name: str):
    new_client = models.Client(
        client_name=client_name,
        documente_incarcate="NEINCARCAT",
        contract_si_anexa="NEINCARCAT", 
        factura_avans="NEINCARCAT", 
        serie_inventor="NEINCARCAT", 
        serie_smart_meter="NEINCARCAT", 
        serie_panouri="NEINCARCAT", 
        dosar_prosumator="NEINCARCAT",
        certificat_racordare="NEINCARCAT", 
        garantii_client="NEINCARCAT",
        documente_incarcate_nume_fisier="",
        contract_si_anexa_nume_fisier="",
        factura_avans_nume_fisier="",
        serie_inventor_nume_fisier="",
        serie_smart_meter_nume_fisier="",
        serie_panouri_nume_fisier="",
        dosar_prosumator_nume_fisier="",
        certificat_racordare_nume_fisier = "",
        garantii_client_nume_fisier=""
        )
    async with database.transaction():
            with SessionLocal() as session:
                try:
                    session.add(new_client)
                    print('Client creat')
                except:
                    print('Failed to create user')
                
                session.commit()
                session.refresh(new_client)
            
            create_user_folders(new_client.client_id)
    
    return {"client_id": new_client.client_id, "client_name": new_client.client_name}


@app.put('/upload_certificat_racordare/{client_id}')
async def update_certificat_racordare(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, new_certificat_racordare: list[UploadFile]):
    destination = Path(f'db/{client_id}/Certificat_Racordare')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in new_certificat_racordare:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.certificat_racordare = "INCARCAT"
            client.certificat_racordare_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client

@app.put('/upload_serie_inventor/{client_id}')
async def update_serie_inventor(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, new_serie_inventor: list[UploadFile]):
    destination = Path(f'db/{client_id}/Serie_Inventor')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in new_serie_inventor:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.serie_inventor = "INCARCAT"
            client.serie_inventor_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client


@app.put('/upload_serie_smart_meter/{client_id}')
async def update_serie_smart_meter(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, new_serie_smart_meter: list[UploadFile]):
    destination = Path(f'db/{client_id}/Serie_Smart_Meter')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in new_serie_smart_meter:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.serie_smart_meter = "INCARCAT"
            client.serie_smart_meter_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client

@app.put('/upload_serie_panouri/{client_id}')
async def upload_and_update_serie_panouri(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, serie_panouri: list[UploadFile]):
    destination = Path(f'db/{client_id}/Serie_Panouri')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in serie_panouri:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.serie_panouri = "INCARCAT"
            client.serie_panouri_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client


@app.put('/upload_documente_incarcate/{client_id}')
async def upload_and_update_documente_incarcate(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, document: list[UploadFile]):
    destination = Path(f'db/{client_id}/Documente_Incarcate')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in document:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.documente_incarcate = "INCARCAT"
            client.documente_incarcate_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client



@app.put('/upload_contract_anexa/{client_id}')
async def upload_and_update_contract_anexa(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, contract_anexa: list[UploadFile]):
    destination = Path(f'db/{client_id}/Contract_Anexa')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in contract_anexa:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.contract_si_anexa = "INCARCAT"
            client.contract_si_anexa_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client


@app.put('/upload_factura_avans/{client_id}')
async def upload_and_update_factura_avans(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, factura: list[UploadFile]):
    destination = Path(f'db/{client_id}/Factura_Avans')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in factura:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.factura_avans = "INCARCAT"
            client.factura_avans_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client


@app.put('/upload_dosar_prosumator/{client_id}')
async def upload_and_update_dosar_prosumator(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, dosar: list[UploadFile]):
    destination = Path(f'db/{client_id}/Dosar_Prosumator')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in dosar:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.dosar_prosumator = "INCARCAT"
            client.dosar_prosumator_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client

@app.put('/upload_garantii_client/{client_id}')
async def upload_and_update_garantii_client(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, garantii: list[UploadFile]):
    destination = Path(f'db/{client_id}/Garantii_Client')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    files_name = []
    for upload_file in garantii:
        destination_file_name = os.path.join(destination, upload_file.filename)
        try:
            with Path(destination_file_name).open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            for f in existing_files:
                if not os.path.basename(f) == upload_file.filename:
                    print()
                    #os.remove(f)
        finally:
            print('document_uploaded!')
            files_name.append(upload_file.filename)
    async with database.transaction():
        with SessionLocal() as session:
            # Retrieve the item by item_id
            client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            
            client.garantii_client = "INCARCAT"
            client.garantii_client_nume_fisier = ','.join(files_name)

            session.commit()
            session.refresh(client)
        
    return client


@app.get('/certificat_racordare/{client_id}')
async def download_certificat_de_racordare_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Certificat_Racordare')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/documente_incarcate/{client_id}')
async def download_documente_incarcate_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Documente_Incarcate')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/contract_anexa/{client_id}')
async def download_contract_anexa_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Contract_Anexa')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/factura_avans/{client_id}')
async def download_factura_avans_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Factura_Avans')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/dosar_prosumator/{client_id}')
async def download_dosar_prosumator_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Dosar_Prosumator')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/garantii_client/{client_id}')
async def download_garantii_client_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Garantii_Client')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/serie_inventor/{client_id}')
async def download_serie_inventor_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Serie_Inventor')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/serie_panouri/{client_id}')
async def download_serie_panouri_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Serie_Panouri')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/serie_smart_meter/{client_id}')
async def downloadserie_smart_meter_by_id(current_user: Annotated[models.Users, Depends(get_current_active_user)], client_id: int, file_name:str):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Serie_Smart_Meter')
    file_path = ''
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_names = os.listdir(document_path)
    except:
        file_names = None
    if file_names is not None:
        for file in file_names:
            if file == file_name[0: -1]:
                file_path = os.path.join(document_path, file)
                if not os.path.exists(file_path):
                    raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))
