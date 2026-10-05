# 🐛 DebugMate

**DebugMate** is a Streamlit web app that helps you explain, fix, and convert code using AI (powered by Ollama's cloud models via LangChain).

## Features

- **Explain working code** — get a breakdown of what your code does, at your chosen level of detail (detailed, short summary, or beginner-friendly)
- **Fix broken code** — paste code with a bug, and DebugMate identifies the problem, explains why it's wrong, and gives you the corrected version. If the code is already correct, it tells you that instead of inventing a fake issue
- **Code Converter** — convert code between Python, Java, C, C++, JavaScript, and C#, with an explanation of the key syntax differences
- **History** — every run is saved automatically and can be filtered by date, so you can revisit past explanations and fixes

## Tech Stack

- [Streamlit](https://streamlit.io/) — web interface
- [LangChain](https://www.langchain.com/) + `langchain-ollama` — connects to the AI model
- [Ollama Cloud](https://ollama.com/) — runs the underlying LLM (`gpt-oss:120b-cloud`)
- Python 3.11

## Setup

1. **Clone this repository**
```bash
   git clone <your-repo-url>
   cd DebugMate
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Add your API key**

   Create a file named `.env` in the project root and add this one line inside it:
5. **Run the app**
```bash
   streamlit run app.py
```

   The app will open at `http://localhost:8501` (or the next available port) in your browser automatically.

## Project Structure
