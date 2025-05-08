# models.py

import os
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import (
    create_engine, Column, Integer, String,
    DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# ---------------------------------------------------
# Configuración de la base de datos
# ---------------------------------------------------
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data.db')
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Para SQLite
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------------------------------------------------
# Modelos
# ---------------------------------------------------

class User(UserMixin, Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    role     = Column(String, nullable=False)

    def get_id(self):
        return self.username

class Residence(Base):
    __tablename__ = 'residences'

    id       = Column(String, primary_key=True)
    name     = Column(String, nullable=False)
    url_base = Column(String, nullable=False)
    type     = Column(String, nullable=False)

    # Relación uno-a-muchos con Relay
    relays = relationship(
        'Relay',
        back_populates='residence',
        cascade='all, delete-orphan'
    )

class Relay(Base):
    __tablename__ = 'relays'

    id            = Column(Integer, primary_key=True, autoincrement=True)
    residence_id  = Column(String, ForeignKey('residences.id'), nullable=False)
    relay_id      = Column(Integer, nullable=False)   # El número de relay en el dispositivo
    name          = Column(String, nullable=False)
    cmd_template  = Column(String, nullable=False)

    # Relación inversa
    residence = relationship('Residence', back_populates='relays')

class Log(Base):
    __tablename__ = 'logs'

    id           = Column(Integer, primary_key=True, autoincrement=True)
    ts           = Column(DateTime, default=datetime.utcnow, nullable=False)
    user         = Column(String, nullable=False)
    residence_id = Column(String, nullable=False)
    relay_id     = Column(Integer, nullable=False)
    action       = Column(String, nullable=False)  # 'ON', 'OFF', 'PING', etc.
    duration     = Column(Integer, nullable=False)  # Segundos de activación
    result       = Column(String)                  # Texto con el resultado de la acción

# ---------------------------------------------------
# Crear las tablas en la base de datos
# ---------------------------------------------------
Base.metadata.create_all(bind=engine)
