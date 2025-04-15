from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(db, email, password):
    """Create a new user"""
    from models import User
    user = User(email=email)
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db, email):
    """Get a user by email"""
    from models import User
    return db.query(User).filter(User.email == email).first()

def save_analysis(db, user_id, filename, analysis_results):
    """Save a contract analysis"""
    from models import ContractAnalysis
    analysis = ContractAnalysis(
        user_id=user_id,
        original_filename=filename,
        analysis_results=analysis_results
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis 