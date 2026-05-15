# AI Resume Screener

An intelligent, production-ready AI Resume Screening platform that leverages semantic matching to rank candidate resumes against a given job description. Built for high performance and clean architecture.

## 🌟 Features
- **Semantic Candidate Matching**: Uses Sentence-Transformers (`all-MiniLM-L6-v2`) to compute cosine similarity between job descriptions and resumes.
- **PDF Processing Pipeline**: Automatically extracts raw text from candidate PDF uploads.
- **Modular FastAPI Backend**: Clean architecture with isolated routing, services, and Pydantic schemas.
- **Premium Angular UI**: A modern, dynamic, responsive dashboard featuring drag-and-drop uploads, loading skeletons, and visual score indicators.

---

## 🏗 Architecture

```mermaid
graph TD;
    UI[Angular Frontend] -->|Multipart Form Data\n(JD + PDFs)| API[FastAPI Match Endpoint]
    API --> Parser[PDF Parser Service]
    API --> Matcher[Matcher Service]
    Matcher --> Model[Sentence Transformer\nEmbeddings]
    Parser --> Matcher
    Matcher --> API
    API -->|JSON Ranked Results| UI
```

## 🚀 Tech Stack
- **Frontend**: Angular 18 (Standalone Components), Vanilla CSS (Glassmorphism & Dark Mode)
- **Backend**: FastAPI, Pydantic, Uvicorn, python-multipart
- **AI/ML**: `sentence-transformers`, `torch`, `scikit-learn` (cosine similarity)
- **PDF Parsing**: `pypdf`

---

## 💻 Getting Started

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. You can test the endpoints at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd resume-screener-ui

# Install dependencies
npm install

# Start the Angular development server
npm run start
```
The UI will be available at `http://localhost:4200`.

---

## ☁️ Deployment Plan

### Vercel (Frontend)
1. Push your repository to GitHub.
2. Connect your GitHub repository to Vercel.
3. Configure the Root Directory to `resume-screener-ui`.
4. Framework Preset: `Angular`.
5. Add environment variable `BACKEND_URL` pointing to your Render backend API.

### Render (Backend)
1. Create a new Web Service on Render and connect your repo.
2. Root Directory: `backend`
3. Environment: `Python`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Note: You may need to allocate more memory (e.g., Starter plan) as PyTorch and SentenceTransformers can be memory intensive.

---

*This project is designed to showcase AI Engineering, Full-Stack Architecture, and modern UI/UX design.*
