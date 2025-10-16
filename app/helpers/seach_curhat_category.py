import re
import random


def find_highest_category(text):
    """
    Finds the category with the highest word count in the text.
    If no words match, a random category is returned.
    """
    """
       Semester Awal
       Keywords: Lingkungan, awal, baru, adaptasi, ekspektasi, ospek, orientasi, perkenalan, eksplorasi, penyesuaian, antusias, tantangan, harapan, mandiri, perantauan.

       Semester Tengah
       Keywords: Tugas, jenuh, saat ini, ujian, tenggat waktu, proyek, kelompok, presentasi, SKS, organisasi, stagnan, rutin, tekanan, kejar-kejaran, kompromi, ambisi, ambivalen.

       Semester Akhir
       Keywords: Bimbingan, tugas akhir, sulit tidur, skripsi, sidang, revisi, yudisium, lulus, bangga, perjuangan, stres, bimbingan, presentasi, revisi, pusing, lega.

       Sosial
       Keywords: Keluarga, teman, hubungan, persahabatan, konflik, komunikasi, interaksi, rekreasi, networking, romantis, pacar, mandiri, toxic, dinamika, kepercayaan, dukungan, kesepian, komunitas, pertemanan.
    """
    # Rule topic
    categories = [
        {"semester_awal": {"lingkungan", "awal", "baru"}},
        {"semester_tengah": {"tugas", "jenuh", "saat ini"}},
        {"semester_akhir": {"bimbingan", "tugas akhir", "sulit tidur"}},
        {
            "sosial": {
                "keluarga",
                "teman",
                "hubungan",
            }
        },
    ]
    lower_text = text.lower()

    category_counts = {}
    highest_count = 0
    highest_category = None

    for category_dict in categories:
        for category_name, words_set in category_dict.items():
            current_count = 0
            for word in words_set:
                if " " in word:
                    count = lower_text.count(word)
                else:
                    count = len(re.findall(r"\b" + re.escape(word) + r"\b", lower_text))
                current_count += count

            category_counts[category_name] = current_count

            if current_count > highest_count:
                highest_count = current_count
                highest_category = category_name

    # If no words matched any category, choose a random category
    if highest_count == 0:
        all_categories = list(category_counts.keys())
        random_category = random.choice(all_categories)
        return random_category, 0

    return highest_category, highest_count
