from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)

TIGER_REQUIRED = {
    "etasphere.com",
    "ftfast.com",
    "gotigerhk.com",
    "iotaskyt.com",
    "iotaskyty.com",
    "itiger-nz.com",
    "itigertrader.com",
    "play-analytics.com",
    "thetigerbrokers.com",
    "tigeresop.com",
    "tigeresop.com.sg",
    "tigerhkgo.com",
    "tigertrader.app",
    "tigr.link",
    "tigrgood.com",
}

HELD_TIGER_DOMAINS = {"tbdesk.com", "tigerbrokers.net", "tigertcp.cn"}

MOOMOO_REQUIRED = {
    "futu.cn",
    "futu.link",
    "futu5.com",
    "futuau.com",
    "futuesop.com",
    "futufin.com",
    "futuhk.com",
    "futuhk1.com",
    "futuhk2.com",
    "futuhkapp.com",
    "futuhn.com",
    "futuholdings.com",
    "futuniuniu.com",
    "futunn.com",
    "futuoa.com",
    "futusg.com",
    "futustatic.com",
    "fututrade.com",
    "fututrustee.com",
    "moomoo.com",
    "moomoo.ca",
    "moomoobull.com",
    "moomooequity.com",
    "moomootrustee.com",
}

REJECTED_DOMAINS = {"futu.inc", "nniuvip.com"}


