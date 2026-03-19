import csv
import json
from rapidfuzz import fuzz

# ==============================
# 🔹 LOAD JSON DATA
# ==============================
with open("data/ipc.json") as f:
    BNS_JSON = json.load(f)

with open("data/crpc.json") as f:
    BNSS_JSON = json.load(f)

# ==============================
# 🔹 GENERIC CSV LOADER
# ==============================
def load_mapping(csv_path, old_key, new_key):
    OLD_TO_NEW = {}
    NEW_TO_OLD = {}
    NEW_TITLE = {}

    with open(csv_path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            old = (row.get(old_key) or "").strip()
            new = (row.get(new_key) or "").strip()
            title = (row.get("title") or "").strip()

            if old:
                OLD_TO_NEW[old] = new if new else None

            if new:
                NEW_TO_OLD[new] = old if old else None
                NEW_TITLE[new] = title

    return OLD_TO_NEW, NEW_TO_OLD, NEW_TITLE


# ==============================
# 🔹 LOAD BOTH SYSTEMS
# ==============================
IPC_TO_BNS, BNS_TO_IPC, BNS_TITLE = load_mapping(
    "data/bns_mappings.csv",
    "ipc_section",
    "bns_section"
)

CRPC_TO_BNSS, BNSS_TO_CRPC, BNSS_TITLE = load_mapping(
    "data/bnss_mappings.csv",
    "crpc_section",
    "bnss_section"
)

# ==============================
# 🔹 MAIN ENTRY
# ==============================
def get_mapping_info(code, section):
    code = code.upper()
    section = section.strip()

    if code in ["IPC", "BNS"]:
        return handle_mapping(
            code,
            section,
            IPC_TO_BNS,
            BNS_TO_IPC,
            BNS_TITLE,
            BNS_JSON,
            "ipc_section",
            "bns_section"
        )

    elif code in ["CRPC", "BNSS"]:
        return handle_mapping(
            code,
            section,
            CRPC_TO_BNSS,
            BNSS_TO_CRPC,
            BNSS_TITLE,
            BNSS_JSON,
            "crpc_section",
            "bnss_section"
        )

    return {
        "status": "Invalid Code",
        "text": None
    }


# ==============================
# 🔹 CORE LOGIC (REUSABLE)
# ==============================
def handle_mapping(code, section, OLD_TO_NEW, NEW_TO_OLD, TITLE_MAP, JSON_DATA, OLD_KEY, NEW_KEY):
    old_sec = None
    new_sec = None
    title = None
    status = "Not Found"
    text = None

    OLD = OLD_KEY.replace("_section", "").upper()
    NEW = NEW_KEY.replace("_section", "").upper()

    # 🔹 OLD → NEW
    if code == OLD:
        old_sec = section

        if section not in OLD_TO_NEW:
            return {
                OLD_KEY: old_sec,
                NEW_KEY: None,
                "title": None,
                "status": "Not Found",
                "text": None
            }

        new_sec = OLD_TO_NEW.get(section)

        if not new_sec:
            return {
                OLD_KEY: old_sec,
                NEW_KEY: None,
                "title": None,
                "status": "Removed",
                "text": None
            }

        text = JSON_DATA.get(new_sec)

        if not text or text == "REMOVED":
            status = "Removed"
        else:
            status = "Equivalent"
            title = TITLE_MAP.get(new_sec)

    # 🔹 NEW → OLD
    elif code == NEW:
        new_sec = section

        text = JSON_DATA.get(section)

        if not text:
            return {
                OLD_KEY: None,
                NEW_KEY: new_sec,
                "title": None,
                "status": "Not Found",
                "text": None
            }

        if text == "REMOVED":
            return {
                OLD_KEY: None,
                NEW_KEY: new_sec,
                "title": None,
                "status": "Removed",
                "text": None
            }

        old_sec = NEW_TO_OLD.get(section)

        if not old_sec:
            status = "New Section"
        else:
            status = "Equivalent"

        title = TITLE_MAP.get(section)

    return {
        OLD_KEY: old_sec,
        NEW_KEY: new_sec,
        "title": title,
        "status": status,
        "text": text
    }


# ==============================
# 🔹 SEARCH (COMBINED)
# ==============================
def extract_title(text):
    if not text or text == "REMOVED":
        return "No title"

    first_line = text.split("\n")[0]

    if "." in first_line:
        return first_line.split(".", 1)[1].strip()

    return first_line.strip()


def search_sections(query):
    query = query.lower()
    results = []

    # 🔹 BNS
    for bns, text in BNS_JSON.items():
        if not text or text == "REMOVED":
            continue

        title = extract_title(text)
        score = fuzz.partial_ratio(query, (title + text).lower())

        if score > 60:
            results.append({
                "code": "BNS",
                "section_number": bns,
                "title": title,
                "ipc_section": BNS_TO_IPC.get(bns)
            })

    # 🔹 BNSS
    for bnss, text in BNSS_JSON.items():
        if not text or text == "REMOVED":
            continue

        title = extract_title(text)
        score = fuzz.partial_ratio(query, (title + text).lower())

        if score > 60:
            results.append({
                "code": "BNSS",
                "section_number": bnss,
                "title": title,
                "crpc_section": BNSS_TO_CRPC.get(bnss)
            })

    return results[:20]