from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    # Define the reverse relationship to Vehicle
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")

class Vehicle(Base):
    __tablename__ = "vehicle"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symboling = Column(Integer, nullable=False)
    CarName = Column(String(255), nullable=False)
    fueltype = Column(String(50), nullable=False)
    aspiration = Column(String(50), nullable=False)
    doornumber = Column(Integer, nullable=False)
    carbody = Column(String(50), nullable=False)
    drivewheel = Column(String(50), nullable=False)
    enginelocation = Column(String(50), nullable=False)
    wheelbase = Column(Float, nullable=False)
    carlength = Column(Float, nullable=False)
    carwidth = Column(Float, nullable=False)
    carheight = Column(Float, nullable=False)
    curbweight = Column(Float, nullable=False)
    enginetype = Column(String(50), nullable=False)
    cylindernumber = Column(Integer, nullable=False)
    enginesize = Column(Integer, nullable=False)
    fuelsystem = Column(String(50), nullable=False)
    boreratio = Column(Float, nullable=False)
    stroke = Column(Float, nullable=False)
    compressionratio = Column(Float, nullable=False)
    horsepower = Column(Integer, nullable=False)
    peakrpm = Column(Integer, nullable=False)
    citympg = Column(Integer, nullable=False)
    highwaympg = Column(Integer, nullable=True)
    price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Define the relationship back to User
    owner = relationship("User", back_populates="vehicles")
