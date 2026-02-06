from flask import Flask, request, jsonify
from flask_cors import CORS
from models import visits_collection
from datetime import datetime

app = Flask(__name__)
CORS(app)

# -------------------------------
# POST: Create new visit (Visitor Form)
# -------------------------------
@app.route("/api/visits", methods=["POST"])
def create_visit():
    data = request.json
    print(request.json)

    data["status"] = "pending"
    data["submittedAt"] = datetime.utcnow().isoformat()

    visits_collection.insert_one(data)

    return jsonify({
        "message": "Visit submitted successfully",
        "receiptId": data["receiptId"]
    }), 201


# -------------------------------
# GET: Fetch all visits (Admin Dashboard)
# -------------------------------
@app.route("/api/visits", methods=["GET"])
def get_visits():
    visits = []

    for v in visits_collection.find({}, {"_id": 0}):
        visits.append(v)

    return jsonify(visits), 200


# -------------------------------
# PUT: Update status (Approve / Reject)
# -------------------------------
@app.route("/api/visits/<receipt_id>/status", methods=["PUT"])
def update_status(receipt_id):
    data = request.json
    new_status = data.get("status")

    if new_status not in ["approved", "rejected", "pending"]:
        return jsonify({"error": "Invalid status"}), 400

    result = visits_collection.update_one(
        {"receiptId": receipt_id},
        {"$set": {"status": new_status}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({"message": "Status updated"}), 200


# -------------------------------
# DELETE: Delete visit (Admin Dashboard)
# -------------------------------
@app.route("/api/visits/<receipt_id>", methods=["DELETE"])
def delete_visit(receipt_id):
    result = visits_collection.delete_one({"receiptId": receipt_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({"message": "Deleted successfully"}), 200


# -------------------------------
# Health Check
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return "Backend is running"


if __name__ == "__main__":
    app.run(debug=True)
