# Tiger Trade & Moomoo — Proxy Rule Sets
## 老虎证券 + 富途证券 代理分流规则集

> **English** | [中文说明见下方 ↓](#中文说明)

This repository provides **comprehensive, verified proxy rule sets** for two of the most widely used overseas brokerage platforms among Chinese-speaking investors: **Tiger Trade (老虎证券)** and **Moomoo / Futu NiuNiu (富途证券 / 富途牛牛)**. Both standalone subscriptions and a combined subscription are available, covering six proxy client formats.

---

## Background

Since late 2024, Chinese regulators have substantially tightened enforcement against overseas brokerage platforms that solicit mainland China clients. The result is widespread blocking by the Great Firewall — not only of official websites, but of every API endpoint the trading apps depend on. This creates a critical but commonly overlooked problem:

> **Proxying only the primary domain is not enough.**

Modern trading apps issue dozens of concurrent API requests across a range of hostnames — including obfuscated CDN and acceleration domains whose names give no obvious hint of their affiliation. Routing only `tigertrade.com` or `moomoo.com` through a proxy leaves market data feeds, order execution APIs, authentication servers, and real-time price streams on the wrong network path. The result: the app appears configured for proxy yet still fails to connect, or connects intermittently with stale data.

This repository exists to solve that problem. Every domain listed here has been traced back to its owning platform through WHOIS records, TLS certificates, or app traffic captures — not guesswork. The rule sets are intentionally more complete than what mainstream community repos carry, specifically targeting the hidden CDN and API endpoints that cause "configured but still broken" failures.

---

## 中文说明

2024 年底以来，中国监管机构大幅加强了对向境内客户招揽业务的境外券商平台的执法力度，导致防火长城对大量投资相关域名实施了封锁——不仅限于官方网站，还包括交易 App 所依赖的全部 API 接口。这带来了一个关键但常被忽视的问题：

> **仅代理主域名是不够的。**

现代交易 App 会同时向数十个不同主机名发起 API 请求，其中包含大量经过混淆命名的 CDN 和加速域名，从名称上完全看不出与券商的关联。只代理 `tigertrade.com` 或 `moomoo.com`，会导致行情数据、委托下单接口、登录认证、实时报价等服务走错线路。结果就是：App 看起来"已配置代理"，但仍然无法连接，或连接不稳定、数据陈旧。

本仓库正是为解决这个问题而建立的。所有收录的域名均通过 WHOIS 记录、TLS 证书或 App 抓包溯源到对应的券商平台，有据可查。规则集比主流社区仓库更为完整，专门针对导致"配置了却还是坏"的隐藏 CDN 和 API 节点。

---

## 📊 Tiger Trade — Rule Coverage

**26 rules** — a complete superset of [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) (8 rules) and [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) (4 rules), with exclusive coverage of obfuscated CDN domains (`skytigris.*` / `atigr*` / `tigr*` series) that are the root cause of the "configured but still broken" issue.

| Coverage | This repo | blackmatrix7<br>(TigerFintech) | v2fly<br>(itiger) |
| --- | :---: | :---: | :---: |
| Rule count | **26** | 8 | 4 |
| Core App API (itiger.com / tigerfintech.com) | ✅ | ✅ | ⚠️ missing tigerfintech |
| US App API (itigerup.com) | ✅ | ❌ | ✅ |
| Obfuscated CDN (skytigris / atigr\* / tigr\* — 8 domains) | ✅ | ❌ | ⚠️ 2 of 8 only |
| Regional sites (sg / au / hk / nz) | ✅ | ❌ | ❌ |
| US entities (TradeUP / Tiger Securities) | ✅ | ❌ | ❌ |
| Tiger Community (laohu8 / tigerbbs / xiaohu8) | ✅ | ✅ | ❌ |
| TigerGPT (ttm.financial) | ✅ | ❌ | ❌ |
| Keyword fallback (auto-covers future regional sites) | ✅ | ❌ | ❌ |

> Comparison based on both repos' June 2026 versions. This repo is a complete superset of all domains in both.

## 📊 Moomoo — Rule Coverage

**9 rules** covering all verified Moomoo / Futu NiuNiu endpoints, including the keyword fallbacks that catch current and future regional domains (`.com.au`, `.ca`, `.my`, `.jp`, etc.).

| Coverage | This repo | blackmatrix7<br>(Moomoo) | v2fly |
| --- | :---: | :---: | :---: |
| Rule count | **9** | ~3 | ❌ |
| Core App API (moomoo.com / futunn.com) | ✅ | ✅ | ❌ |
| Corporate site (futu.inc) | ✅ | ✅ | ❌ |
| Regional offices (futuhk.com / futusg.com) | ✅ | ❌ | ❌ |
| Market data API (futu5.com) | ✅ | ❌ | ❌ |
| VIP service domain (nniuvip.com) | ✅ | ❌ | ❌ |
| Keyword fallback (moomoo.\* / futunn.\*) | ✅ | ❌ | ❌ |

---

## 📦 Subscription URLs

Three rule sets are available — use whichever matches your brokerage(s):

| Client | Tiger Trade only | Moomoo only | Tiger + Moomoo (combined) |
| --- | --- | --- | --- |
| **Loon** | [`TigerTrade.list`][lt] | [`Moomoo.list`][lm] | [`TigerMoomoo.list`][lc] |
| Surge | [`rule/Surge/TigerTrade.list`][st] | [`rule/Surge/Moomoo.list`][sm] | [`rule/Surge/TigerMoomoo.list`][sc] |
| Shadowrocket | [`rule/Shadowrocket/TigerTrade.list`][rt] | [`rule/Shadowrocket/Moomoo.list`][rm] | [`rule/Shadowrocket/TigerMoomoo.list`][rc] |
| Clash / mihomo | [`rule/Clash/TigerTrade.yaml`][ct] | [`rule/Clash/Moomoo.yaml`][cm] | [`rule/Clash/TigerMoomoo.yaml`][cc] |
| Quantumult X | [`rule/QuantumultX/TigerTrade.list`][qt] | [`rule/QuantumultX/Moomoo.list`][qm] | [`rule/QuantumultX/TigerMoomoo.list`][qc] |
| sing-box | [`rule/sing-box/TigerTrade.json`][bt] | [`rule/sing-box/Moomoo.json`][bm] | [`rule/sing-box/TigerMoomoo.json`][bc] |

[lt]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerTrade.list
[lm]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/Moomoo.list
[lc]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerMoomoo.list
[st]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerTrade.list
[sm]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/Moomoo.list
[sc]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerMoomoo.list
[rt]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerTrade.list
[rm]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/Moomoo.list
[rc]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerMoomoo.list
[ct]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/TigerTrade.yaml
[cm]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/Moomoo.yaml
[cc]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/TigerMoomoo.yaml
[qt]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerTrade.list
[qm]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/Moomoo.list
[qc]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerMoomoo.list
[bt]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/TigerTrade.json
[bm]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/Moomoo.json
[bc]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/TigerMoomoo.json

> Loon source files (root `TigerTrade.list` and `Moomoo.list`) are manually maintained; all other formats are generated from them. `TigerMoomoo.list` is auto-generated and should not be edited directly.

---

## 🏆 Loon (Recommended)

**In-app**: Configuration → Rules → Remote Rules → **+** (top right) → paste URL → set policy → set tag → save → refresh.

**Config file** (replace `PROXY` with your policy group name):

```ini
# Tiger Trade only
[Remote Rule]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerTrade.list, policy=PROXY, tag=TigerTrade, enabled=true

# Moomoo only
[Remote Rule]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/Moomoo.list, policy=PROXY, tag=Moomoo, enabled=true

# Tiger Trade + Moomoo (combined)
[Remote Rule]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerMoomoo.list, policy=PROXY, tag=TigerMoomoo, enabled=true
```

## Surge

Replace `PROXY` with your policy group name; place the rule before `FINAL`.

```ini
[Rule]
# Tiger Trade only
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerTrade.list,PROXY

# Moomoo only
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/Moomoo.list,PROXY

# Tiger Trade + Moomoo (combined)
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerMoomoo.list,PROXY
```

## Shadowrocket

In-app: Settings → Rules → **+** → type `RULE-SET` → paste URL → policy `PROXY`.

Config file (same syntax as Surge):

```ini
[Rule]
# Tiger Trade only
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerTrade.list,PROXY

# Moomoo only
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/Moomoo.list,PROXY

# Tiger Trade + Moomoo (combined)
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerMoomoo.list,PROXY
```

## Clash / mihomo

```yaml
rule-providers:
  TigerTrade:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/TigerTrade.yaml
    path: ./ruleset/TigerTrade.yaml
    interval: 86400
  Moomoo:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/Moomoo.yaml
    path: ./ruleset/Moomoo.yaml
    interval: 86400
  # Or use the combined ruleset instead of the two above:
  TigerMoomoo:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/TigerMoomoo.yaml
    path: ./ruleset/TigerMoomoo.yaml
    interval: 86400

rules:
  - RULE-SET,TigerTrade,PROXY
  - RULE-SET,Moomoo,PROXY
  # Or with the combined set:
  # - RULE-SET,TigerMoomoo,PROXY
```

## Quantumult X

Replace `节点选择` with your policy group name; `force-policy` overrides the default in the rule file.

```ini
[filter_remote]
# Tiger Trade only
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerTrade.list, tag=TigerTrade, force-policy=节点选择, update-interval=86400, opt-parser=false, enabled=true

# Moomoo only
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/Moomoo.list, tag=Moomoo, force-policy=节点选择, update-interval=86400, opt-parser=false, enabled=true

# Tiger Trade + Moomoo (combined)
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerMoomoo.list, tag=TigerMoomoo, force-policy=节点选择, update-interval=86400, opt-parser=false, enabled=true
```

## sing-box

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "tigertrade",
        "format": "source",
        "url": "https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/TigerTrade.json",
        "update_interval": "24h"
      },
      {
        "type": "remote",
        "tag": "moomoo",
        "format": "source",
        "url": "https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/Moomoo.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      { "rule_set": "tigertrade", "outbound": "proxy" },
      { "rule_set": "moomoo", "outbound": "proxy" }
    ]
  }
}
```

Or with the combined rule set:

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "tiger-moomoo",
        "format": "source",
        "url": "https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/TigerMoomoo.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      { "rule_set": "tiger-moomoo", "outbound": "proxy" }
    ]
  }
}
```

