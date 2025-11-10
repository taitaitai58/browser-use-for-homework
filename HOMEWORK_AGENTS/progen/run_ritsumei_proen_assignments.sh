
#このようなスクリプトを立てると、まとめての自動実行が可能になります、
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/ritsumei_puroen_assignment.py"

for week_index in {9..13}; do
  for assignment_number in {1..4}; do
    printf '%s\n%s\n' "${week_index}" "${assignment_number}" | uv run "${PYTHON_SCRIPT}"
  done
done

