from fastapi import FastAPI
from app.services.mapping_service import get_mapping_info
from app.services.ai_service import generate_explanation

app = FastAPI(
    title="Law Bridge API",
    description="IPC ↔ BNS mapping with AI meaning",
    version="2.0.0"
)


@app.get("/")
def root():
    return {"message": "Law Bridge API is running 🚀"}


@app.get("/law/{code}/{section}")
def get_law(code: str, section: str):

    result = get_mapping_info(code, section)

    meaning = "No explanation available."

    if result.get("title"):
        meaning = generate_explanation(
            "",
            f"Section {result['bns_section']} - {result['title']}",
            {"added": [], "removed": []}
        )

    return {
        "ipc_section": result["ipc_section"],
        "bns_section": result["bns_section"],
        "title": result["title"],
        "status": result["status"],
        "meaning": meaning
    }

@app.get("/search")
def search_law(q: str):
    if not q:
        return {"results": []}

    from app.services.mapping_service import search_sections

    results = search_sections(q)

    return {"results": results}