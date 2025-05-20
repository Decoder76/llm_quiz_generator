# 📚 LLM Quiz Generator

**Generate customized quizzes on any topic using powerful Large Language Models (LLMs) with just a few clicks!**  
A minimal, intuitive web app powered by Hugging Face and built with Streamlit.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-%E2%9C%85-green)

---

## 🚀 Features

🎯 **Configurable Quiz Parameters**  
Define your quiz settings:
- **Topic** (e.g., Science, History, Python)
- **Difficulty**: Easy | Medium | Hard
- **Number of Questions**
- **Question Types**: Multiple Choice | True/False | Short Answer

🧠 **Smart Generation with LLMs**  
Leverages Hugging Face's Inference API (default: `HuggingFaceH4/zephyr-7b-beta`) for accurate, context-aware quiz creation.

🔍 **Advanced Options (Optional)**  
- Sub-topics
- Context keywords
- Target audience (e.g., middle school, professionals)
- Max question length

🖥️ **Minimal & Clean Interface**  
User-friendly UI powered by **Streamlit** – no clutter, just quizzes.

🔐 **Secure Token Management**  
API tokens are securely handled via `.env` and never exposed to the frontend or logs.

---

## 🛠️ Getting Started

Follow these steps to get the app up and running locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Decoder76/llm_quiz_generator.git
cd llm_quiz_generator
````

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### Core Dependencies:

* `streamlit`
* `python-dotenv`
* `langchain-huggingface`

> *(Check `requirements.txt` for the full list.)*

### 4. Configure Hugging Face API Token

Create a `.env` file in the root directory with your token:

```dotenv
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here
```

🚨 **Note:** Keep this file private! Never share or commit your token.

---

### 5. Run the Application

```bash
streamlit run app.py
```

Open the provided local URL (typically `http://localhost:8501`) in your browser.

---

## ⚙️ How It Works

1. **📝 Input** – Users fill out a form with quiz preferences.
2. **🔧 Prompt Builder** – The app crafts a tailored prompt for the LLM.
3. **📡 API Call** – Prompt is sent to the Hugging Face model via their Inference API.
4. **📋 Output** – Quiz appears instantly on-screen in a clean, readable format.

---

## 🧰 Tech Stack

* **Streamlit** – Simple Python web app framework
* **Langchain (Hugging Face)** – LLM integration
* **python-dotenv** – Environment variable management
* **Hugging Face Inference API** – LLMs as a service

---

## 🔐 Security Notes

* The Hugging Face API token is stored securely via `.env` and **never** exposed in frontend code or logs.
* The app avoids transmitting any sensitive information externally.

---

## 📄 License

**MIT License** – Free to use, modify, and contribute!
See [LICENSE](./LICENSE) for more details.

---

## 🙋‍♂️ Contact & Feedback

For support, suggestions, or contributions, feel free to:

* Open an [Issue](https://github.com/Decoder76/llm_quiz_generator/issues)
* Connect on GitHub: [@Decoder76](https://github.com/Decoder76)

---

> ✨ Whether you're a teacher, developer, or student, this app lets you **generate smart quizzes in seconds**.
> Happy learning!

````
