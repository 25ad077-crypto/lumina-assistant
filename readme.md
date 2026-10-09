# ⚡ Lumina Assistant

A high-performance, responsive AI chatbot web application powered by **Groq Cloud** and open-source models (Llama 3.3, Llama 3.1, Gemma 2). Built with **Streamlit** using 100% free services and zero subscriptions.

---

## 🚀 Features

- **Blazing-Fast Inference:** Powered by **Groq Cloud Free Tier** (~300–800 tokens/sec).
- **Leading Open-Source Models:** Switch seamlessly between:
  - `llama-3.3-70b-versatile` (State-of-the-art open reasoning, 128k context)
  - `llama-3.1-8b-instant` (Ultra-low latency)
  - `gemma2-9b-it` (Google Gemma 2)
  - `mixtral-8x7b-32768` (Mixture of Experts)
- **Real-Time Streaming:** Live typing cursor effect with sub-second response times.
- **Custom Personas:** Switch between Helpful Assistant, Senior Software Engineer, Concise Executive, Creative Writer, or define custom system prompts.
- **Dynamic Context Memory:** Adjustable sliding context window to retain conversation history.
- **Chat Actions:** Instant conversation clearing, statistics, and one-click export to Markdown (`.md`).
- **Free Cloud Deployment:** Ready to deploy in 2 minutes on **Streamlit Community Cloud** or **Hugging Face Spaces**.

---

## 📦 Project Structure

```text
ai-chatbot/
├── .streamlit/
│   ├── config.toml             # Sleek dark theme configuration
│   └── secrets.toml.example    # Example secrets template
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules for secrets and virtualenvs
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── run.bat                     # 1-Click launcher for Windows
├── run.ps1                     # PowerShell launcher
└── README.md                   # Complete documentation
```

---

## 🔑 Getting Your Free API Key (No Credit Card)

1. Go to [Groq Console](https://console.groq.com).
2. Sign in with your Google or GitHub account.
3. Click on **API Keys** $\rightarrow$ **Create API Key**.
4. Copy the key (starts with `gsk_...`).

> **Rate Limits on Free Tier:** ~30 requests/min and up to 14,400 requests/day, completely free indefinitely.

---

## 🏃 Local Quickstart

### Method 1: Using the 1-Click Launcher (Windows)
Simply double-click `run.bat` in File Explorer. It automatically creates the virtual environment, installs packages, and launches the browser!

### Method 2: Manual Terminal Setup

1. **Navigate to project directory:**
   ```powershell
   cd "C:\Users\HP\.gemini\antigravity\scratch\ai-chatbot"
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```powershell
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## 🌐 100% Free Cloud Deployment (Streamlit Community Cloud)

1. **Initialize Git & Push to GitHub:**
   ```powershell
   git init
   git add app.py requirements.txt .streamlit/config.toml .gitignore README.md
   git commit -m "Initial chatbot release"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Community Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
   - Click **New app**.
   - Select your repository and branch (`main`), with `app.py` as the file path.
   - Click **Advanced Settings** $\rightarrow$ **Secrets**, then add:
     ```toml
     GROQ_API_KEY = "gsk_your_actual_groq_key"
     ```
   - Click **Deploy!** Your app is live 24/7 on a free `streamlit.app` URL.
