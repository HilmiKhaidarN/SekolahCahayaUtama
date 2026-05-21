from flask import Blueprint, render_template, request, session, current_app
from flask_login import login_required, current_user

sdg_bp = Blueprint("sdg", __name__)

# 10 soal kuis SDG — mencakup berbagai poin SDG
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "sdg": 4,
        "question": "SDG 4 berfokus pada bidang apa?",
        "options": ["Kesehatan", "Pendidikan Berkualitas", "Energi Bersih", "Kesetaraan Gender"],
        "answer": 1,
        "explanation": "SDG 4 (Quality Education) bertujuan memastikan pendidikan inklusif dan berkualitas serta mendorong kesempatan belajar seumur hidup bagi semua orang.",
    },
    {
        "id": 2,
        "sdg": 1,
        "question": "SDG 1 menargetkan penghapusan apa pada tahun 2030?",
        "options": ["Polusi udara", "Kemiskinan ekstrem", "Korupsi", "Pengangguran"],
        "answer": 1,
        "explanation": "SDG 1 (No Poverty) menargetkan mengakhiri kemiskinan dalam segala bentuknya di seluruh dunia, termasuk kemiskinan ekstrem di bawah $1,90/hari.",
    },
    {
        "id": 3,
        "sdg": 13,
        "question": "SDG 13 berkaitan dengan tindakan terhadap apa?",
        "options": ["Perdagangan bebas", "Perubahan iklim", "Migrasi penduduk", "Teknologi digital"],
        "answer": 1,
        "explanation": "SDG 13 (Climate Action) mendorong tindakan segera untuk memerangi perubahan iklim dan dampaknya melalui kebijakan, edukasi, dan inovasi.",
    },
    {
        "id": 4,
        "sdg": 3,
        "question": "SDG 3 bertujuan memastikan apa bagi semua orang?",
        "options": ["Akses internet", "Kehidupan sehat dan sejahtera", "Perumahan layak", "Pekerjaan tetap"],
        "answer": 1,
        "explanation": "SDG 3 (Good Health and Well-Being) memastikan kehidupan yang sehat dan mendorong kesejahteraan bagi semua orang di segala usia.",
    },
    {
        "id": 5,
        "sdg": 6,
        "question": "SDG 6 berfokus pada akses universal terhadap apa?",
        "options": ["Listrik", "Air bersih dan sanitasi", "Transportasi", "Pangan bergizi"],
        "answer": 1,
        "explanation": "SDG 6 (Clean Water and Sanitation) memastikan ketersediaan dan pengelolaan air bersih serta sanitasi yang berkelanjutan untuk semua.",
    },
    {
        "id": 6,
        "sdg": 5,
        "question": "SDG 5 berfokus pada pencapaian apa?",
        "options": ["Kesetaraan gender", "Perdamaian dunia", "Energi terbarukan", "Kota berkelanjutan"],
        "answer": 0,
        "explanation": "SDG 5 (Gender Equality) bertujuan mencapai kesetaraan gender dan memberdayakan semua perempuan dan anak perempuan di seluruh dunia.",
    },
    {
        "id": 7,
        "sdg": 2,
        "question": "SDG 2 bertujuan mengakhiri apa pada 2030?",
        "options": ["Perang", "Kelaparan", "Kemiskinan kota", "Polusi laut"],
        "answer": 1,
        "explanation": "SDG 2 (Zero Hunger) bertujuan mengakhiri kelaparan, mencapai ketahanan pangan, meningkatkan gizi, dan mendorong pertanian berkelanjutan.",
    },
    {
        "id": 8,
        "sdg": 7,
        "question": "SDG 7 mendorong akses universal terhadap energi yang bagaimana?",
        "options": ["Murah dan berlimpah", "Terjangkau, andal, dan berkelanjutan", "Nuklir dan efisien", "Fosil dan terbarukan"],
        "answer": 1,
        "explanation": "SDG 7 (Affordable and Clean Energy) memastikan akses ke energi yang terjangkau, andal, berkelanjutan, dan modern bagi semua orang.",
    },
    {
        "id": 9,
        "sdg": 14,
        "question": "SDG 14 berfokus pada konservasi apa?",
        "options": ["Hutan hujan", "Kehidupan di bawah air / lautan", "Satwa liar darat", "Lapisan ozon"],
        "answer": 1,
        "explanation": "SDG 14 (Life Below Water) bertujuan melestarikan dan memanfaatkan secara berkelanjutan samudra, laut, dan sumber daya kelautan.",
    },
    {
        "id": 10,
        "sdg": 17,
        "question": "SDG 17 menekankan pentingnya apa untuk mencapai semua tujuan SDG?",
        "options": ["Teknologi AI", "Kemitraan global", "Militer yang kuat", "Ekspansi ekonomi"],
        "answer": 1,
        "explanation": "SDG 17 (Partnerships for the Goals) memperkuat sarana pelaksanaan dan merevitalisasi kemitraan global untuk pembangunan berkelanjutan.",
    },
]

