# Tiger Trade + Moomoo/Futu 代理分流规则

[![Release](https://img.shields.io/github/v/release/proxyBug/tigertrade-loon-rules?display_name=tag)](https://github.com/proxyBug/tigertrade-loon-rules/releases/latest)
[![Validate rules](https://github.com/proxyBug/tigertrade-loon-rules/actions/workflows/validate.yml/badge.svg)](https://github.com/proxyBug/tigertrade-loon-rules/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 官网能打开，行情、登录、下单或活动页却仍旧偶发卡住？问题往往出在 App 背后那批不显眼的 API、CDN、交易接口和地区门户。

这个仓库给 **老虎证券 Tiger Trade** 与 **富途证券 / Moomoo** 做完整的应用级代理分流。它不只收几个官网域名，也不靠一条宽泛关键字把无关网站一起兜进代理：规则来自官方 runtime、OpenAPI、地区站、DNS/TLS 与社区数据的交叉核验，再统一生成六种客户端格式。

- **三套规则**：Tiger、Moomoo/Futu、Tiger + Moomoo 合并版
- **六种客户端**：Loon、Surge、Shadowrocket、Clash/mihomo、Quantumult X、sing-box
- **零宽泛关键字**：全部使用显式 `DOMAIN-SUFFIX`，减少误伤
- **可复现维护**：两份源文件生成全部格式，11 项测试与 GitHub Actions 自动防漂移

## 为什么值得用

### Tiger Trade：从“常见域名列表”推进到“官方运行时覆盖”

2026-08-20 的官方 runtime/bootstrap 审计提取到 **185 条 URL 引用、125 个唯一主机**。本仓库覆盖其中 **120 个 Tiger 第一方主机**；剩余 5 个是 USAA、微博、微信、小米、Facebook 等第三方集成，按边界主动排除。

| 覆盖能力 | 本仓库 | blackmatrix7 TigerFintech | v2fly itiger |
| --- | :---: | :---: | :---: |
| 显式后缀规则数 | **40** | 19 | 9 |
| 官方 runtime 字段级核验 | **✅ 120 / 125 主机** | — | — |
| App 核心 API / 行情 / 交易 | ✅ | ✅ | ✅ |
| 升级、配置、数据与加速域名 | **✅ 完整度更高** | ⚠️ 部分 | ⚠️ 部分 |
| 新西兰交易与客户接口 | ✅ | ❌ | ❌ |
| Tiger ESOP 接口 | ✅ | ❌ | ❌ |
| 香港、澳洲、新马、印尼、越南地区门户 | ✅ | ❌ | ❌ |
| 各地区官网、美国关联实体 | ✅ | ⚠️ 少量 | ❌ |
| 社区、资讯与 TigerGPT | ✅ | ⚠️ 部分 | ⚠️ 部分 |
| 可直接订阅的客户端格式 | **6 种** | 5 种常见客户端 | 上游域名数据源 |
| 收录/撤下证据矩阵 | ✅ | ❌ | ❌ |

对比基于 2026-08-20 的公开版本：

- [blackmatrix7 TigerFintech](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Loon/TigerFintech)：19 条，与本仓库共有 16 条；`tbdesk.com`、`tigertcp.cn`、`tigerbrokers.net` 暂无当前官方 runtime 或实时流量证据，因此没有盲目照抄。
- [v2fly `data/itiger`](https://github.com/v2fly/domain-list-community/blob/master/data/itiger)：9 条，本仓库全部覆盖，并另外收录 31 条经独立证据确认的第一方域名。

所以这里追求的并非“数字越大越好”。真正的差别是：**该补的补到交易、客户与地区门户；证据不足的，哪怕别家有，也先按住。**

### Moomoo/Futu：完整覆盖 v2fly，再补三处官方服务

| 覆盖能力 | 本仓库 | v2fly `data/futu` |
| --- | :---: | :---: |
| 显式后缀规则数 | **24** | 21 |
| v2fly 当前域名 | **✅ 21 / 21** | ✅ |
| Moomoo Canada | ✅ `moomoo.ca` | ❌ |
| Moomoo Bull 服务域名 | ✅ `moomoobull.com` | ❌ |
| Futu Trustee 官方信托服务 | ✅ `fututrustee.com` | ❌ |
| 六客户端独立规则 + 合并规则 | ✅ | ❌ |
| 宽泛 `moomoo` / `futunn` 关键字 | **❌ 主动不用** | ❌ |

`moomoo.com.au` 当前已成为停放域名，`moomoo.jp` 属于无关动物医院；这类“名字看起来很像”的域名不会因为好看就进入规则。

## 选哪一套

| 你的情况 | 推荐规则 |
| --- | --- |
| 只使用 Tiger Trade | `TigerTrade` |
| 只使用 Moomoo / 富途牛牛 | `Moomoo` |
| 两款都用，或懒得分别配置 | **`TigerMoomoo` 合并规则** |

当前规模：Tiger **40** 条、Moomoo/Futu **24** 条、合并版 **64** 条；全部为显式后缀规则。

## 订阅地址

| 客户端 | Tiger Trade | Moomoo / Futu | Tiger + Moomoo |
| --- | --- | --- | --- |
| **Loon** | [`TigerTrade.list`][loon-tiger] | [`Moomoo.list`][loon-moomoo] | **[`TigerMoomoo.list`][loon-combined]** |
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

> 上表是持续更新的 `main` 通道。需要固定版本时，把 URL 中的 `main` 换成版本号，例如 `v0.1.1`。

## 怎么添加

下面以 **TigerMoomoo 合并规则** 为例。只用一家券商时，换成上表对应文件即可。

### Loon

App 内进入：**配置 → 规则 → 远程规则 → 右上角 +**，粘贴 Loon 链接并选择策略。

```ini
[Remote Rule]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerMoomoo.list, policy=PROXY, tag=TigerMoomoo, enabled=true
```

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerMoomoo.list,PROXY
```

将 `PROXY` 换成自己的策略组，规则放在 `FINAL` 前。

### Shadowrocket

App 内进入：**设置 → 规则 → 右上角 + → 类型选择 RULE-SET**。

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerMoomoo.list,PROXY
```

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

需要 sing-box **1.10 或更新版本**。把示例中的 `proxy` 换成配置里真实存在的 outbound tag。

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

## 规则里有什么

### Tiger Trade（40 条）

- **核心 App / API**：`itiger.com`、`itigerup.com`、`tigerfintech.com`
- **新西兰交易与客户接口**：`itiger-nz.com`
- **ESOP**：`tigeresop.com`、`tigeresop.com.sg`
- **升级、配置、日志与数据**：`play-analytics.com`、`ftfast.com`、`iotaskyt.com`、`iotaskyty.com`
- **加速与备用链路**：`skytigris.*`、`itigergrowth*`、`atigr*`、`tigr*`
- **地区门户**：`etasphere.com`、`gotigerhk.com`、`itigertrader.com`、`tigerhkgo.com`、`tigertrader.app`、`tigrgood.com` 等
- **地区官网与关联实体**：Tiger Brokers 各地区站、Tiger Securities、TradeUP
- **社区与资讯**：老虎社区、TigerBBS、TTM / TigerGPT

完整清单见 [`TigerTrade.list`](TigerTrade.list)。官方 runtime 的字段路径、DNS/TLS 交叉结果以及“为什么加、为什么不加”见 [`evidence/tiger-runtime-2026-08-20.json`](evidence/tiger-runtime-2026-08-20.json)。

### Moomoo / Futu（24 条）

- **核心平台 / OpenAPI**：`moomoo.com`、`futunn.com`、`moomoobull.com`
- **地区与企业服务**：香港、新加坡、澳洲、加拿大站及 Futu Holdings
- **行情、交易与静态资源**：`futu5.com`、`futustatic.com`、`fututrade.com` 等
- **ESOP 与信托**：`futuesop.com`、`fututrustee.com`、`moomooequity.com`、`moomootrustee.com`

完整清单见 [`Moomoo.list`](Moomoo.list)。

## 这套规则如何维护

根目录只有两份手工维护源：

- `TigerTrade.list`
- `Moomoo.list`

其余客户端文件和合并规则都由脚本生成：

```bash
python3 scripts/generate.py
python3 -m unittest discover -s tests -v
python3 scripts/generate.py --check
```

生成器会拒绝空值、非法域名、未知类型、重复规则和多余字段；`--check` 只检查漂移，不改文件。GitHub Actions 会在每个 PR 与 `main` 提交上执行同一套验证。

## 证据边界

- 直接证据优先：官方 runtime、OpenAPI、官网与当前 App 服务字段。
- DNS、TLS SAN、HTTP 跳转用于确认归属和现状。
- v2fly、blackmatrix7 与社区抓包用于发现候选，不作为“见到就抄”的授权。
- 共享云厂商 IP、通用推送、社交平台和宽泛关键字默认排除。
- 暂无当前证据的域名留在候选记录里，等 App 制品或实时流量再次证明。

最近审计：**2026-08-20**。上游版本、许可证与来源说明见 [NOTICE.md](NOTICE.md)。

## English

Evidence-driven, domain-suffix-only proxy rules for Tiger Trade and Moomoo/Futu. The repository provides standalone and combined subscriptions for six clients. Tiger coverage is validated against the current official runtime/bootstrap map; Moomoo/Futu includes the complete current v2fly set plus independently confirmed service domains. Generated formats are deterministic and protected by tests and CI.

## 说明与许可

- 本项目只提供网络分流规则，与 Tiger Brokers、Futu Holdings、Moomoo Financial 无隶属关系。
- 规则不会绕过账户资格、地区限制或平台风控；请自行遵守当地法律与平台条款。
- 如发现缺失域名，请提交可复现的主机名、功能和来源；请勿上传账户标识、Token 或完整流量载荷。
- 项目采用 [MIT License](LICENSE)；第三方来源及许可证见 [NOTICE.md](NOTICE.md)。
