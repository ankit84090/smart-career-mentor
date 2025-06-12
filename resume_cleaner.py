# 📦 Import libraries
import re           # For pattern matching (emails, phone numbers)
import spacy        # spaCy is a powerful NLP library for text processing

# 🔧 Load spaCy’s small English language model
nlp = spacy.load("en_core_web_sm")

# 🧹 Function to clean up extra whitespace from the resume text
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()  # replaces multiple spaces/newlines with single space

# 📧 Function to extract email using regex pattern
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

# 📱 Function to extract phone number (basic 10-digit format)
def extract_phone(text):
    match = re.search(r'\b\d{10}\b', text)
    return match.group(0) if match else None

# 🧑 Function to extract person's name using NLP (NER)
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":  # spaCy identifies "PERSON" entities
            return ent.text
    return None

# 🛠️ Function to extract known skills from text
def extract_skills(text):
    # This is a simple skill list - we’ll enhance it later using GPT
    skill_keywords = [
        'python', 'azure', 'aws', 'kubernetes', 'terraform',
        'pandas', 'sql', 'docker', 'streamlit'
    ]
    
    found = []
    for skill in skill_keywords:
        if skill.lower() in text.lower():  # case-insensitive match
            found.append(skill)

    return list(set(found))  # remove duplicates

# 🔄 Main function to combine all extraction into one dictionary
def parse_structured_data(text):
    text = clean_text(text)  # Clean up the raw text first

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "raw_text": text  # store original cleaned text for reference
    }
