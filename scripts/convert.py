import zipfile
from pathlib import Path

import fitz  # PyMuPDF


def svg_to_png(input_path: Path, output_path: Path, dpi=300):
    doc = fitz.open(input_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=dpi, alpha=True)
    pix.save(output_path)
    doc.close()


def zip_folders(*folders: tuple[Path], output: Path):
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zipf:
        for folder in folders:
            folder = Path(folder)

            if not folder.exists():
                continue

            base_path = folder.parent
            for file in folder.rglob("*"):
                if not file.is_file():
                    continue

                relative_path = file.relative_to(base_path)
                zipf.write(file, relative_path)


def main():
    svg_base_path = Path("data/svg/")
    png_base_path = Path("data/png/")

    for svg_path in svg_base_path.glob("*.svg"):
        png_path = png_base_path / svg_path.with_suffix(".png").name
        svg_to_png(svg_path, png_path)
    zip_folders("data/png", "data/svg", output="data/vibra_open_pulse_logos.zip")


if __name__ == "__main__":
    main()
