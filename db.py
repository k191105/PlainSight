from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_URL
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database engine with connection pooling options
try:
    # Configure the engine with pooling options
    engine_args = {}
    
    # Set PostgreSQL-specific connection args
    if DATABASE_URL.startswith('postgresql'):
        engine_args.update({
            'pool_pre_ping': True,       # Verify connections before using
            'pool_recycle': 3600,        # Recycle connections after 1 hour
            'pool_size': 5,              # Connection pool size
            'max_overflow': 10,          # Allow up to 10 connections over pool_size
            'connect_args': {
                'connect_timeout': 10,   # Connection timeout
                'keepalives': 1,         # Enable keepalives
                'keepalives_idle': 30,   # Time before sending keepalive
                'keepalives_interval': 10 # Interval between keepalives
            }
        })
    
    # Create engine
    engine = create_engine(DATABASE_URL, **engine_args)
    logger.info(f"Database connection established successfully")
except Exception as e:
    logger.error(f"Error connecting to database: {str(e)}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created or verified")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

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
    from config import DEFAULT_CREDITS
    
    user = User(email=email, credits=DEFAULT_CREDITS)
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