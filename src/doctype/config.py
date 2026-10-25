"""Settings from environment variables, with an optional .env file in the working directory."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


@dataclass(frozen=True)
class Settings:
    model: str = "simulated"                 # simulated | laya
    laya_repo: str = "convaiinnovations/laya"
    laya_subfolder: str = "typed-decisions"  # typed-decisions | multilingual | "" for english
    fallback: str = "simulated"              # simulated | ollama | bedrock
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"
    aws_region: str = "eu-west-2"
    bedrock_model_id: str = "amazon.nova-micro-v1:0"
    trainer: str = "simulated"               # simulated | export | laya
    laya_base: str = "english"           # alias, Hub id or local dir
    laya_device: str = "auto"            # auto | cpu | cuda | mps
    laya_output_dir: str = "./models"
    threshold: float = 0.85
    audit_rate: float = 0.25
    data_dir: str = "./data"
    var_dir: str = "./var"
    tenant: str = "fcci"

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        e = os.environ.get
        model = e("DOCTYPE_MODEL", cls.model)
        return cls(
            model=model,
            laya_repo=e("LAYA_REPO", cls.laya_repo),
            laya_subfolder=e("LAYA_SUBFOLDER", cls.laya_subfolder),
            fallback=e("DOCTYPE_FALLBACK", cls.fallback),
            ollama_host=e("OLLAMA_HOST", cls.ollama_host),
            ollama_model=e("OLLAMA_MODEL", cls.ollama_model),
            aws_region=e("AWS_REGION", cls.aws_region),
            bedrock_model_id=e("BEDROCK_MODEL_ID", cls.bedrock_model_id),
            trainer=e("DOCTYPE_TRAINER", "export" if model == "laya" else cls.trainer),
            laya_base=e("LAYA_BASE", cls.laya_base),
            laya_device=e("LAYA_DEVICE", cls.laya_device),
            laya_output_dir=e("LAYA_OUTPUT_DIR", cls.laya_output_dir),
            threshold=float(e("DOCTYPE_THRESHOLD", cls.threshold)),
            audit_rate=float(e("DOCTYPE_AUDIT_RATE", cls.audit_rate)),
            data_dir=e("DOCTYPE_DATA_DIR", cls.data_dir),
            var_dir=e("DOCTYPE_VAR_DIR", cls.var_dir),
            tenant=e("DOCTYPE_TENANT", cls.tenant),
        )
