"""
Seed script untuk menambahkan entri knowledge base baru ke RAG HerbalCheck.
Jalankan: python seed_knowledge_base.py
Pastikan server berjalan di http://localhost:8000 atau sesuaikan BASE_URL.

Topik yang dicakup (BARU — tidak menduplikasi entri yang sudah ada):
  1.  Temulawak & hepatoprotektif hati
  2.  Sambiloto / Andrographis — anti-inflamasi (mekanisme)
  3.  Sambiloto — imunomodulator & batasan klinis
  4.  Jamu pahitan & diabetes (in-vitro)
  5.  Jamu pahitan — risiko pemalsuan & bahan kimia obat (BKO)
  6.  Obat herbal & hepatotoksisitas (risiko organ)
  7.  Obat herbal & nefrotoksisitas (kerusakan ginjal)
  8.  Daun kelor — kandungan gizi & bukti ilmiah
  9.  Daun kelor — intervensi stunting di Indonesia
 10.  Propolis — antibakteri & antiviral
 11.  Propolis Indonesia — penelitian spesifik lokal
 12.  Temu ireng (Curcuma aeruginosa) — bukti farmakologi
 13.  Temu ireng — aktivitas antioksidan & imunostimulan
 14.  Klaim herbal anti-kanker Indonesia — status bukti
 15.  Herbal anti-kanker — risiko penghentian terapi konvensional
 16.  Interaksi herbal–warfarin — risiko perdarahan
 17.  Interaksi herbal–antikoagulan — mekanisme farmakokinetik
 18.  Swamedikasi jamu — prevalensi & risiko di Indonesia
 19.  Swamedikasi jamu — penundaan pengobatan medis
 20.  Temulawak — studi klinis pada manusia & profil keamanan
"""

import sys
import requests

BASE_URL = "http://localhost:8000"

