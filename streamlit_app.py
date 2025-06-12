import streamlit as st
import os
import tempfile
import uuid
import json

from resume_parser import parse_resume
from ai_skill_role_extractor import extract_skills_and_role_gpt
from role_mapper import match_skills_to_roles
from skill_gap_recommender import get_required_skills_from_gpt, get_course_recommendations
from fpdf import FPDF

# Streamlit Config
# Fancy Header for Smart Career Mentor
st.markdown(
    """
    <div style='
        border: 2px solid #4CAF50;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
        text-align: center;
    '>
        <h1 style='
            font-size: 36px;
            color: #2E7D32;
            font-family: "Segoe UI", sans-serif;
            margin: 0;
        '>🎯 Smart Career Mentor</h1>
        <p style='
            font-size: 16px;
            color: #555;
        '>Personalized skill gap reports and learning paths based on your resume</p>
    </div>
    """,
    unsafe_allow_html=True
)


def safe_text(text):
    return text.encode('latin1', errors='ignore').decode('latin1')

uploaded_files = st.file_uploader("📄 Upload Resume Files", type=["pdf", "docx"], accept_multiple_files=True)

resume_outputs = {}

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[1].lower()
        unique_id = str(uuid.uuid4())[:8]

        try:
            # Save uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(file.read())
                tmp_file_path = tmp_file.name

            # Pass the file path to parse_resume
            parsed_result = parse_resume(tmp_file_path)
            extracted_skills = parsed_result.get("skills", [])
            extracted_text = parsed_result.get("text", "")

            gpt_result = extract_skills_and_role_gpt(extracted_text)
            resume_skills = gpt_result.get("skills", [])
            suggested_role = gpt_result.get("suggested_role", "Not identified")

            matched_role = match_skills_to_roles(resume_skills)
            target_role = matched_role or suggested_role

            required_skills = get_required_skills_from_gpt(target_role)
            missing_skills = list(set(required_skills) - set(resume_skills))
            recommendations_md = get_course_recommendations(missing_skills, target_role)

            resume_outputs[file.name] = {
                "resume_skills": resume_skills,
                "required_skills": required_skills,
                "missing_skills": missing_skills,
                "suggested_role": target_role,
                "recommendations_md": recommendations_md
            }

            os.remove(tmp_file_path)  # Clean up

        except Exception as e:
            st.error(f"⚠️ Error processing `{file.name}`: {str(e)}")

    # UI to Select and Show Output
    if resume_outputs:
        selected_resume = st.selectbox("🔍 Select Resume to View Analysis", list(resume_outputs.keys()))
        result = resume_outputs[selected_resume]

        st.markdown(f"<h4 style='color:#4CAF50;'>🎯 Suggested Role:</h4><b>{result['suggested_role']}</b>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='color:#03A9F4;'>🧠 Resume Skills:</h5>{', '.join(result['resume_skills'])}", unsafe_allow_html=True)
        st.markdown(f"<h5 style='color:#FFC107;'>✅ Required Skills:</h5>{', '.join(result['required_skills'])}", unsafe_allow_html=True)
        st.markdown(f"<h5 style='color:#F44336;'>❌ Missing Skills:</h5>{', '.join(result['missing_skills']) or 'None 🎉'}", unsafe_allow_html=True)
        st.markdown(f"<h5 style='color:#9C27B0;'>📚 Course Recommendations:</h5>", unsafe_allow_html=True)
        st.markdown(result["recommendations_md"], unsafe_allow_html=True)

        # PDF Generator
        def generate_pdf(data, filename):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(33, 150, 243)
            pdf.set_font("Arial", style="B")
            pdf.cell(200, 10, txt=safe_text(f"Smart Career Mentor Report: {filename}"), ln=True, align="C")
            pdf.set_font("Arial")
            pdf.set_text_color(0, 0, 0)

            pdf.ln(10)
            pdf.multi_cell(0, 8, txt=safe_text(f"🎯 Suggested Role: {data['suggested_role']}"))
            pdf.ln(4)
            pdf.multi_cell(0, 8, txt=safe_text(f"🧠 Resume Skills:\n{', '.join(data['resume_skills'])}"))
            pdf.ln(2)
            pdf.multi_cell(0, 8, txt=safe_text(f"✅ Required Skills:\n{', '.join(data['required_skills'])}"))
            pdf.ln(2)
            pdf.multi_cell(0, 8, txt=safe_text(f"❌ Missing Skills:\n{', '.join(data['missing_skills']) or 'None'}"))

            pdf.ln(4)
            pdf.set_font("Arial", style="B")
            pdf.cell(0, 10, txt=safe_text("📚 Course Recommendations"), ln=True)
            pdf.set_font("Arial")

            lines = data["recommendations_md"].replace('<h6>', '').replace('</h6>', '') \
                .replace('<ul>', '').replace('</ul>', '') \
                .replace('<li>', '- ').replace('</li>', '').split('\n')

            for line in lines:
                clean = line.strip()
                if clean:
                    pdf.multi_cell(0, 7, txt=safe_text(clean))

            tmp_dir = tempfile.gettempdir()
            safe_filename = filename.replace('.pdf', '').replace(' ', '_')
            tmp_pdf_path = os.path.join(tmp_dir, f"{safe_filename}_report.pdf")
            pdf.output(tmp_pdf_path)
            return tmp_pdf_path

        pdf_path = generate_pdf(result, selected_resume)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Full Analysis (PDF)",
                data=pdf_file,
                file_name=f"{selected_resume.replace('.pdf','')}_analysis.pdf",
                mime="application/pdf"
            )

else:
    st.info("📌 Please upload at least one resume (PDF) to begin.")
