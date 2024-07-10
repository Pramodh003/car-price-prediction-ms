from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP,text
from .config.database import Base , get_db

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index=True)
    email = Column(String(100), nullable = False, unique = True)
    password = Column(String(100), nullable = False)
    date_created = Column(TIMESTAMP(timezone=True),
                          nullable=False, server_default=text('now()'))
    date_modified = Column(TIMESTAMP(timezone=True), nullable=False,
                           server_default=text('now()'), onupdate=text('now()'))
    
    