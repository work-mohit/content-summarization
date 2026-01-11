# Content Summarization 
It is a LLM based text summarizer, built with the help of the Langchain framework. 


# How it works 

The application follows these steps to provide summary for the provided Url:

1. User will provide the details like : `LLM Provider`, `API_KEY`, and a valid `URL` of a youtube video or a website, of which you want to generate summary.

2. Content Fetch: The content inside a website url or youtube video transcript being fetched.

3. Language Model: A model from user selected provider being initialized. This model will take a prompt and the content of the given url and based on the prompt it generates a detialed summary. 


# Project Setup

# 🚀 LangChain Project Setup using `uv`

This documentation demonstrates how to set up the project using **`uv`** for fast virtual environment and dependency management.

The setup follows **LangChain ≥1.x best practices** and is suitable for:
- LLM applications
- RAG systems
- Agents (LangGraph)
- FastAPI / Streamlit deployments

---

## ✅ Prerequisites

Ensure you have the following installed:

- Python **3.10+**
- Git (recommended)

Check Python version:
```bash
python --version
```

---

## 1️⃣ Install `uv`

### Windows / macOS / Linux
```bash
pip install uv
```

Verify installation:
```bash
uv --version
```

**Why `uv`?**
- ⚡ Extremely fast (Rust-based)
- 📦 Manages virtual environments and dependencies together
- 🧼 Replaces `pip`, `venv`, and `requirements.txt`

---


## 1️⃣ Clone the Repository

```bash
git clone https://github.com/work-mohit/content-summarization.git
cd content-summarization
```

---

## 2️⃣ Install `uv` (One-time Setup)

If `uv` is not installed:

```bash
pip install uv
```

Verify:
```bash
uv --version
```

## 3️⃣ Create & Activate Virtual Environment

Create the virtual environment:
```bash
uv venv
```

Activate it:

### Windows
```powershell
.venv\Scripts\activate
```

### macOS / Linux
```bash
source .venv/bin/activate
```

You should now see `(.venv)` in your terminal.

---

## 4️⃣ Install Project Dependencies

Install all dependencies defined in `pyproject.toml`:

```bash
uv sync
```

📌 If this is the **first setup**, this will:
- Resolve versions
- Install dependencies
- Use `uv.lock` if present

---

## 5️⃣ Environment Variables Setup

Technically this setup is only required when you're testing out things for yourself. As in the project we're taking `API_KEY` as an input fromt user, we don't need to use `.env`. But in case you don't want that and want to run locally, you can refer to below setup.

Create a `.env` file in the project root:

```env
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
OPENAI_API_KEY=your_openai_key_here
```

⚠️ **Important**
- Do NOT commit `.env` to Git
- Add `.env` to `.gitignore` (I have already added, you can cross check in `.gitignore` file.)

---

## 6️⃣ Project Structure (Reference)

```text
content-summarization/
│
├── app/
│   ├── __init__.py
│   ├── main.py
├── .venv/
├── pyproject.toml
├── uv.lock
|── README.md
└── SETUP.md
```
---

## 7️⃣ Run the Application


Run below commad to run the  **Streamlit** Application:
```bash
streamlit run app/main.py
```
