import os
import openai
from openai import AzureOpenAI
import json
import re

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
deployment_id = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def extract_skills_and_role_gpt(resume_text):
    prompt = (
        "Based on the following resume text, extract:\n"
        "- A list of professional skills\n"
        "- A single suggested career role (e.g., 'Cloud Consultant')\n\n"
        "Return your response strictly in this JSON format:\n"
        "{\n"
        '  "skills": ["skill1", "skill2", ...],\n'
        '  "suggested_role": "Role Name"\n'
        "}\n\n"
        f"Resume:\n{resume_text}\n"
    )

    try:
        response = client.chat.completions.create(
            model=deployment_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300,
        )
        content = response.choices[0].message.content.strip()

        # Try to load valid JSON from GPT response
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            return {
                "skills": data.get("skills", []),
                "suggested_role": data.get("suggested_role", "Not identified")
            }

    except Exception as e:
        print(f"GPT parsing error: {e}")

    return {
        "skills": [],
        "suggested_role": "Not identified"
    }