def parse_header(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^# ([A-Z-]+):\s*(.+)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def parse_loon_source(path: Path) -> tuple[dict[str, str], set[str], set[str]]:
    text = path.read_text(encoding="utf-8")
    suffixes: list[str] = []
    keywords: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        kind, separator, value = line.partition(",")
        if not separator or not value:
            raise AssertionError(f"Malformed rule in {path}: {line}")
        if kind == "DOMAIN-SUFFIX":
            suffixes.append(value)
        elif kind == "DOMAIN-KEYWORD":
            keywords.append(value)
        else:
            raise AssertionError(f"Unsupported rule in {path}: {line}")
    if len(suffixes) != len(set(suffixes)):
        raise AssertionError(f"Duplicate DOMAIN-SUFFIX rule in {path}")
    if len(keywords) != len(set(keywords)):
        raise AssertionError(f"Duplicate DOMAIN-KEYWORD rule in {path}")
    return parse_header(text), set(suffixes), set(keywords)


def parse_plain_generated(path: Path) -> tuple[set[str], set[str]]:
    suffixes: set[str] = set()
    keywords: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- "):
            line = line[2:]
        if line.startswith("DOMAIN-SUFFIX,"):
            suffixes.add(line.split(",", 1)[1])
        elif line.startswith("DOMAIN-KEYWORD,"):
            keywords.add(line.split(",", 1)[1])
    return suffixes, keywords


def parse_qx(path: Path) -> tuple[set[str], set[str]]:
    suffixes: set[str] = set()
    keywords: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("HOST-SUFFIX,"):
            suffixes.add(line.split(",", 2)[1])
        elif line.startswith("HOST-KEYWORD,"):
            keywords.add(line.split(",", 2)[1])
    return suffixes, keywords


def parse_sing_box(path: Path) -> tuple[set[str], set[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rules = payload["rules"]
    if len(rules) != 1:
        raise AssertionError(f"Expected one sing-box rule object in {path}")
    return set(rules[0]["domain_suffix"]), set(rules[0]["domain_keyword"])


class RuleRepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tiger_header, cls.tiger_suffixes, cls.tiger_keywords = parse_loon_source(
            ROOT / "TigerTrade.list"
        )
        cls.moomoo_header, cls.moomoo_suffixes, cls.moomoo_keywords = parse_loon_source(
            ROOT / "Moomoo.list"
        )

    def test_source_rules_are_normalized_and_headers_match(self) -> None:
        for name, header, suffixes, keywords in (
            ("TigerTrade", self.tiger_header, self.tiger_suffixes, self.tiger_keywords),
            ("Moomoo", self.moomoo_header, self.moomoo_suffixes, self.moomoo_keywords),
        ):
            self.assertEqual(int(header["DOMAIN-SUFFIX"]), len(suffixes), name)
            self.assertEqual(int(header["DOMAIN-KEYWORD"]), len(keywords), name)
            self.assertEqual(int(header["TOTAL"]), len(suffixes) + len(keywords), name)
            for domain in suffixes:
                self.assertEqual(domain, domain.lower(), domain)
                self.assertRegex(domain, DOMAIN_RE)
            for keyword in keywords:
                self.assertEqual(keyword, keyword.lower(), keyword)
                self.assertNotIn(".", keyword, keyword)

    def test_high_confidence_domain_coverage(self) -> None:
        self.assertTrue(TIGER_REQUIRED <= self.tiger_suffixes)
        self.assertFalse(HELD_TIGER_DOMAINS & self.tiger_suffixes)
        self.assertTrue(MOOMOO_REQUIRED <= self.moomoo_suffixes)
        self.assertFalse(REJECTED_DOMAINS & self.moomoo_suffixes)

    def test_tiger_runtime_evidence_drives_inclusion_and_exclusion(self) -> None:
        evidence_path = ROOT / "evidence/tiger-runtime-2026-08-20.json"
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["source_url"], "https://up.play-analytics.com/")
        self.assertRegex(
            evidence["semantic_occurrences_sha256"], r"^[0-9a-f]{64}$"
        )
        self.assertNotIn("source_sha256", evidence)

        included = {row["root_domain"] for row in evidence["included_first_party"]}
        held = {row["root_domain"] for row in evidence["held_or_removed"]}
        excluded = {row["root_domain"] for row in evidence["excluded_third_party"]}

        self.assertTrue(included <= self.tiger_suffixes)
        self.assertFalse((held | excluded) & self.tiger_suffixes)

        for group in ("included_first_party", "excluded_third_party"):
            for row in evidence[group]:
                self.assertTrue(row["field_paths"], row["root_domain"])
                for field_path in row["field_paths"]:
                    self.assertTrue(field_path.startswith("root.items[0]."), field_path)

        def covered(hostname: str) -> bool:
            return any(
                hostname == suffix or hostname.endswith("." + suffix)
                for suffix in self.tiger_suffixes
            )

        for row in evidence["included_first_party"]:
            for hostname in row["runtime_hosts"]:
                with self.subTest(hostname=hostname, decision="include"):
                    self.assertTrue(covered(hostname))
        for row in evidence["excluded_third_party"]:
            for hostname in row["runtime_hosts"]:
                with self.subTest(hostname=hostname, decision="exclude"):
                    self.assertFalse(covered(hostname))

    def test_rules_use_explicit_suffixes_without_keyword_false_positives(self) -> None:
        self.assertEqual(self.tiger_keywords, set())
        self.assertEqual(self.moomoo_keywords, set())

        combined_suffixes = self.tiger_suffixes | self.moomoo_suffixes
        combined_keywords = self.tiger_keywords | self.moomoo_keywords

        def matches(hostname: str) -> bool:
            return any(
                hostname == suffix or hostname.endswith("." + suffix)
                for suffix in combined_suffixes
            ) or any(keyword in hostname for keyword in combined_keywords)

        for unrelated in (
            "moomooi.com",
            "futunneling.example",
            "tigerbrokers-fan.example",
        ):
            with self.subTest(hostname=unrelated):
                self.assertFalse(matches(unrelated))

    def test_every_generated_format_matches_its_source(self) -> None:
        expected = {
            "TigerTrade": (self.tiger_suffixes, self.tiger_keywords),
            "Moomoo": (self.moomoo_suffixes, self.moomoo_keywords),
            "TigerMoomoo": (
                self.tiger_suffixes | self.moomoo_suffixes,
                self.tiger_keywords | self.moomoo_keywords,
            ),
        }
        for name, values in expected.items():
            with self.subTest(name=name, format="root-or-surge"):
                path = ROOT / (f"{name}.list" if name == "TigerMoomoo" else f"rule/Surge/{name}.list")
                self.assertEqual(parse_plain_generated(path), values)
            with self.subTest(name=name, format="shadowrocket"):
                self.assertEqual(parse_plain_generated(ROOT / f"rule/Shadowrocket/{name}.list"), values)
            with self.subTest(name=name, format="clash"):
                self.assertEqual(parse_plain_generated(ROOT / f"rule/Clash/{name}.yaml"), values)
            with self.subTest(name=name, format="quantumult-x"):
                self.assertEqual(parse_qx(ROOT / f"rule/QuantumultX/{name}.list"), values)
            with self.subTest(name=name, format="sing-box"):
                self.assertEqual(parse_sing_box(ROOT / f"rule/sing-box/{name}.json"), values)

    def test_generated_dates_come_from_source_metadata(self) -> None:
        expected_dates = {
            "TigerTrade": self.tiger_header["UPDATED"],
            "Moomoo": self.moomoo_header["UPDATED"],
            "TigerMoomoo": max(
                self.tiger_header["UPDATED"], self.moomoo_header["UPDATED"]
            ),
        }
        for name, expected_date in expected_dates.items():
            paths = [
                ROOT / f"rule/Surge/{name}.list",
                ROOT / f"rule/Shadowrocket/{name}.list",
                ROOT / f"rule/QuantumultX/{name}.list",
                ROOT / f"rule/Clash/{name}.yaml",
            ]
            if name == "TigerMoomoo":
                paths.append(ROOT / "TigerMoomoo.list")
            for path in paths:
                with self.subTest(path=path):
                    self.assertEqual(parse_header(path.read_text(encoding="utf-8"))["UPDATED"], expected_date)

    def test_readme_raw_links_resolve_to_tracked_files(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        prefix = "https://raw.githubusercontent.com/proxyBug/tigertrade-moomoo-rules/main/"
        targets = {
            match
            for match in re.findall(
                re.escape(prefix) + r"([A-Za-z0-9._/-]+)", text
            )
        }
        self.assertGreaterEqual(len(targets), 18)
        for target in targets:
            with self.subTest(target=target):
                self.assertTrue((ROOT / target).is_file(), target)

    def test_repository_identity_uses_new_name_without_old_slug(self) -> None:
        old_slug = "tigertrade-" + "loon-rules"
        new_slug = "tigertrade-moomoo-rules"
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        inspected = 0
        for relative in tracked:
            path = ROOT / relative
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            inspected += 1
            if relative == "CHANGELOG.md":
                self.assertEqual(text.count(old_slug), 1)
                continue
            with self.subTest(path=relative):
                self.assertNotIn(old_slug, text)
        self.assertGreater(inspected, 20)
        self.assertIn(
            f"https://github.com/proxyBug/{new_slug}",
            (ROOT / "TigerTrade.list").read_text(encoding="utf-8"),
        )

    def test_readme_comparison_matches_pinned_community_evidence(self) -> None:
        comparison = json.loads(
            (ROOT / "evidence/community-comparison-2026-08-20.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(comparison["tiger"]["repository_count"], len(self.tiger_suffixes))
        self.assertEqual(comparison["moomoo"]["repository_count"], len(self.moomoo_suffixes))

        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("12 项测试", text)
        tiger = comparison["tiger"]
        moomoo = comparison["moomoo"]
        self.assertIn(
            f'| 显式后缀规则数 | **{tiger["repository_count"]}** | '
            f'{tiger["blackmatrix"]["count"]} | {tiger["v2fly"]["count"]} |',
            text,
        )
        self.assertIn(
            f'| 显式后缀规则数 | **{moomoo["repository_count"]}** | '
            f'{moomoo["v2fly"]["count"]} |',
            text,
        )
        self.assertEqual(tiger["v2fly"]["missing_from_repository"], [])
        self.assertEqual(moomoo["v2fly"]["missing_from_repository"], [])

    def test_generator_check_mode_detects_drift_without_rewriting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            clone = Path(temporary) / "repo"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            target = clone / "rule/Surge/TigerTrade.list"
            drifted = target.read_text(encoding="utf-8") + "# deliberate drift\n"
            target.write_text(drifted, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/generate.py", "--check"],
                cwd=clone,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), drifted)

    def test_generator_rejects_malformed_source_rules(self) -> None:
        cases = {
            "DOMAIN-SUFFIX,example.com,EXTRA": "exactly two comma-separated fields",
            "DOMAIN-SUFFIX,Example.com": "lowercase",
        }
        for bad_rule, expected_error in cases.items():
            with self.subTest(rule=bad_rule), tempfile.TemporaryDirectory() as temporary:
                clone = Path(temporary) / "repo"
                shutil.copytree(
                    ROOT,
                    clone,
                    ignore=shutil.ignore_patterns(".git", "__pycache__"),
                )
                source = clone / "Moomoo.list"
                source.write_text(
                    source.read_text(encoding="utf-8") + bad_rule + "\n",
                    encoding="utf-8",
                )
                result = subprocess.run(
                    [sys.executable, "scripts/generate.py"],
                    cwd=clone,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                output = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0, output)
                self.assertIn(expected_error, output)

    def test_ci_runs_repository_validation(self) -> None:
        workflow = ROOT / ".github/workflows/validate.yml"
        self.assertTrue(workflow.is_file())
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("python3 -m unittest", text)
        self.assertIn("scripts/generate.py --check", text)


if __name__ == "__main__":
    unittest.main()
