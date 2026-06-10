#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从根目录 TigerTrade.list (Loon 格式,源文件) 生成其他客户端的规则文件。

用法: python3 scripts/generate.py
新增/删除域名只需修改根目录 TigerTrade.list,然后运行本脚本同步所有格式。
"""
import datetime
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "TigerTrade.list")
REPO = "https://github.com/proxyBug/tigertrade-loon-rules"


def parse_source():
    suffixes, keywords = set(), set()
    with io.open(SOURCE, encoding="utf-8") as f:
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


def header(target, suffixes, keywords, extra=()):
    today = datetime.date.today().isoformat()
    lines = [
        "# NAME: TigerTrade",
        "# DESC: 老虎证券 / 老虎国际 (Tiger Trade) 代理分流规则合集",
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
    print("generated %s" % relpath)


def main():
    suffixes, keywords = parse_source()

    # Surge / Shadowrocket: 与 Loon 同为 RULE-SET 纯列表格式
    body = "".join("DOMAIN-SUFFIX,%s\n" % d for d in suffixes)
    body += "".join("DOMAIN-KEYWORD,%s\n" % k for k in keywords)
    write("rule/Surge/TigerTrade.list", header("Surge", suffixes, keywords) + body)
    write("rule/Shadowrocket/TigerTrade.list", header("Shadowrocket", suffixes, keywords) + body)

    # Quantumult X: filter_remote 格式,策略名占位 TigerTrade,订阅时用 force-policy 覆盖
    qx = "".join("HOST-SUFFIX,%s,TigerTrade\n" % d for d in suffixes)
    qx += "".join("HOST-KEYWORD,%s,TigerTrade\n" % k for k in keywords)
    extra = ("# 订阅时建议使用 force-policy=你的策略 覆盖默认策略名",)
    write("rule/QuantumultX/TigerTrade.list", header("Quantumult X", suffixes, keywords, extra) + qx)

    # Clash / mihomo: classical rule-provider (YAML)
    clash = header("Clash(mihomo) rule-provider, behavior: classical", suffixes, keywords)
    clash += "payload:\n"
    clash += "".join("  - DOMAIN-SUFFIX,%s\n" % d for d in suffixes)
    clash += "".join("  - DOMAIN-KEYWORD,%s\n" % k for k in keywords)
    write("rule/Clash/TigerTrade.yaml", clash)

    # sing-box: source 格式 rule-set (JSON 不支持注释)
    sb = {
        "version": 2,
        "rules": [{"domain_suffix": suffixes, "domain_keyword": keywords}],
    }
    write("rule/sing-box/TigerTrade.json", json.dumps(sb, indent=2) + "\n")


if __name__ == "__main__":
    main()
