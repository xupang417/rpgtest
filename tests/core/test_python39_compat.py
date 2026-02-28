from pathlib import Path
import ast


def _assert_py39_parseable(rel_path: str):
    root = Path(__file__).resolve().parents[2]
    src = (root / rel_path).read_text(encoding="utf-8")
    ast.parse(src, filename=rel_path, feature_version=(3, 9))


def test_type_hints_parse_in_python39():
    _assert_py39_parseable("src/rpg/skill.py")
    _assert_py39_parseable("src/world/npc_system.py")
