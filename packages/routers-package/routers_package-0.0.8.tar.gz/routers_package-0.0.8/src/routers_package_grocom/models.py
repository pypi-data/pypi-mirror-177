from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, event
import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    username = Column(String)
    email = Column(String(256), index=True, unique=True, nullable=False)
    password_hash = Column(String)
    phone_number = Column(String(256), nullable=False)
    time_zone = Column(String(54), nullable=False)
    businesses = relationship('Business')


class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    jti = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # token = Column(String)
    blacklisted_at = Column(DateTime, default=datetime.datetime.utcnow)