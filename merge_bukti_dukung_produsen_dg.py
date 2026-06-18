"""
merge_bukti_dukung_produsen_dg.py
=================================
Merges and sorts Produsen DG (Data Geospasial) bukti dukung (evidence documents)
for SIGAP Award 2025.

Usage:
    python merge_bukti_dukung_produsen_dg.py

Input  : produsen_form/produsen_*/
Output : produsen_output/{question_folder}/MERGED_{question_folder}.pdf
"""

import os
import re
import io
from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.enums import TA_CENTER
from pypdf import PdfReader, PdfWriter

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "produsen_form"
OUTPUT_DIR = BASE_DIR / "produsen_output"

SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}

QUESTION_MAP = {
    "1_1": "1_1_pembentukan_kelompok_kerja",
    "1_2": "1_2_peran_geospasial_kelembagaan",
    "1_3": "1_3_strategi_geospasial",
    "2_1": "2_1_berbagi_data",
    "2_2": "2_2_hak_kekayaan_intelektual",
    "3_1": "3_1_tata_kelola_keuangan_dan_akuntabilitas",
    "3_2": "3_2_sumber_pendanaan",
    "4_1": "4_1_infrastruktur_geodetik",
    "4_2": "4_2_inventaris_data_dan_profil_data",
    "4_3": "4_3_analisis_kesenjangan_data",
    "4_4": "4_4_peta_jalan_tema_data",
    "4_5": "4_5_kualitas_data",
    "4_6": "4_6_metadata",
    "4_7": "4_7_penyimpanan_dan_pengambilan_data",
    "4_8": "4_8_siklus_aliran_data",
    "4_9": "4_9_interoperabilitas_data",
    "5_1": "5_1_strategi_inovasi_geospasial",
    "5_2": "5_2_infrastruktur_ict_inti",
    "5_3": "5_3_modernisasi_aset_data",
    "5_4": "5_4_sistem_inovasi_nasional",
    "5_5": "5_5_sistem_terpadu_dari_sistem",
    "6_1": "6_1_tata_kelola_standar",
    "6_2": "6_2_strategi_rencana_standar",
    "6_3": "6_3_implementasi",
    "6_4": "6_4_kepatuhan_standar",
    "7_1": "7_1_kesadaran_dan_peluang_kemitraan",
    "7_2": "7_2_kolaborasi_lintas_sektor",
    "7_3": "7_3_mengelola_kemitraan",
    "8_1": "8_1_kelompok_kerja_peningkatan_kapasitas",
    "8_2": "8_2_penilaian_dan_analisis",
    "8_3": "8_3_strategi_dan_rencana_implementasi",
    "8_4": "8_4_program_pendidikan_tinggi",
    "8_5": "8_5_pendekatan_pengembangan_profesional",
    "8_6": "8_6_jf_surveyor_pemetaan",
    "8_7": "8_7_jf_pranata_komputer",
    "9_1": "9_1_tata_kelola_komunikasi",
    "9_2": "9_2_basis_data_studi_kasus",
    "9_3": "9_3_tautan_ke_sdgs",
}

# Questions that do NOT require evidence upload — skip entirely
NO_BUKTI_DUKUNG_QUESTIONS = {
    "1_2", "4_4", "5_4", "6_2", "6_4", "7_3", "8_3", "9_1", "9_2", "9_3"
}

# ---------------------------------------------------------------------------
# Colour constants (ReportLab uses 0–1 floats)
# ---------------------------------------------------------------------------

COLOR_SEPARATOR_BG = colors.HexColor("#1B5E20")   # dark green
COLOR_SEPARATOR_FG = colors.white
COLOR_MISSING_BG   = colors.HexColor("#FFF9C4")   # light yellow
COLOR_MISSING_FG   = colors.HexColor("#F57F17")   # amber
COLOR_WHITE        = colors.white
COLOR_BLACK        = colors.black

A4_W, A4_H = A4   # 595.27 x 841.89 points


# ===========================================================================
# Step 1 — Scan & index files
# ===========================================================================

def parse_question_key(filename: str) -> str | None:
    """Return 'X_Y' from filenames like 'no_X_Y_...' or None if no match."""
    m = re.match(r"^no_(\d+)_(\d+)_", filename, re.IGNORECASE)
    if m:
        return f"{m.group(1)}_{m.group(2)}"
    return None


def folder_to_label(folder_name: str) -> str:
    """Convert 'produsen_bina_usaha_pemanfaatan_hutan' →
    'PRODUSEN DG - BINA USAHA PEMANFAATAN HUTAN'."""
    name = folder_name.replace("produsen_", "", 1)
    name = name.replace("_", " ").upper()
    return f"PRODUSEN DG - {name}"


