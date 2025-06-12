from azure.ai.formrecognizer import DocumentAnalysisClient # It's what sends documents to Azure and gets results
from azure.core.credentials import AzureKeyCredential      # This lets you securely authenticate using your API key
import os
from dotenv import load_dotenv # utility that loads sensitive variables (like API keys, endpoints) from a hidden .env file into Python code

# Load environment variables
load_dotenv()

# Load Secrets
endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT") # load_dotenv() loads secrets from the .env file
key      = os.getenv("FORM_RECOGNIZER_KEY")      # os.getenv("XYZ") fetches them in your code

# This line creates an authenticated Form Recognizer client so you can send documents to Azure
client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# This defines a function that will take a resume (PDF) file path and return extracted text
def parse_resume(file_path):
    with open(file_path, "rb") as f: # Open the PDF file in binary mode
        # Sends the document to Azure using the "prebuilt-document" model.
        # "prebuilt-document" is a pre-trained model that can extract text from various document types. 
        # This is a general model that works well for resumes, invoices, etc.
        poller = client.begin_analyze_document("prebuilt-document", document=f)
        # Wait for the analysis to complete and get the result
        result = poller.result()

    # Goes through every page and every line.
    # Collects all the text in order.
    # Stores in a single extracted_text variable.
    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"

    # Extract structured data using existing cleaner logic
    from resume_cleaner import parse_structured_data
    structured_data = parse_structured_data(extracted_text)

    # Return both raw text and structured skills as a dictionary
    return {
        "text": extracted_text,
        "skills": structured_data.get("skills", [])
    }

# This is the main entry point of the script.
# It imports the parse_resume function from this file and the parse_structured_data function from resume_cleaner.py.
# It then calls parse_resume to extract text from a sample resume file and prints the structured data.
from resume_cleaner import parse_structured_data
if __name__ == "__main__": # Only run this part when I’m running this file directly, not when it’s imported somewhere else.
    parsed_result = parse_resume("sample_resume.pdf") # Extract text and structured skills from the resume PDF file
    print("\n==== EXTRACTED TEXT ====\n")
    print(parsed_result["text"])
    print("\n==== STRUCTURED DATA ====\n")
    print(parsed_result["skills"])
