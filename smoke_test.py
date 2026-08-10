#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rowan Homestead 玩家包冒烟测试。

在与 homestead.py 相同的目录运行：
    python3 smoke_test.py
会在临时目录里开一个新农场，验证接口、存档、抉择与自动经营。
"""
import json
import os
import re
import tempfile

os.environ["RH_HOME"] = tempfile.mkdtemp(prefix="rh_smoke_")

from homestead import cmd  # noqa: E402

FAILED = []


def check(name, cond, detail=""):
    mark = "✓" if cond else "✗"
    print(f"{mark} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        FAILED.append(name)


def status_bar(text):
    m = re.search(r"📊 (\{.*\})", text)
    return json.loads(m.group(1)) if m else None


# 1. 接口与新游戏
out = cmd("new standard 42")
sb = status_bar(out)
check("cmd('new') 返回状态栏", sb is not None)
check("初始资金/天数正确", sb and sb["coins"] == 600 and sb["day"] == 1)

# 2. 基础农事闭环
cmd("plant wheat 3; plant potato 2")
out = cmd("water all; feed all")
sb = status_bar(out)
check("批量指令与行动点扣减", sb and sb["plots"] == "5/8" and sb["ap"] <= 1)
out = cmd("advance")
sb = status_bar(out)
check("advance 进入第 2 天且行动点恢复", sb and sb["day"] == 2 and sb["ap"] == 3)

# 3. 存档
save_path = os.path.join(os.environ["RH_HOME"], "homestead_save.json")
check("存档文件已写入", os.path.exists(save_path))
with open(save_path, encoding="utf-8") as f:
    save = json.load(f)
check("存档含 schema_version", save.get("schema_version") == 1)

# 4. 自动经营 + 抉择暂停
out = cmd("auto 30 strategy=balanced stop=decision,disaster,achievement")
check("auto 可运行并给出摘要", "自动经营" in out)
sb = status_bar(out)
if sb and sb["pending"]:
    out2 = cmd("choose 1")
    check("choose 可结算待决事件", status_bar(out2)["pending"] is None)
else:
    check("choose 可结算待决事件（本轮无待决，跳过）", True)

# 5. 确定性：同种子同指令序列 → 同样状态
def run_sequence():
    os.environ["RH_HOME"] = tempfile.mkdtemp(prefix="rh_det_")
    cmd("new standard 42 confirm")  # 同进程内单例仍在，confirm 强制重开
    cmd("plant wheat 3; plant potato 2; water all; feed all; advance")
    cmd("auto 10 strategy=balanced stop=decision decide=auto")
    with open(os.path.join(os.environ["RH_HOME"], "homestead_save.json"), encoding="utf-8") as f:
        return json.load(f)

a, b = run_sequence(), run_sequence()
check("确定性（同种子同指令结果一致）", a == b)

print()
if FAILED:
    print("冒烟测试未通过：", ", ".join(FAILED))
    raise SystemExit(1)
print("全部通过。农场一切正常，祝丰收。🌾")
