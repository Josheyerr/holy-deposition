from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(r"C:\ck3_workshop_upload")
CONTENT = Path(
    r"C:\Users\kmkjk\OneDrive\Documents\Paradox Interactive\Crusader Kings III\mod\holy_deposition"
)


def esc(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def main() -> None:
    published = ROOT / "publishedfileid.txt"
    file_id = published.read_text().split()[0] if published.exists() else "0"
    description = (ROOT / "description.txt").read_text(encoding="utf-8").strip()
    fields = {
        "appid": "1158310",
        "publishedfileid": file_id,
        "contentfolder": str(CONTENT),
        "previewfile": str(ROOT / "preview.jpg"),
        "visibility": "0",
        "title": "Holy Deposition",
        "description": description,
        "changenote": "Initial release: Holy Deposition casus belli with clergy and temporal ruler choices.",
    }
    body = "\n".join(f'\t"{k}"\t\t"{esc(v)}"' for k, v in fields.items())
    UPLOAD_DIR.mkdir(exist_ok=True)
    out = UPLOAD_DIR / "holy_deposition.vdf"
    out.write_text('"workshopitem"\n{\n' + body + "\n}\n", encoding="utf-8")
    print(out, len(description), "chars")


if __name__ == "__main__":
    main()
