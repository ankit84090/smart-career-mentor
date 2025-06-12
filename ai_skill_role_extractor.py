import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI  # New in openai>=1.0.0

# Load environment variables
load_dotenv()

# Configure Azure OpenAI Client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # The specific deployment/model name

# Function to extract skills and suggest job roles from resume text using Azure OpenAI
def extract_skills_and_role_gpt(text):
    """
    Sends the cleaned resume text to Azure OpenAI to extract skills and suggest job roles.

    Args:
        text (str): The resume content as plain text.

    Returns:
        dict: JSON object with name, skills list, and suggested role, or fallback if failed.
    """

    prompt = f"""
You are an intelligent AI resume parser and expert career assistant.
Based on the following resume text, extract:
- Full name (if available)
- Key technical or professional skills
- A recommended job role

Please return ONLY a JSON object with this structure:

{{
  "name": "<full_name>",
  "skills": ["skill1", "skill2", "skill3"],
  "suggested_role": "<best_matched_role>"
}}

Resume Text:
\"\"\"
{text}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        result_text = response.choices[0].message.content.strip()

        # Attempt to parse JSON from response
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            print("⚠️ GPT response was not valid JSON:\n", result_text)
            return {
                "name": None,
                "skills": [],
                "suggested_role": "Not identified"
            }

    except Exception as e:
        print("Error during GPT call:", str(e))
        return {
            "name": None,
            "skills": [],
            "suggested_role": "Not identified"
        }

# For local test runs
if __name__ == "__main__":
    from resume_parser import parse_resume
    resume_text = parse_resume("sample_resume.pdf")
    result = extract_skills_and_role_gpt(resume_text)
    print("\n==== GPT Output ====\n")
    print(result)