SDG_LIST = [
    {"no": 1,  "title": "Tanpa Kemiskinan",         "color": "block-coral",  "icon": "🏠", "desc": "Mengakhiri kemiskinan dalam segala bentuknya di seluruh dunia."},
    {"no": 2,  "title": "Tanpa Kelaparan",           "color": "block-lime",   "icon": "🌾", "desc": "Mengakhiri kelaparan, mencapai ketahanan pangan dan gizi yang baik."},
    {"no": 3,  "title": "Kehidupan Sehat",           "color": "block-mint",   "icon": "❤️", "desc": "Memastikan kehidupan sehat dan mendorong kesejahteraan semua usia."},
    {"no": 4,  "title": "Pendidikan Berkualitas",    "color": "block-lilac",  "icon": "📚", "desc": "Pendidikan inklusif, berkualitas, dan kesempatan belajar seumur hidup."},
    {"no": 5,  "title": "Kesetaraan Gender",         "color": "block-pink",   "icon": "⚖️", "desc": "Mencapai kesetaraan gender dan memberdayakan perempuan dan anak perempuan."},
    {"no": 6,  "title": "Air Bersih & Sanitasi",     "color": "block-cream",  "icon": "💧", "desc": "Ketersediaan dan pengelolaan air bersih serta sanitasi berkelanjutan."},
    {"no": 7,  "title": "Energi Bersih",             "color": "block-lime",   "icon": "⚡", "desc": "Akses ke energi terjangkau, andal, berkelanjutan, dan modern."},
    {"no": 8,  "title": "Pekerjaan Layak",           "color": "block-coral",  "icon": "💼", "desc": "Pertumbuhan ekonomi inklusif dan pekerjaan layak untuk semua."},
    {"no": 9,  "title": "Industri & Inovasi",        "color": "block-cream",  "icon": "🏭", "desc": "Infrastruktur tangguh, industrialisasi inklusif, dan inovasi."},
    {"no": 10, "title": "Berkurangnya Kesenjangan",  "color": "block-lilac",  "icon": "📊", "desc": "Mengurangi ketimpangan di dalam dan antar negara."},
    {"no": 11, "title": "Kota Berkelanjutan",        "color": "block-mint",   "icon": "🏙️", "desc": "Kota dan permukiman yang inklusif, aman, tangguh, dan berkelanjutan."},
    {"no": 12, "title": "Konsumsi Bertanggung Jawab","color": "block-lime",   "icon": "♻️", "desc": "Pola konsumsi dan produksi yang bertanggung jawab."},
    {"no": 13, "title": "Penanganan Perubahan Iklim","color": "block-navy",   "icon": "🌍", "desc": "Tindakan segera untuk memerangi perubahan iklim dan dampaknya."},
    {"no": 14, "title": "Ekosistem Lautan",          "color": "block-mint",   "icon": "🌊", "desc": "Melestarikan dan memanfaatkan samudra dan sumber daya kelautan."},
    {"no": 15, "title": "Ekosistem Daratan",         "color": "block-lime",   "icon": "🌳", "desc": "Melindungi ekosistem darat, hutan, dan keanekaragaman hayati."},
    {"no": 16, "title": "Perdamaian & Keadilan",     "color": "block-lilac",  "icon": "🕊️", "desc": "Masyarakat damai, inklusif, akses keadilan, dan institusi kuat."},
    {"no": 17, "title": "Kemitraan Global",          "color": "block-coral",  "icon": "🤝", "desc": "Memperkuat kemitraan global untuk pembangunan berkelanjutan."},
]


@sdg_bp.route("/sdg")
@login_required
def sdg_overview():
    school_name = current_app.config.get("SCHOOL_NAME")
    return render_template("sdg/overview.html", school_name=school_name, sdg_list=SDG_LIST)


@sdg_bp.route("/sdg/quiz", methods=["GET", "POST"])
@login_required
def sdg_quiz():
    school_name = current_app.config.get("SCHOOL_NAME")

    if request.method == "POST":
        score = 0
        results = []
        for q in QUIZ_QUESTIONS:
            key = f"q{q['id']}"
            raw = request.form.get(key)
            answered = int(raw) if raw is not None else -1
            correct = answered == q["answer"]
            if correct:
                score += 1
            results.append({
                "question": q["question"],
                "sdg": q["sdg"],
                "options": q["options"],
                "answered": answered,
                "answer": q["answer"],
                "correct": correct,
                "explanation": q["explanation"],
            })
        percent = int(score / len(QUIZ_QUESTIONS) * 100)
        session["last_quiz_score"] = score
        return render_template(
            "sdg/quiz_result.html",
            school_name=school_name,
            results=results,
            score=score,
            total=len(QUIZ_QUESTIONS),
            percent=percent,
        )

    return render_template(
        "sdg/quiz.html",
        school_name=school_name,
        questions=QUIZ_QUESTIONS,
        total=len(QUIZ_QUESTIONS),
    )
