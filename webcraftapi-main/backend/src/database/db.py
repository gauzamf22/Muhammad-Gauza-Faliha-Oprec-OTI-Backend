from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# =========================
# Konfigurasi Database
# =========================

# Langsung pakai DATABASE_URL (password sudah di-encode: awkwkwk128@#!)
DATABASE_URL="postgresql://postgres.xvjoxzfbctpfdbtiuchb:R4pl4Webcraft@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres"
engine = create_engine(DATABASE_URL, echo=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base untuk model
Base = declarative_base()


# =========================
# Dependency untuk FastAPI
# =========================
def get_db():
    """
    Generator function untuk database session.
    Dipakai di FastAPI sebagai dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
