
container exec -i codex sh -s <<'SCRIPT'
set -eu

REPO="github.com/adamnovotnycom/ProjectTrust.git"
WORKDIR="ProjectTrust"

rm -rf "$WORKDIR"
git clone "https://x-access-token:${GH_TOKEN}@${REPO}"
cd "$WORKDIR"
git remote set-url origin "https://x-access-token:${GH_TOKEN}@${REPO}"
git status
git checkout -b "branch_update_$(date +%Y%m%d%H%M%S)"

cd ".."
codex exec \
  --model gpt-5.6-sol \
  --skip-git-repo-check \
  --sandbox danger-full-access \
  -c 'model_reasoning_effort="medium"' \
  -c 'web_search="live"' \
  "$(cat task-new.md)"

cd "$WORKDIR"
git status
git config --global user.email 'codex@adamnovotny.com'
git config --global user.name 'Codex'
git add .
if git diff --cached --quiet; then
  echo "No changes to commit; skipping commit and push."
else
  git commit -m 'Update pages'
  git push origin HEAD
fi

SCRIPT
