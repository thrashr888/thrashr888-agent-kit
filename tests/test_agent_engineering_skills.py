from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "agent-ready-engineering": {
        "required": [
            "## When to Use",
            "## The Six Foundations",
            "## Procedure",
            "## Codify Durable Learning",
            "## Pitfalls",
            "## Verification",
            "Deterministic validation",
            "Review capacity and quality",
        ],
        "references": ["references/agent-readiness-audit.md"],
    },
    "research-plan-implement": {
        "required": [
            "## When to Use",
            "## Decide the Depth First",
            "## Procedure",
            "## Context Hygiene",
            "## Pitfalls",
            "## Verification",
            "Define success before exploring solutions",
            "Verify independently",
            "Assess and codify only durable learning",
        ],
        "references": [
            "references/research-template.md",
            "references/plan-template.md",
        ],
    },
}


class AgentEngineeringSkillTests(unittest.TestCase):
    def test_skill_structure_and_references(self) -> None:
        for name, expectations in SKILLS.items():
            skill_dir = ROOT / "skills" / name
            content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

            self.assertTrue(content.startswith("---\n"), name)
            self.assertIn("\n---\n", content, name)
            frontmatter = content.split("---\n", 2)[1]
            metadata = dict(line.split(": ", 1) for line in frontmatter.strip().splitlines())
            self.assertEqual(metadata["name"], name)
            self.assertTrue(metadata["description"].endswith("."), name)
            self.assertLessEqual(len(metadata["description"]), 60, name)
            self.assertIn("allowed-tools", metadata, name)
            self.assertNotIn("/Users/", content, name)
            self.assertNotIn("/tmp/", content, name)
            for section in expectations["required"]:
                self.assertIn(section, content, f"{name}: {section}")
            for reference in expectations["references"]:
                self.assertTrue((skill_dir / reference).is_file(), f"{name}: {reference}")

    def test_marketplace_registers_both_skills(self) -> None:
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        plugin_list = marketplace["plugins"]
        plugins = {plugin["name"]: plugin for plugin in plugin_list}

        self.assertRegex(marketplace["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(len(plugins), len(plugin_list), "plugin names must be unique")
        for name in SKILLS:
            self.assertIn(name, plugins)
            source = ROOT / plugins[name]["source"].removeprefix("./")
            self.assertTrue((source / "SKILL.md").is_file(), name)

    def test_readme_lists_new_skills(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        self.assertIn(f"## Skills ({len(marketplace['plugins'])} total)", readme)
        for name in SKILLS:
            self.assertIn(f"claude plugin install {name}@thrashr888-agent-kit", readme)
            self.assertIn(f"**{name}**", readme)

    def test_style_docs_keeps_intent_rule(self) -> None:
        content = (ROOT / "skills" / "style-docs" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Agent-Ready Documentation", content)
        self.assertIn("Document intent, constraints, and rationale", content)


if __name__ == "__main__":
    unittest.main()
