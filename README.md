# Rowan Homestead 🌾

一座给 AI 玩家（也欢迎人类）的文字农场。

你继承了 8 块田、两只母鸡和几百个铜板。春夏秋冬各 28 天，种地、养殖、
盖房、加工、和脾气各异的商人打交道；天气会预报但不一定准，灾祸来之前
农场会给你暗示。没有硬性结局——农场的灯可以一直亮着。

- **纯 Python 标准库**（3.11+），不联网、零依赖，单个 `homestead.py` 就是全部
- **为 AI 玩家设计**：唯一接口 `cmd(text) -> str`，每次返回文本 + 紧凑 JSON 状态栏
- **确定性**：固定 seed + 相同指令序列 → 完全相同的结果，可做可复现实验
- **自动存档**：原子写入，随时可以关掉，下次接着玩

## 快速开始（30 秒）

```bash
git clone https://github.com/yaofengxia676-dotcom/rowan-homestead.git
cd rowan-homestead
python3 -c "
from homestead import cmd
print(cmd('new'))
print(cmd('help'))"
```

人类玩家照 `help` 玩即可；详细规则见 [README_PLAYER.md](README_PLAYER.md)
（无剧透，隐藏事件和概率都封装在引擎内部）。

## 给 AI 玩家的接入说明

```python
from homestead import cmd

print(cmd("new standard 42"))   # story | standard | banished，可带种子
print(cmd("status"))            # 文本 + 末尾 📊 {...} JSON 状态栏
print(cmd("plant wheat 3; water all; feed all; advance"))   # 分号批量
print(cmd("auto 30 strategy=balanced stop=decision,disaster,achievement"))
```

- 状态栏字段：`day/year/season/weather/coins/debt/plots/animals/buildings/ap/atlas/achievements/pending`
- `pending` 非空 = 有事件等你做主，回 `choose 1`（或 2、3）
- 存档写在当前目录（或环境变量 `RH_HOME`）的 `homestead_save.json`，跨进程保留
- 想重复实验就用同一个 seed + 同一目录

也可以先跑 `python3 smoke_test.py` 自检（新建/存档/auto/抉择/确定性，共 9 项）。

## 这个仓库里有什么

| 文件 | 说明 |
| --- | --- |
| `homestead.py` | 游戏本体（引擎+内容打包，只暴露 `cmd()`） |
| `README_PLAYER.md` | 玩家手册（玩法、命令表、不剧透的忠告） |
| `smoke_test.py` | 冒烟测试，验证环境能正常跑 |
| `LICENSE` | MIT |

开发源码（内容数据明文）暂不公开——隐藏事件和概率被剧透了，
盲玩就没意思了。

## 协议

MIT。欢迎任何 AI 或人类来当农场主——几年后欢迎回来讲讲：
你成了资本主义农场大亨，还是给篱笆外的狗留了一辈子饭。🐕🌾
