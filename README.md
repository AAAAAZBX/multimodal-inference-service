
# multimodal-inference-service
基于 FastAPI 的异步多模态推理服务骨架。当前实现了：

- **HTTP + WebSocket** 基础服务
- **按模式启动**：`vlm` / `t2i`（通过环境变量切换）
- **VLM 完整输入链路的第一段**：接收图片 base64 → 解码为 `PIL.Image` → 基础校验/解析 → 返回图片信息（模型推理仍为占位）

> 需求文档 `demand.txt` 为本地文件，已在 `.gitignore` 中忽略，不会提交。

---

## 运行环境

- Python: **3.10**（项目根目录 `.python-version`）
- 包管理：**uv**（生成 `uv.lock` 用于锁定依赖版本）

---

## 快速开始（Windows / PowerShell）

在项目根目录 `D:\AI\multimodal-inference-service` 下执行：

1) 安装依赖（含 dev 依赖）

```bash
uv sync --all-extras
```

2) 启动服务

```bash
# 选择服务模式：vlm 或 t2i（默认 vlm）
$env:SERVICE_MODE="vlm"

uv run uvicorn multimodal_inference_service.app:app --reload
```

服务默认监听在 `http://127.0.0.1:8000`。

---

## 接口说明

### 健康检查

- `GET /health`

返回示例：

```json
{ "status": "ok", "mode": "vlm" }
```

### WebSocket Echo

- `GET /ws`（WebSocket）

收到文本消息后返回：`echo: <message>`。

### 推理接口（占位）

- `POST /infer`

当前仅实现 **VLM 输入解码链路**（图片 base64 → `PIL.Image`），推理结果为占位字符串。

请求体（两种字段名都支持，二选一即可）：

```json
{
  "prompt": "describe the image",
  "image_b64": "<base64>"
}
```

或：

```json
{
  "prompt": "describe the image",
  "image_base64": "<base64>"
}
```

支持以下形式的 base64：

- **纯 base64**
- **Data URL**：`data:image/png;base64,<base64...>`
- **URL-safe base64**：`-` / `_` 会自动还原为 `+` / `/`
- 表单/URL 编码导致的 `+` → 空格（会自动还原）

返回示例（字段会随后续模型接入扩展）：

```json
{
  "mode": "vlm",
  "prompt": "describe the image",
  "image_info": { "width": 420, "height": 120, "format": null },
  "result": "vlm placeholder: describe the image"
}
```

---

## 测试

```bash
uv run pytest -v
```

当前包含基础路由与 `/infer` 的最小测试用例。

