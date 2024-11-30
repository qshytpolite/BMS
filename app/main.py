# Define the main application and endpoints.

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from .auth import authenticate_user, create_access_token, get_current_user
from .database import get_db
from .models import Expense
from PIL import Image
import pytesseract
from typing import List
from collections import defaultdict

router = APIRouter()


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.post("/token")
def login(
    # Use the OAuth2PasswordRequestForm as the request body
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)  # Get the database session
):
    """
    Handle authentication and issue an access token if the user is valid.

    This endpoint takes the username and password from the request body and
    attempts to authenticate the user. If the authentication is successful, it
    issues an access token in the form of a JSON Web Token (JWT).

    The access token is signed with the SECRET_KEY environment variable and
    contains the username in the payload. The token is then returned as a
    JSON response with the key 'access_token' and the value of the issued token.
    """

    # Attempt to authenticate the user
    user = authenticate_user(db, form_data.username, form_data.password)

    # If the authentication fails, return a 401 Unauthorized response
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")

    # If the authentication is successful, issue an access token
    access_token = create_access_token(data={"sub": user.username})

    # Return the access token as a JSON response
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.post("/expenses/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate,
                   db: Session = Depends(database.get_db),
                   current_user: models.User = Depends(get_current_user)):
    # Call the create_expense function from the CRUD module
    # Pass the database session, the expense data, and the current user's ID
    # This function adds the expense to the database and returns the created expense
    return crud.create_expense(db, expense, current_user.id.value)


@app.get("/expenses/", response_model=List[schemas.ExpenseResponse])
def read_expenses(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_expenses_by_user(db, current_user.id.value)


@app.get("/analytics/")
def get_expense_trend(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return crud.calculate_expense_trend(db, current_user.id.value)

# Add Receipt Upload Feature


@app.post("/upload-receipt/")
def upload_receipt(file: UploadFile, current_user: models.User = Depends(get_current_user)):
    image = Image.open(file.file)
    text = pytesseract.image_to_string(image)
    # Basic parsing to extract data (improve with NLP if needed)
    return {"extracted_text": text}

# Add Expense analytics endpoints to provide data for visualization


@router.get("/analytics/expenses")
def get_expense_analytics(db: Session = Depends(get_db)):
    # """Returns aggregated expense data for visualization."""
    # expenses = db.query(Expense).all()

    # Aggregate data
    analytics = {}
    for expense in db.query(Expense).all():
        if expense.category in analytics:
            analytics[expense.category] += expense.amount
        else:
            analytics[expense.category] = expense.amount

    # Format for frontend
    formatted_data = [{"category": key, "amount": value}
                      for key, value in analytics.items()]
    return {"data": formatted_data}
