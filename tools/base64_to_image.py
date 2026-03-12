"""
将 base64 文本还原为图片文件。

默认行为：
- 读取同目录下的 `image_base64.txt`
- 解码为二进制
- 写出为 `image_decoded.png`

你可以用 `image_to_base64.py` 生成 base64，再用本脚本还原，验证是否与原图一致。
"""

import argparse
import base64
from pathlib import Path


def base64_to_image(base64_path: str, output_path: str) -> None:
    """从 base64 文本文件还原图片。"""
    b64_file = Path(base64_path)
    if not b64_file.is_file():
        raise FileNotFoundError(f"Base64 file not found: {b64_file}")

    base64_str = b64_file.read_text(encoding="utf-8")

    # 兼容 data URL / URL-safe / 带空格的情况，复用服务端的处理思路（简化版）
    base64_str = base64_str.strip()
    if "," in base64_str and base64_str.startswith("data:image"):
        base64_str = base64_str.split(",", 1)[1]

    # 表单/URL 编码可能把 + 变成空格
    base64_str = base64_str.replace(" ", "+")

    # URL-safe 还原为标准 base64 字符集
    base64_str = base64_str.replace("-", "+").replace("_", "/")

    # 去掉可能的换行
    base64_str = base64_str.replace("\n", "").replace("\r", "")

    # padding 补齐到 4 的倍数
    missing = len(base64_str) % 4
    if missing:
        base64_str += "=" * (4 - missing)

    image_bytes = base64.b64decode(base64_str)

    out_file = Path(output_path)
    out_file.write_bytes(image_bytes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Decode base64 text file to image.")
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default=r"D:/AI/multimodal-inference-service/tools/image_base64.txt",
        help="Base64 文本文件路径（默认：tools/image_base64.txt）",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=r"D:/AI/multimodal-inference-service/tools/image_decoded.png",
        help="输出图片路径（默认：tools/image_decoded.png）",
    )

    args = parser.parse_args()
    base64_to_image(args.input, args.output)
    print(f"已从 {args.input} 还原图片到: {args.output}")


if __name__ == "__main__":
    main()