def scan_produsen_folders() -> tuple[list[str], dict]:
    """
    Returns:
        sorted_produsen : list of folder names sorted alphabetically
        index           : { question_key: { produsen_folder: [Path, ...] } }
    """
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Input directory not found: {INPUT_DIR}")

    instansi_folders = sorted(
        [p for p in INPUT_DIR.iterdir() if p.is_dir() and p.name.startswith("produsen_")],
        key=lambda p: p.name,
    )
    sorted_produsen = [p.name for p in instansi_folders]

    # Initialise index: every required question × every instansi starts empty
    index: dict[str, dict[str, list[Path]]] = {
        q_key: {inst: [] for inst in sorted_produsen}
        for q_key in QUESTION_MAP
        if q_key not in NO_BUKTI_DUKUNG_QUESTIONS
    }

    for inst_name in sorted_produsen:
        folder_path = INPUT_DIR / inst_name
        for file in sorted(folder_path.iterdir()):
            if not file.is_file():
                continue
            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            q_key = parse_question_key(file.name)
            if q_key and q_key in index:
                index[q_key][inst_name].append(file)

    return sorted_produsen, index


# ===========================================================================
# ReportLab page generators
# ===========================================================================

def _build_single_page_pdf(
    story: list,
    bg_color=None,
) -> bytes:
    """
    Render a ReportLab *Platypus* story into a single-page PDF in memory.
    Returns raw PDF bytes.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    if bg_color:
        def on_page(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(bg_color)
            canvas.rect(0, 0, A4_W, A4_H, fill=1, stroke=0)
            canvas.restoreState()

        doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    else:
        doc.build(story)

    buf.seek(0)
    return buf.read()


def make_cover_page(question_folder_name: str) -> bytes:
    """Generate the white cover page for a question."""
    title_text = question_folder_name.replace("_", " ").upper()

    heading_style = ParagraphStyle(
        "CoverHeading",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=COLOR_BLACK,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=20,
    )
    title_style = ParagraphStyle(
        "CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        textColor=COLOR_BLACK,
        alignment=TA_CENTER,
        spaceAfter=20,
        leading=32,
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        fontName="Helvetica",
        fontSize=14,
        textColor=COLOR_BLACK,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=20,
    )

    story = [
        Spacer(1, 6 * cm),
        Paragraph("LAMPIRAN BUKTI DUKUNG", heading_style),
        Spacer(1, 0.5 * cm),
        Paragraph(title_text, title_style),
        Spacer(1, 0.5 * cm),
        Paragraph("SELURUH PRODUSEN DG", heading_style),
        Spacer(1, 1 * cm),
        Paragraph("SIGAP Award 2025", subtitle_style),
    ]
    return _build_single_page_pdf(story, bg_color=None)


def make_separator_page(instansi_label: str, question_folder_name: str) -> bytes:
    """Generate the dark-green separator page for an instansi."""
    question_label = question_folder_name.replace("_", " ").upper()

    name_style = ParagraphStyle(
        "SepName",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=COLOR_SEPARATOR_FG,
        alignment=TA_CENTER,
        spaceAfter=16,
        leading=28,
    )
    sub_style = ParagraphStyle(
        "SepSub",
        fontName="Helvetica",
        fontSize=14,
        textColor=COLOR_SEPARATOR_FG,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=20,
    )

    story = [
        Spacer(1, 7 * cm),
        Paragraph(instansi_label, name_style),
        Spacer(1, 0.5 * cm),
        Paragraph("Lampiran Bukti Dukung", sub_style),
        Spacer(1, 0.3 * cm),
        Paragraph(question_label, sub_style),
    ]
    return _build_single_page_pdf(story, bg_color=COLOR_SEPARATOR_BG)


def make_missing_page(instansi_label: str) -> bytes:
    """Generate the light-yellow 'not submitted' page."""
    warn_style = ParagraphStyle(
        "MissWarn",
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=COLOR_MISSING_FG,
        alignment=TA_CENTER,
        spaceAfter=20,
        leading=26,
    )
    body_style = ParagraphStyle(
        "MissBody",
        fontName="Helvetica",
        fontSize=14,
        textColor=COLOR_MISSING_FG,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=20,
    )

    story = [
        Spacer(1, 7 * cm),
        Paragraph("⚠ BELUM MELAMPIRKAN BUKTI DUKUNG", warn_style),
        Spacer(1, 0.5 * cm),
        Paragraph(instansi_label, body_style),
        Spacer(1, 0.3 * cm),
        Paragraph("tidak melampirkan bukti dukung", body_style),
        Paragraph("untuk soal ini.", body_style),
    ]
    return _build_single_page_pdf(story, bg_color=COLOR_MISSING_BG)


# ===========================================================================
# File conversion helpers
# ===========================================================================

def image_to_pdf_bytes(image_path: str) -> bytes:
    """Convert an image file to a single-page PDF bytes."""
    img = Image.open(image_path)  # open from PATH (str), not BytesIO
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')

    page_w, page_h = A4
    margin = 28.35  # 1cm margin

    avail_w = page_w - 2 * margin
    avail_h = page_h - 2 * margin

    img_w, img_h = img.size
    ratio = min(avail_w / img_w, avail_h / img_h)
    draw_w = img_w * ratio
    draw_h = img_h * ratio

    x = margin + (avail_w - draw_w) / 2
    y = margin + (avail_h - draw_h) / 2

    img_buf = io.BytesIO()
    img.save(img_buf, format='PNG')
    img_buf.seek(0)

    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=A4)
    c.drawImage(ImageReader(img_buf), x, y, width=draw_w, height=draw_h)
    c.save()
    buf.seek(0)
    return buf.read()


def append_pdf_bytes(writer: PdfWriter, pdf_bytes: bytes):
    """Append all pages from raw PDF bytes into a PdfWriter."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    for page in reader.pages:
        writer.add_page(page)


