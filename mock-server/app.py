from flask import Flask, jsonify, request
import json
import math

app = Flask(__name__)

# Load customers from JSON file
with open("data/customers.json") as f:
    customers = json.load(f)

@app.route("/api/health")
def health():
    return jsonify({"status": "up"}), 200

@app.route("/api/customers")
def get_customers():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    start = (page - 1) * limit
    end = start + limit  
    total = len(customers)
    data = customers[start:end]
    return jsonify({
        "data": data,
        "total": total,
        "page": page,
        "limit": limit
    })

@app.route("/api/customers/<string:customer_id>")
def get_customer(customer_id):
    customer = next((c for c in customers if c["customer_id"] == customer_id), None)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)