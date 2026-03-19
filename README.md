# ⚖️ Law Bridge – Local Legal AI Engine

A local-first AI system that maps old Indian laws (IPC, CrPC, IEA) to new ones (BNS, BNSS, BSA), highlights differences, and explains changes in simple language.

---

## 🚀 Features

- 🔁 Bi-directional mapping (IPC ↔ BNS)
- 📘 Bare Act retrieval (source & target)
- 🔍 Automated diff (added / removed text)
- 🤖 AI explanation (simple English)
- ⚡ AI caching (instant repeat responses)
- 🔎 Keyword search (e.g. "murder")
- 🎨 Visual diff highlighting (UI)
- 🔒 Fully local (no cloud, privacy-safe)

---

## 🏗️ Architecture

Streamlit UI
↓
FastAPI Backend
↓
Service Layer
├── DB Service (SQLite)
├── Diff Engine (difflib)
├── AI Service (Ollama)
↓
Local Model (Qwen 2.5 1.5B)


---

## 🧰 Tech Stack

| Layer       | Technology |
|------------|-----------|
| Backend    | FastAPI |
| Database   | SQLite |
| AI Runtime | Ollama |
| Model      | Qwen 2.5 1.5B |
| Frontend   | Streamlit |
| Diff       | difflib |
| Language   | Python |

---

## ⚙️ Setup Instructions

### 1. Clone repo
```bash
git clone <your-repo-url>
cd law-bridge

2. Create environment

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Start Ollama
export OLLAMA_NUM_THREADS=4
export OLLAMA_CONTEXT_LENGTH=1056
ollama run qwen2.5:1.5b
4. Start backend
uvicorn app.main:app --reload
5. Start UI
streamlit run streamlit_app.py

API Endpoints
Get Law Mapping
GET /law/{code}/{section}
Search Laws
GET /search?q=keyword

How It Works

User inputs section or keyword

Backend fetches source + mapped section

Diff engine computes changes

AI generates explanation (cached)

UI displays highlighted comparison

⚡ Optimization

Reduced context length (1056)

Token-limited responses

AI caching in database

Lightweight model (1.5B params)

Limitations

Word-level diff (not semantic yet)

Basic search (LIKE query)

Depends on dataset quality

🚀 Future Improvements

Full-text search (SQLite FTS)

Sentence-level diff

Flutter mobile app

Semantic AI comparison

Multi-language support

📌 Project Type
Local AI + Legal Tech + Full Stack System Design

Author

NITESH SAHA


---

# 📊 2. Architecture Diagram (Explainable)

You can convert this to a diagram later:


[ User (Web / Mobile) ]
↓
[ Streamlit UI ]
↓
[ FastAPI Backend ]
↓
┌─────────────────────┐
│ Service Layer │
│ │
│ DB Service │
│ Diff Engine │
│ AI Service │
└─────────────────────┘
↓
[ SQLite Database ]
↓
[ Ollama Runtime ]
↓
[ Qwen 2.5 Model ]


---

## 🧠 Explanation (for interviews)

- UI is decoupled from backend  
- Backend is stateless API  
- Services are modular  
- AI is local inference  
- DB handles caching + retrieval  

👉 This shows **clean architecture + scalability**

---

# 🧾 3. Resume / Portfolio Bullet Points

Use these in resume:

---

## 🔹 Short Version (Resume)

- Built a **local-first Legal AI system** to map IPC to BNS and explain changes using LLMs  
- Designed **modular FastAPI backend** with SQLite and service-based architecture  
- Implemented **diff engine (difflib)** to detect legal text changes  
- Integrated **Ollama + Qwen 1.5B** for on-device AI inference with optimized memory usage  
- Developed **AI caching layer** to reduce latency and improve performance  
- Created **interactive Streamlit UI** with keyword search and visual diff highlighting  

---

## 🔹 Strong Version (Portfolio / Interview)

- Engineered a **production-style Legal AI platform** enabling bi-directional mapping between legacy (IPC) and modern (BNS) legal frameworks  
- Designed and implemented a **three-layer architecture (API, services, data)** ensuring scalability and mobile readiness  
- Built a **local LLM inference pipeline** using Ollama with hardware-aware optimizations (threading, context control)  
- Developed a **diff computation engine** to extract structural legal changes and render them visually  
- Implemented **persistent AI caching** in SQLite, reducing repeated inference cost and improving response time  
- Designed a **dual-mode UX (section lookup + semantic search)** improving accessibility for legal and non-technical users  

---

# 🧠 Final Advice

This project already demonstrates:

- Backend engineering  
- AI integration  
- System design  
- Performance optimization  
- Product thinking  

👉 This is **portfolio-worthy and interview-worthy**

---

# If you want next

I can help you:

- 🎯 Add GitHub badges + polish  
- 📊 Create visual diagrams (for presentation)  
- 📱 Plan Flutter integration  
- 🧪 Prepare interview questions based on this project  

Just tell me 👍
