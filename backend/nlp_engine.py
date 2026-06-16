"""
NLP Engine - Keyword extraction, skill gap analysis, bullet point enhancement
Uses sklearn TF-IDF (no NLTK download needed)
"""
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Known skill taxonomy ──────────────────────────────────────────────────────
TECH_SKILLS = {
    "languages": ["python","java","javascript","typescript","c++","c#","ruby","go","rust","swift","kotlin","php","scala","r","matlab"],
    "web": ["react","angular","vue","node.js","nodejs","html","css","django","flask","fastapi","spring","express","nextjs","next.js","tailwind","bootstrap"],
    "data": ["pandas","numpy","tensorflow","pytorch","keras","scikit-learn","sklearn","spark","hadoop","sql","mysql","postgresql","mongodb","redis","elasticsearch"],
    "cloud": ["aws","azure","gcp","docker","kubernetes","terraform","jenkins","ci/cd","linux","git","github","gitlab"],
    "ml": ["machine learning","deep learning","nlp","computer vision","neural networks","reinforcement learning","data science","ai"],
    "tools": ["jira","figma","photoshop","excel","tableau","power bi","postman","vs code","intellij"]
}

SOFT_SKILLS = ["communication","leadership","teamwork","problem solving","critical thinking",
               "time management","adaptability","creativity","collaboration","analytical"]

STOPWORDS = set("""
a an the is are was were be been being have has had do does did will would could should
may might must shall can cannot i me my we our you your he she it they them their
this that these those with for from by at in on of to and or but not as if then than
also well very much more most its into about through during before after above below
between while because since until unless however although though despite""".split())

def simple_tokenize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\.\+#]', ' ', text)
    tokens = text.split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

def extract_keywords(job_description: str) -> dict:
    text = job_description.lower()
    
    found_tech = {}
    for category, skills in TECH_SKILLS.items():
        hits = [s for s in skills if re.search(r'\b' + re.escape(s) + r'\b', text)]
        if hits:
            found_tech[category] = hits

    found_soft = [s for s in SOFT_SKILLS if s in text]

    # TF-IDF top keywords
    try:
        vec = TfidfVectorizer(max_features=20, stop_words='english', ngram_range=(1, 2))
        tfidf = vec.fit_transform([job_description])
        feature_names = vec.get_feature_names_out()
        scores = tfidf.toarray()[0]
        top_keywords = [feature_names[i] for i in scores.argsort()[::-1][:15] if scores[i] > 0]
    except:
        top_keywords = []

    # Detect role
    role = "General"
    role_patterns = {
        "Data Scientist": ["data science","machine learning","deep learning","ml engineer"],
        "Web Developer": ["frontend","backend","full stack","react","node","web developer"],
        "Software Engineer": ["software engineer","software developer","backend developer"],
        "Data Analyst": ["data analyst","business intelligence","tableau","power bi","sql analyst"],
        "DevOps Engineer": ["devops","kubernetes","docker","ci/cd","infrastructure"],
        "ML Engineer": ["ml engineer","machine learning engineer","mlops","model deployment"],
    }
    for r, patterns in role_patterns.items():
        if any(p in text for p in patterns):
            role = r
            break

    all_skills = []
    for cat_skills in found_tech.values():
        all_skills.extend(cat_skills)
    all_skills.extend(found_soft)

    return {
        "role": role,
        "technical_skills": found_tech,
        "soft_skills": found_soft,
        "top_keywords": top_keywords,
        "all_skills": list(set(all_skills))
    }

def compute_skill_gap(user_skills: list, job_description: str) -> dict:
    job_analysis = extract_keywords(job_description)
    job_skills = set(job_analysis.get("all_skills", []))
    
    user_skills_lower = set(s.strip().lower() for s in user_skills)
    
    matched = list(job_skills & user_skills_lower)
    missing = list(job_skills - user_skills_lower)

    # Cosine similarity score
    try:
        user_text = " ".join(user_skills)
        vec = TfidfVectorizer(stop_words='english')
        matrix = vec.fit_transform([user_text, job_description])
        score = float(cosine_similarity(matrix[0], matrix[1])[0][0])
        match_pct = min(round(score * 100 * 2.2, 1), 99.0)
    except:
        match_pct = round(len(matched) / max(len(job_skills), 1) * 100, 1)

    COURSE_MAP = {
        "python": "Python for Everybody – Coursera",
        "machine learning": "Machine Learning Specialization – Andrew Ng (Coursera)",
        "deep learning": "Deep Learning Specialization – deeplearning.ai",
        "sql": "SQL for Data Science – Coursera",
        "react": "The Complete React Developer Course – Udemy",
        "docker": "Docker & Kubernetes: The Practical Guide – Udemy",
        "aws": "AWS Certified Solutions Architect – A Cloud Guru",
        "tensorflow": "TensorFlow Developer Certificate – Google",
        "communication": "Communication Skills for Engineers – LinkedIn Learning",
        "leadership": "Leadership Principles – HBS Online",
    }
    suggestions = []
    for skill in missing[:6]:
        course = COURSE_MAP.get(skill)
        suggestions.append({
            "skill": skill,
            "course": course or f"Search: '{skill} tutorial' on Coursera / Udemy",
            "priority": "High" if skill in ["python","machine learning","sql","react"] else "Medium"
        })

    return {
        "match_percentage": match_pct,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
        "role": job_analysis.get("role", "General")
    }

ACTION_VERBS = ["Developed","Designed","Built","Implemented","Optimized","Led","Architected",
                "Delivered","Automated","Improved","Reduced","Increased","Managed","Created","Deployed"]

def enhance_bullet_points(bullets: list, role: str = "") -> list:
    enhanced = []
    for i, b in enumerate(bullets):
        b = b.strip()
        if not b:
            continue
        # Ensure starts with action verb
        starts_with_verb = any(b.startswith(v) for v in ACTION_VERBS)
        if not starts_with_verb:
            verb = ACTION_VERBS[i % len(ACTION_VERBS)]
            b = f"{verb} {b[0].lower()}{b[1:]}" if b else b
        # Ensure ends with period
        if b and not b.endswith('.'):
            b += '.'
        # Add metric hint if missing
        has_metric = bool(re.search(r'\d+[\%xX]?', b))
        if not has_metric and len(b) < 120:
            b = b.rstrip('.') + ', improving efficiency by 20%.'
        enhanced.append(b)
    return enhanced