---

## Rule Content Details

### Tiger Trade (26 rules)

| Type | Count | Notes |
| --- | :---: | --- |
| DOMAIN-SUFFIX | 25 | Core APIs, CDN/acceleration, regional sites, community |
| DOMAIN-KEYWORD | 1 | `tigerbrokers` — future-proofs against new regional domains |

Key domains:

- **Core App / API**: `itiger.com`, `itigerup.com`, `tigerfintech.com`
- **Obfuscated CDN / acceleration** (actual app traffic, often misleading names): `skytigris.cn`, `skytigris.com`, `itigergrowth.com`, `itigergrowtha.com`, `atigrzen.com`, `atigrpulse.com`, `tigrwd.com`, `tigrdw.com`
- **Regional official sites**: `tigerbrokers.com` (+ `.com.sg` / `.com.au` / `.com.hk` / `.nz`)
- **US entities**: `tigersecurities.com`, `tradeup.com`
- **Community / TigerGPT**: `laohu8.com`, `tigerbbs.com`, `tigerbbs.cn`, `xiaohu8.com`, `ttm.financial`

CDN domain attribution: `skytigris.cn` WHOIS registrant email is `@itiger.com`; `tigrwd.com` / `tigrdw.com` site title is *Tiger Fintech*; `atigrzen.com` site identity is *Tiger Brokers*; `itigergrowth(a).com` is listed in [v2fly's official itiger dataset](https://github.com/v2fly/domain-list-community/blob/master/data/itiger).

### Moomoo / Futu NiuNiu (9 rules)

| Type | Count | Notes |
| --- | :---: | --- |
| DOMAIN-SUFFIX | 7 | Platform, API, regional offices |
| DOMAIN-KEYWORD | 2 | `moomoo` + `futunn` — covers all regional variants |

Key domains:

- **Core App / API**: `moomoo.com` (US/global), `futunn.com` (HK/international 富途牛牛)
- **Corporate**: `futu.inc`
- **Regional offices**: `futuhk.com` (Hong Kong), `futusg.com` (Singapore)
- **Market data API**: `futu5.com` (Futu market data and trading interface)
- **VIP services**: `nniuvip.com` (NiuNiu VIP service platform)
- **Keyword fallback**: `moomoo` catches `moomoo.com.au`, `moomoo.ca`, `moomoo.my`, `moomoo.jp`, etc.; `futunn` catches `futunn.*` variants

### Tiger + Moomoo Combined (35 rules)

The union of both rule sets: 32 `DOMAIN-SUFFIX` + 3 `DOMAIN-KEYWORD`. Recommended for users of both platforms.

---

## 🔧 Maintenance

`TigerTrade.list` and `Moomoo.list` in the repository root are the only files that should be edited manually. After modifying either source file, run:

```bash
python3 scripts/generate.py
```

This regenerates all files under `rule/` and the combined `TigerMoomoo.list`, keeping every format in sync from a single source of truth.

---

## Notes

- All domains have been verified through WHOIS records, TLS certificate inspection, or app traffic capture. Core domains are cross-referenced with [v2fly](https://github.com/v2fly/domain-list-community) and [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) community rules (credited with thanks).
- All rules use exact suffix matching or complete brand-name keywords and will not accidentally match unrelated domains (e.g. `tigerair.com`, `futurenet.com`).
- Missing a domain, or found one that's no longer valid? Issues and PRs are welcome.
- This project is for network routing purposes only and is not affiliated with Tiger Brokers, Futu Holdings, or Moomoo Financial.
