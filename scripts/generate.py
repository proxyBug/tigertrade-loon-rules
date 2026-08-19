#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all client rule formats from the two root Loon sources.

Manually maintained sources:
  TigerTrade.list
  Moomoo.list

Usage:
  python3 scripts/generate.py
  python3 scripts/generate.py --check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/proxyBug/tigertrade-moomoo-rules"

TIGER_DESC = "老虎证券 / 老虎国际 (Tiger Trade) 代理分流规则合集"
MOOMOO_DESC = "富途证券 / Moomoo 代理分流规则合集"
COMBINED_DESC = "老虎证券 (Tiger Trade) + 富途证券 (Moomoo) 代理分流规则合集"
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)
KEYWORD_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")


@dataclass(frozen=True)
class SourceRules:
    updated: str
    suffixes: tuple[str, ...]
    keywords: tuple[str, ...]


def parse_source(relpath: str) -> SourceRules:
    path = ROOT / relpath
    updated: str | None = None
    suffixes: list[str] = []
    keywords: list[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("# UPDATED:"):
            updated = line.partition(":")[2].strip()
            continue
        if not line or line.startswith("#"):
            continue

        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 2:
            raise ValueError(
                f"{relpath}: rule must contain exactly two comma-separated fields: "
                f"{raw_line}"
            )
        rule_type, value = parts
        if not value:
            raise ValueError(f"{relpath}: rule value cannot be empty: {raw_line}")
        if value != value.lower():
            raise ValueError(f"{relpath}: rule values must be lowercase: {raw_line}")
        if rule_type == "DOMAIN-SUFFIX":
            if not DOMAIN_RE.fullmatch(value):
                raise ValueError(f"{relpath}: invalid domain suffix: {value}")
            suffixes.append(value)
        elif rule_type == "DOMAIN-KEYWORD":
            if not KEYWORD_RE.fullmatch(value):
                raise ValueError(f"{relpath}: invalid domain keyword: {value}")
            keywords.append(value)
        else:
            raise ValueError(f"Unsupported rule type in {relpath}: {rule_type}")

    if updated is None:
        raise ValueError(f"Missing # UPDATED metadata in {relpath}")
    if len(suffixes) != len(set(suffixes)):
        raise ValueError(f"Duplicate DOMAIN-SUFFIX rule in {relpath}")
    if len(keywords) != len(set(keywords)):
        raise ValueError(f"Duplicate DOMAIN-KEYWORD rule in {relpath}")

    return SourceRules(
        updated=updated,
        suffixes=tuple(sorted(suffixes)),
        keywords=tuple(sorted(keywords)),
    )


def render_header(
    name: str,
    description: str,
    target: str,
    updated: str,
    suffixes: tuple[str, ...],
    keywords: tuple[str, ...],
    extra: tuple[str, ...] = (),
) -> str:
    lines = [
        f"# NAME: {name}",
        f"# DESC: {description}",
        "# AUTHOR: proxyBug",
        f"# REPO: {REPO}",
        f"# TARGET: {target}",
        f"# UPDATED: {updated}",
        f"# DOMAIN-SUFFIX: {len(suffixes)}",
        f"# DOMAIN-KEYWORD: {len(keywords)}",
        f"# TOTAL: {len(suffixes) + len(keywords)}",
    ]
    lines.extend(extra)
    return "\n".join(lines) + "\n\n"


def render_client_formats(
    name: str,
    description: str,
    rules: SourceRules,
) -> dict[str, str]:
    outputs: dict[str, str] = {}

    plain_body = "".join(f"DOMAIN-SUFFIX,{domain}\n" for domain in rules.suffixes)
    plain_body += "".join(f"DOMAIN-KEYWORD,{keyword}\n" for keyword in rules.keywords)
    for client in ("Surge", "Shadowrocket"):
        outputs[f"rule/{client}/{name}.list"] = (
            render_header(
                name,
                description,
                client,
                rules.updated,
                rules.suffixes,
                rules.keywords,
            )
            + plain_body
        )

    qx_body = "".join(
        f"HOST-SUFFIX,{domain},{name}\n" for domain in rules.suffixes
    )
    qx_body += "".join(
        f"HOST-KEYWORD,{keyword},{name}\n" for keyword in rules.keywords
    )
    outputs[f"rule/QuantumultX/{name}.list"] = (
        render_header(
            name,
            description,
            "Quantumult X",
            rules.updated,
            rules.suffixes,
            rules.keywords,
            ("# 订阅时建议使用 force-policy=你的策略 覆盖默认策略名",),
        )
        + qx_body
    )

    clash = render_header(
        name,
        description,
        "Clash(mihomo) rule-provider, behavior: classical",
        rules.updated,
        rules.suffixes,
        rules.keywords,
    )
    clash += "payload:\n"
    clash += "".join(f"  - DOMAIN-SUFFIX,{domain}\n" for domain in rules.suffixes)
    clash += "".join(f"  - DOMAIN-KEYWORD,{keyword}\n" for keyword in rules.keywords)
    outputs[f"rule/Clash/{name}.yaml"] = clash

    sing_box = {
        "version": 2,
        "rules": [
            {
                "domain_suffix": list(rules.suffixes),
                "domain_keyword": list(rules.keywords),
            }
        ],
    }
    outputs[f"rule/sing-box/{name}.json"] = json.dumps(sing_box, indent=2) + "\n"
    return outputs


def render_combined_loon(name: str, description: str, rules: SourceRules) -> str:
    lines = [
        f"# NAME: {name}",
        f"# DESC: {description}",
        "# AUTHOR: proxyBug",
        f"# REPO: {REPO}",
        f"# UPDATED: {rules.updated}",
        f"# DOMAIN-SUFFIX: {len(rules.suffixes)}",
        f"# DOMAIN-KEYWORD: {len(rules.keywords)}",
        f"# TOTAL: {len(rules.suffixes) + len(rules.keywords)}",
        "# 适用于 Loon 远程规则 (Remote Rule) 订阅,策略组在订阅时自行指定",
        "# 此文件由 scripts/generate.py 自动生成,请勿手动编辑",
        "",
    ]
    lines.extend(f"DOMAIN-SUFFIX,{domain}" for domain in rules.suffixes)
    lines.extend(f"DOMAIN-KEYWORD,{keyword}" for keyword in rules.keywords)
    return "\n".join(lines) + "\n"


def build_outputs() -> dict[str, str]:
    tiger = parse_source("TigerTrade.list")
    moomoo = parse_source("Moomoo.list")
    combined = SourceRules(
        updated=max(tiger.updated, moomoo.updated),
        suffixes=tuple(sorted(set(tiger.suffixes) | set(moomoo.suffixes))),
        keywords=tuple(sorted(set(tiger.keywords) | set(moomoo.keywords))),
    )

    outputs: dict[str, str] = {}
    outputs.update(render_client_formats("TigerTrade", TIGER_DESC, tiger))
    outputs.update(render_client_formats("Moomoo", MOOMOO_DESC, moomoo))
    outputs.update(render_client_formats("TigerMoomoo", COMBINED_DESC, combined))
    outputs["TigerMoomoo.list"] = render_combined_loon(
        "TigerMoomoo", COMBINED_DESC, combined
    )
    return outputs


def apply_outputs(outputs: dict[str, str], check: bool) -> int:
    stale: list[str] = []
    for relpath, content in sorted(outputs.items()):
        path = ROOT / relpath
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        if check:
            stale.append(relpath)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"generated {relpath}")

    if check and stale:
        print("Generated files are stale:")
        for relpath in stale:
            print(f"  {relpath}")
        print("Run: python3 scripts/generate.py")
        return 1
    if check:
        print("All generated files are up to date.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report stale generated files without rewriting them",
    )
    args = parser.parse_args()
    try:
        outputs = build_outputs()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return apply_outputs(outputs, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
