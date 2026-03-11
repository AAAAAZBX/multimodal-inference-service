"""VLM 输入预处理：base64 图片解码与校验。"""

import base64
import io
import re

from PIL import Image

# 常见图片格式的文件头魔数
_IMAGE_MAGIC = (
    (b"\x89PNG", "PNG"),
    (b"\xff\xd8\xff", "JPEG"),
    (b"GIF87a", "GIF"),
    (b"GIF89a", "GIF"),
    (b"RIFF", "WebP"),  # 需再检查 8:12 是否为 "WEBP"
)


def _normalize_base64(s: str) -> str:
    """去掉 data URL 前缀，统一 base64 字符集，并补足 padding。"""
    s = re.sub(r"^data:image/[^;]+;base64,", "", s)
    s = s.strip()
    # 表单/URL 编码常把 + 变成空格，先还原
    s = s.replace(" ", "+")
    # URL-safe base64 使用 - 和 _，还原为标准字符
    s = s.replace("-", "+").replace("_", "/")
    # 只保留合法 base64 字符，去掉换行等
    s = re.sub(r"[^A-Za-z0-9+/]", "", s)
    missing = len(s) % 4
    if missing:
        s += "=" * (4 - missing)
    return s


def _is_image_bytes(data: bytes) -> bool:
    """检查字节是否像常见图片格式。"""
    if len(data) < 12:
        return False
    for magic, _ in _IMAGE_MAGIC:
        if data.startswith(magic):
            return True
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return True
    return False


def decode_base64_image(base64_str: str) -> Image.Image:
    base64_data = _normalize_base64(base64_str)
    byte_data = base64.b64decode(base64_data)
    if not _is_image_bytes(byte_data):
        raise ValueError(
            "Decoded data is not a valid image (expected PNG/JPEG/GIF/WebP header). "
            "Check that image_b64 contains the raw base64 of an image file."
        )
    image_data = io.BytesIO(byte_data)
    img = Image.open(image_data)
    img = img.convert("RGB")
    return img


def get_image_info(image: Image.Image) -> dict[str, object]:
    return {
        "width": image.width,
        "height": image.height,
        "format": image.format,
    }

