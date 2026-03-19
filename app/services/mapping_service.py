import csv
import json
from rapidfuzz import fuzz


# ==============================
# 🔹 LOAD JSON (BNS DATA)
# ==============================
with open("data/ipc.json") as f:
    BNS_JSON = json.load(f)

# ==============================
# 🔹 LOAD CSV (MAPPING)
# ==============================
IPC_TO_BNS = {}
BNS_TO_IPC = {}
BNS_TITLE = {}

with open("data/bns_mappings.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:
        ipc = (row.get("ipc_section") or row.get("IPC") or "").strip()
        bns = (row.get("bns_section") or row.get("BNS") or "").strip()
        title = (row.get("title") or row.get("Title") or "").strip()

        if ipc:
            IPC_TO_BNS[ipc] = bns

        if bns:
            BNS_TO_IPC[bns] = ipc if ipc else None
            BNS_TITLE[bns] = title


# ==============================
# 🔹 MAIN LOGIC
# ==============================
def get_mapping_info(code, section):
    code = code.upper()
    section = section.strip()

    ipc_sec = None
    bns_sec = None
    title = None
    status = "Unknown"
    text = None

    # ==============================
    # 🔹 IPC → BNS
    # ==============================
    if code == "IPC":
        ipc_sec = section
        bns_sec = IPC_TO_BNS.get(section)

        if section not in IPC_TO_BNS:
            status = "Not Found"

        elif not bns_sec:
            status = "Removed"

        else:
            text = BNS_JSON.get(bns_sec)

            if not text or text == "REMOVED":
                status = "Removed"
            else:
                status = "Equivalent"
                title = BNS_TITLE.get(bns_sec)

    # ==============================
    # 🔹 BNS → IPC
    # ==============================
    elif code == "BNS":
        bns_sec = section
        ipc_sec = BNS_TO_IPC.get(section)

        text = BNS_JSON.get(section)

        if not text:
            status = "Not Found"

        elif text == "REMOVED":
            status = "Removed"

        elif not ipc_sec:
            status = "New Section"
            title = BNS_TITLE.get(section)

        else:
            status = "Equivalent"
            title = BNS_TITLE.get(section)

    return {
        "ipc_section": ipc_sec,
        "bns_section": bns_sec,
        "title": title,
        "status": status,
        "text": text  # 🔥 IMPORTANT (fixes your crash)
    }


# ==============================
# 🔹 SEARCH (IMPROVED)
# ==============================
def extract_title(text):
    if not text or text == "REMOVED":
        return "No title"

    # Take first meaningful line
    first_line = text.split("\n")[0]

    # Clean numbering like "39. Something"
    if "." in first_line:
        return first_line.split(".", 1)[1].strip()

    return first_line.strip()

def search_sections(query):
    query = query.lower()
    results = []

    for bns, text in BNS_JSON.items():

        if not text or text == "REMOVED":
            continue

        title = extract_title(text)

        combined = (title + " " + text).lower()

        # 🔥 Fuzzy matching
        score = fuzz.partial_ratio(query, combined)

        if score > 70:  # threshold
            results.append({
                "code": "BNS",
                "section_number": bns,
                "title": title,
                "ipc_section": BNS_TO_IPC.get(bns),
                "score": score
            })

    # 🔥 Sort by best match
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:20]