
container exec -i codex sh -s <<'SCRIPT'
set -eu

REPO="github.com/adamnovotnycom/ProjectTrust.git"
WORKDIR="ProjectTrust"

rm -rf "$WORKDIR"
git clone "https://x-access-token:${GH_TOKEN}@${REPO}"
cd "$WORKDIR"
git remote set-url origin "https://x-access-token:${GH_TOKEN}@${REPO}"
git fetch --all --prune
git status
TASK="$(cat ../task-existing.md)

Available remote branches:
$(git branch --remotes --format='%(refname:short)' | sed 's#^origin/##' | sort -u)

Choose the appropriate existing branch from this list based on the task. Check it out before making edits. Do not create a branch."
codex exec \
  --model gpt-5.6-sol \
  --sandbox danger-full-access \
  -c 'model_reasoning_effort="medium"' \
  -c 'web_search="live"' \
  "$TASK"

BRANCH="$(git branch --show-current)"
if [ -z "$BRANCH" ] || ! git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  echo "Codex must leave the repository on an existing origin branch; current branch is '$BRANCH'." >&2
  exit 1
fi

git status
git config --global user.email 'codex@adamnovotny.com'
git config --global user.name 'Codex'
git add .
if git diff --cached --quiet; then
  echo "No changes to commit; skipping commit and push."
else
  git commit -m 'Update pages'
  git push origin "HEAD:refs/heads/$BRANCH"
fi

SCRIPT
