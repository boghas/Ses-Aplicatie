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


app = FastAPI()

origins = [
    "*"  # Replace this with the actual origin of your frontend
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


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> models.Token:
    user = models.authenticate_user(models.fake_users_db, form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user)
    access_token_expires = timedelta(minutes=models.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = models.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return ({"access_token": access_token, "token_type": "bearer"})
    #return models.Token(access_token=access_token, token_type="bearer")


@app.get('/')
async def get_all_clients(current_user: Annotated[models.User, Depends(models.get_current_active_user)]):
    query = models.Client.__table__.select()
    clients = {
        'clients': database.fetch_all(query)
    }
    return await database.fetch_all(query)

@app.get('/client/{client_id}')
async def get_client_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
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
async def create_new_client(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_name: str):
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
    print('inserting into database')
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
async def update_certificat_racordare(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, new_certificat_racordare: list[UploadFile]):
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
async def update_serie_inventor(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, new_serie_inventor: UploadFile):
    print('test')
    print(new_serie_inventor.filename)
    destination = Path(f'db/{client_id}/Serie_Inventor')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    destination_file_name = os.path.join(destination, new_serie_inventor.filename)
    try:
        with Path(destination_file_name).open("wb") as buffer:
            shutil.copyfileobj(new_serie_inventor.file, buffer)
        for f in existing_files:
            if not os.path.basename(f) == new_serie_inventor.filename:
                os.remove(f)
        async with database.transaction():
            with SessionLocal() as session:
                # Retrieve the item by item_id
                client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
                if not client:
                    raise HTTPException(status_code=404, detail="Client not found")

                client.serie_inventor = "INCARCAT"
                client.serie_inventor_nume_fisier = new_serie_inventor.filename

                session.commit()
                session.refresh(client)
    finally:
        print('document_uploaded!')
    return client


@app.put('/upload_serie_smart_meter/{client_id}')
async def update_serie_smart_meter(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, new_serie_smart_meter: UploadFile):
    destination = Path(f'db/{client_id}/Serie_Smart_Meter')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    destination_file_name = os.path.join(destination, new_serie_smart_meter.filename)
    try:
        with Path(destination_file_name).open("wb") as buffer:
            shutil.copyfileobj(new_serie_smart_meter.file, buffer)
        for f in existing_files:
            if not os.path.basename(f) == new_serie_smart_meter.filename:
                os.remove(f)
        async with database.transaction():
            with SessionLocal() as session:
                # Retrieve the item by item_id
                client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
                if not client:
                    raise HTTPException(status_code=404, detail="Client not found")

                client.serie_smart_meter = "INCARCAT"
                client.serie_smart_meter_nume_fisier = new_serie_smart_meter.filename

                session.commit()
                session.refresh(client)
    finally:
        print('document_uploaded!')
    return client


@app.put('/upload_serie_panouri/{client_id}')
async def upload_and_update_serie_panouri(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, serie_panouri: UploadFile):
    destination = Path(f'db/{client_id}/Serie_Panouri')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    destination_file_name = os.path.join(destination, serie_panouri.filename)
    try:
        with Path(destination_file_name).open("wb") as buffer:
            shutil.copyfileobj(serie_panouri.file, buffer)
        for f in existing_files:
            if not os.path.basename(f) == serie_panouri.filename:
                os.remove(f)
        async with database.transaction():
            with SessionLocal() as session:
                # Retrieve the item by item_id
                client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
                if not client:
                    raise HTTPException(status_code=404, detail="Client not found")

                client.serie_panouri = "INCARCAT"
                client.serie_panouri_nume_fisier = serie_panouri.filename

                session.commit()
                session.refresh(client)
    finally:
        print('document_uploaded!')
    return client


@app.put('/upload_documente_incarcate/{client_id}')
async def upload_and_update_documente_incarcate(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, document: UploadFile):
    destination = Path(f'db/{client_id}/Documente_Incarcate')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    destination_file_name = os.path.join(destination, document.filename)
    try:
        with Path(destination_file_name).open("wb") as buffer:
            shutil.copyfileobj(document.file, buffer)
        for f in existing_files:
            if not os.path.basename(f) == document.filename:
                os.remove(f)
        async with database.transaction():
            with SessionLocal() as session:
                # Retrieve the item by item_id
                client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
                if not client:
                    raise HTTPException(status_code=404, detail="Client not found")

                client.documente_incarcate = "INCARCAT"
                client.documente_incarcate_nume_fisier = document.filename

                session.commit()
                session.refresh(client)
    finally:
        print('document_uploaded!')
    return client


@app.put('/upload_contract_anexa/{client_id}')
async def upload_and_update_contract_anexa(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, contract_anexa: UploadFile):
    destination = os.path.join(os.path.join('db', str(client_id)), 'Contract_Anexa')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        print('this')
        raise HTTPException(status_code=404, detail="Client not found")
    destination_file_name = os.path.join(destination, contract_anexa.filename)
    print('nah')
    try:
        with Path(destination_file_name).open("wb") as buffer:
            shutil.copyfileobj(contract_anexa.file, buffer)
        for f in existing_files:
            if not os.path.basename(f) == contract_anexa.filename:
                os.remove(f)
        async with database.transaction():
            with SessionLocal() as session:
                # Retrieve the item by item_id
                client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
                if not client:
                    raise HTTPException(status_code=404, detail="Client not found")

                client.contract_anexa = "INCARCAT"
                client.contract_anexa_nume_fisier = contract_anexa.filename

                session.commit()
                session.refresh(client)
    finally:
        print('document_uploaded!')
    return client
    

@app.put('/upload_factura_avans/{client_id}')
async def upload_and_update_factura_avans(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, factura: UploadFile):
    destination = os.path.join(os.path.join('db', str(client_id)), 'Factura_Avans')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    destination_file_name = os.path.join(destination, factura.filename)
    try:
        with Path(destination_file_name).open("wb") as buffer:
            shutil.copyfileobj(factura.file, buffer)
        for f in existing_files:
            if not os.path.basename(f) == factura.filename:
                os.remove(f)
        async with database.transaction():
            with SessionLocal() as session:
                # Retrieve the item by item_id
                client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
                if not client:
                    raise HTTPException(status_code=404, detail="Client not found")

                client.factura_avans = "INCARCAT"
                client.factura_avans_nume_fisier = factura.filename

                session.commit()
                session.refresh(client)
    finally:
        print('document_uploaded!')
    return client


@app.put('/upload_dosar_prosumator/{client_id}')
async def upload_and_update_dosar_prosumator(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, dosar: UploadFile):
    destination = os.path.join(os.path.join('db', str(client_id)), 'Dosar_Prosumator')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    destination_file_name = os.path.join(destination, dosar.filename)
    try:
        with Path(destination_file_name).open("wb") as buffer:
            shutil.copyfileobj(dosar.file, buffer)
        for f in existing_files:
            if not os.path.basename(f) == dosar.filename:
                os.remove(f)
        async with database.transaction():
            with SessionLocal() as session:
                # Retrieve the item by item_id
                client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
                if not client:
                    raise HTTPException(status_code=404, detail="Client not found")

                client.dosar_prosumator = "INCARCAT"
                client.dosar_prosumator = dosar.filename

                session.commit()
                session.refresh(client)
    finally:
        print('document_uploaded!')
    return client


@app.put('/upload_garantii_client/{client_id}')
async def upload_and_update_garantii_client(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int, garantii: UploadFile):
    try:
        print('here')
    except Exception as e:
        print(e)
    destination = os.path.join(os.path.join('db', str(client_id)), 'Garantii_Client')
    existing_files = [os.path.join(destination, f) for f in os.listdir(destination)]
    if not os.path.exists(destination):
        raise HTTPException(status_code=404, detail="Client not found")
    destination_file_name = os.path.join(destination, garantii.filename)
    try:
        with Path(destination_file_name).open("wb") as buffer:
            shutil.copyfileobj(garantii.file, buffer)
        for f in existing_files:
            if not os.path.basename(f) == garantii.filename:
                os.remove(f)
        async with database.transaction():
            with SessionLocal() as session:
                # Retrieve the item by item_id
                client = session.query(models.Client).filter(models.Client.client_id == client_id).first()
                if not client:
                    raise HTTPException(status_code=404, detail="Client not found")

                client.garantii_client = "INCARCAT"
                client.garantii_client = garantii.filename

                session.commit()
                session.refresh(client)
    finally:
        print('document_uploaded!')
    #return client


@app.get('/documente_incarcate/{client_id}')
async def download_documente_incarcate_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
    print('test')
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Documente_Incarcate')
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_name = os.listdir(document_path)[0]
    except:
        file_name = None
    if file_name is not None:
        file_path = os.path.join(document_path, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/contract_anexa/{client_id}')
async def download_contract_anexa_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Contract_Anexa')
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_name = os.listdir(document_path)[0]
    except:
        file_name = None
    if file_name is not None:
        file_path = os.path.join(document_path, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/factura_avans/{client_id}')
async def download_factura_avans_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
    print('test')
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Factura_Avans')
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_name = os.listdir(document_path)[0]
    except:
        file_name = None
    if file_name is not None:
        file_path = os.path.join(document_path, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/dosar_prosumator/{client_id}')
async def download_dosar_prosumator_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Dosar_Prosumator')
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_name = os.listdir(document_path)[0]
    except:
        file_name = None
    if file_name is not None:
        file_path = os.path.join(document_path, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/garantii_client/{client_id}')
async def download_garantii_client_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Garantii_Client')
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_name = os.listdir(document_path)[0]
    except:
        file_name = None
    if file_name is not None:
        file_path = os.path.join(document_path, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/serie_inventor/{client_id}')
async def download_serie_inventor_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Serie_Inventor')
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_name = os.listdir(document_path)[0]
    except:
        file_name = None
    if file_name is not None:
        file_path = os.path.join(document_path, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/serie_panouri/{client_id}')
async def download_serie_panouri_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Serie_Panouri')
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_name = os.listdir(document_path)[0]
    except:
        file_name = None
    if file_name is not None:
        file_path = os.path.join(document_path, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))


@app.get('/serie_smart_meter/{client_id}')
async def downloadserie_smart_meter_by_id(current_user: Annotated[models.User, Depends(models.get_current_active_user)], client_id: int):
    db_id_path = os.path.join('db', str(client_id))
    document_path = os.path.join(db_id_path, 'Serie_Smart_Meter')
    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        file_name = os.listdir(document_path)[0]
    except:
        file_name = None
    if file_name is not None:
        file_path = os.path.join(document_path, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found!")
    return FileResponse(path=file_path, filename=os.path.basename(file_path))