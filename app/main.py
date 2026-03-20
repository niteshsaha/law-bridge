from fastapi import FastAPI, Query
from app.services.mapping_service import get_mapping_info, search_sections
from app.services.ai_service import generate_explanation
from app.services.draft_service import (
    load_drafts,
    add_draft,
    delete_draft,
    search_drafts
)

app = FastAPI(
    title="Law Bridge API",
    description="IPC ↔ BNS mapping with AI meaning",
    version="2.0.0"
)

# ==============================
# 🔹 ROOT
# ==============================
@app.get("/")
def root():
    return {"message": "Law Bridge API is running 🚀"}


# ==============================
# 🔹 LAW LOOKUP
# ==============================
@app.get("/law/{code}/{section}")
def get_law(code: str, section: str):

    result = get_mapping_info(code, section)

    section_label = None

    if result.get("bns_section"):
        section_label = f"BNS {result['bns_section']}"
    elif result.get("ipc_section"):
        section_label = f"IPC {result['ipc_section']}"
    elif result.get("bnss_section"):
        section_label = f"BNSS {result['bnss_section']}"
    elif result.get("crpc_section"):
        section_label = f"CRPC {result['crpc_section']}"

    meaning = "No explanation available."

    if result.get("title") and section_label:
        meaning = generate_explanation(
            "",
            f"{section_label} - {result['title']}",
            {"added": [], "removed": []}
        )

    return {
        "ipc_section": result.get("ipc_section"),
        "bns_section": result.get("bns_section"),
        "crpc_section": result.get("crpc_section"),
        "bnss_section": result.get("bnss_section"),
        "title": result.get("title"),
        "status": result.get("status"),
        "meaning": meaning
    }


# ==============================
# 🔹 SEARCH
# ==============================
@app.get("/search")
def search_law(q: str):
    if not q:
        return {"results": []}

    results = search_sections(q)
    return {"results": results}


# ==============================
# 🔹 DRAFT APIs (MULTI-USER)
# ==============================
@app.post("/draft")
def create_draft(username: str, data: dict):
    result = add_draft(
        username,
        data.get("title"),
        data.get("content")
    )

    if "error" in result:
        return {"status": "error", "message": result["error"]}

    return {"status": "success", "data": result}

@app.get("/drafts")
def get_all_drafts(username: str):
    return load_drafts(username)

@app.delete("/draft/{draft_id}")
def remove_draft(draft_id: str, username: str):
    return delete_draft(username, draft_id)

@app.get("/drafts/search")
def search_draft(username: str, q: str):
    return search_drafts(username, q)