# TigerTrade 代理分流规则

老虎证券 / 老虎国际(Tiger Trade)代理分流规则合集,覆盖 App 行情交易接口、加速 CDN、开放平台 API、各地区官网及老虎社区等 26 条域名规则。

支持 **Loon · Surge · Shadowrocket · Clash(mihomo) · Quantumult X · sing-box** 六种客户端,所有格式由同一份源文件生成,内容完全一致。

## 📦 订阅地址总览

| 客户端 | 规则文件 |
| --- | --- |
| **Loon**(首选) | `https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerTrade.list` |
| Surge | `https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerTrade.list` |
| Shadowrocket | `https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerTrade.list` |
| Clash / mihomo | `https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Clash/TigerTrade.yaml` |
| Quantumult X | `https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerTrade.list` |
| sing-box | `https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/sing-box/TigerTrade.json` |

---

## 🏆 Loon(首选)

**App 内添加**:配置 → 规则 → 远程规则 → 右上角 **+**,粘贴订阅地址,策略选择目标节点/策略组,标签填 `TigerTrade`,保存后刷新配置。

**配置文件添加**(策略名按需替换):

```ini
[Remote Rule]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerTrade.list, policy=PROXY, tag=TigerTrade, enabled=true
```

> Loon 规则位于仓库根目录,是所有其他格式的源文件;老订阅地址永久有效。

## Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Surge/TigerTrade.list,PROXY
```

`PROXY` 替换为你的策略组名,规则放在 `FINAL` 之前。

## Shadowrocket

App 内:设置 → 规则 → 右上角 **+** → 类型选 `RULE-SET`,粘贴订阅地址,策略选 `PROXY`(或指定节点)。

配置文件方式与 Surge 相同:

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/Shadowrocket/TigerTrade.list,PROXY
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

rules:
  - RULE-SET,TigerTrade,PROXY
```

## Quantumult X

```ini
[filter_remote]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/rule/QuantumultX/TigerTrade.list, tag=TigerTrade, force-policy=节点选择, update-interval=86400, opt-parser=false, enabled=true
```

`force-policy` 填你的策略组名,会覆盖规则文件内的默认策略。

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
      }
    ],
    "rules": [
      { "rule_set": "tigertrade", "outbound": "proxy" }
    ]
  }
}
```

---

## 规则内容

| 类型 | 数量 | 说明 |
| --- | --- | --- |
| DOMAIN-SUFFIX | 25 | 核心 API、CDN、各地区官网、社区等域名 |
| DOMAIN-KEYWORD | 1 | `tigerbrokers` 关键字兜底,覆盖未来新增地区站点 |

涵盖的主要域名:

- **核心 App / API**:`itiger.com`、`itigerup.com`、`tigerfintech.com`
- **加速 / 备用 CDN**(App 内实际请求,多为混淆命名):`skytigris.cn`、`skytigris.com`、`itigergrowth.com`、`itigergrowtha.com`、`atigrzen.com`、`atigrpulse.com`、`tigrwd.com`、`tigrdw.com`
- **各地区官网**:`tigerbrokers.com`(及 `.com.sg` / `.com.au` / `.com.hk` / `.nz`)
- **美国子公司 / 关联品牌**:`tigersecurities.com`、`tradeup.com`
- **老虎社区 / TTM**:`laohu8.com`、`tigerbbs.com`、`tigerbbs.cn`、`xiaohu8.com`、`ttm.financial`(TigerGPT)

CDN 类域名的归属均经核验:`skytigris.cn` whois 注册邮箱为 `@itiger.com`;`tigrwd.com` / `tigrdw.com` 站点标题为 *Tiger Fintech*;`atigrzen.com` 站点标识为 *Tiger Brokers*;`hktrade.skytigris.com` 为老虎港股交易接口;`itigergrowth(a).com` 收录于 [v2fly 官方 itiger 列表](https://github.com/v2fly/domain-list-community/blob/master/data/itiger)。

所有规则均为精确后缀匹配或完整品牌名关键字,不会误伤 `tigerair.com`、`tigergraph.com` 等无关 tiger 域名。

## 🔧 维护

根目录 [TigerTrade.list](TigerTrade.list)(Loon 格式)是唯一源文件,增删域名后运行:

```bash
python3 scripts/generate.py
```

即可同步生成 `rule/` 下所有客户端格式,避免多份文件漂移。

## 说明

- 域名整理自老虎证券公开官网、[v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)、[blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) 等社区规则,并经过逐一核验;
- 如发现域名缺失或失效,欢迎提 Issue / PR;
- 本项目仅作网络分流用途,与老虎证券官方无关。
