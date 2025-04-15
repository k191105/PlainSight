from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    credits = Column(Integer, default=5)  # Default 5 credits
    created_at = Column(DateTime, default=datetime.utcnow)
    analyses = relationship('ContractAnalysis', back_populates='user')
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

class ContractAnalysis(Base):
    __tablename__ = 'contract_analyses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    original_filename = Column(String(255))
    analysis_results = Column(JSON)  # Store the full analysis results
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='analyses') 