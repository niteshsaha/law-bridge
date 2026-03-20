import streamlit as st
import requests

#API_BASE = "http://127.0.0.1:8000"
API_BASE = "https://law-bridge-1-gc9l.onrender.com" #for render deployment

# ==============================
# 🔹 CONFIG
# ==============================
st.set_page_config(page_title="Law Bridge", layout="wide")

if "user" not in st.session_state:
    st.session_state["user"] = None

# 🔥 local message (for button-level feedback)
if "local_msg" not in st.session_state:
    st.session_state["local_msg"] = None

# ==============================
# 🔹 STYLING
# ==============================
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
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
# 🔹 SIDEBAR
# ==============================
with st.sidebar:
    st.title("⚖️ Law Bridge")

    if not st.session_state["user"]:
        st.markdown("### 🔐 Login")
        username = st.text_input("Username", key="login_user")

        if st.button("Login"):
            if username:
                st.session_state["user"] = username
                st.success(f"Welcome {username}")
                st.rerun()
            else:
                st.warning("Enter username")
    else:
        st.write(f"👤 {st.session_state['user']}")

        if st.button("Logout"):
            st.session_state["user"] = None
            st.rerun()

    st.markdown("---")

    if st.button("🔄 Clear Result"):
        st.session_state.pop("result", None)
        st.rerun()

    st.markdown("---")

    if st.session_state["user"]:
        try:
            res = requests.get(
                f"{API_BASE}/drafts",
                params={"username": st.session_state["user"]}
            )
            drafts = res.json() if res.status_code == 200 else []
            st.write(f"Drafts: **{len(drafts)}**")
            st.write("Max. 10 Draft allowed")
        except:
            st.caption("API error")

    st.markdown("---")
    st.markdown("### 👨‍💻 Author")
    st.write("NITESH SAHA")

# ==============================
# 🔹 DISPLAY RESULT
# ==============================
def show_result(data):

    st.markdown("## ⚖️ Section Mapping")

    ipc = data.get("ipc_section")
    bns = data.get("bns_section")
    crpc = data.get("crpc_section")
    bnss = data.get("bnss_section")

    if ipc or bns:
        st.success(f"IPC {ipc or '-'} → BNS {bns or '-'}")
    elif crpc or bnss:
        st.success(f"CRPC {crpc or '-'} → BNSS {bnss or '-'}")
    else:
        st.warning("Mapping not available")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if data.get("title"):
        st.write(data["title"])

    st.info(data.get("meaning", ""))

    # 🔥 BUTTON + MESSAGE SIDE BY SIDE
    col1, col2 = st.columns([1, 2])

    with col1:
        clicked = st.button("💾 Save Draft", key="save_result_btn")

    with col2:
        if st.session_state.get("local_msg"):
            st.write(st.session_state["local_msg"])
            st.session_state["local_msg"] = None

    if clicked:

        if not st.session_state.get("user"):
            st.session_state["local_msg"] = "⚠️ Login required"
            st.rerun()

        USER = st.session_state["user"]

        try:
            res_check = requests.get(
                f"{API_BASE}/drafts",
                params={"username": USER}
            )
            existing = res_check.json() if res_check.status_code == 200 else []

            title_val = (data.get("title") or "Untitled").strip()
            content_val = data.get("meaning", "")

            if any(d["title"].lower() == title_val.lower() for d in existing):
                st.session_state["local_msg"] = "⚠️ Already exists"
            else:
                res = requests.post(
                    f"{API_BASE}/draft",
                    params={"username": USER},
                    json={"title": title_val, "content": content_val}
                )

                if res.status_code == 200:
                    response = res.json()
                    if response.get("status") == "error":
                        st.session_state["local_msg"] = f"⚠️ {response.get('message')}"
                    else:
                        st.session_state["local_msg"] = "✅ Saved"
                else:
                    st.session_state["local_msg"] = "❌ Save failed"

        except:
            st.session_state["local_msg"] = "⚠️ Error"

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# 🔹 HEADER
# ==============================
st.title("⚖️ Law Bridge")

if not st.session_state["user"]:
    st.info("Login from sidebar to save drafts")

mode = st.radio(
    "Mode",
    ["Section Lookup", "Search", "Drafts"],
    horizontal=True
)

prev_mode = st.session_state.get("mode")
if prev_mode != mode:
    st.session_state.pop("result", None)

st.session_state["mode"] = mode

# ==============================
# 🔹 LOOKUP
# ==============================
if mode == "Section Lookup":

    section = st.text_input("Section")
    code = st.selectbox("Code", ["IPC", "BNS", "BNSS", "CRPC"])

    if st.button("Get Result"):

        if not section or not section.strip():
            st.warning("Please enter a section number")
            st.session_state.pop("result", None)

        else:
            try:
                res = requests.get(f"{API_BASE}/law/{code}/{section}")

                if res.status_code == 200:
                    data = res.json()

                    if isinstance(data, dict):
                        st.session_state["result"] = data
                    else:
                        st.warning("Invalid response")

                else:
                    st.error(f"API error: {res.status_code}")

            except Exception as e:
                st.error(str(e))

    if "result" in st.session_state and isinstance(st.session_state["result"], dict):
        show_result(st.session_state["result"])

# ==============================
# 🔹 SEARCH
# ==============================
elif mode == "Search":

    q = st.text_input("Search")

    if st.button("Search"):
        res = requests.get(f"{API_BASE}/search?q={q}")

        if res.status_code == 200:
            results = res.json().get("results", [])

            if not results:
                st.warning("No results found")

            for i, item in enumerate(results):
                st.write(item.get("title"))

                if st.button("View", key=f"view_{i}"):
                    full = requests.get(
                        f"{API_BASE}/law/{item['code']}/{item['section_number']}"
                    ).json()

                    st.session_state["result"] = full
                    st.session_state["mode"] = "Section Lookup"
                    st.rerun()
        else:
            st.error("Search failed")

# ==============================
# 🔹 DRAFTS
# ==============================
else:

    if not st.session_state.get("user"):
        st.warning("🔐 Please login to access drafts")
        st.stop()

    USER = st.session_state["user"]

    tab1, tab2 = st.tabs(["Create", "View"])

    with tab1:
        title = st.text_input("Title")
        content = st.text_area("Content")

        save_btn = st.button("Save Draft")

        if st.session_state.get("local_msg"):
            st.write(st.session_state["local_msg"])
            st.session_state["local_msg"] = None

        if save_btn:

            if not title or not content:
                st.session_state["local_msg"] = "⚠️ Fill all fields"
            else:
                try:
                    res = requests.post(
                        f"{API_BASE}/draft",
                        params={"username": USER},
                        json={"title": title, "content": content}
                    )

                    if res.status_code == 200:
                        st.session_state["local_msg"] = "✅ Saved"
                    else:
                        st.session_state["local_msg"] = "❌ Failed"

                except:
                    st.session_state["local_msg"] = "⚠️ Error"

            st.rerun()

    with tab2:
        res = requests.get(f"{API_BASE}/drafts", params={"username": USER})
        drafts = res.json() if res.status_code == 200 else []

        if not drafts:
            st.info("No drafts available")
        else:
            for d in drafts:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.markdown(f"### {d['title']}")
                st.write(d["content"])

                if st.button("🗑️ Delete", key=f"del_{d['id']}"):
                    requests.delete(
                        f"{API_BASE}/draft/{d['id']}",
                        params={"username": USER}
                    )
                    st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# 🔹 FOOTER
# ==============================
st.markdown("---")
st.caption("For informational purposes only")
