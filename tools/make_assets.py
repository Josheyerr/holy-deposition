from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(r"C:\Users\kmkjk\.cursor\projects\f-bap-ce-compatch\assets")
OUT = ROOT / "images"
OUT.mkdir(parents=True, exist_ok=True)

FONT = r"C:\Windows\Fonts\BOOKOSB.TTF"
GOLD = (214, 182, 104, 255)
LINE = (214, 182, 104, 200)
WIDTH = 630


def header(text: str, name: str) -> None:
    big = ImageFont.truetype(FONT, 58)
    small = ImageFont.truetype(FONT, 36)
    img = Image.new("RGBA", (WIDTH, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    x = 6
    baseline = 64
    for i, word in enumerate(text.split(" ")):
        if i:
            x += 14
        if word.lower() in {"of", "the"}:
            first, rest = "", word.upper()
        else:
            first, rest = word[0].upper(), word[1:].upper()
        if first:
            draw.text((x, baseline), first, font=big, fill=GOLD, anchor="ls")
            x += draw.textlength(first, font=big)
        if rest:
            draw.text((x + 2, baseline), rest, font=small, fill=GOLD, anchor="ls")
            x += draw.textlength(rest, font=small) + 2
    line_y = baseline - 13
    draw.line([(x + 16, line_y), (WIDTH - 6, line_y)], fill=LINE, width=2)
    img.save(OUT / f"header_{name}.png")


def split_box(left: str, right: str, name: str) -> None:
    font = ImageFont.truetype(FONT, 22)
    img = Image.new("RGBA", (WIDTH, 50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([1, 1, WIDTH - 2, 48], outline=(190, 200, 210, 220), width=2)
    draw.text((16, 25), left, font=font, fill=GOLD, anchor="lm")
    draw.text((WIDTH - 16, 25), right, font=font, fill=GOLD, anchor="rm")
    draw.line([(WIDTH // 2, 10), (WIDTH // 2, 40)], fill=(190, 200, 210, 120), width=1)
    img.save(OUT / f"box_{name}.png")


def icons() -> None:
    sheet = Image.open(SRC / "holy_deposition_icons.jpg").convert("RGBA")
    w, h = sheet.size
    names = ["war", "clergy", "temporal", "dynasty"]
    boxes = [
        (0.06, 0.04, 0.46, 0.45),
        (0.53, 0.04, 0.93, 0.45),
        (0.06, 0.50, 0.46, 0.91),
        (0.53, 0.50, 0.93, 0.91),
    ]
    for name, (l, t, r, b) in zip(names, boxes):
        crop = sheet.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
        side = min(crop.size)
        crop = crop.crop((0, 0, side, side)).resize((48, 48), Image.LANCZOS)
        mask = Image.new("L", (48, 48), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, 47, 47], fill=255)
        crop.putalpha(mask)
        crop.save(OUT / f"icon_{name}.png")


def banner_and_preview() -> None:
    banner = Image.open(SRC / "holy_deposition_banner.jpg").convert("RGB")
    banner.resize((WIDTH, int(WIDTH * banner.height / banner.width)), Image.LANCZOS).save(
        OUT / "banner.jpg", quality=90
    )
    preview = Image.open(SRC / "holy_deposition_preview.jpg").convert("RGB")
    preview.resize((512, 512), Image.LANCZOS).save(ROOT / "preview.jpg", quality=92)


if __name__ == "__main__":
    for text, name in [
        ("Overview", "overview"),
        ("Features", "features"),
        ("Who Can Declare", "who"),
        ("Valid Targets", "targets"),
        ("Spoils of Victory", "victory"),
        ("Compatibility", "compat"),
    ]:
        header(text, name)
    split_box("TEMPORAL RULERS", "CLERGY RULERS", "rulers")
    icons()
    banner_and_preview()
    print("ok", sorted(p.name for p in OUT.iterdir()))