KNOWLEDGE_ENTRIES = [
    # ─── 1. TEMULAWAK & HEPATOPROTEKTIF ────────────────────────────────────────
    (
        "TEMULAWAK (Curcuma xanthorrhiza) DAN HEPATOPROTEKTIF HATI — BUKTI ILMIAH: "
        "Temulawak mengandung dua senyawa aktif utama yaitu xanthorrhizol dan kurkuminoid "
        "(kurkumin, demethoxycurkumin, bisdemethoxycurkumin). Penelitian yang dipublikasikan "
        "di PubMed (PMID 8571920) oleh tim Taipei Medical University menunjukkan bahwa ekstrak "
        "C. xanthorrhiza secara signifikan menurunkan kadar serum transaminase (SGOT/SGPT) yang "
        "meningkat akibat hepatotoksin seperti karbon tetraklorida dan galaktosamin pada hewan uji. "
        "Studi lain (PMID 25133223) di jurnal BMC Complementary and Alternative Medicine mengonfirmasi "
        "aktivitas antioksidan dan hepatoprotektif ekstrak terstandar rimpang temulawak. "
        "KESIMPULAN: Bukti praklinis (hewan) mendukung manfaat hepatoprotektif temulawak; "
        "studi klinis pada manusia masih terbatas sehingga temulawak belum dapat menggantikan "
        "terapi medis standar untuk penyakit hati."
    ),

    # ─── 2. SAMBILOTO — MEKANISME ANTI-INFLAMASI NF-κB ────────────────────────
    (
        "SAMBILOTO (Andrographis paniculata) DAN ANTI-INFLAMASI — MEKANISME MOLEKULER: "
        "Andrographolide, senyawa diterpenoid utama dalam daun sambiloto, terbukti secara ilmiah "
        "menghambat jalur inflamasi NF-κB (Nuclear Factor kappa-light-chain-enhancer of activated B cells). "
        "Penelitian di jurnal Frontiers in Pharmacology (2022, doi:10.3389/fphar.2022.920435) menyatakan "
        "bahwa andrographolide membentuk ikatan kovalen dengan residu sistein-38 subunit p50 NF-κB, "
        "sehingga menghambat pengikatan NF-κB ke DNA promotor gen pro-inflamasi. "
        "Studi pada LPS-stimulated RAW264.7 cells (PMC5476883) menunjukkan penekanan signifikan "
        "terhadap sekresi sitokin inflamasi IL-1β, IL-6, dan TNF-α. "
        "KESIMPULAN: Bukti in vitro dan in vivo mendukung aktivitas anti-inflamasi sambiloto; "
        "namun uji klinis fase III pada manusia masih diperlukan untuk menetapkan dosis terapeutik "
        "yang aman dan efektif."
    ),

    # ─── 3. SAMBILOTO — IMUNOMODULATOR & KETERBATASAN KLINIS ──────────────────
    (
        "SAMBILOTO (Andrographis paniculata) SEBAGAI IMUNOMODULATOR — STATUS BUKTI KLINIS: "
        "Tinjauan literatur yang dipublikasikan di Jurnal Kesmas dan Gizi (MEDISTRA, 2022) menyimpulkan "
        "bahwa daun sambiloto memiliki potensi sebagai imunomodulator herbal dengan efek anti-inflamasi "
        "dan peningkatan imunitas. Di Tiongkok, andrographolide telah disetujui sebagai obat untuk "
        "faringitis dan infeksi saluran pernapasan atas. "
        "Akan tetapi, penelitian di Universitas Airlangga dan jurnal Keluwih (2023) menekankan bahwa "
        "uji klinis pada kolitis ulseratif menunjukkan potensi sebanding dengan mesalazin, namun "
        "jumlah sampel masih kecil dan metodologi perlu diperkuat. "
        "KESIMPULAN: Sambiloto memiliki dasar ilmiah yang menjanjikan sebagai anti-inflamasi dan "
        "imunomodulator, tetapi penggunaan mandiri tanpa supervisi tenaga medis berisiko karena "
        "dosis terapeutik optimal pada manusia belum ditetapkan secara konsisten."
    ),

    # ─── 4. JAMU PAHITAN & DIABETES — BUKTI IN-VITRO ──────────────────────────
    (
        "JAMU PAHITAN DAN DIABETES MELLITUS — BUKTI ILMIAH IN-VITRO: "
        "Jamu pahitan adalah ramuan tradisional Jawa yang umumnya mengandung Andrographis paniculata "
        "dan Tinospora cordifolia, digunakan turun-temurun untuk pengelolaan gula darah. "
        "Sebuah studi yang dipublikasikan di jurnal Heliyon (PubMed PMID 36873515, 2023) oleh peneliti "
        "Indonesia menguji formulasi jamu pahitan terstandar secara in vitro dan menemukan bahwa "
        "sediaan tersebut meningkatkan ambilan glukosa di sel otot dan stimulasi sekresi insulin di "
        "sel beta pankreas. "
        "KESIMPULAN: Bukti in-vitro mendukung plausibilitas antidiabetik jamu pahitan, namun "
        "penelitian ini BUKAN uji klinis pada manusia. Penderita diabetes tidak boleh mengganti "
        "obat antidiabetik resep dokter dengan jamu tanpa konsultasi medis karena risiko hipoglikemia "
        "dan komplikasi tidak terkontrol."
    ),

    # ─── 5. JAMU — RISIKO PEMALSUAN & BAHAN KIMIA OBAT (BKO) ─────────────────
    (
        "JAMU DAN RISIKO PEMALSUAN BAHAN KIMIA OBAT (BKO) — TEMUAN INVESTIGASI: "
        "Masalah serius dalam konsumsi jamu di Indonesia adalah adultasi (pemalsuan) dengan "
        "Bahan Kimia Obat (BKO). Penelitian yang dipublikasikan di Natural Sciences Engineering "
        "and Technology Journal menemukan kandungan deksametason dan parasetamol yang tidak "
        "dicantumkan dalam label pada produk jamu yang dipasarkan di Kudus, Jawa Tengah. "
        "Analisis regulatori menunjukkan bahwa 9 dari 10 sampel jamu beredar memiliki nomor "
        "registrasi BPOM yang tidak dapat diverifikasi di database resmi BPOM. "
        "Deksametason yang dikonsumsi jangka panjang tanpa pengawasan medis dapat menyebabkan "
        "Sindrom Cushing, osteoporosis, dan imunosupresi berbahaya. "
        "KESIMPULAN: Konsumen wajib membeli jamu dengan nomor registrasi BPOM yang valid dan "
        "dapat diverifikasi di aplikasi Cek BPOM; produk yang menjanjikan efek instan patut dicurigai "
        "mengandung BKO."
    ),

    # ─── 6. HERBAL & HEPATOTOKSISITAS ─────────────────────────────────────────
    (
        "OBAT HERBAL DAN RISIKO HEPATOTOKSISITAS (KERUSAKAN HATI) — BUKTI ILMIAH: "
        "Drug-Induced Liver Injury (DILI) akibat konsumsi herbal merupakan masalah kesehatan global "
        "yang semakin meningkat. Sebuah tinjauan sistematis di jurnal PMC/NIH (PMC4561772) melaporkan "
        "bahwa obat herbal menyumbang sekitar 25% dari seluruh kasus DILI di negara-negara Asia. "
        "Jurnal Medicine (LWW, 2022) mengidentifikasi lebih dari 65 jenis tanaman herbal yang "
        "terdokumentasi sebagai penyebab penyakit hati, termasuk tanaman mengandung alkaloid "
        "pyrrolizidine seperti Comfrey, serta campuran jamu tradisional Tiongkok. "
        "Mekanisme hepatotoksisitas herbal meliputi stres oksidatif, gangguan fungsi mitokondria, "
        "dan aktivasi respons imun terhadap metabolit reaktif. "
        "KESIMPULAN: Herbal 'alami' tidak otomatis aman bagi hati; konsumsi berlebihan atau "
        "jangka panjang tanpa pengawasan dapat merusak organ hati secara serius."
    ),

    # ─── 7. HERBAL & NEFROTOKSISITAS (KERUSAKAN GINJAL) ──────────────────────
    (
        "OBAT HERBAL DAN RISIKO NEFROTOKSISITAS (KERUSAKAN GINJAL) — BUKTI ILMIAH: "
        "Tinjauan yang dipublikasikan di Iranian Journal of Kidney Diseases (PMC5297591) berjudul "
        "'Herbal medicines and kidney; friends or foes?' menelaah bukti tentang dampak herbal "
        "terhadap fungsi ginjal. Studi ini menemukan bahwa sejumlah herbal dapat menyebabkan "
        "nefrotoksisitas akut maupun kronis, termasuk produk mengandung aristolochic acid "
        "(Aristolochia spp.) yang diketahui menyebabkan Aristolochic Acid Nephropathy (AAN) "
        "dan meningkatkan risiko karsinoma ureter. "
        "LiverTox NCBI Bookshelf (NBK548589) juga mendokumentasikan bahwa beberapa herbal Asia "
        "dapat menyebabkan kerusakan simultan pada hati DAN ginjal secara bersamaan. "
        "KESIMPULAN: Pasien dengan gangguan fungsi ginjal atau riwayat penyakit ginjal harus "
        "sangat berhati-hati mengonsumsi herbal tanpa rekomendasi dokter atau apoteker."
    ),

    # ─── 8. DAUN KELOR — KANDUNGAN GIZI & BUKTI ILMIAH ───────────────────────
    (
        "DAUN KELOR (Moringa oleifera) DAN KANDUNGAN GIZI — FAKTA ILMIAH: "
        "Moringa oleifera, dikenal sebagai daun kelor di Indonesia, telah diteliti secara ekstensif. "
        "Kajian komprehensif di jurnal Nutrients (MDPI, PMC12194112, 2025) mengidentifikasi daun kelor "
        "mengandung protein esensial, vitamin A, B-kompleks, C dan E, serta mineral kalsium, kalium, "
        "zat besi, dan magnesium dalam kadar yang signifikan. "
        "Lebih dari 200 studi peer-reviewed mendokumentasikan efek antioksidan, anti-inflamasi, "
        "antimikroba, antidiabetik, dan hepatoprotektif dari berbagai bagian tanaman kelor. "
        "Tinjauan di jurnal Life (MDPI, 2025, doi:10.3390/life15060881) mengonfirmasi kandungan "
        "fitokimia aktif termasuk flavonoid, asam fenolik, glukosinolat, dan isotiocianat. "
        "KESIMPULAN: Klaim kandungan gizi daun kelor didukung oleh bukti ilmiah yang kuat; "
        "kelor legitimate sebagai suplemen gizi, namun klaim penyembuhan penyakit spesifik "
        "memerlukan uji klinis lebih lanjut."
    ),

    # ─── 9. DAUN KELOR — INTERVENSI STUNTING INDONESIA ───────────────────────
    (
        "DAUN KELOR (Moringa oleifera) DAN PENCEGAHAN STUNTING DI INDONESIA — BUKTI KLINIS: "
        "Stunting merupakan masalah gizi kronis di Indonesia yang mendapat perhatian nasional. "
        "Sejumlah penelitian intervensi di Indonesia telah menguji suplementasi daun kelor pada "
        "balita. Studi quasi-eksperimental yang dipublikasikan di jurnal Media Gizi Indonesia "
        "(Universitas Airlangga) menemukan peningkatan berat badan rata-rata 2,01 kg dan tinggi "
        "badan 1,3 cm pada balita kurang gizi setelah suplementasi daun kelor selama periode tertentu. "
        "Tinjauan sistematis di Indonesian Journal of Global Health Research (2024) yang menelaah "
        "6 artikel (2014–2024) dari PubMed, ScienceDirect, dan Google Scholar menyimpulkan bahwa "
        "suplementasi Moringa berpotensi mendukung pertumbuhan anak, dengan kandungan vitamin C "
        "dan flavonoid lebih tinggi pada kelor dataran tinggi. "
        "KESIMPULAN: Daun kelor memiliki potensi sebagai intervensi gizi berbasis pangan lokal "
        "untuk pencegahan stunting, namun harus menjadi komplemen — bukan pengganti — program "
        "gizi terintegrasi dari Kemenkes RI."
    ),

    # ─── 10. PROPOLIS — ANTIBAKTERI & ANTIVIRAL ───────────────────────────────
    (
        "PROPOLIS — AKTIVITAS ANTIBAKTERI DAN ANTIVIRAL: BUKTI ILMIAH: "
        "Propolis adalah produk lebah yang kaya flavonoid, asam fenolik, dan turunannya. "
        "Tinjauan di jurnal Molecules (PMC8231288, 2021) berjudul 'Antiviral, Antibacterial, "
        "Antifungal, and Antiparasitic Properties of Propolis' menyatakan bahwa aktivitas "
        "antibakteri propolis telah terdokumentasi pada sekitar 600 strain bakteri. "
        "Sifat antiviral propolis mencakup penghambatan infektivitas dan replikasi virus, "
        "serta modulasi produksi sitokin dan aktivasi sel imun, sebagaimana diulas dalam "
        "Medicinal Research Reviews (Wiley, 2022, doi:10.1002/med.21866). "
        "KESIMPULAN: Bukti ilmiah mendukung aktivitas antibakteri dan antiviral propolis "
        "secara in vitro; propolis dapat digunakan sebagai suplemen penunjang imunitas, "
        "namun tidak dapat menggantikan antibiotik resep untuk infeksi bakteri yang serius."
    ),

    # ─── 11. PROPOLIS INDONESIA — PENELITIAN LOKAL ────────────────────────────
    (
        "PROPOLIS INDONESIA — PENELITIAN SPESIFIK DARI TANAMAN LOKAL: "
        "Indonesia memiliki keanekaragaman sumber propolis yang unik karena keanekaragaman flora "
        "tropisnya. Penelitian yang dipublikasikan di PMC (PMC9073061) menguji propolis kapsul "
        "Indonesia dari Tetragonula sapiens yang mengandung terpenoid berasal dari Mangifera indica "
        "(mangga) sebagai sumber botani. Studi ini menunjukkan aktivitas antioksidan in-vitro dan "
        "anti-inflamasi in-vivo yang signifikan, serta profil toksisitas akut yang aman. "
        "Studi di ScienceDirect (2021) mengidentifikasi senyawa baru dari propolis Lombok, Indonesia "
        "dengan aktivitas antibakteri terhadap bakteri uji. "
        "Formulasi self-emulsifying propolis Indonesia yang dikembangkan (PMC7961237) menunjukkan "
        "aktivitas antibakteri terhadap E. coli dan S. aureus. "
        "KESIMPULAN: Propolis asal Indonesia menunjukkan aktivitas biologis yang menjanjikan, "
        "namun standardisasi produk dan uji klinis fase II/III pada manusia masih sangat diperlukan."
    ),

    # ─── 12. TEMU IRENG — FARMAKOLOGI DASAR ───────────────────────────────────
    (
        "TEMU IRENG (Curcuma aeruginosa Roxb.) — BUKTI FARMAKOLOGI DASAR: "
        "Temu ireng atau temu hitam (Curcuma aeruginosa) merupakan tanaman herbal Indonesia yang "
        "secara tradisional digunakan untuk pengobatan dispepsia, kembung, infeksi, dan sebagai "
        "anthelmintik (pembasmi cacing). "
        "Penelitian di Farmasains: Jurnal Farmasi dan Ilmu Kesehatan (Universitas Muhammadiyah Malang, "
        "2025) mengevaluasi aktivitas mukolitik ekstrak etanol temu ireng dan menemukan penurunan "
        "viskositas mukus yang signifikan pada konsentrasi 1,0%, 1,5%, dan 2,0%. "
        "Tinjauan di PMC (PMC8120430) tentang efek imunomodulatori spesies Curcuma mengidentifikasi "
        "bahwa monoterpen dan seskuiterpen dalam rimpang temu ireng memiliki aktivitas imunostimulasi. "
        "KESIMPULAN: Temu ireng memiliki basis ilmiah untuk aktivitas mukolitik dan imunomodulatori, "
        "namun penelitian klinis pada manusia masih sangat terbatas dibandingkan temulawak atau kunyit."
    ),

    # ─── 13. TEMU IRENG — ANTIOKSIDAN & IMUNOSTIMULAN ────────────────────────
    (
        "TEMU IRENG (Curcuma aeruginosa) — AKTIVITAS ANTIOKSIDAN DAN IMUNOSTIMULAN: "
        "Studi fitokimia yang diterbitkan oleh peneliti Institut Pertanian Bogor (IPB) memetakan "
        "variabilitas kandungan kurkumin, demethoxycurkumin, dan bisdemethoxycurkumin pada 10 "
        "kultivar temu ireng yang ditanam di Jawa Barat. Temu ireng mengandung flavonoid, steroid, "
        "saponin, terpenoid, dan alkaloid sebagai senyawa bioaktif utama. "
        "Penelitian yang dipublikasikan di AIP Conference Proceedings (2019) oleh peneliti Indonesia "
        "menemukan bahwa ekstrak rimpang temu ireng dapat mengurangi efek imunosupresi akibat "
        "doxorubicin pada hewan percobaan, menunjukkan potensi imunostimulan. "
        "Aktivitas antioksidan menggunakan metode DPPH juga telah dikonfirmasi dalam penelitian "
        "lokal yang diterbitkan di ResearchGate. "
        "KESIMPULAN: Temu ireng memiliki potensi farmakologi sebagai antioksidan dan imunostimulan, "
        "tetapi seluruh bukti yang tersedia masih bersifat praklinis (in-vitro dan hewan)."
    ),

    # ─── 14. KLAIM HERBAL ANTI-KANKER INDONESIA — STATUS BUKTI ───────────────
    (
        "KLAIM HERBAL ANTI-KANKER DI INDONESIA — STATUS BUKTI ILMIAH: "
        "Penggunaan obat herbal sebagai terapi kanker di Indonesia sangat umum, namun bukti klinis "
        "masih sangat terbatas. Tinjauan sistematis yang dipublikasikan di Cancer Management and "
        "Research (Dove Press/PMC10441583, 2023) menelaah 23 artikel uji in-vitro (2018–2023) dan "
        "menemukan bahwa tiga tanaman Indonesia yang paling banyak diteliti secara in-vitro sebagai "
        "antikanker adalah Sirsak (Annona muricata), Rasamala (Altingia excelsa), dan Benalu Cengkeh "
        "(Dendrophthoe pentandra). Mekanisme antikanker yang paling banyak dilaporkan adalah "
        "penghambatan proliferasi sel melalui jalur intrinsik apoptosis. "
        "KESIMPULAN: Seluruh bukti antikanker herbal Indonesia saat ini masih berada di level "
        "in-vitro (sel) dan sangat memerlukan uji in-vivo (hewan) dan uji klinis terkontrol "
        "sebelum dapat diklaim efektif untuk pasien kanker manusia."
    ),

    # ─── 15. HERBAL KANKER — RISIKO PENGHENTIAN TERAPI KONVENSIONAL ──────────
    (
        "HERBAL UNTUK KANKER — RISIKO PENGHENTIAN TERAPI KONVENSIONAL: "
        "Studi kohort prospektif yang dipublikasikan di ScienceDirect (2025) oleh peneliti Indonesia "
        "menginvestigasi penggunaan obat herbal pada pasien kanker dan menemukan bahwa meskipun "
        "herbal berkontribusi pada peningkatan kesejahteraan umum pasien, tidak ada bukti bahwa "
        "herbal dapat menyembuhkan kanker secara klinis. "
        "Tinjauan di Cancer Management and Research menekankan bahwa 'validasi sistematis melalui "
        "studi in-vivo terkontrol dan uji klinis sangat penting untuk membedakan kandidat yang "
        "menjanjikan dari yang menimbulkan risiko tidak dapat diterima.' "
        "IDI (Ikatan Dokter Indonesia) menegaskan bahwa penghentian kemoterapi, radioterapi, "
        "atau imunoterapi demi beralih ke herbal tanpa konfirmasi dokter dapat memperburuk prognosis "
        "secara signifikan. "
        "KESIMPULAN: Herbal BOLEH digunakan sebagai komplementer (pendamping) terapi kanker "
        "konvensional setelah dikonsultasikan dengan dokter onkologi, tetapi TIDAK BOLEH "
        "menggantikan terapi berbasis bukti yang sudah terbukti efektif."
    ),

    # ─── 16. INTERAKSI HERBAL–WARFARIN ────────────────────────────────────────
    (
        "INTERAKSI OBAT HERBAL DENGAN WARFARIN (ANTIKOAGULAN) — RISIKO PERDARAHAN: "
        "Warfarin adalah antikoagulan (pengencer darah) yang paling banyak digunakan dan memiliki "
        "indeks terapeutik sempit — perubahan kecil pada kadarnya dapat menyebabkan perdarahan "
        "berbahaya atau pembekuan darah. Tinjauan sistematis di British Journal of Clinical "
        "Pharmacology (Wiley, 2021, doi:10.1111/bcp.14404) menganalisis interaksi warfarin dengan "
        "herbal dan makanan, menyimpulkan bahwa 84% herbal yang diteliti berpotensi MENINGKATKAN "
        "efek antikoagulan warfarin sehingga meningkatkan risiko perdarahan. "
        "Herbal berisiko tinggi termasuk bawang putih, jahe, ginkgo, ginseng, dan danshen. "
        "Ulasan di PubMed (PMID 27470545, Biomedicine & Pharmacotherapy) mengidentifikasi bahwa "
        "kumarin, kuinon, xanton, terpen, dan lignan dalam herbal signifikan memengaruhi metabolisme "
        "warfarin. "
        "KESIMPULAN: Pasien yang mengonsumsi warfarin atau antikoagulan lain WAJIB melaporkan "
        "semua konsumsi herbal kepada dokter atau apoteker untuk pemantauan INR yang ketat."
    ),

    # ─── 17. INTERAKSI HERBAL–ANTIKOAGULAN — MEKANISME ───────────────────────
    (
        "MEKANISME INTERAKSI FARMAKOKINETIK HERBAL DENGAN ANTIKOAGULAN: "
        "Interaksi herbal–warfarin terjadi melalui dua mekanisme utama: farmakokinetik (mempengaruhi "
        "metabolisme warfarin) dan farmakodinamik (efek aditif pada pembekuan darah). "
        "Penelitian di PMC (PMC3976951) berjudul 'Updates on the Clinical Evidenced Herb-Warfarin "
        "Interactions' mendokumentasikan bahwa pomegranate (delima), ginkgo, horse chestnut, dan "
        "danshen menghambat enzim CYP2C9 yang bertanggung jawab memetabolisme warfarin, sehingga "
        "kadar warfarin dalam darah meningkat dan memperpanjang waktu perdarahan. "
        "Studi pada model kelinci (PMC6270155) menunjukkan bahwa formula herbal Tiongkok "
        "Shu-Jing-Hwo-Shiee-Tang mempotensasi aktivitas antikoagulan warfarin secara signifikan. "
        "KESIMPULAN: Mekanisme interaksi herbal–antikoagulan bersifat nyata dan berbasis bukti; "
        "anggapan bahwa herbal 'alami' aman diminum bersama obat dokter adalah MITOS yang berbahaya "
        "bagi pasien dengan kondisi jantung atau stroke."
    ),

    # ─── 18. SWAMEDIKASI JAMU — PREVALENSI & RISIKO ───────────────────────────
    (
        "SWAMEDIKASI JAMU DI INDONESIA — PREVALENSI DAN RISIKO KESEHATAN: "
        "Swamedikasi (pengobatan mandiri) menggunakan jamu merupakan praktik yang sangat umum di "
        "Indonesia. Analisis data Riset Kesehatan Dasar (Riskesdas) 2010 yang melibatkan 177.927 "
        "responden dari 33 provinsi menemukan proporsi signifikan penduduk Indonesia menggunakan "
        "jamu buatan sendiri sebagai pengobatan utama tanpa konsultasi medis. "
        "Penelitian cross-sectional di Yogyakarta (2024) yang diterbitkan di ResearchGate "
        "mengevaluasi praktik swamedikasi dan literasi masyarakat, menemukan bahwa kurangnya "
        "literasi mengenai dosis, kontraindikasi, dan interaksi obat menjadi faktor risiko utama. "
        "Studi di PMC (PMC5362041) pada populasi endemis malaria di Indonesia menemukan bahwa "
        "penggunaan jamu tradisional berdampingan dengan obat antimalaria dapat mengurangi kepatuhan "
        "terhadap protokol pengobatan standar. "
        "KESIMPULAN: Swamedikasi jamu berisiko menyebabkan penggunaan yang tidak tepat, "
        "resistensi obat, dan keterlambatan diagnosis penyakit serius."
    ),

    # ─── 19. SWAMEDIKASI JAMU — PENUNDAAN PENGOBATAN MEDIS ───────────────────
    (
        "SWAMEDIKASI JAMU DAN PENUNDAAN PENGOBATAN MEDIS — IMPLIKASI KESEHATAN: "
        "Salah satu risiko terbesar swamedikasi jamu adalah penundaan diagnosis dan pengobatan "
        "medis yang tepat, terutama untuk penyakit serius seperti kanker, tuberkulosis, dan diabetes. "
        "Tinjauan risiko jamu di jurnal Critical Reviews in Toxicology (Taylor & Francis, 2021) "
        "berjudul 'Risk characterisation of constituents present in jamu to promote its safe use' "
        "mengidentifikasi berbagai senyawa dalam jamu yang memerlukan karakterisasi risiko lebih "
        "lanjut untuk memastikan keamanan penggunaan. "
        "Kemenkes RI melalui pedoman pelayanan kesehatan tradisional menegaskan bahwa jamu "
        "yang telah terdaftar di BPOM dapat digunakan sebagai komplemen — bukan pengganti — "
        "layanan kesehatan primer, terutama untuk kondisi yang membutuhkan diagnosis medis. "
        "KESIMPULAN: Masyarakat yang menggunakan jamu untuk gejala yang berlangsung lebih dari "
        "2 minggu atau gejala berat (darah dalam urin/feses, nyeri dada, sesak napas) wajib "
        "segera berkonsultasi dengan tenaga medis tanpa menunggu hasil 'pengobatan herbal'."
    ),

    # ─── 20. TEMULAWAK — PROFIL KEAMANAN & TOKSISITAS ────────────────────────
    (
        "TEMULAWAK (Curcuma xanthorrhiza) — PROFIL KEAMANAN DAN TOKSISITAS: "
        "Di samping manfaatnya, profil keamanan temulawak juga telah dievaluasi secara ilmiah. "
        "Studi toksisitas akut yang dipublikasikan di ResearchGate mengevaluasi suplemen "
        "hepatoprotektif berbasis temulawak dan secara umum menyimpulkan bahwa temulawak memiliki "
        "profil keamanan yang baik pada dosis terapi. "
        "Kajian komprehensif di PMC (PMC8214482) berjudul 'Javanese Turmeric (Curcuma xanthorrhiza): "
        "Ethnobotany, Phytochemistry, Biotechnology, and Pharmacological Activities' menyatakan bahwa "
        "konsumsi oral pada tikus dan mencit menunjukkan efek hepatoprotektif tanpa toksisitas "
        "signifikan pada dosis terapi, namun dosis tinggi dan jangka panjang belum dievaluasi "
        "secara klinis pada manusia. "
        "BPOM RI mengklasifikasikan produk berbasis temulawak terstandar dalam kategori Obat "
        "Herbal Terstandar (OHT) bila memenuhi persyaratan uji praklinik. "
        "KESIMPULAN: Temulawak aman dikonsumsi pada dosis wajar sesuai aturan pakai; namun "
        "penggunaan berlebihan (megadosis) dan jangka sangat panjang tetap memerlukan pemantauan "
        "fungsi hati, terutama bagi pasien dengan penyakit hati yang sudah ada sebelumnya."
    ),
]


def seed(base_url: str = BASE_URL):
    print(f"Mengirim {len(KNOWLEDGE_ENTRIES)} entri ke {base_url}/add ...\n")
    success, failed = 0, 0
    for i, text in enumerate(KNOWLEDGE_ENTRIES, 1):
        try:
            resp = requests.post(f"{base_url}/add", json={"text": text}, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            print(f"[{i:02d}] OK  — doc_id={data.get('id')}  ({len(text)} chars)")
            success += 1
        except Exception as exc:
            print(f"[{i:02d}] GAGAL — {exc}")
            failed += 1
    print(f"\nSelesai: {success} berhasil, {failed} gagal dari {len(KNOWLEDGE_ENTRIES)} entri.")
    return failed == 0


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    ok = seed(url)
    sys.exit(0 if ok else 1)
