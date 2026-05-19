"""
Seed script untuk HealthTruth-AI knowledge base.
Jalankan:
  python seed_knowledge_base.py                          # lokal (localhost:8000)
  python seed_knowledge_base.py https://xxx.railway.app  # Railway

Topik (35 entri):
  Batch 1 — Herbal & mekanisme (20 entri):
  1.  Temulawak & hepatoprotektif hati
  2.  Sambiloto — anti-inflamasi (mekanisme)
  3.  Sambiloto — imunomodulator & batasan klinis
  4.  Jamu pahitan & diabetes (in-vitro)
  5.  Jamu pahitan — risiko pemalsuan & BKO
  6.  Obat herbal & hepatotoksisitas
  7.  Obat herbal & nefrotoksisitas
  8.  Daun kelor — kandungan gizi & bukti ilmiah
  9.  Daun kelor — intervensi stunting
 10.  Propolis — antibakteri & antiviral
 11.  Propolis Indonesia — penelitian lokal
 12.  Temu ireng — bukti farmakologi
 13.  Temu ireng — antioksidan & imunostimulan
 14.  Klaim herbal anti-kanker — status bukti
 15.  Herbal anti-kanker — risiko penghentian terapi konvensional
 16.  Interaksi herbal–warfarin — risiko perdarahan
 17.  Interaksi herbal–antikoagulan — farmakokinetik
 18.  Swamedikasi jamu — prevalensi & risiko
 19.  Swamedikasi jamu — penundaan pengobatan medis
 20.  Temulawak — studi klinis & profil keamanan

  Batch 2 — Personalisasi profil kesehatan (15 entri):
 21.  Hipertensi & herbal — interaksi antihipertensi
 22.  Kolesterol tinggi, statin & herbal — interaksi CYP3A4
 23.  Asam urat & herbal — bukti ilmiah
 24.  Hamil/menyusui & herbal — kontraindikasi
 25.  Asma & herbal — risiko produk lebah
 26.  Jahe — profil keamanan & interaksi obat
 27.  Kunyit (Curcuma longa) — manfaat, keterbatasan & interaksi
 28.  Kayu manis — diabetes, kolesterol & risiko coumarin
 29.  Insulin & herbal — risiko hipoglikemia
 30.  Amlodipin & herbal — interaksi CYP3A4
 31.  Simvastatin & herbal — risiko miopati & rhabdomyolisis
 32.  Antidepresan & herbal — risiko sindrom serotonin
 33.  Obat tiroid & herbal — gangguan penyerapan
 34.  Aspirin dosis rendah & herbal — risiko perdarahan ganda
 35.  Obesitas & herbal pelangsing — bukti & risiko
"""

import os
import sys
import requests

