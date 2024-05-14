from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated, Union
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt


Base = declarative_base()

# Authentication
class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean)


class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String)
    documente_incarcate = Column(String)
    contract_si_anexa = Column(String)
    factura_avans = Column(String)
    serie_inventor = Column(String)
    serie_smart_meter = Column(String)
    serie_panouri = Column(String)
    dosar_prosumator = Column(String)
    certificat_racordare= Column(String)
    garantii_client = Column(String)
    documente_incarcate_nume_fisier = Column(String)
    contract_si_anexa_nume_fisier = Column(String)
    factura_avans_nume_fisier = Column(String)
    serie_inventor_nume_fisier = Column(String)
    serie_smart_meter_nume_fisier = Column(String)
    serie_panouri_nume_fisier = Column(String)
    dosar_prosumator_nume_fisier = Column(String)
    certificat_racordare_nume_fisier = Column(String)
    garantii_client_nume_fisier = Column(String)
