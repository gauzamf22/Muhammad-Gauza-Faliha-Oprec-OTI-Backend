# Penugasan Backend OmahTI 2025

Ini adalah submission untuk penugasan Backend Division OmahTI 2025. Proyek ini adalah RESTful API untuk sistem manajemen kantin digital yang dibangun menggunakan Python, FastAPI, SQLAlchemy, dan PostgreSQL (Supabase).


## Dokumentasi Postman Untuk Login dan Register 
https://gauzamf22-2508967.postman.co/workspace/Muhammad-Gauza-Faliha's-Workspa~6c09f98e-5c2c-44f6-8620-7fcccff11730/collection/49766368-26ad752a-8677-42d4-ba7c-f78f30c9a9aa?action=share&creator=49766368

## 🌐 Database Connection

API ini terhubung dengan PostgreSQL database yang di-hosting di Supabase.

* **Database Host**: `aws-1-ap-southeast-2.pooler.supabase.com`
* **Database Type**: PostgreSQL
* **ORM**: SQLAlchemy

## 📊 Database Schema

Project ini memiliki 6 tabel utama:

1. **Users** - Tabel pengguna (customer & pemilik warung)
2. **Kantin** - Tabel kantin/food court
3. **Warung** - Tabel warung/tenant dalam kantin
4. **Menu Items** - Tabel menu makanan/minuman
5. **Orders** - Tabel pesanan
6. **Order Items** - Tabel detail item dalam pesanan

### Entity Relationship:
```
Users ─┬─> Warung (sebagai owner)
       └─> Orders (sebagai customer)

Kantin ──> Warung (one-to-many)

Warung ─┬─> Menu Items (one-to-many)
        └─> Orders (one-to-many)

Orders ──> Order Items (one-to-many)

Menu Items ──> Order Items (one-to-many)
```

## 🛠️ Tech Stack

* **Language**: Python 3.x
* **Framework**: FastAPI (planned)
* **ORM**: SQLAlchemy
* **Database**: PostgreSQL (Supabase Connection Pooler)
* **Authentication**: OAuth 2.0 (Google) + JWT (planned)

## 📁 Project Structure
```
webcraftapi-main/
├── backend/
│   └── src/
│       ├── database/
│       │   ├── __init__.py
│       │   └── db.py          # Database configuration
│       ├── models/
│       │   ├── __init__.py
│       │   └── model.py       # SQLAlchemy models
│       └── schemas/
│           ├── kantin.py
│           ├── login.py
│           ├── menuitem.py
│           ├── order.py
│           ├── orderitem.py
│           ├── users.py
│           └── warung.py
```

## 🚀 Setup & Installation

### 1. Clone Repository
```bash
git clone https://github.com/gauzamf22/Muhammad-Gauza-Faliha-Oprec-OTI-Backend.git
cd Muhammad-Gauza-Faliha-Oprec-OTI-Backend/webcraftapi-main/backend/src
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install sqlalchemy psycopg2-binary fastapi uvicorn
```

### 3. Setup Database
Jalankan script untuk membuat tables di database:
```bash
python -m models.model
```

Expected output:
```
Dropping old tables...
Creating new tables...
All tables created successfully!
```

### 4. Verifikasi Database
Cek di Supabase Dashboard:
1. Login ke [supabase.com](https://supabase.com)
2. Pilih project
3. Buka **Table Editor**
4. Pastikan 6 tabel sudah terbuat

## 📝 Database Models

### User Model
```python
- id (Primary Key)
- name
- email (Unique)
- oauth_provider (default: "google")
- oauth_id
- password_hash
- role (default: "customer")
- phone_number
```

### Kantin Model
```python
- id (Primary Key)
- name
- description
- location
- image_url
```

### Warung Model
```python
- id (Primary Key)
- name
- owner_id (Foreign Key -> users.id)
- kantin_id (Foreign Key -> kantin.id)
- image_url
```

### MenuItem Model
```python
- id (Primary Key)
- warung_id (Foreign Key -> warung.id)
- name
- price (Numeric 10,2)
- image_url
- stock
```

### Order Model
```python
- id (Primary Key)
- user_id (Foreign Key -> users.id)
- warung_id (Foreign Key -> warung.id)
- total_price (Numeric 10,2)
- payment_status (default: "pending")
- created_at (Timestamp)
```

### OrderItem Model
```python
- id (Primary Key)
- order_id (Foreign Key -> orders.id)
- menu_item_id (Foreign Key -> menu_items.id)
- quantity
- price_at_purchase (Numeric 10,2)
```

## 🔐 Security Notes (Tidak ada SQL Injection)

⚠️ **IMPORTANT**: Jangan commit credential ke repository!

Untuk production, gunakan environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# dst...
```

## 👨‍💻 Author

**Muhammad Gauza Faliha**  
Backend Developer Candidate - OmahTI 2025

## 📄 License

This project is created for OmahTI 2025 Backend Division recruitment purposes.
```

**File tambahan yang perlu dibuat:**

**`.gitignore`:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# IDE
.vscode/
.idea/

# Database
*.db
*.sqlite3

# Logs
*.log
```

**`requirements.txt`:**
```
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
pydantic==2.5.0
