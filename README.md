# Tiger Trade & Moomoo Proxy Rules

[![Validate rules](https://github.com/proxyBug/tigertrade-loon-rules/actions/workflows/validate.yml/badge.svg)](https://github.com/proxyBug/tigertrade-loon-rules/actions/workflows/validate.yml)

老虎证券（Tiger Trade）与富途证券 / Moomoo 的代理分流规则集。提供单独订阅与合并订阅，覆盖 **Loon、Surge、Shadowrocket、Clash/mihomo、Quantumult X、sing-box** 六种客户端。

> 仓库名称为兼容既有订阅地址而保留。所有 `main` 分支 Raw URL 持续有效。

## 规则集

| 规则集 | DOMAIN-SUFFIX | DOMAIN-KEYWORD | 合计 | 适用场景 |
| --- | ---: | ---: | ---: | --- |
| Tiger Trade | 33 | 0 | **33** | 仅使用老虎证券 |
| Moomoo / Futu | 24 | 0 | **24** | 仅使用富途 / Moomoo |
| Tiger + Moomoo | 57 | 0 | **57** | 同时使用两家平台 |

本项目采用经过核验的显式域名后缀白名单，不使用宽泛的子串关键字。共享云厂商 IP、通用推送域名及进程名暂不收入主规则集，以降低误分流和地址漂移风险。

## 订阅地址

| 客户端 | Tiger Trade | Moomoo / Futu | 合并规则 |
| --- | --- | --- | --- |
| **Loon** | [`TigerTrade.list`][loon-tiger] | [`Moomoo.list`][loon-moomoo] | [`TigerMoomoo.list`][loon-combined] |
| Surge | [`TigerTrade.list`][surge-tiger] | [`Moomoo.list`][surge-moomoo] | [`TigerMoomoo.list`][surge-combined] |
| Shadowrocket | [`TigerTrade.list`][shadowrocket-tiger] | [`Moomoo.list`][shadowrocket-moomoo] | [`TigerMoomoo.list`][shadowrocket-combined] |
| Clash / mihomo | [`TigerTrade.yaml`][clash-tiger] | [`Moomoo.yaml`][clash-moomoo] | [`TigerMoomoo.yaml`][clash-combined] |
| Quantumult X | [`TigerTrade.list`][qx-tiger] | [`Moomoo.list`][qx-moomoo] | [`TigerMoomoo.list`][qx-combined] |
| sing-box | [`TigerTrade.json`][singbox-tiger] | [`Moomoo.json`][singbox-moomoo] | [`TigerMoomoo.json`][singbox-combined] |

[loon-tiger]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerTrade.list
[loon-moomoo]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/Moomoo.list
[loon-combined]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerMoomoo.list
[surge-tiger]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerTrade.list
[surge-moomoo]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/Moomoo.list
[surge-combined]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerMoomoo.list
[shadowrocket-tiger]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerTrade.list
[shadowrocket-moomoo]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/Moomoo.list
[shadowrocket-combined]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerMoomoo.list
[clash-tiger]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/TigerTrade.yaml
[clash-moomoo]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/Moomoo.yaml
[clash-combined]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/TigerMoomoo.yaml
[qx-tiger]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerTrade.list
[qx-moomoo]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/Moomoo.list
[qx-combined]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerMoomoo.list
[singbox-tiger]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/TigerTrade.json
[singbox-moomoo]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/Moomoo.json
[singbox-combined]: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/TigerMoomoo.json

## 客户端示例

以下示例使用合并规则。只使用一家平台时，替换为上表对应链接即可。

### Loon

```ini
[Remote Rule]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerMoomoo.list, policy=PROXY, tag=TigerMoomoo, enabled=true
```

### Surge / Shadowrocket

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerMoomoo.list,PROXY
```

Shadowrocket 用户将 URL 换成 `rule/Shadowrocket/TigerMoomoo.list`。`PROXY` 替换为自己的策略组名，并将规则放在 `FINAL` 前。

### Clash / mihomo

```yaml
rule-providers:
  TigerMoomoo:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/TigerMoomoo.yaml
    path: ./ruleset/TigerMoomoo.yaml
    interval: 86400

rules:
  - RULE-SET,TigerMoomoo,PROXY
```

### Quantumult X

```ini
[filter_remote]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerMoomoo.list, tag=TigerMoomoo, force-policy=节点选择, update-interval=86400, opt-parser=false, enabled=true
```

### sing-box

需要 sing-box **1.10 或更新版本**。将示例中的 `proxy` 替换为配置里真实存在的 outbound tag。

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

## 数据来源与收录原则

最近审计：**2026-08-20**。

规则按以下证据层级维护：

1. 平台官网、OpenAPI 文档、地区站及企业服务页面；
2. [v2fly `data/itiger`](https://github.com/v2fly/domain-list-community/blob/master/data/itiger) 与 [v2fly `data/futu`](https://github.com/v2fly/domain-list-community/blob/master/data/futu)；
3. [blackmatrix7 TigerFintech](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Loon/TigerFintech)；
4. DNS、TLS、HTTP 跳转及社区抓包资料，用作交叉确认。

单次 DNS 失效不自动触发删除：部分交易、备用或地区端点可能按网络位置和业务状态启停。新增与移除均以多源证据为准。宽泛关键字、共享 CDN、云厂商 IP 段和第三方推送域名默认排除。

## 维护与验证

根目录的 `TigerTrade.list` 与 `Moomoo.list` 是手工维护源。其余规则文件均由生成器产出：

```bash
python3 scripts/generate.py
python3 -m unittest discover -s tests -v
python3 scripts/generate.py --check
```

`--check` 只检查生成文件是否漂移，不改写工作区。GitHub Actions 会在每次 Pull Request 和 `main` 分支提交时运行同一套验证。

## English

Explicit domain-suffix proxy rule sets for Tiger Trade and Moomoo/Futu, available separately or as a combined set for six proxy clients. The two root Loon files are the maintained sources; all other formats are generated and validated in CI. Broad substring keywords, shared-CDN IP ranges, and generic push-service domains are intentionally excluded to reduce false routing.

## 说明

- 本项目仅用于网络分流，与 Tiger Brokers、Futu Holdings 或 Moomoo Financial 无隶属关系。
- 规则无法保证覆盖平台未来新增的全部端点；欢迎通过 Issue 提交可复现的缺失域名证据。
- 使用者应自行确认当地法律、平台条款与账户风险。

## License

[MIT](LICENSE)

Upstream comparison sources and their licenses are recorded in [NOTICE.md](NOTICE.md).
