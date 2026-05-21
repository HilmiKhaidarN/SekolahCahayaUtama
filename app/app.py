from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cahaya-utama-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///sekolah.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Nama sekolah dari environment / ConfigMap Kubernetes
    app.config["SCHOOL_NAME"] = os.environ.get("SCHOOL_NAME", "Sekolah Cahaya Utama")
    app.config["SCHOOL_TAGLINE"] = os.environ.get(
        "SCHOOL_TAGLINE", "Belajar Cerdas, Berprestasi Gemilang"
    )

    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Silakan login terlebih dahulu."
    login_manager.login_message_category = "warning"

    # Tambahkan fungsi bawaan Python ke Jinja2
    app.jinja_env.globals.update(enumerate=enumerate)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.student import student_bp
    from app.stress import stress_bp
    from app.sdg import sdg_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(stress_bp)
    app.register_blueprint(sdg_bp)

    # Seed default data
    with app.app_context():
        db.create_all()
        _seed_admin()
        _seed_lessons()

    return app


def _seed_admin():
    from app.models import User

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@cahayautama.sch.id",
            full_name="Administrator",
            role="admin",
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("[SEED] Admin default dibuat: admin / admin123")


def _seed_lessons():
    from app.models import Lesson

    if Lesson.query.count() > 0:
        return  # sudah ada materi, skip

    lessons = [
        # ── Matematika ──
        Lesson(
            title="Operasi Bilangan Bulat",
            subject="Matematika",
            level="Dasar",
            description="Memahami penjumlahan, pengurangan, perkalian, dan pembagian bilangan bulat.",
            content=(
                "BILANGAN BULAT\n\n"
                "Bilangan bulat adalah bilangan yang tidak memiliki pecahan desimal. "
                "Contoh: ..., -3, -2, -1, 0, 1, 2, 3, ...\n\n"
                "OPERASI DASAR\n\n"
                "1. Penjumlahan\n"
                "   Contoh: 5 + (-3) = 2\n"
                "   Aturan: positif + negatif → kurangi, ambil tanda yang lebih besar\n\n"
                "2. Pengurangan\n"
                "   Contoh: 7 - (-2) = 7 + 2 = 9\n"
                "   Aturan: mengurangi bilangan negatif = menambah\n\n"
                "3. Perkalian\n"
                "   (+) × (+) = (+)  →  3 × 4 = 12\n"
                "   (+) × (-) = (-)  →  3 × (-4) = -12\n"
                "   (-) × (-) = (+)  →  (-3) × (-4) = 12\n\n"
                "4. Pembagian\n"
                "   Aturan tanda sama dengan perkalian.\n"
                "   Contoh: (-12) ÷ (-3) = 4\n\n"
                "LATIHAN\n"
                "1. Hitung: (-8) + 15 = ?\n"
                "2. Hitung: 6 × (-7) = ?\n"
                "3. Hitung: (-20) ÷ 4 = ?"
            ),
        ),
        Lesson(
            title="Persamaan Linear Satu Variabel",
            subject="Matematika",
            level="Menengah",
            description="Menyelesaikan persamaan linear dengan satu variabel menggunakan sifat kesetaraan.",
            content=(
                "PERSAMAAN LINEAR SATU VARIABEL (PLSV)\n\n"
                "Bentuk umum: ax + b = c, di mana a ≠ 0\n\n"
                "LANGKAH PENYELESAIAN\n\n"
                "1. Pindahkan konstanta ke ruas kanan\n"
                "2. Pindahkan koefisien variabel ke ruas kiri\n"
                "3. Bagi kedua ruas dengan koefisien variabel\n\n"
                "CONTOH 1\n"
                "2x + 5 = 13\n"
                "2x = 13 - 5\n"
                "2x = 8\n"
                "x = 4\n\n"
                "CONTOH 2\n"
                "3x - 7 = 2x + 1\n"
                "3x - 2x = 1 + 7\n"
                "x = 8\n\n"
                "CONTOH 3 (dengan pecahan)\n"
                "x/2 + 3 = 7\n"
                "x/2 = 4\n"
                "x = 8\n\n"
                "LATIHAN\n"
                "1. Selesaikan: 4x - 3 = 17\n"
                "2. Selesaikan: 5x + 2 = 3x + 10\n"
                "3. Selesaikan: x/3 - 1 = 5"
            ),
        ),
        Lesson(
            title="Teorema Pythagoras",
            subject="Matematika",
            level="Menengah",
            description="Memahami dan menerapkan teorema Pythagoras pada segitiga siku-siku.",
            content=(
                "TEOREMA PYTHAGORAS\n\n"
                "Pada segitiga siku-siku, kuadrat sisi miring (hipotenusa) sama dengan "
                "jumlah kuadrat dua sisi lainnya.\n\n"
                "RUMUS: c² = a² + b²\n"
                "di mana c = hipotenusa (sisi terpanjang)\n\n"
                "CONTOH 1 — Mencari hipotenusa\n"
                "Diketahui: a = 3, b = 4\n"
                "c² = 3² + 4² = 9 + 16 = 25\n"
                "c = √25 = 5\n\n"
                "CONTOH 2 — Mencari sisi lain\n"
                "Diketahui: c = 13, a = 5\n"
                "b² = c² - a² = 169 - 25 = 144\n"
                "b = √144 = 12\n\n"
                "TRIPLE PYTHAGORAS UMUM\n"
                "3-4-5 | 5-12-13 | 8-15-17 | 7-24-25\n\n"
                "LATIHAN\n"
                "1. Segitiga dengan sisi 6 dan 8, berapa hipotenusanya?\n"
                "2. Hipotenusa 10, satu sisi 6, berapa sisi lainnya?\n"
                "3. Apakah 9, 40, 41 merupakan triple Pythagoras?"
            ),
        ),

        # ── Bahasa Indonesia ──
        Lesson(
            title="Teks Deskripsi",
            subject="Bahasa Indonesia",
            level="Dasar",
            description="Memahami struktur dan ciri-ciri teks deskripsi serta cara menulisnya.",
            content=(
                "TEKS DESKRIPSI\n\n"
                "Teks deskripsi adalah teks yang menggambarkan suatu objek secara rinci "
                "sehingga pembaca seolah-olah melihat, mendengar, atau merasakan langsung.\n\n"
                "STRUKTUR TEKS DESKRIPSI\n\n"
                "1. Identifikasi\n"
                "   Pengenalan objek yang akan dideskripsikan.\n"
                "   Contoh: 'Pantai Kuta adalah salah satu pantai terindah di Bali.'\n\n"
                "2. Deskripsi Bagian\n"
                "   Penggambaran detail objek dari berbagai aspek.\n"
                "   Contoh: warna, bentuk, ukuran, suasana, dll.\n\n"
                "3. Simpulan/Kesan\n"
                "   Kesan umum penulis terhadap objek.\n\n"
                "CIRI-CIRI TEKS DESKRIPSI\n"
                "• Menggunakan kata sifat (indah, besar, harum)\n"
                "• Menggunakan kata kerja aktif (mengalir, bersinar, bergoyang)\n"
                "• Menggunakan majas (perumpamaan, personifikasi)\n"
                "• Bersifat spesifik dan detail\n\n"
                "LATIHAN\n"
                "Tulislah teks deskripsi singkat (3 paragraf) tentang ruang kelasmu!"
            ),
        ),
        Lesson(
            title="Teks Argumentasi",
            subject="Bahasa Indonesia",
            level="Lanjutan",
            description="Menyusun teks argumentasi yang logis dengan bukti dan alasan yang kuat.",
            content=(
                "TEKS ARGUMENTASI\n\n"
                "Teks argumentasi adalah teks yang berisi pendapat disertai alasan dan bukti "
                "untuk meyakinkan pembaca.\n\n"
                "STRUKTUR\n\n"
                "1. Pernyataan Posisi (Tesis)\n"
                "   Menyatakan pendapat/posisi penulis secara jelas.\n\n"
                "2. Argumen\n"
                "   Alasan-alasan yang mendukung tesis, disertai data/fakta/contoh.\n\n"
                "3. Penegasan Ulang\n"
                "   Menyimpulkan dan menegaskan kembali posisi penulis.\n\n"
                "TEKNIK ARGUMENTASI\n"
                "• Fakta dan data statistik\n"
                "• Kutipan ahli/pakar\n"
                "• Contoh kasus nyata\n"
                "• Analogi (perbandingan)\n\n"
                "CONTOH TESIS\n"
                "'Penggunaan gadget berlebihan berdampak negatif pada prestasi belajar siswa.'\n\n"
                "CONTOH ARGUMEN\n"
                "Berdasarkan penelitian Universitas Indonesia (2023), siswa yang menggunakan "
                "gadget lebih dari 4 jam/hari memiliki nilai rata-rata 15% lebih rendah.\n\n"
                "LATIHAN\n"
                "Tulislah teks argumentasi tentang: 'Apakah PR (pekerjaan rumah) masih relevan?'"
            ),
        ),

        # ── IPA ──
        Lesson(
            title="Sel — Unit Terkecil Kehidupan",
            subject="IPA",
            level="Dasar",
            description="Mengenal struktur sel, organel, dan perbedaan sel hewan dengan sel tumbuhan.",
            content=(
                "SEL — UNIT TERKECIL KEHIDUPAN\n\n"
                "Sel adalah unit struktural dan fungsional terkecil dari makhluk hidup. "
                "Semua makhluk hidup tersusun dari sel.\n\n"
                "BAGIAN-BAGIAN SEL\n\n"
                "1. Membran Sel\n"
                "   Lapisan tipis yang membungkus sel. Berfungsi mengatur keluar-masuk zat.\n\n"
                "2. Sitoplasma\n"
                "   Cairan kental di dalam sel tempat organel berada.\n\n"
                "3. Inti Sel (Nukleus)\n"
                "   Pusat kendali sel. Mengandung DNA dan mengatur aktivitas sel.\n\n"
                "4. Mitokondria\n"
                "   'Pembangkit listrik' sel. Menghasilkan energi (ATP) melalui respirasi.\n\n"
                "5. Ribosom\n"
                "   Tempat sintesis (pembuatan) protein.\n\n"
                "PERBEDAAN SEL HEWAN & SEL TUMBUHAN\n\n"
                "Sel Tumbuhan memiliki:\n"
                "✓ Dinding sel (dari selulosa)\n"
                "✓ Kloroplas (untuk fotosintesis)\n"
                "✓ Vakuola besar\n\n"
                "Sel Hewan memiliki:\n"
                "✓ Sentriol (untuk pembelahan sel)\n"
                "✗ Tidak punya dinding sel\n"
                "✗ Tidak punya kloroplas\n\n"
                "LATIHAN\n"
                "1. Organel apa yang hanya ada di sel tumbuhan?\n"
                "2. Apa fungsi mitokondria?\n"
                "3. Mengapa sel disebut unit terkecil kehidupan?"
            ),
        ),
        Lesson(
            title="Ekosistem dan Rantai Makanan",
            subject="IPA",
            level="Menengah",
            description="Memahami komponen ekosistem, rantai makanan, dan jaring-jaring makanan.",
            content=(
                "EKOSISTEM\n\n"
                "Ekosistem adalah sistem yang terbentuk dari interaksi antara makhluk hidup "
                "(biotik) dengan lingkungan tak hidup (abiotik).\n\n"
                "KOMPONEN EKOSISTEM\n\n"
                "Biotik (makhluk hidup):\n"
                "• Produsen — tumbuhan hijau (membuat makanan sendiri via fotosintesis)\n"
                "• Konsumen — hewan yang memakan produsen atau konsumen lain\n"
                "• Dekomposer — jamur & bakteri (mengurai sisa organisme)\n\n"
                "Abiotik (tak hidup):\n"
                "• Cahaya matahari, air, tanah, udara, suhu\n\n"
                "RANTAI MAKANAN\n\n"
                "Aliran energi dari satu organisme ke organisme lain.\n\n"
                "Contoh:\n"
                "Rumput → Belalang → Katak → Ular → Elang\n"
                "(Produsen → Konsumen I → Konsumen II → Konsumen III → Konsumen IV)\n\n"
                "JARING-JARING MAKANAN\n"
                "Gabungan beberapa rantai makanan yang saling berhubungan.\n\n"
                "PIRAMIDA ENERGI\n"
                "Energi berkurang ~90% di setiap tingkat trofik. "
                "Itulah mengapa hewan karnivora puncak jumlahnya sedikit.\n\n"
                "LATIHAN\n"
                "1. Buatlah rantai makanan dari ekosistem sawah!\n"
                "2. Apa yang terjadi jika katak punah dari rantai makanan di atas?\n"
                "3. Apa peran dekomposer dalam ekosistem?"
            ),
        ),

        # ── IPS ──
        Lesson(
            title="Letak Geografis Indonesia",
            subject="IPS",
            level="Dasar",
            description="Memahami posisi geografis Indonesia dan pengaruhnya terhadap kehidupan.",
            content=(
                "LETAK GEOGRAFIS INDONESIA\n\n"
                "Indonesia terletak di antara dua benua (Asia dan Australia) dan "
                "dua samudra (Hindia dan Pasifik).\n\n"
                "KOORDINAT GEOGRAFIS\n"
                "• Lintang: 6°LU – 11°LS\n"
                "• Bujur: 95°BT – 141°BT\n\n"
                "BATAS WILAYAH\n"
                "• Utara: Malaysia, Singapura, Filipina, Laut China Selatan\n"
                "• Selatan: Australia, Samudra Hindia\n"
                "• Barat: Samudra Hindia\n"
                "• Timur: Papua Nugini, Samudra Pasifik\n\n"
                "PENGARUH LETAK GEOGRAFIS\n\n"
                "1. Iklim Tropis\n"
                "   Indonesia beriklim tropis karena dilalui garis khatulistiwa. "
                "Suhu rata-rata 26-28°C sepanjang tahun.\n\n"
                "2. Dua Musim\n"
                "   Musim hujan (Oktober–April) dan musim kemarau (April–Oktober).\n\n"
                "3. Jalur Perdagangan Internasional\n"
                "   Selat Malaka adalah salah satu jalur pelayaran tersibuk di dunia.\n\n"
                "4. Keanekaragaman Hayati\n"
                "   Iklim tropis mendukung keanekaragaman flora dan fauna yang tinggi.\n\n"
                "LATIHAN\n"
                "1. Mengapa Indonesia beriklim tropis?\n"
                "2. Sebutkan 3 negara yang berbatasan langsung dengan Indonesia!\n"
                "3. Apa keuntungan letak Indonesia di jalur perdagangan internasional?"
            ),
        ),

        # ── SDG / Pendidikan Global ──
        Lesson(
            title="Mengenal 17 Tujuan SDG",
            subject="Pendidikan Global",
            level="Dasar",
            description="Memahami Sustainable Development Goals (SDGs) dan relevansinya bagi kehidupan sehari-hari.",
            content=(
                "SUSTAINABLE DEVELOPMENT GOALS (SDGs)\n\n"
                "SDGs adalah 17 tujuan pembangunan berkelanjutan yang ditetapkan PBB pada 2015 "
                "untuk dicapai pada tahun 2030. Tujuan ini berlaku untuk semua negara di dunia.\n\n"
                "MENGAPA SDGs PENTING?\n"
                "SDGs hadir karena dunia menghadapi tantangan besar:\n"
                "• 700 juta orang masih hidup dalam kemiskinan ekstrem\n"
                "• 800 juta orang kekurangan pangan\n"
                "• Perubahan iklim mengancam kehidupan di bumi\n"
                "• Jutaan anak tidak mendapat akses pendidikan\n\n"
                "5 PILAR SDGs (5P)\n\n"
                "1. People (Manusia)\n"
                "   SDG 1-5: Mengakhiri kemiskinan, kelaparan, dan ketidaksetaraan.\n\n"
                "2. Planet (Bumi)\n"
                "   SDG 6, 12-15: Melindungi lingkungan dan sumber daya alam.\n\n"
                "3. Prosperity (Kemakmuran)\n"
                "   SDG 7-11: Memastikan kehidupan yang sejahtera dan bermartabat.\n\n"
                "4. Peace (Perdamaian)\n"
                "   SDG 16: Masyarakat damai, adil, dan inklusif.\n\n"
                "5. Partnership (Kemitraan)\n"
                "   SDG 17: Kerjasama global untuk mencapai semua tujuan.\n\n"
                "SDG 4 DAN KITA\n"
                "Sebagai pelajar, kamu langsung berkontribusi pada SDG 4 (Pendidikan Berkualitas) "
                "setiap kali kamu belajar, membaca, dan berbagi ilmu dengan orang lain.\n\n"
                "LATIHAN\n"
                "1. Sebutkan 5 pilar SDGs!\n"
                "2. Apa yang bisa kamu lakukan sehari-hari untuk mendukung SDG 4?\n"
                "3. Mengapa SDG 17 (Kemitraan) penting untuk mencapai semua tujuan lainnya?"
            ),
        ),
        Lesson(
            title="Perubahan Iklim dan Dampaknya",
            subject="Pendidikan Global",
            level="Menengah",
            description="Memahami penyebab perubahan iklim, dampaknya, dan tindakan nyata yang bisa dilakukan (SDG 13).",
            content=(
                "PERUBAHAN IKLIM (SDG 13)\n\n"
                "Perubahan iklim adalah perubahan jangka panjang pada suhu dan pola cuaca bumi. "
                "Sejak abad ke-20, aktivitas manusia menjadi penyebab utama.\n\n"
                "PENYEBAB UTAMA\n\n"
                "1. Efek Rumah Kaca\n"
                "   Gas CO₂, metana (CH₄), dan N₂O memerangkap panas matahari di atmosfer.\n\n"
                "2. Pembakaran Bahan Bakar Fosil\n"
                "   Batu bara, minyak bumi, dan gas alam menghasilkan CO₂ dalam jumlah besar.\n\n"
                "3. Deforestasi\n"
                "   Penebangan hutan mengurangi penyerapan CO₂ dan melepaskan karbon tersimpan.\n\n"
                "4. Pertanian Intensif\n"
                "   Peternakan sapi menghasilkan metana; sawah menghasilkan gas rumah kaca.\n\n"
                "DAMPAK PERUBAHAN IKLIM\n"
                "• Kenaikan suhu rata-rata bumi (+1.1°C sejak era pra-industri)\n"
                "• Mencairnya es di kutub → naiknya permukaan laut\n"
                "• Cuaca ekstrem: banjir, kekeringan, badai lebih sering\n"
                "• Kepunahan spesies dan kerusakan ekosistem\n"
                "• Ancaman ketahanan pangan global\n\n"
                "APA YANG BISA KITA LAKUKAN?\n"
                "✓ Hemat listrik dan air\n"
                "✓ Kurangi penggunaan plastik sekali pakai\n"
                "✓ Pilih transportasi umum atau sepeda\n"
                "✓ Tanam pohon di sekitar rumah\n"
                "✓ Kurangi konsumsi daging\n"
                "✓ Edukasi orang lain tentang perubahan iklim\n\n"
                "LATIHAN\n"
                "1. Apa perbedaan cuaca dan iklim?\n"
                "2. Sebutkan 3 dampak perubahan iklim yang sudah terasa di Indonesia!\n"
                "3. Buat rencana aksi pribadi: 5 hal yang akan kamu lakukan untuk mengurangi jejak karbonmu."
            ),
        ),
    ]

    db.session.add_all(lessons)
    db.session.commit()
    print(f"[SEED] {len(lessons)} materi default berhasil ditambahkan.")
