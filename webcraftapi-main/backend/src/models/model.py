import sys
import os

# Tambahkan src ke Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from database.db import engine, Base  # ← Ganti base jadi Base

# =========================
# Tabel User
# =========================
class User(Base):  # ← Ganti base jadi Base
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    oauth_provider = Column(String, default="google")
    oauth_id = Column(String)
    password_hash = Column(String)
    role = Column(String, nullable=False, default="customer")
    phone_number = Column(String)

    warungs = relationship("Warung", back_populates="owner")
    orders = relationship("Order", back_populates="user")


# =========================
# Tabel Kantin
# =========================
class Kantin(Base):  # ← Ganti base jadi Base
    __tablename__ = "kantin"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    image_url = Column(String)

    warungs = relationship("Warung", back_populates="kantin")


# =========================
# Tabel Warung
# =========================
class Warung(Base):  # ← Ganti base jadi Base
    __tablename__ = "warung"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    kantin_id = Column(Integer, ForeignKey("kantin.id"))
    image_url = Column(String)

    kantin = relationship("Kantin", back_populates="warungs")
    owner = relationship("User", back_populates="warungs")
    menu_items = relationship("MenuItem", back_populates="warung")
    orders = relationship("Order", back_populates="warung")


# =========================
# Tabel MenuItem
# =========================
class MenuItem(Base):  # ← Ganti base jadi Base
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    warung_id = Column(Integer, ForeignKey("warung.id"))
    name = Column(String, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    image_url = Column(String)
    stock = Column(Integer, default=0)

    warung = relationship("Warung", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")


# =========================
# Tabel Order
# =========================
class Order(Base):  # ← Ganti base jadi Base
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    warung_id = Column(Integer, ForeignKey("warung.id"))
    total_price = Column(Numeric(10,2), nullable=False)
    payment_status = Column(String, default="pending")
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="orders")
    warung = relationship("Warung", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


# =========================
# Tabel OrderItem
# =========================
class OrderItem(Base):  # ← Ganti base jadi Base
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Numeric(10,2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")


# =========================
# CREATE / DROP TABLE
# =========================
if __name__ == "__main__":
    print("Dropping old tables...")
    Base.metadata.drop_all(engine)  # ← Ganti base jadi Base
    print("Creating new tables...")
    Base.metadata.create_all(engine)  # ← Ganti base jadi Base
    print("All tables created successfully!")

# =========================
# CREATE / DROP TABLE
# =========================
if __name__ == "__main__":
    print("Dropping old tables...")
    Base.metadata.drop_all(engine)
    print("Creating new tables...")
    Base.metadata.create_all(engine)
    print("All tables created successfully!")