# Create helper functions for database operations

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

import numpy as np

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    db_expense = models.Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses_by_user(db: Session, user_id: int):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()


def calculate_expense_trend(db: Session, user_id: int):
    expenses = db.query(models.Expense).filter(
        models.Expense.user_id == user_id).all()
    if not expenses:
        return {"message": "No expenses to analyze"}

    amounts = [expense.amount for expense in expenses]
    categories = [expense.category for expense in expenses]

    # Trend analysis (simple example: total and average expenses)
    total_expenses = sum(amounts)
    average_expense = np.mean(amounts)
    category_breakdown = {category: amounts.count(
        category) for category in set(categories)}

    return {
        "total_expenses": total_expenses,
        "average_expense": average_expense,
        "category_breakdown": category_breakdown,
    }
