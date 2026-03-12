# multimodal-inference-service

<img src="https://img.shields.io/badge/Python-3568A3?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
<img src="https://img.shields.io/badge/uv-Package_Manager-FF9F4B?style=for-the-badge" alt="uv"/>
<img src="https://img.shields.io/badge/Uvicorn-5A4EE4?style=for-the-badge&logo=uvicorn&logoColor=white" alt="Uvicorn"/>
<img src="https://img.shields.io/badge/Ruff-EE4C2C?style=for-the-badge&logo=ruff&logoColor=white" alt="Ruff"/>
<img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face"/>

基于 **FastAPI** 的异步多模态推理服务：提供 **文生图（T2I）** 与 **图片理解（VLM）** 两种模式，单实例二选一，通过环境变量切换。使用 **uv** 管理依赖与锁定版本，代码带类型标注并用 **Ruff** 格式化与检查，支持 **Docker** 打包为可部署镜像。

当前进度：

- **HTTP + WebSocket** 基础服务
- **按模式启动**：`vlm` / `t2i`（通过 `SERVICE_MODE` 环境变量切换）
- **VLM 输入链路**：接收图片 base64 → 解码为 `PIL.Image` → 校验/解析 → 返回图片信息（模型推理当前为占位，可接入 Qwen2.5-VL 等）
- **请求排队**：单实例串行推理，多请求自动排队，避免显存并发冲突

---

## 项目优势

相比直接使用 LangChain、Dify、Coze 等框架/平台，本仓库采用 **自建 FastAPI 服务** 的方式，具有以下特点：

| 维度 | 说明 |
|------|------|
| **可复用、可嵌入** | 就是一个 HTTP/WebSocket 服务，任意系统通过 `POST /infer` 或 WebSocket 即可调用，无需引入框架或平台依赖；可迁入量化系统做监测机器人、聊天助手，也可接入其他项目作为多模态能力组件。 |
| **模型可自行替换** | 模型加载在本地代码中完成（如 Hugging Face `transformers` / `diffusers`），换模型只需改配置或加载逻辑，对外接口保持不变，调用方无感知。 |
| **数据链路透明** | 从「原始输入 → processor → 模型输入」的完整流程在代码中可见，便于排查、优化与学习，不依赖框架黑盒。 |
| **部署与运维简单** | 单进程/单容器，排队与并发策略自己掌控；可配合就绪探针、优雅退出、队列深度等做观测与扩缩容。 |
| **技术栈清晰** | Python 3.10 + uv + FastAPI + 类型标注 + Ruff，便于协作与 CI（GitHub Actions CI）。 |

适合作为 **多模态推理后端** 独立部署，或作为 **可插拔服务** 集成到量化、运维、内部工具等场景。

---

## 运行环境

- Python: **3.10**（项目根目录 `.python-version`）
- 包管理：**uv**（生成 `uv.lock` 用于锁定依赖版本）

---

**本项目目前还在开发中。** 快速开始、接口说明与测试文档将随开发进度补充。