BASE_URL = "https://rag-chatbot-service-production.up.railway.app"
ADD_API_KEY = os.getenv("ADD_API_KEY", "")

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

    # ─── 21. HIPERTENSI & HERBAL ───────────────────────────────────────────────
    (
        "HIPERTENSI DAN HERBAL — BUKTI DAN RISIKO INTERAKSI: Beberapa tanaman herbal memiliki "
        "efek menurunkan tekanan darah yang telah diteliti secara ilmiah. Bawang putih (Allium sativum) "
        "dalam meta-analisis Cochrane (2012) menunjukkan penurunan sistolik rata-rata 4.6 mmHg pada "
        "pasien hipertensi ringan. Seledri (Apium graveolens) mengandung phthalide yang diduga bekerja "
        "sebagai vasodilator, namun uji klinis pada manusia masih terbatas. "
        "RISIKO INTERAKSI: Pasien yang sudah mengonsumsi obat antihipertensi seperti Amlodipin, "
        "Lisinopril, atau Valsartan berisiko mengalami hipotensi jika menambahkan herbal antihipertensi "
        "secara bersamaan. Gejala: pusing, pingsan, lemas mendadak. IDI dan BPOM menekankan bahwa "
        "herbal TIDAK boleh menggantikan obat antihipertensi resep tanpa supervisi dokter. "
        "Sumber: Cochrane Database 2012, Jurnal Hipertensi Indonesia."
    ),

    # ─── 22. KOLESTEROL TINGGI & STATIN ───────────────────────────────────────
    (
        "KOLESTEROL TINGGI, STATIN, DAN HERBAL — INTERAKSI DAN RISIKO: Simvastatin dan statin "
        "lainnya dimetabolisme terutama melalui enzim CYP3A4 di hati. Red yeast rice (angkak) "
        "mengandung monacolin K yang identik secara kimia dengan lovastatin. Mengonsumsi red yeast rice "
        "bersamaan dengan simvastatin dapat menyebabkan double dosing tidak disengaja, meningkatkan "
        "risiko miopati dan rhabdomyolysis (kerusakan otot serius). Studi di Journal of Clinical "
        "Lipidology (2010) mengonfirmasi risiko ini. Bawang putih dosis tinggi dapat sedikit menurunkan "
        "kolesterol LDL (rata-rata 5-10%), namun tidak cukup kuat untuk menggantikan statin pada pasien "
        "dengan risiko kardiovaskular tinggi. KESIMPULAN: Pasien statin WAJIB menghindari suplemen red "
        "yeast rice. Sumber: Journal of Clinical Lipidology 2010, BPOM RI."
    ),

    # ─── 23. ASAM URAT ────────────────────────────────────────────────────────
    (
        "ASAM URAT (HIPERURISEMIA) DAN HERBAL — BUKTI ILMIAH DAN RISIKO: Asam urat terjadi akibat "
        "penumpukan kristal monosodium urat di sendi. Tempuyung (Sonchus arvensis) secara tradisional "
        "digunakan untuk hiperurisemia; uji praklinis menunjukkan aktivitas xantin oksidase inhibitor "
        "lemah. Daun sirsak sering diklaim menurunkan asam urat, namun penelitian klinis berkualitas "
        "tinggi pada manusia masih sangat terbatas. PERINGATAN: Beberapa jamu pahitan dan ekstrak "
        "herbal dapat meningkatkan kadar asam urat pada individu tertentu. Pasien asam urat yang "
        "mengonsumsi allopurinol atau febuxostat harus berhati-hati karena interaksi herbal dapat "
        "memengaruhi efektivitas obat tersebut. "
        "Sumber: Jurnal Farmakologi Indonesia, Penelitian Etnobotani Universitas Gadjah Mada."
    ),

    # ─── 24. HAMIL/MENYUSUI ───────────────────────────────────────────────────
    (
        "HERBAL DAN KEHAMILAN/MENYUSUI — KONTRAINDIKASI DAN PANDUAN AMAN: Penggunaan herbal selama "
        "kehamilan dan menyusui memerlukan kehati-hatian ekstra karena potensi dampak pada janin atau "
        "bayi. HERBAL YANG DIKONTRAINDIKASIKAN SAAT HAMIL: (1) Sambiloto — studi praklinis menunjukkan "
        "efek abortifasien dan teratogenik pada hewan; pantang dikonsumsi selama kehamilan. "
        "(2) Kayu manis dosis tinggi — dapat merangsang kontraksi uterus. (3) Jamu pahitan dan jamu "
        "pelancar haid — mengandung senyawa yang dapat memicu kontraksi. "
        "HERBAL YANG RELATIF AMAN DALAM DOSIS RENDAH: Jahe dalam dosis rendah (≤1 gram/hari) telah "
        "diteliti untuk mual kehamilan dan dinilai relatif aman oleh beberapa panduan medis. "
        "SELAMA MENYUSUI: Beberapa senyawa herbal dapat masuk ke ASI. IDI merekomendasikan konsultasi "
        "dokter sebelum konsumsi herbal apapun selama hamil dan menyusui. "
        "Sumber: WHO Traditional Medicine Guidelines, IDI, Jurnal Obstetri Indonesia."
    ),

    # ─── 25. ASMA ─────────────────────────────────────────────────────────────
    (
        "ASMA DAN HERBAL — POTENSI MANFAAT DAN RISIKO: Asma adalah penyakit inflamasi kronik saluran "
        "napas. Madu telah diteliti dalam beberapa studi kecil untuk gejala batuk terkait asma, namun "
        "buktinya lemah dan tidak dapat menggantikan bronkodilator atau kortikosteroid inhalasi. "
        "RISIKO: Propolis dan produk lebah lainnya (madu, bee pollen) dapat memicu reaksi alergi berat "
        "(anafilaksis) pada pasien asma yang sensitif terhadap produk lebah — ini adalah kontraindikasi "
        "penting. Asap dari membakar herbal (termasuk kemenyan, dupa) dapat memperparah bronkospasme. "
        "Beberapa minyak esensial herbal (eucalyptus, peppermint) dapat memicu bronkospasme pada "
        "sebagian pasien asma sensitif. KESIMPULAN: Pasien asma harus sangat berhati-hati dengan "
        "produk berbasis lebah dan herbal yang dihirup. Pengobatan asma konvensional tidak boleh "
        "dihentikan. Sumber: Global Initiative for Asthma (GINA), Jurnal Alergi Imunologi Indonesia."
    ),

    # ─── 26. JAHE ─────────────────────────────────────────────────────────────
    (
        "JAHE (Zingiber officinale) — PROFIL KEAMANAN DAN INTERAKSI OBAT: Jahe merupakan rempah "
        "dengan aktivitas anti-inflamasi, antiemetik, dan antioksidan yang didukung bukti ilmiah. "
        "Senyawa aktif utama: gingerol dan shogaol. MANFAAT TERBUKTI: Meta-analisis di British Journal "
        "of Anaesthesia (2014) mengonfirmasi efektivitas jahe untuk mual pascaoperasi dan morning "
        "sickness. INTERAKSI OBAT: (1) Antikoagulan (warfarin, aspirin): jahe memiliki sifat "
        "antiplatelet lemah; penggunaan bersamaan dapat meningkatkan risiko perdarahan. (2) Obat "
        "diabetes (metformin, insulin): jahe dapat menurunkan kadar gula darah; risiko hipoglikemia "
        "jika dikombinasikan. (3) Obat antihipertensi: efek aditif penurunan tekanan darah. "
        "KONTRAINDIKASI: Pasien dengan alergi jahe harus menghindari sepenuhnya. "
        "KEAMANAN IBU HAMIL: Dosis rendah (≤1g/hari) umumnya dianggap aman untuk morning sickness; "
        "dosis tinggi perlu dihindari. Sumber: British Journal of Anaesthesia 2014, BPOM RI."
    ),

    # ─── 27. KUNYIT ───────────────────────────────────────────────────────────
    (
        "KUNYIT (Curcuma longa) — MANFAAT, KETERBATASAN, DAN INTERAKSI: Kunyit berbeda dengan "
        "temulawak (Curcuma xanthorrhiza) meskipun satu genus. Senyawa aktif utama: kurkumin. "
        "MASALAH BIOAVAILABILITAS: Kurkumin murni memiliki bioavailabilitas oral sangat rendah (<1%). "
        "Produk komersial sering dikombinasikan dengan piperin untuk meningkatkan penyerapan hingga "
        "2000%. INTERAKSI OBAT: (1) Obat diabetes: kurkumin dapat menurunkan kadar gula darah; risiko "
        "hipoglikemia jika dikombinasikan dengan metformin atau insulin. (2) Antikoagulan: efek "
        "antiplatelet ringan; tidak direkomendasikan bersamaan dengan warfarin tanpa pemantauan. "
        "(3) Amlodipin dan obat CYP3A4: kurkumin dosis tinggi dapat menghambat enzim ini. "
        "KEAMANAN IBU HAMIL: Kunyit sebagai bumbu masakan aman; suplemen kurkumin dosis tinggi tidak "
        "direkomendasikan saat hamil. Sumber: Journal of Nutritional Biochemistry, BPOM RI."
    ),

    # ─── 28. KAYU MANIS ───────────────────────────────────────────────────────
    (
        "KAYU MANIS (Cinnamomum) — DIABETES, KOLESTEROL, DAN RISIKO TOKSISITAS: Kayu manis cassia "
        "(Cinnamomum cassia) dan ceylon (Cinnamomum verum) adalah dua jenis dengan profil keamanan "
        "berbeda. MANFAAT: Meta-analisis di Diabetes Care (2013) menunjukkan kayu manis cassia dapat "
        "menurunkan gula darah puasa rata-rata 24.59 mg/dL dan LDL kolesterol pada pasien diabetes "
        "tipe 2. RISIKO TOKSISITAS HATI: Kayu manis cassia mengandung coumarin kadar tinggi yang dapat "
        "menyebabkan kerusakan hati pada individu sensitif. European Food Safety Authority (EFSA) "
        "menetapkan batas toleransi harian 0.1 mg coumarin/kg berat badan. Pasien gangguan hati harus "
        "menghindari suplemen kayu manis cassia dosis tinggi. INTERAKSI: Kombinasi dengan obat diabetes "
        "dapat menyebabkan hipoglikemia. Sumber: Diabetes Care 2013, EFSA Scientific Opinion, BPOM RI."
    ),

    # ─── 29. INSULIN ──────────────────────────────────────────────────────────
    (
        "INSULIN DAN HERBAL — RISIKO HIPOGLIKEMIA: Pasien diabetes yang menggunakan insulin berada "
        "pada risiko tinggi hipoglikemia jika mengonsumsi herbal penurun gula darah secara bersamaan. "
        "Herbal yang terbukti atau diduga memiliki efek hipoglikemik: (1) Pare (Momordica charantia) — "
        "mengandung polipeptida-P mirip insulin. (2) Kayu manis — lihat bukti di atas. (3) Kunyit/"
        "kurkumin — efek insulin-sensitizing. (4) Lidah buaya — beberapa studi kecil menunjukkan efek "
        "hipoglikemik. (5) Biji klabet (fenugreek) — merangsang sekresi insulin. "
        "DAMPAK KLINIS: Hipoglikemia berat (gula darah <70 mg/dL) dapat membahayakan jiwa. Gejala: "
        "tremor, keringat dingin, penurunan kesadaran. REKOMENDASI: Pasien pengguna insulin WAJIB "
        "berkonsultasi dengan dokter sebelum mengonsumsi herbal apapun. "
        "Sumber: Diabetes Care, American Diabetes Association Guidelines, Jurnal Endokrinologi Indonesia."
    ),

    # ─── 30. AMLODIPIN ────────────────────────────────────────────────────────
    (
        "AMLODIPIN (CALCIUM CHANNEL BLOCKER) DAN HERBAL — INTERAKSI CYP3A4: Amlodipin adalah obat "
        "antihipertensi yang dimetabolisme secara ekstensif oleh enzim CYP3A4 di hati. "
        "HERBAL YANG MENINGKATKAN KADAR AMLODIPIN (inhibitor CYP3A4): (1) Grapefruit/jeruk bali — "
        "inhibitor CYP3A4 kuat; dapat meningkatkan kadar amlodipin dalam darah hingga 2x lipat, "
        "meningkatkan risiko hipotensi dan edema kaki. (2) Kurkumin dosis tinggi — inhibisi CYP3A4 "
        "sedang. HERBAL YANG MENURUNKAN KADAR AMLODIPIN (inducer CYP3A4): St. John's Wort dapat "
        "menurunkan efektivitas amlodipin. HERBAL DENGAN EFEK ADITIF: Bawang putih, seledri, dan "
        "herbal antihipertensi lain dapat memberikan efek penurunan tekanan darah tambahan — risiko "
        "hipotensi. REKOMENDASI: Pasien pengguna amlodipin harus menghindari jeruk bali dan melaporkan "
        "semua suplemen herbal kepada dokter. Sumber: British Journal of Clinical Pharmacology."
    ),

    # ─── 31. SIMVASTATIN ──────────────────────────────────────────────────────
    (
        "SIMVASTATIN DAN HERBAL — RISIKO MIOPATI DAN RHABDOMYOLISIS: Simvastatin dimetabolisme oleh "
        "CYP3A4. RISIKO TERTINGGI — RED YEAST RICE (Angkak): Mengandung monacolin K yang identik "
        "secara kimia dengan lovastatin. Mengonsumsinya bersamaan simvastatin adalah double statin "
        "dosing — risiko miopati (nyeri otot parah) dan rhabdomyolysis (kerusakan otot masif yang "
        "dapat menyebabkan gagal ginjal akut). INTERAKSI CYP3A4: Herbal yang menghambat CYP3A4 "
        "(termasuk kurkumin dosis tinggi) dapat meningkatkan kadar simvastatin dan risiko toksisitas. "
        "TANDA BAHAYA: Nyeri atau kelemahan otot yang tidak biasa saat mengonsumsi statin harus segera "
        "dilaporkan ke dokter. REKOMENDASI: Pasien statin WAJIB menghindari red yeast rice dan "
        "melaporkan semua suplemen ke dokter atau apoteker. "
        "Sumber: Journal of Clinical Lipidology, FDA Drug Safety Communication."
    ),

    # ─── 32. ANTIDEPRESAN ─────────────────────────────────────────────────────
    (
        "ANTIDEPRESAN DAN HERBAL — RISIKO SINDROM SEROTONIN DAN INTERAKSI SERIUS: Pasien yang "
        "mengonsumsi antidepresan (SSRI seperti fluoxetin, sertralin; SNRI seperti venlafaxine; atau "
        "MAO inhibitor) berisiko mengalami interaksi berbahaya dengan herbal tertentu. "
        "ST. JOHN'S WORT (Hypericum perforatum) — KONTRAINDIKASI MUTLAK dengan SSRI/SNRI: Dapat "
        "menyebabkan sindrom serotonin (kelebihan serotonin) yang mengancam jiwa — gejala: agitasi, "
        "tremor, diare, demam, kejang, penurunan kesadaran. Selain itu menginduksi CYP3A4, menurunkan "
        "efektivitas banyak obat. HERBAL LAIN: (1) Ginseng — dapat mempengaruhi kadar neurotransmiter. "
        "(2) Kava — risiko hepatotoksisitas dan sedasi berlebih. REKOMENDASI: Pasien pengguna "
        "antidepresan WAJIB melaporkan semua suplemen kepada psikiater. Jangan menghentikan antidepresan "
        "dan menggantinya dengan herbal tanpa supervisi medis. Sumber: Clinical Pharmacology, FDA, WHO."
    ),

    # ─── 33. OBAT TIROID ──────────────────────────────────────────────────────
    (
        "OBAT TIROID (LEVOTHYROXINE) DAN HERBAL — GANGGUAN PENYERAPAN: Levothyroxine (T4 sintetis) "
        "memiliki jendela terapeutik sempit — perubahan kecil dalam penyerapan dapat memengaruhi "
        "kontrol tiroid secara signifikan. HERBAL YANG MENGGANGGU PENYERAPAN: (1) Produk kedelai "
        "(susu kedelai, isoflavon): mengurangi penyerapan levothyroxine secara signifikan; harus "
        "dikonsumsi dengan jeda minimal 4 jam. (2) Spirulina dan suplemen alga (chlorella, kelp): "
        "mengandung iodine yang dapat memengaruhi fungsi tiroid. HERBAL YANG MEMPENGARUHI FUNGSI "
        "TIROID LANGSUNG: Kelp dan produk iodine tinggi dapat menyebabkan hipertiroidisme atau "
        "hipotiroidisme pada individu rentan. REKOMENDASI: Levothyroxine diminum 30-60 menit sebelum "
        "makan, jauh dari suplemen apapun. Pemeriksaan TSH rutin diperlukan. "
        "Sumber: Thyroid Journal, American Thyroid Association Guidelines."
    ),

    # ─── 34. ASPIRIN DOSIS RENDAH ─────────────────────────────────────────────
    (
        "ASPIRIN DOSIS RENDAH DAN HERBAL — RISIKO PERDARAHAN GANDA: Aspirin dosis rendah (80-160 "
        "mg/hari) digunakan sebagai antiplatelet untuk mencegah serangan jantung dan stroke. "
        "HERBAL DENGAN EFEK ANTIPLATELET YANG MEMPERKUAT ASPIRIN: (1) Bawang putih dosis tinggi — "
        "mengandung ajoene dan allicin yang menghambat agregasi trombosit. (2) Jahe dosis tinggi — "
        "efek antiplatelet ringan via inhibisi COX. (3) Ginkgo biloba — inhibisi faktor pengaktivasi "
        "trombosit (PAF). (4) Kunyit/kurkumin dosis tinggi — efek antiplatelet. Kombinasi aspirin "
        "dengan herbal antiplatelet meningkatkan risiko perdarahan, terutama perdarahan lambung dan "
        "perdarahan otak. PERHATIAN KHUSUS: Pasien yang akan menjalani operasi harus menghentikan "
        "semua suplemen herbal antiplatelet minimal 7-10 hari sebelumnya. "
        "Sumber: Thrombosis Journal, European Heart Journal."
    ),

    # ─── 35. OBESITAS ─────────────────────────────────────────────────────────
    (
        "OBESITAS DAN HERBAL PELANGSING — BUKTI DAN RISIKO: Obesitas (IMT >30 kg/m²) memerlukan "
        "pendekatan komprehensif. Banyak produk herbal diklaim sebagai pelangsing tanpa bukti klinis "
        "kuat. HERBAL YANG DITELITI: (1) Garcinia cambogia (HCA) — meta-analisis menunjukkan penurunan "
        "berat badan kecil (1-2 kg) dibanding plasebo; laporan kasus hepatotoksisitas telah dikaitkan. "
        "(2) Green tea extract (EGCG) — penurunan berat badan rata-rata 0.2-3.5 kg; bukti lemah. "
        "RISIKO SERIUS: Banyak jamu pelangsing tidak standar mengandung bahan kimia obat (BKO) "
        "berbahaya seperti sibutramin atau fenfluramin yang sudah ditarik dari pasar. BPOM RI secara "
        "rutin merilis daftar produk jamu pelangsing mengandung BKO yang dilarang. Pasien obesitas "
        "WAJIB menghindari produk tidak berlabel BPOM. Pendekatan medis (diet terstruktur, olahraga) "
        "jauh lebih aman dan terbukti. Sumber: Cochrane Database, BPOM RI Warning Letters."
    ),
]


def seed(base_url: str = BASE_URL, api_key: str = ADD_API_KEY):
    print(f"Mengirim {len(KNOWLEDGE_ENTRIES)} entri ke {base_url}/add ...\n")
    headers = {"X-Api-Key": api_key} if api_key else {}
    success, failed = 0, 0
    for i, text in enumerate(KNOWLEDGE_ENTRIES, 1):
        try:
            resp = requests.post(f"{base_url}/add", json={"text": text}, headers=headers, timeout=30)
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
