# Smart Career Mentor Agent

A multi-step intelligent application that parses resumes, extracts key skills and roles using OpenAI, maps skills to suitable career roles, identifies skill gaps, and recommends personalized courses.

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt

## 📁 File Descriptions

| File Name                  | Description |
|----------------------------|-------------|
| `.env`                     | Stores sensitive environment variables such as API keys and endpoints for Azure services. |
| `.gitignore`               | Specifies files and folders to be ignored by git (e.g., `.env`, `__pycache__/`). |
| `ai_skill_role_extractor.py` | Uses Azure OpenAI to extract skills and suggest job roles from resume text. |
| `parsed_resume.json`       | Stores structured data extracted from a resume, including name, skills, and suggested role. |
| `Readme.md`                | Project documentation and instructions. |
| `requirements.txt`         | Lists all required packages like Python, Open AI, PDF etc. for the project. |
| `requirements_old.txt`     | Legacy requirements and sample outputs for reference and testing. |
| `resume_cleaner.py`        | Cleans and processes raw resume text, extracts structured data (name, email, phone, skills) using regex, spaCy, and Azure OpenAI. |
| `resume_parser.py`         | Extracts text from PDF resumes using Azure Form Recognizer and calls `resume_cleaner.py` for further processing. |
| `role_mapper.py`           | Maps extracted skills to predefined job roles and saves structured output to JSON. |
| `sample_resume.pdf`        | Example resume file for testing the pipeline. |
| `skill_gap_output.json`    | Stores the output of skill gap analysis, including missing skills and recommended courses. |
| `skill_gap_recommender.py` | Analyzes skill gaps between resume and target role using Azure OpenAI, and recommends courses for missing skills. |
| `streamlit_app.py`         | Streamlit web application for uploading resumes, running the analysis pipeline, and displaying results with download option. |
| `__pycache__/`             | Directory for Python bytecode cache files (auto-generated, ignored by git). |

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚡ Azure CLI Commands Used

Below are the `az` commands used for deploying and configuring the web app, with comments:

```sh
# Set the startup command for the Azure Web App to run Streamlit on port 8000
az webapp config set \
  --resource-group Smart_Career_Mentor_Agent \
  --name smart-career-mentor-app \
  --startup-file "streamlit run streamlit_app.py --server.port 8000"

# Set the PORT environment variable to 8000 for the web app
az webapp config appsettings set \
  --resource-group Smart_Career_Mentor_Agent \
  --name smart-career-mentor-app \
  --settings PORT=8000

# Set all required environment variables (API keys, endpoints, deployment info) for the web app
az webapp config appsettings set \
  --name smart-career-mentor-app \
  --resource-group Smart_Career_Mentor_Agent \
  --settings \
    AZURE_OPENAI_KEY="<>" \
    FORM_RECOGNIZER_KEY="<>" \
    FORM_RECOGNIZER_ENDPOINT=https://form-recognizer-career-agent.cognitiveservices.azure.com/ \
    AZURE_OPENAI_ENDPOINT=https://openai-career-agent.openai.azure.com/ \
    AZURE_OPENAI_DEPLOYMENT=chat-gpt-35-turbo \
    AZURE_OPENAI_VERSION=2025-04-01-preview
```

---

## 💼 Features

- Resume parsing with structured data output.
- Skill and role extraction using GPT models.
- Mapping skills to job roles.
- Skill gap analysis and personalized course recommendations.
- Streamlit-based interactive UI.
