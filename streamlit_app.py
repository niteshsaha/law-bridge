import streamlit as st
import re
from app.services.mapping_service import get_mapping_info, search_sections
from app.services.ai_service import generate_explanation

# ==============================
# 🔹 CONFIG
# ==============================
st.set_page_config(page_title="Law Bridge", layout="wide")

# ==============================
# 🔹 STYLE
# ==============================
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f9fafb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🔹 RESULT DISPLAY
# ==============================
def show_result(data):
    st.markdown("## ⚖️ Section Mapping")

    st.success(f"IPC {data['ipc_section'] or '-'} → BNS {data['bns_section'] or '-'}")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if data.get("title"):
        st.markdown("### 📌 Title")
        st.write(data["title"])

    st.markdown("### 🔍 Status")

    if data["status"] == "Equivalent":
        st.info("Equivalent Section")
    elif data["status"] == "Removed":
        st.error("Removed in BNS")
    elif data["status"] == "New Section":
        st.warning("New Section in BNS")
    else:
        st.write(data["status"])

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Meaning")
    st.info(data["meaning"])
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# 🔹 SIDEBAR
# ==============================
with st.sidebar:
    st.title("⚖️ Law Bridge")
    st.write("NITESH SAHA")

# ==============================
# 🔹 HEADER
# ==============================
st.title("⚖️ Law Bridge")
st.caption("Compare Indian laws with AI")

mode = st.radio("Mode", ["Section Lookup", "Search"], horizontal=True)

# ==============================
# 🔹 SECTION LOOKUP
# ==============================
if mode == "Section Lookup":

    col1, col2 = st.columns([2, 3])

    with col1:
        section = st.text_input("Section")

    with col2:
        code = st.selectbox("Code", ["IPC", "BNS"])

    if st.button("Get Result"):

        if not section:
            st.warning("Enter section")
        else:
            result = get_mapping_info(code, section)

            meaning = "No explanation available."

            if result.get("title"):
                meaning = generate_explanation("", result["title"], {"added": [], "removed": []})

            result["meaning"] = meaning

            show_result(result)

# ==============================
# 🔹 SEARCH
# ==============================
else:

    query = st.text_input("Search")

    if st.button("Search"):

        results = search_sections(query)

        if not results:
            st.warning("No results found")
        else:
            for i, item in enumerate(results):

                ipc = item.get("ipc_section") or "-"
                bns = item.get("section_number") or "-"

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"**IPC {ipc} → BNS {bns}**")
                st.caption(item.get("title"))

                if st.button("View", key=i):

                    result = get_mapping_info(item["code"], item["section_number"])

                    meaning = generate_explanation("", result.get("title", ""), {"added": [], "removed": []})
                    result["meaning"] = meaning

                    show_result(result)

                st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# 🔹 FOOTER
# ==============================
st.markdown("---")
st.markdown("<center>Built with ❤️ by NITESH SAHA</center>", unsafe_allow_html=True)