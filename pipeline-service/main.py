from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models.customer import Customer
from services.ingestion import fetch_all_customers, upsert_customers

Base.metadata.create_all(bind=engine)  # Creates the table if it doesn't exist

app = FastAPI()


@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    try:
        customers = fetch_all_customers()
        count = upsert_customers(customers, db)
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    total = db.query(Customer).count()
    customers = db.query(Customer).offset(offset).limit(limit).all()

    return {
        "data": [
            {
                "customer_id":     c.customer_id,
                "first_name":      c.first_name,
                "last_name":       c.last_name,
                "email":           c.email,
                "phone":           c.phone,
                "address":         c.address,
                "date_of_birth":   str(c.date_of_birth) if c.date_of_birth else None,
                "account_balance": float(c.account_balance) if c.account_balance else None,
                "created_at":      str(c.created_at) if c.created_at else None,
            }
            for c in customers
        ],
        "total": total,
        "page": page,
        "limit": limit,
    }


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {
        "customer_id":     customer.customer_id,
        "first_name":      customer.first_name,
        "last_name":       customer.last_name,
        "email":           customer.email,
        "phone":           customer.phone,
        "address":         customer.address,
        "date_of_birth":   str(customer.date_of_birth) if customer.date_of_birth else None,
        "account_balance": float(customer.account_balance) if customer.account_balance else None,
        "created_at":      str(customer.created_at) if customer.created_at else None,
    }