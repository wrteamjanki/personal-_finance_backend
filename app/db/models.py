from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, func, select
from app.db.database import Base
from sqlalchemy.orm import relationship

# ------------------ Existing Models ------------------

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 👈 Add this
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    note = Column(String, default="", nullable=True)

class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 👈 Add this
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    note = Column(String, default="", nullable=True)

# ------------------ NEW: User Model ------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    savings = relationship("Saving", back_populates="user") 

# ------------------ NEW: Saving Model ------------------

class Saving(Base):
    __tablename__ = "savings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)  # ✅ Match Income/Expense format
    note = Column(String, default="", nullable=True)  # ✅ Optional note
    title = Column(String, nullable=False)

    user = relationship("User", back_populates="savings")  # 👈 Link back to User