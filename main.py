import os
from utils import (
    extract_text_from_pdf,
    skill_gap_analysis,
    generate_questions
)

def main():

    print("\n" + "="*60)
    print("🚀 AI INTERVIEW MENTOR + SKILL GAP ANALYZER")
    print("="*60 + "\n")

    resume_path = input("📄 Enter Resume PDF Path: ").strip().strip('"')
    resume_path = resume_path.replace("\\", "/")

    if not os.path.exists(resume_path):
        print("\n❌ Resume file not found.")
        return

    print("\n📝 Paste Job Description (Press Enter twice to finish):")

    jd_lines = []
    while True:
        line = input()
        if line == "":
            break
        jd_lines.append(line)

    jd_text = "\n".join(jd_lines)

    if not jd_text.strip():
        print("\n❌ Job description cannot be empty.")
        return

    print("\n🔍 Processing...\n")

    resume_text = extract_text_from_pdf(resume_path)
    resume_skills, jd_skills, missing_skills = skill_gap_analysis(resume_text, jd_text)

    print("="*60)
    print("✅ YOUR SKILLS:")
    print(resume_skills)

    print("\n📌 REQUIRED SKILLS:")
    print(jd_skills)

    print("\n❌ MISSING SKILLS:")
    print(missing_skills)
    print("="*60)

    if missing_skills:
        choice = input("\nGenerate Interview Questions? (y/n): ")

        if choice.lower() == "y":
            print("\n🧠 Generating Questions...\n")
            questions = generate_questions(missing_skills)

            print("="*60)
            print("🎯 INTERVIEW QUESTIONS")
            print("="*60)
            print(questions)
    else:
        print("\n🎉 Great! No major skill gaps found.")


if __name__ == "__main__":
    main()