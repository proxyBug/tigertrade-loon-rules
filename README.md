# TigerTrade Loon 分流规则

老虎证券 / 老虎国际(Tiger Trade)代理规则合集,按 [Loon](https://nsloon.app/) 远程规则(Remote Rule)格式编写,覆盖 App 行情交易接口、开放平台 API、各地区官网及老虎社区等域名。

## 订阅地址

```
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerTrade.list
```

## 在 Loon 中使用

### 方式一:App 内添加

1. 打开 Loon,进入 **配置 → 规则 → 远程规则**;
2. 点击右上角 **+**,粘贴上面的订阅地址;
3. **策略** 选择你希望老虎证券流量走的节点或策略组(如 `香港节点`、`PROXY`),**标签** 填 `TigerTrade`;
4. 保存后下拉刷新配置生效。

### 方式二:配置文件添加

在配置文件的 `[Remote Rule]` 段中加入(策略名按需替换):

```ini
[Remote Rule]
https://raw.githubusercontent.com/proxyBug/tigertrade-loon-rules/main/TigerTrade.list, policy=PROXY, tag=TigerTrade, enabled=true
```

> 注意:远程规则文件本身不包含策略,生效策略以订阅时指定的为准;规则需放在 `FINAL` 兜底规则之前。

## 规则内容

| 类型 | 数量 | 说明 |
| --- | --- | --- |
| DOMAIN-SUFFIX | 16 | 核心 API、各地区官网、社区等域名 |
| DOMAIN-KEYWORD | 1 | `tigerbrokers` 关键字兜底,覆盖未来新增地区站点 |

涵盖的主要域名:

- **核心 App / API**:`itiger.com`、`itigerup.com`、`tigerfintech.com`
- **各地区官网**:`tigerbrokers.com`(及 `.com.sg` / `.com.au` / `.com.hk` / `.nz`)
- **美国子公司 / 关联品牌**:`tigersecurities.com`、`tradeup.com`
- **老虎社区**:`laohu8.com`、`tigerbbs.com`、`tigerbbs.cn`、`xiaohu8.com`

## 说明

- 域名整理自老虎证券公开官网及 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) 等社区规则,并经过逐一核验;
- 如发现域名缺失或失效,欢迎提 Issue / PR;
- 本项目仅作网络分流用途,与老虎证券官方无关。
