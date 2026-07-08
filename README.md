# GunTower TD 炮塔防御游戏

基于 GunTower.sb3 复刻的 2D 塔防游戏。

## 目录结构

```
GunTower/
├── guntower_refactor.py          ← 🎮 主版本（最新稳定版）
├── GunTower_TD.py                ← 📦 稳定备份版
├── guntower_v2.py                ← 🕸️ 深色主题初版
├── guntower_debug.py             ← 🔧 调试版（带事件日志）
├── guntower_refactor_debug.py    ← 🔧 重构版调试版
├── monitor_game.py               ← 📊 游戏监控脚本
├── test_guntower.py              ← 🧪 自动化测试脚本
├── guntower_monitor.log          ← 📋 监控日志
├── assets/                       ← 🖼️ 游戏素材（405个SVG）
│   ├── enemy_*.svg               │   敌人精灵图
│   ├── tower_*.svg               │   塔精灵图
│   ├── bullet_*.svg              │   子弹精灵图
│   ├── map_*.svg                 │   地图瓦片
│   ├── button_*.svg              │   UI按钮
│   ├── icon_*.svg                │   图标
│   ├── tip_*.svg                 │   提示文字
│   ├── number_*.svg              │   数字贴图
│   ├── price_*.svg               │   价格贴图
│   ├── top effect_*.svg          │   顶部特效
│   ├── bottom effect_*.svg       │   底部特效
│   └── text_*.svg                │   文本素材
└── README.md                     │   本文件
```

## 快速开始

```bash
cd /Users/mac/Desktop/GunTower
python3 guntower_refactor.py
```

## 操作指南

| 按键 | 功能 |
|------|------|
| `1` | 选择 MG塔（$50，射程180） |
| `2` | 选择 Cannon（$100，射程360=2倍） |
| `3` | 选择 Sniper塔（$75，射程250） |
| `4` | 选择 Ice塔（$60，射程160） |
| `ESC` | 取消放置 |
| `空格` | 开始下一波 |
| `鼠标左键` | 放置炮塔 / 点击Next Wave |
| `鼠标右键` | 卖掉炮塔（返还70%金币） |
| `R` | 游戏结束后重开 |

## 功能特性

- ✅ 4种防御塔（MG/Cannon/Sniper/Ice）
- ✅ 半透明射程预览圈
- ✅ Cannon 塔2倍射程（360像素）
- ✅ 右键卖掉塔（返还70%）
- ✅ 波次系统（自动递增难度）
- ✅ 4种敌人（普通/快速/坦克/Boss）
- ✅ Game Over 统计 + R重开
- ✅ 深色主题UI
- ✅ 固定地图（15×10格子）

## 素材说明

`assets/` 目录包含从 GunTower.sb3 提取的 405 个 SVG 素材，按功能分类：

- **enemy_*** — 敌人外观（15种不同敌人）
- **tower_*** — 防御塔外观（4种塔 × 多个动画帧）
- **bullet_*** — 子弹外观（多种子弹类型）
- **map_*** — 地图瓦片（草地/道路/水域/石头）
- **button_*** — UI按钮（各种状态）
- **icon_*** — 界面图标
- **tip_*** — 游戏内提示文字
- **number_*** — 数字贴图（0-9）
- **price_*** — 价格贴图（0-9）
- **effect_*** — 顶部/底部装饰特效

## 开发说明

- **guntower_refactor.py** — 当前主版本，所有修复已合并
- **guntower_debug.py** — 带详细事件日志，用于排查崩溃
- **monitor_game.py** — 监控游戏进程，记录存活时间和内存
- **test_guntower.py** — 自动化测试脚本（stdin注入命令）
