import re
import os
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -------------------------------------------------
# ROLE → SKILL DICTIONARY
# -------------------------------------------------
ROLE_SKILLS = {

    "ML Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch", "Scikit-learn",
        "NLP", "Computer Vision",
        "Data Structures", "Algorithms",
        "SQL", "Docker", "Kubernetes"
    ],

    "Data Scientist": [
        "Python", "Machine Learning", "Deep Learning",
        "Pandas", "NumPy", "SQL",
        "Statistics", "Matplotlib",
        "Seaborn", "NLP"
    ],

    "Data Analyst": [
        "SQL", "Power BI", "Tableau",
        "Excel", "Python",
        "Statistics", "Pandas"
    ],

    "Data Engineer": [
        "Python", "SQL", "Spark",
        "Hadoop", "ETL",
        "AWS", "Azure",
        "Airflow", "Docker"
    ],

    "Software Engineer": [
        "Java", "C++", "Python",
        "Data Structures", "Algorithms",
        "System Design", "OOP"
    ],

    "Backend Developer": [
        "Java", "Python", "Node.js",
        "SQL", "MongoDB",
        "REST API", "Docker"
    ],

    "Frontend Developer": [
        "HTML", "CSS", "JavaScript",
        "React", "Angular",
        "TypeScript"
    ],

    "Full Stack Developer": [
        "JavaScript", "React",
        "Node.js", "SQL",
        "MongoDB", "Docker"
    ],

    "DevOps Engineer": [
        "Docker", "Kubernetes",
        "CI/CD", "Jenkins",
        "AWS", "Linux", "Terraform"
    ]
}


# -------------------------------------------------
# ROLE ALIASES (VERY IMPORTANT)
# -------------------------------------------------
ROLE_ALIASES = {
    "ML Engineer": ["ml engineer", "machine learning engineer"],
    "Data Scientist": ["data scientist"],
    "Data Analyst": ["data analyst"],
    "Data Engineer": ["data engineer"],
    "Software Engineer": ["software engineer", "sde"],
    "Backend Developer": ["backend developer", "backend engineer"],
    "Frontend Developer": ["frontend developer"],
    "Full Stack Developer": ["full stack developer"],
    "DevOps Engineer": ["devops engineer"]
}


# -------------------------------------------------
# PDF TEXT EXTRACTION
# -------------------------------------------------
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


# -------------------------------------------------
# DETECT ROLE
# -------------------------------------------------
def detect_role(jd_text):
    jd_text = jd_text.lower()

    for role, aliases in ROLE_ALIASES.items():
        for alias in aliases:
            if alias in jd_text:
                return role

    return None


# -------------------------------------------------
# NORMALIZE TEXT (handles ML, PowerBI etc.)
# -------------------------------------------------
def normalize_text(text):
    replacements = {
        "ml": "Machine Learning",
        "powerbi": "Power BI",
        "deep learning": "Deep Learning"
    }

    text_lower = text.lower()

    for key, value in replacements.items():
        if key in text_lower:
            text += " " + value

    return text


# -------------------------------------------------
# EXTRACT SKILLS
# -------------------------------------------------
def extract_skills(text, role=None):

    text = normalize_text(text)

    if role and role in ROLE_SKILLS:
        skill_list = ROLE_SKILLS[role]
    else:
        # fallback to all skills
        skill_list = list(
            set(skill for skills in ROLE_SKILLS.values() for skill in skills)
        )

    found_skills = []

    for skill in skill_list:
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


# -------------------------------------------------
# SKILL GAP ANALYSIS
# -------------------------------------------------
def skill_gap_analysis(resume_text, jd_text):

    role = detect_role(jd_text)

    if role:
        print(f"\n🎯 Detected Role: {role}")
    else:
        print("\n⚠ Role not detected. Using general skill matching.")

    resume_skills = extract_skills(resume_text, role)
    jd_skills = extract_skills(jd_text, role)

    missing_skills = list(set(jd_skills) - set(resume_skills))

    return resume_skills, jd_skills, sorted(missing_skills)


# -------------------------------------------------
# GENERATE INTERVIEW QUESTIONS
# -------------------------------------------------
def generate_questions(missing_skills):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("❌ OpenAI API Key not found. Check your .env file.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are a technical interviewer.

    Generate 5 interview questions based on:
    {missing_skills}

    For each question include:
    - Difficulty level
    - What interviewer expects
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content