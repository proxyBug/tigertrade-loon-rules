#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从根目录源文件生成各客户端格式的规则文件。

源文件 (手动维护):
  TigerTrade.list  — 老虎证券 (Tiger Trade)
  Moomoo.list      — 富途证券 / Moomoo

生成文件:
  rule/*/TigerTrade.*    — 老虎证券各客户端格式
  rule/*/Moomoo.*        — 富途 / Moomoo 各客户端格式
  TigerMoomoo.list       — 合并 Loon 格式 (根目录)
  rule/*/TigerMoomoo.*   — 合并各客户端格式

用法: python3 scripts/generate.py
"""
import datetime
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/proxyBug/tigertrade-loon-rules"

TIGER_DESC = "老虎证券 / 老虎国际 (Tiger Trade) 代理分流规则合集"
MOOMOO_DESC = "富途证券 / Moomoo 代理分流规则合集"
COMBINED_DESC = "老虎证券 (Tiger Trade) + 富途证券 (Moomoo) 代理分流规则合集"


def parse_source(relpath):
    suffixes, keywords = set(), set()
    path = os.path.join(ROOT, relpath)
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rtype, _, value = line.partition(",")
            value = value.strip()
            if rtype == "DOMAIN-SUFFIX":
                suffixes.add(value)
            elif rtype == "DOMAIN-KEYWORD":
                keywords.add(value)
    return sorted(suffixes), sorted(keywords)


def _header(name, desc, target, suffixes, keywords, extra=()):
    today = datetime.date.today().isoformat()
    lines = [
        "# NAME: " + name,
        "# DESC: " + desc,
        "# AUTHOR: proxyBug",
        "# REPO: " + REPO,
        "# TARGET: " + target,
        "# UPDATED: " + today,
        "# DOMAIN-SUFFIX: %d" % len(suffixes),
        "# DOMAIN-KEYWORD: %d" % len(keywords),
        "# TOTAL: %d" % (len(suffixes) + len(keywords)),
    ]
    lines.extend(extra)
    return "\n".join(lines) + "\n\n"


def write(relpath, content):
    path = os.path.join(ROOT, relpath)
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("generated", relpath)


def generate_all_formats(name, desc, suffixes, keywords):
    """Write rule files for all proxy client formats."""

    # Surge / Shadowrocket — plain RULE-SET list
    body = "".join("DOMAIN-SUFFIX,%s\n" % d for d in suffixes)
    body += "".join("DOMAIN-KEYWORD,%s\n" % k for k in keywords)
    write("rule/Surge/%s.list" % name,
          _header(name, desc, "Surge", suffixes, keywords) + body)
    write("rule/Shadowrocket/%s.list" % name,
          _header(name, desc, "Shadowrocket", suffixes, keywords) + body)

    # Quantumult X — filter_remote format
    qx = "".join("HOST-SUFFIX,%s,%s\n" % (d, name) for d in suffixes)
    qx += "".join("HOST-KEYWORD,%s,%s\n" % (k, name) for k in keywords)
    extra = ("# 订阅时建议使用 force-policy=你的策略 覆盖默认策略名",)
    write("rule/QuantumultX/%s.list" % name,
          _header(name, desc, "Quantumult X", suffixes, keywords, extra) + qx)

    # Clash / mihomo — classical rule-provider (YAML)
    clash = _header(name, desc,
                    "Clash(mihomo) rule-provider, behavior: classical",
                    suffixes, keywords)
    clash += "payload:\n"
    clash += "".join("  - DOMAIN-SUFFIX,%s\n" % d for d in suffixes)
    clash += "".join("  - DOMAIN-KEYWORD,%s\n" % k for k in keywords)
    write("rule/Clash/%s.yaml" % name, clash)

    # sing-box — source format rule-set (JSON)
    sb = {
        "version": 2,
        "rules": [{"domain_suffix": list(suffixes), "domain_keyword": list(keywords)}],
    }
    write("rule/sing-box/%s.json" % name, json.dumps(sb, indent=2) + "\n")


def generate_loon_root(name, desc, suffixes, keywords):
    """Write a generated Loon-format root file (TigerMoomoo.list)."""
    today = datetime.date.today().isoformat()
    lines = [
        "# NAME: " + name,
        "# DESC: " + desc,
        "# AUTHOR: proxyBug",
        "# REPO: " + REPO,
        "# UPDATED: " + today,
        "# DOMAIN-SUFFIX: %d" % len(suffixes),
        "# DOMAIN-KEYWORD: %d" % len(keywords),
        "# TOTAL: %d" % (len(suffixes) + len(keywords)),
        "# 适用于 Loon 远程规则 (Remote Rule) 订阅,策略组在订阅时自行指定",
        "# 此文件由 scripts/generate.py 自动生成,请勿手动编辑",
        "",
    ]
    for d in suffixes:
        lines.append("DOMAIN-SUFFIX," + d)
    for k in keywords:
        lines.append("DOMAIN-KEYWORD," + k)
    write(name + ".list", "\n".join(lines) + "\n")


def main():
    tiger_s, tiger_k = parse_source("TigerTrade.list")
    moomoo_s, moomoo_k = parse_source("Moomoo.list")

    # Per-app rule files
    generate_all_formats("TigerTrade", TIGER_DESC, tiger_s, tiger_k)
    generate_all_formats("Moomoo", MOOMOO_DESC, moomoo_s, moomoo_k)

    # Combined Tiger + Moomoo
    combined_s = sorted(set(tiger_s) | set(moomoo_s))
    combined_k = sorted(set(tiger_k) | set(moomoo_k))
    generate_all_formats("TigerMoomoo", COMBINED_DESC, combined_s, combined_k)
    generate_loon_root("TigerMoomoo", COMBINED_DESC, combined_s, combined_k)

    print("\nDone. Source files (TigerTrade.list, Moomoo.list) were not modified.")


if __name__ == "__main__":
    main()