def append_file(writer: PdfWriter, file_path: Path):
    """Append a single file (PDF or image) into a PdfWriter."""
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        try:
            reader = PdfReader(str(file_path))
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            print(f"    [WARN] Could not read PDF {file_path.name}: {e}")
    elif suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        try:
            pdf_bytes = image_to_pdf_bytes(str(file_path))
            append_pdf_bytes(writer, pdf_bytes)
        except Exception as e:
            print(f"    [WARN] Could not convert image {file_path.name}: {e}")
    else:
        print(f"    [SKIP] Unsupported file type: {file_path.name}")


# ===========================================================================
# Main merge loop
# ===========================================================================

def merge_question(
    q_key: str,
    q_folder: str,
    sorted_produsen: list[str],
    index: dict,
) -> tuple[int, int]:
    """
    Build the merged PDF for one question.
    Returns (submitted_count, missing_count).
    """
    out_dir = OUTPUT_DIR / q_folder
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"MERGED_{q_folder}.pdf"

    writer = PdfWriter()

    # -- Cover page --
    cover_bytes = make_cover_page(q_folder)
    append_pdf_bytes(writer, cover_bytes)

    submitted = 0
    missing = 0

    for inst_name in sorted_produsen:
        inst_label = folder_to_label(inst_name)
        files = index[q_key][inst_name]

        # Separator page
        sep_bytes = make_separator_page(inst_label, q_folder)
        append_pdf_bytes(writer, sep_bytes)

        if files:
            for f in files:
                append_file(writer, f)
            submitted += 1
        else:
            missing_bytes = make_missing_page(inst_label)
            append_pdf_bytes(writer, missing_bytes)
            missing += 1

    with open(out_file, "wb") as fh:
        writer.write(fh)

    print(f"  ✔  {q_key:<4}  →  {out_file.name}  "
          f"({submitted} submitted, {missing} missing)")

    return submitted, missing


# ===========================================================================
# Summary
# ===========================================================================

def print_summary(results: dict, sorted_produsen: list[str]):
    total_instansi = len(sorted_produsen)
    print()
    print("=" * 65)
    print("=== SUMMARY ===")
    print("=" * 65)
    print(f"{'Question':<8} | {'Total Instansi':>14} | {'Submitted':>9} | {'Missing':>7}")
    print("-" * 65)
    for q_key, (submitted, missing) in results.items():
        print(f"{q_key:<8} | {total_instansi:>14} | {submitted:>9} | {missing:>7}")
    print("=" * 65)
    grand_submitted = sum(v[0] for v in results.values())
    grand_missing   = sum(v[1] for v in results.values())
    total_cells     = len(results) * total_instansi
    print(f"{'TOTAL':<8} | {total_cells:>14} | {grand_submitted:>9} | {grand_missing:>7}")
    print("=" * 65)


# ===========================================================================
# Entry point
# ===========================================================================

def main():
    print("=" * 65)
    print("  Merge Bukti Dukung — SIGAP Award 2025 (PRODUSEN DG)")
    print("=" * 65)

    # Step 1: Scan and index
    print(f"\n[1/3] Scanning: {INPUT_DIR}")
    sorted_produsen, index = scan_produsen_folders()
    print(f"      Found {len(sorted_produsen)} Produsen DG folders (sorted):")
    for inst in sorted_produsen:
        print(f"        • {folder_to_label(inst)}")

    # Step 2: Merge
    active_questions = len(QUESTION_MAP) - len(NO_BUKTI_DUKUNG_QUESTIONS)
    print(f"\n[2/3] Merging {active_questions} questions "
          f"({len(NO_BUKTI_DUKUNG_QUESTIONS)} skipped) → {OUTPUT_DIR}\n")
    results = {}
    for q_key, q_folder in QUESTION_MAP.items():
        if q_key in NO_BUKTI_DUKUNG_QUESTIONS:
            print(f"  –  {q_key:<4}  →  SKIPPED (no bukti dukung required)")
            continue
        submitted, missing = merge_question(q_key, q_folder, sorted_produsen, index)
        results[q_key] = (submitted, missing)

    # Step 3: Done + Summary
    print("\n[3/3] Done!")
    print_summary(results, sorted_produsen)


if __name__ == "__main__":
    main()
