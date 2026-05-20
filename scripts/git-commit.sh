#!/bin/bash
# Commit without Cursor co-author trailer. Run from Terminal, not via Cursor agent.
set -e
cd "$(dirname "$0")/.."

export GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-Rahul Aggarwal}"
export GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-rahul.agg1804@gmail.com}"
export GIT_COMMITTER_NAME="${GIT_COMMITTER_NAME:-Rahul Aggarwal}"
export GIT_COMMITTER_EMAIL="${GIT_COMMITTER_EMAIL:-rahul.agg1804@gmail.com}"

git commit -F - <<'EOF'
Add truck trip planner with HOS routing and ELD logs

Django API for trip planning, React frontend with map and daily log sheets.
EOF

echo ""
echo "Commit message:"
git log -1 --format=%B
