# Rowan Homestead V0.1.4 · 玩家包

一座慢节奏的文字农场。你继承了 8 块田、两只母鸡和几百个铜板，
剩下的故事由四季、天气、商人和你自己的决定来写。

本包面向**人类玩家和 AI 玩家**：所有操作都通过一个函数完成。

## 快速开始

```python
from homestead import cmd

print(cmd("new"))        # 开始新农场（可选 new story|standard|banished [seed]）
print(cmd("help"))       # 查看全部指令
print(cmd("status"))     # 看看家底
```

要求：Python 3.11+，**只用标准库**，无需联网、无需安装任何东西。
把 `homestead.py` 放在你喜欢的目录，存档（`homestead_save.json`）会写在该目录；
也可以用环境变量 `RH_HOME` 指定存档目录。

## 基本节奏

- 一年 4 季，每季 28 天。每天 **3 个行动点**，查询类指令不耗点。
- 典型的一天：`plant wheat 3` → `water all` → `feed all` → `advance`。
- 用分号批量下指令，一次最多 8 条：`water all; feed all; advance`。
- 不想手动操作时交给自动经营：
  `auto 30 strategy=balanced stop=decision,disaster,achievement`
  （有抉择、灾害或新成就时会停下来等你。）

## 可以做的事

| 方面 | 指令举例 |
| --- | --- |
| 种地 | `hoe` 翻地，`plant potato 2` 播种，`water all` 浇水，`harvest all` 收获 |
| 养殖 | `buy animal chicken 2`，`feed all`，`collect all`，`incubate egg` |
| 建设 | `build well`，`upgrade workshop`，`repair barn`，`process bread` 加工 |
| 买卖 | `market` 看商人，`buy wheat_seed 5`，`sell egg all`，还有每周只来一天的大头菜贩子 |
| 财务 | `borrow 300` 周转，`repay all` 还债 |
| 野趣 | `forage` 拾荒（永远免费），`explore forest` 探索 |
| 时间 | `forecast` 看天气预报，`advance` 睡觉，`auto` 自动经营 |
| 记录 | `atlas` 图鉴，`achievements` 成就，`journal` 日志，`report` 阶段战报 |
| 查看 | `look wheat` / `look 小麦` / `look coop` 看作物、建筑、配方详情 |

遇到要你拿主意的事（窗口会提示 ❗），用 `choose <编号>` 做出选择。

## 一些不剧透的忠告

1. 播种前看清季节；温室会改变规则。
2. 雨天不用浇水；水井等级决定一天能浇几块地。
3. 商人各有各的脾气和喜好，同一件货在不同人手里价格差很多。
4. 天气预报大多数时候是准的。「大多数时候。」
5. 灾祸来之前，农场会给你一些暗示。看懂暗示的人，损失会小很多。
6. 有些东西埋在土里、沉在溪底、躲在森林深处。探索永远不亏。
7. 破产不是终点：拾荒永远免费，饲料在最困难时有救济价。
8. 图鉴有 8 类、成就有公开的也有不公开的。好奇心会被奖励。

## 给 AI 玩家的说明

- 唯一接口是 `cmd(text: str) -> str`，每次返回文本叙述 + 末尾的 `📊 {...}` 紧凑 JSON 状态栏。
- 状态栏字段：day/year/season/weather/coins/debt/plots/animals/buildings/ap/atlas/achievements/pending。
- `pending` 非空表示有待决事件，请用 `choose 1|2|3` 回应。
- 同一存档目录下，状态会跨进程保留（每次指令后自动存档）。
- 想要可复现的实验：`new standard 42` 固定种子，之后同样的指令序列会得到完全一样的结果。

祝丰收。🌾
