import requests
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from models.customer import Customer

FLASK_BASE_URL = "http://mock-server:5000"

def fetch_all_customers():
    """Fetch all customers from Flask, handling pagination automatically."""
    all_customers = []
    page = 1
    limit = 10

    while True:
        response = requests.get(f"{FLASK_BASE_URL}/api/customers", params={"page": page, "limit": limit})
        response.raise_for_status()
        data = response.json()

        records = data.get("data", [])
        all_customers.extend(records)

        # Stop when we've fetched everything
        total = data.get("total", 0)
        if len(all_customers) >= total or len(records) == 0:
            break

        page += 1

    return all_customers


def upsert_customers(customers: list, db: Session):
    """Insert customers, update if customer_id already exists."""
    for c in customers:
        stmt = insert(Customer).values(
            customer_id     = c["customer_id"],
            first_name      = c["first_name"],
            last_name       = c["last_name"],
            email           = c["email"],
            phone           = c.get("phone"),
            address         = c.get("address"),
            date_of_birth   = c.get("date_of_birth"),
            account_balance = c.get("account_balance"),
            created_at      = c.get("created_at"),
        ).on_conflict_do_update(
            index_elements=["customer_id"],
            set_={
                "first_name":       c["first_name"],
                "last_name":        c["last_name"],
                "email":            c["email"],
                "phone":            c.get("phone"),
                "address":          c.get("address"),
                "account_balance":  c.get("account_balance"),
            }
        )
        db.execute(stmt)

    db.commit()
    return len(customers)