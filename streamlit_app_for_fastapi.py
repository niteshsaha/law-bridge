import streamlit as st
import requests
import re

API_BASE = "http://127.0.0.1:8000"

# ==============================
# 🔹 PREMIUM STYLING
# ==============================
st.set_page_config(page_title="Law Bridge", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f9fafb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
}

.small-text {
    color: #6b7280;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🔹 HIGHLIGHT FUNCTION
# ==============================

def highlight_text(text, added, removed):
    highlighted = text

    # Highlight added (green)
    for word in added:
        if word.strip():
            pattern = re.escape(word)
            highlighted = re.sub(
                pattern,
                f"<span style='background-color:#d4edda; padding:2px 4px; border-radius:4px;'>{word}</span>",
                highlighted,
                flags=re.IGNORECASE
            )

    # Highlight removed (red)
    for word in removed:
        if word.strip():
            pattern = re.escape(word)
            highlighted = re.sub(
                pattern,
                f"<span style='background-color:#f8d7da; padding:2px 4px; border-radius:4px;'>{word}</span>",
                highlighted,
                flags=re.IGNORECASE
            )

    return highlighted

# ==============================
# 🔹 DISPLAY RESULT
# ==============================
def show_result(data):
    st.markdown("## ⚖️ Section Mapping")

    ipc = data.get("ipc_section")
    bns = data.get("bns_section")
    crpc = data.get("crpc_section")
    bnss = data.get("bnss_section")

    if ipc is not None or bns is not None:
        st.success(f"IPC {ipc or '-'} → BNS {bns or '-'}")

    elif crpc is not None or bnss is not None:
        st.success(f"CRPC {crpc or '-'} → BNSS {bnss or '-'}")

    else:
        st.warning("Mapping not available")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Title
    if data.get("title"):
        st.markdown("### 📌 Title")
        st.write(data["title"])

    # Status
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

    # Meaning
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Meaning")
    st.info(data["meaning"])
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# 🔹 SIDEBAR (PREMIUM TOUCH)
# ==============================
with st.sidebar:
    st.title("⚖️ Law Bridge")
    st.markdown("### 👨‍💻 Author")
    st.write("NITESH SAHA")
    st.markdown("---")
    st.caption("AI-powered legal comparison system")


# ==============================
# 🔹 HEADER
# ==============================
st.title("⚖️ Law Bridge")
st.caption("Compare Indian laws and understand changes instantly with AI")

st.markdown("---")

# ==============================
# 🔹 MODE SELECT
# ==============================
mode = st.radio(
    "Select Mode",
    ["Section Lookup", "Search"],
    horizontal=True
)

st.markdown("## 🔍 Input")

# ==============================
# 🔹 SECTION LOOKUP
# ==============================
if mode == "Section Lookup":

    col1, col2 = st.columns([2, 3])

    with col1:
        section = st.text_input("Section Number", placeholder="e.g. 302")

    with col2:
        code = st.selectbox(
            "Law Code",
            ["IPC", "BNS", "BNSS", "CrPC", "BSA", "IEA"]
        )

    if st.button("🚀 Get Result", use_container_width=True):

        if not section:
            st.warning("Enter a section number")
        else:
            with st.spinner("Processing..."):
                try:
                    res = requests.get(f"{API_BASE}/law/{code}/{section}")

                    if res.status_code == 200:
                        data = res.json()

                        if "error" in data:
                            st.error(data["error"])
                        else:
                            show_result(data)
                    else:
                        st.error("API error")

                except Exception as e:
                    st.error(str(e))

# ==============================
# 🔹 SEARCH MODE
# ==============================
else:
    query = st.text_input("Search Keyword", placeholder="e.g. murder")

    if st.button("🔍 Search", use_container_width=True):

        if not query:
            st.warning("Enter a keyword")
        else:
            with st.spinner("Searching..."):
                try:
                    res = requests.get(f"{API_BASE}/search?q={query}")

                    if res.status_code == 200:
                        data = res.json()

                        # 🔥 DEBUG (remove later)
                        #st.write(data)

                        results = data.get("results", [])

                        if not results:
                            st.warning("No results found")
                        else:
                            st.markdown("## 📋 Results")

                            for i, item in enumerate(results):

                                ipc = item.get("ipc_section") or "-"
                                bns = item.get("section_number") or "-"
                                title = item.get("title", "No title")

                                label = f"IPC {ipc} → BNS {bns}"

                                st.markdown('<div class="card">', unsafe_allow_html=True)

                                st.markdown(f"**{label}**")
                                st.caption(title)

                                if st.button("View", key=f"{i}"):

                                    full = requests.get(
                                        f"{API_BASE}/law/{item['code']}/{item['section_number']}"
                                    ).json()

                                    show_result(full)

                                st.markdown('</div>', unsafe_allow_html=True)

                    else:
                        st.error("API error")

                except Exception as e:
                    st.error(str(e))


# ==============================
# 🔹 FOOTER
# ==============================
st.markdown("---")
st.markdown(
    "<center style='color: grey; font-size:14px;'>For informational purposes only</center>",
    unsafe_allow_html=True
)