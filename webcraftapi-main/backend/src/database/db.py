from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# =========================
# Konfigurasi Database
# =========================

# Connection string Supabase temanmu
DB_USER = "postgres.xvjoxzfbctpfdbtiuchb"
DB_PASSWORD = "R4pl4Webcraft"
DB_HOST = "aws-1-ap-southeast-2.pooler.supabase.com"
DB_PORT = "5432"
DB_NAME = "postgres"

# URL encode password jika ada karakter khusus
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True supaya SQL terlihat di console

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base untuk model
base = declarative_base()