import random
from pathlib import Path

# ===== CONFIG =====
FOLDER = Path("images")          # dossier des images
PADDING = 2                      # 001, 002, ...
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SEED = None                      # mets un nombre (ex: 42) si tu veux un shuffle reproductible
START_I = 2                      # --i commence à 2 (mets 1 si tu veux)
OUTPUT_HTML = "sections.html"    # fichier généré
PRINT_SECTIONS = True            # affiche les sections dans la console
# ==================

def main():
    if not FOLDER.exists() or not FOLDER.is_dir():
        raise FileNotFoundError(f"Dossier introuvable: {FOLDER.resolve()}")

    files = [p for p in FOLDER.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_EXTENSIONS]
    if not files:
        raise RuntimeError("Aucune image trouvée dans le dossier.")

    # Shuffle
    rng = random.Random(SEED)
    rng.shuffle(files)

    # 1) Renommage temporaire (évite collisions)
    temp_files = []
    for idx, p in enumerate(files, start=1):
        tmp = p.with_name(f"__tmp__{idx:04d}{p.suffix.lower()}")
        p.rename(tmp)
        temp_files.append(tmp)

    # 2) Renommage final 001..N
    final_files = []
    for idx, tmp in enumerate(temp_files, start=1):
        new_name = f"{idx:0{PADDING}d}{tmp.suffix.lower()}"
        final_path = tmp.with_name(new_name)
        tmp.rename(final_path)
        final_files.append(final_path)

    # 3) Génération des sections
    lines = []
    i_val = START_I
    for idx, p in enumerate(final_files, start=1):
        number = f"{idx:0{PADDING}d}"
        ext = p.suffix.lower().lstrip(".")
        lines.append(
            f"<section class=\"frame stack\" data-caption=\"\" style=\"--i:{i_val}; --img:url('images/{number}.{ext}')\"></section>"
        )
        i_val += 1

    html_blob = "\n".join(lines) + "\n"

    # Écriture fichier
    Path(OUTPUT_HTML).write_text(html_blob, encoding="utf-8")

    # Console output : UNIQUEMENT les sections (comme ta capture)
    if PRINT_SECTIONS:
        print(html_blob, end="")

    # Logs (si tu veux les garder, sinon commente ces 2 lignes)
    # print(f"✔ {len(final_files)} images mélangées et renommées en 001..{len(final_files):0{PADDING}d}")
    # print(f"✔ HTML généré dans: {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
