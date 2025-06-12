import json
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# ✅ Load Azure OpenAI credentials from .env
load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION")
)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# ✅ Load resume details
with open("parsed_resume.json", "r") as f:
    structured_data = json.load(f)

resume_skills = structured_data["skills"]
target_role = structured_data["suggested_role"]

# ✅ GPT to dynamically suggest balanced required skills
def get_required_skills_from_gpt(role):
    prompt = f"""
You are an AI career mentor. A candidate has resume skills: {resume_skills} and wants to become a {role}.
Your goal is to identify the most relevant technical and soft skills they should know for this role.

💡 Guidelines:
1. Recommend 6–10 balanced and practical skills (not just Azure-specific).
2. Skills should include general architecture, DevOps, security, cloud principles, and platform-specific ones where needed.
3. Expand abbreviations (e.g., IaC → Infrastructure as Code), but avoid redundancy if both are present.
4. If 'IaC' is already in skills, don't re-suggest it as 'Infrastructure as Code'.
5. Do not overfit to just one cloud (e.g., Azure), suggest transferable skills too (e.g., CI/CD, Networking).
6. Return a clean Python list of strings.

Return output like:
['Solution Design', 'Infrastructure as Code', 'CI/CD', 'Monitoring', 'Cost Optimization']
    """
    response = client.chat.completions.create(
        model=deployment_name,
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a helpful AI career advisor."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content.strip()

    try:
        required_skills = eval(content) if isinstance(content, str) else content
        if isinstance(required_skills, list):
            return required_skills
        else:
            raise ValueError("Expected a list.")
    except Exception as e:
        print("⚠️ Invalid skill list from GPT:", e)
        return []

required_skills = get_required_skills_from_gpt(target_role)
missing_skills = list(set(required_skills) - set(resume_skills))

print("\n==== SKILL GAP REPORT ====")
print(f"🎯 Suggested Role: {target_role}")
print(f"📎 Resume Skills: {resume_skills}")
print(f"📌 Required Skills (GPT): {required_skills}")
print(f"❌ Missing Skills: {missing_skills}")

# ✅ GPT to recommend platform-matched, beginner-level courses
def get_course_recommendations(missing_skills, role):
    if not missing_skills:
        return "🎉 You already have all key skills needed!"

    prompt = f"""
Act as a personalized AI career coach and course recommender.

A user is targeting the role: {role}.
They are missing these skills: {missing_skills}

🎯 Task:
For each missing skill, recommend:
1. 4-5 beginner-level online course from platform like eg. Microsoft Learn, Linkedin, Coursera, edX, YouTube, Udemy, etc.
2. 3-4 trusted learning website for self-paced tutorials from platform like eg. Microsoft Learn, Medium, MS Community, trusted websites, etc.

🎯 Rules:
- Match the learning platform and content to the domain like Azure, AWS, Data Science, GCP, DevOps, etc.
- Avoid platform mismatch (e.g., AWS content for Azure role)
- Provide URLs if possible
- Expand abbreviations (e.g., IaC → Infrastructure as Code), but avoid duplicates

Output in readable markdown-style format.
    """
    response = client.chat.completions.create(
        model=deployment_name,
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a career mentor and course recommender."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

recommendations = get_course_recommendations(missing_skills, target_role)

print("\n==== RECOMMENDED COURSES ====\n")
print(recommendations)

# ✅ Save the skill gap report and recommendations to a JSON file
output_data = {
    "target_role": target_role,
    "resume_skills": resume_skills,
    "required_skills": required_skills,
    "missing_skills": missing_skills,
    "course_recommendations_markdown": recommendations
}

with open("skill_gap_output.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("\n✅ Skill gap report saved to skill_gap_output.json")
