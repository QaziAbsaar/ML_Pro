#!/usr/bin/env bash
set -euo pipefail

# Helper script to push the current repo to a Hugging Face Space remote.
# Usage:
#   export HF_USERNAME=your_hf_username
#   export HF_SPACE=your_space_name
#   export HF_TOKEN=your_hf_token
#   ./push_to_hf.sh

if [ -z "${HF_USERNAME:-}" ] || [ -z "${HF_SPACE:-}" ] || [ -z "${HF_TOKEN:-}" ]; then
  echo "Missing environment variables. Set HF_USERNAME, HF_SPACE, HF_TOKEN." >&2
  exit 1
fi

REMOTE_NAME=huggingface
REMOTE_URL="https://${HF_TOKEN}@huggingface.co/spaces/${HF_USERNAME}/${HF_SPACE}.git"

# Add remote if not present
if git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
  echo "Remote '$REMOTE_NAME' already exists. Updating URL to use provided token temporarily."
  git remote remove "$REMOTE_NAME"
fi

echo "Adding remote $REMOTE_NAME -> $REMOTE_URL"
git remote add "$REMOTE_NAME" "$REMOTE_URL"

echo "Pushing branch 'main' to $REMOTE_NAME (force) ..."
git push "$REMOTE_NAME" main --force

echo "Push complete. Removing remote to avoid leaking token in git config."
git remote remove "$REMOTE_NAME"

echo "Done. The Space should be building now. Check https://huggingface.co/spaces/${HF_USERNAME}/${HF_SPACE} for logs."