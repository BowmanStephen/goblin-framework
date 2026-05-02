#!/bin/bash
# Trigger the render-banner workflow via GitHub API
# Requires gh CLI or GITHUB_TOKEN
set -e
REPO="BowmanStephen/goblin-framework"
echo "Triggering render-banner workflow..."
curl -s -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/$REPO/actions/workflows/render-banner.yml/dispatches" \
  -d '{"ref":"main"}'
echo "✓ Workflow dispatched. Check https://github.com/$REPO/actions"