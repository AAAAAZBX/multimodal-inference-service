import base64
from pathlib import Path


def image_to_base64(image_path: str) -> str:
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    with path.open("rb") as f:
        image_bytes = f.read()

    return base64.b64encode(image_bytes).decode("utf-8")


if __name__ == "__main__":
    image_path = r"D:/AI/multimodal-inference-service/tools/image.png"
    output_path = r"D:/AI/multimodal-inference-service/tools/image_base64.txt"

    image_base64 = image_to_base64(image_path)

    print("Base64 预览（前 100 个字符）:")
    print(image_base64[:100] + "...")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(image_base64)

    print(f"\n完整 base64 已保存到: {output_path}")

