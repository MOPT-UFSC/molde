import zipfile
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


def svg_to_png(input_path: Path, output_path: Path, dpi=300):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(input_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=dpi, alpha=True)
    pix.save(output_path)
    doc.close()


def png_to_ico(input_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(input_path)
    img.save(
        output_path,
        format="ICO",
        sizes=[
            (16, 16),
            (32, 32),
            (48, 48),
            (64, 64),
            (128, 128),
            (256, 256),
        ],
    )


def zip_folders(*folders: tuple[Path], output: Path):
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zip:
        for folder in folders:
            folder = Path(folder)

            if not folder.exists():
                continue

            base_path = folder.parent
            for file in folder.rglob("*"):
                if not file.is_file():
                    continue

                relative_path = file.relative_to(base_path)
                zip.write(file, relative_path)


def main():
    for svg_path in Path("data/open_pulse/svg").glob("*.svg"):
        png_path = Path("data/open_pulse/png") / svg_path.with_suffix(".png").name
        svg_to_png(svg_path, png_path)

    for svg_path in Path("data/vibra/svg").glob("*.svg"):
        png_path = Path("data/vibra/png") / svg_path.with_suffix(".png").name
        svg_to_png(svg_path, png_path)

    for png_path in Path("data/open_pulse/png").glob("open_pulse_circle_*.png"):
        ico_path = Path("data/open_pulse/ico") / png_path.with_suffix(".ico").name
        png_to_ico(png_path, ico_path)

    for png_path in Path("data/vibra/png").glob("vibra_circle_*.png"):
        ico_path = Path("data/vibra/ico") / png_path.with_suffix(".ico").name
        png_to_ico(png_path, ico_path)

    zip_folders("data/vibra", "data/open_pulse", output="data/all_logos.zip")


if __name__ == "__main__":
    main()
