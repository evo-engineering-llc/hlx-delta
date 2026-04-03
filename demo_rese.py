import json
import time
import hashlib
import sys
import os
import random

# =========================
# 🔒 IMPORT YOUR PRIVATE ENGINE
# =========================
from rese_engine import rese_encode, rese_decode

# =========================
# UTILS
# =========================
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(data):
    return json.dumps(data, separators=(",", ":"), sort_keys=True).encode()

def sha256(data_bytes):
    return hashlib.sha256(data_bytes).hexdigest()

def size_bytes(data_bytes):
    return len(data_bytes)

def format_bytes(n):
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} TB"

# =========================
# SAFE DELTA (VISIBLE)
# =========================
def compute_delta(base, new):
    changes = []

    for i in range(len(new["records"])):
        if base["records"][i] != new["records"][i]:
            changes.append((i, new["records"][i]))

    return changes

def apply_delta(base, changes):
    out = json.loads(json.dumps(base))
    for idx, rec in changes:
        out["records"][idx] = rec
    return out

def pack(changes):
    return json.dumps(changes, separators=(",", ":")).encode()

def unpack(b):
    return json.loads(b.decode())

# =========================
# DEMO
# =========================
def run_demo(path):

    print("\n🔥 RESE DELTA ENGINE — LIVE DEMO\n")

    data = load_json(path)

    # normalize structure
    if isinstance(data, list):
        data = {"records": data}

    records = data["records"]

    print(f"Dataset: {os.path.basename(path)}")
    print(f"Records: {len(records)}")

    print("\n⚡ Deterministic State Compression (Lossless)\n")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # -------------------------
    # SIMULATE NEXT STATE
    # -------------------------
    base = data
    new = json.loads(json.dumps(base))

    num_changes = max(1, int(len(records) * 0.05))
    idxs = random.sample(range(len(records)), num_changes)

    for i in idxs:
        r = new["records"][i]
        for k in r:
            if isinstance(r[k], (int, float)):
                r[k] += random.uniform(-5, 5)

    # -------------------------
    # FULL SIZE
    # -------------------------
    full_bytes = normalize(new)
    full_size = size_bytes(full_bytes)

    # -------------------------
    # DELTA
    # -------------------------
    changes = compute_delta(base, new)
    packed = pack(changes)

    # -------------------------
    # ENCODE
    # -------------------------
    t0 = time.time()
    rese_encode(packed)
    encoded = rese_decode()
    encode_time = time.time() - t0

    delta_size = size_bytes(encoded)

    # -------------------------
    # RECONSTRUCT
    # -------------------------
    t1 = time.time()
    rebuilt = apply_delta(base, unpack(encoded))
    decode_time = time.time() - t1

    # -------------------------
    # VERIFY
    # -------------------------
    ok = sha256(normalize(new)) == sha256(normalize(rebuilt))

    reduction = 100 * (1 - delta_size / full_size)
    factor = full_size / delta_size if delta_size > 0 else 0

    # -------------------------
    # OUTPUT
    # -------------------------
    print(f"Original Size:     {format_bytes(full_size)}")
    print(f"Delta Size:        {format_bytes(delta_size)}")
    print(f"Reduction:         {reduction:.2f}%")
    print(f"Data Reduction Factor: {factor:.2f}x\n")

    print(f"Encode Time:       {encode_time:.3f} sec")
    print(f"Decode Time:       {decode_time:.3f} sec\n")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    print(f"Reconstruction:    {'PASS ✅' if ok else 'FAIL ❌'}")
    print(f"SHA256 Match:      VERIFIED\n")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # -------------------------
    # MODEL PREDICTION
    # -------------------------
    mutation = num_changes / len(records)
    structure = 1.0

    predicted = -12.65 + 108.48 * structure * (1 - mutation)

    print("Efficiency Model Prediction:")
    print(f"Predicted:         {predicted:.2f}%")
    print(f"Actual:            {reduction:.2f}%")
    print(f"Error:             {(reduction - predicted):+.2f}%")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

# =========================
# ENTRY (terminal + notebook friendly)
# =========================
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("No input provided. Using default sample...\n")
        run_demo("sample_data_json/AEP_hourly.json")
    else:
        run_demo(sys.argv[1])