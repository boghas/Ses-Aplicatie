from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String)
    documente_incarcate = Column(String)
    contract_anexa = Column(String)
    factura_avans = Column(String)
    serie_inventor = Column(String)
    serie_smart_meter = Column(String)
    serie_panouri = Column(String)
    dosar_prosumator = Column(String)
    garantii_client = Column(String)