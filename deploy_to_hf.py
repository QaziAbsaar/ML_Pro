from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import HfApi


ROOT = Path(__file__).resolve().parent
REQUIRED_FILES = [
    "app.py",
    "taxi_fare.py",
    "requirements.txt",
    "README.md",
    "HF_DEPLOYMENT_GUIDE.md",
    "PROJECT_SUMMARY.md",
    "DATASET_GUIDE.md",
    "train.py",
    "download_dataset.py",
    "generate_synthetic_data.py",
    "push_to_hf.sh",
    "artifacts/taxi_fare_ann_model.joblib",
    "artifacts/metrics.json",
    "artifacts/training_summary.txt",
]

IGNORE_PATTERNS = [
    ".git/**",
    ".venv/**",
    "**/__pycache__/**",
    "**/.ipynb_checkpoints/**",
    "**/*.pyc",
    "**/*.pyo",
]


def main() -> None:
    username = os.environ.get("HF_USERNAME")
    space_name = os.environ.get("HF_SPACE")
    token = os.environ.get("HF_TOKEN")

    if not username or not space_name or not token:
        raise SystemExit("Missing HF_USERNAME, HF_SPACE, or HF_TOKEN environment variables.")

    repo_id = f"{username}/{space_name}"
    api = HfApi()

    api.create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True,
        token=token,
    )

    missing_files = [relative_path for relative_path in REQUIRED_FILES if not (ROOT / relative_path).exists()]
    if missing_files:
        print("Skipping missing files:")
        for relative_path in missing_files:
            print(f"  - {relative_path}")

    print(f"Uploading workspace files to https://huggingface.co/spaces/{repo_id} ...")

    api.upload_folder(
        repo_id=repo_id,
        repo_type="space",
        folder_path=str(ROOT),
        commit_message="Deploy Space from local workspace",
        token=token,
        ignore_patterns=IGNORE_PATTERNS,
    )

    print("Upload complete.")
    print(f"Open https://huggingface.co/spaces/{repo_id} to see the build status.")