import json
from resume_parser import parse_resume  # Step 1 parser
from ai_skill_role_extractor import extract_skills_and_role_gpt  # Step 2 GPT skill extractor

# ---------------------------------------------------------
# - Step 3A: Save structured output to local JSON
# ---------------------------------------------------------
def save_to_json(data, filename="parsed_resume.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Data saved to {filename}")

# ---------------------------------------------------------
# - Step 3B: Define role-to-skill mapping manually
# ---------------------------------------------------------
role_skill_map = {
    "Data Analyst": ["SQL", "Excel", "Python", "Tableau"],
    "ML Engineer": ["Python", "Pandas", "Scikit-learn", "ML"],
    "Cloud Architect": ["Azure", "VM", "Networking", "Security"],
    "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes", "Terraform"],
    "Data Engineer": ["Spark", "Hadoop", "Python", "ETL"]
}

# Function to match extracted skills to suitable roles
def match_skills_to_roles(extracted_skills):
    matched_roles = []
    for role, required_skills in role_skill_map.items():
        overlap = set(skill.lower() for skill in extracted_skills) & set(skill.lower() for skill in required_skills)
        if len(overlap) >= 2:  # Simple logic: match if 2+ skills overlap
            matched_roles.append(role)
    return matched_roles

# ---------------------------
# - Main Program
# ---------------------------
if __name__ == "__main__":
    # Step 1: Extract raw text from PDF
    raw_text = parse_resume("sample_resume.pdf")

    # Step 2: Use GPT to extract structured data
    result_string = extract_skills_and_role_gpt(raw_text)
    print("\n==== RAW GPT OUTPUT ====")
    print(result_string)
    try:
        structured_data = json.loads(result_string)
    except json.JSONDecodeError:
        print("❌ Error: GPT output is not valid JSON.")
        structured_data = {}

    print("\n==== STRUCTURED OUTPUT FROM GPT ====")
    print(structured_data)

    # Step 3A: Save to JSON
    save_to_json(structured_data)

    # Step 3B: Match roles
    extracted_skills = structured_data.get("skills", [])
    if isinstance(extracted_skills, str):
        extracted_skills = [skill.strip() for skill in extracted_skills.split(",")]

    recommended_roles = match_skills_to_roles(extracted_skills)

    print("\n==== RECOMMENDED ROLES BASED ON SKILLS ====")
    for role in recommended_roles:
        print(f"- {role}")
