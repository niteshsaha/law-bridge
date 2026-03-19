import json
import os
from datetime import datetime
import uuid

# ==============================
# 🔹 BASE PATH (per-user storage)
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../../data/drafts")

os.makedirs(DATA_DIR, exist_ok=True)


# ==============================
# 🔹 HELPERS
# ==============================
def get_user_file(username):
    return os.path.join(DATA_DIR, f"{username}.json")


def load_drafts(username):
    file_path = get_user_file(username)

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path) as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception:
        return []


def save_drafts(username, drafts):
    file_path = get_user_file(username)

    with open(file_path, "w") as f:
        json.dump(drafts, f, indent=2)


# ==============================
# 🔹 CREATE
# ==============================
def add_draft(username, title, content, tags=None):
    drafts = load_drafts(username)

    # 🔥 Prevent duplicate title
    if any(d["title"].lower() == title.lower() for d in drafts):
        return {"error": "Draft already exists"}

    draft = {
        "id": str(uuid.uuid4()),
        "title": title,
        "content": content,
        "tags": tags or [],
        "created_at": datetime.now().isoformat()
    }

    drafts.append(draft)
    save_drafts(username, drafts)

    return draft


# ==============================
# 🔹 DELETE
# ==============================
def delete_draft(username, draft_id):
    drafts = load_drafts(username)
    drafts = [d for d in drafts if d["id"] != draft_id]

    save_drafts(username, drafts)
    return {"message": "Deleted"}


# ==============================
# 🔹 UPDATE
# ==============================
def update_draft(username, draft_id, title, content):
    drafts = load_drafts(username)

    for d in drafts:
        if d["id"] == draft_id:
            d["title"] = title
            d["content"] = content

    save_drafts(username, drafts)
    return {"message": "Updated"}


# ==============================
# 🔹 SEARCH
# ==============================
def search_drafts(username, query):
    drafts = load_drafts(username)
    query = query.lower()

    return [
        d for d in drafts
        if query in d["title"].lower() or query in d["content"].lower()
    ]