// Use explicit DB
db = db.getSiblingDB("entry_shield");

// 1️⃣ Create unique index (receiptNumber must be unique)
db.receipts.createIndex(
  { receiptNumber: 1 },
  { unique: true }
);

// 2️⃣ Prepare receipt document
const receipt = {
  // Reference to gate_passes._id
  gatePassId: ObjectId(),

  receiptNumber: "GP-2026-000123",
  category: "VISITOR_PARENT",

  generatedAt: new Date(),

  generatedBy: {
    userId: ObjectId(),
    role: "SECURITY"
  }
};

// 3️⃣ Idempotent insert (UPSERT)
db.receipts.updateOne(
  { receiptNumber: receipt.receiptNumber },
  { $setOnInsert: receipt },
  { upsert: true }
);

print("✅ receipt seed completed");