# GunTower TD 🎮

基于 *GunTower.sb3* 复刻的 2D 塔防游戏，使用 Python + Pygame 开发。

## 游戏截图

（待补充：建议游戏运行后截图 main menu、gameplay、game over 界面）

## 快速开始

### 依赖安装

```bash
pip install pygame cairosvg
```

> **注意**：macOS 用户如果在 import 阶段卡住，设置环境变量再启动：
> ```bash
> export SDL_VIDEODRIVER=dummy
> ```

### 运行

```bash
cd GunTower
python3 guntower_refactor.py
```

## 操作指南

| 按键 | 功能 |
|------|------|
| `1` | 选择 MG塔（$50，射程180） |
| `2` | 选择 Cannon（$100，射程360） |
| `3` | 选择 Sniper塔（$75，射程250） |
| `4` | 选择 Ice塔（$60，射程160） |
| `ESC` | 取消放置 |
| `空格` | 开始下一波 |
| `鼠标左键` | 放置炮塔 / 点击 Next Wave |
| `鼠标右键` | 卖掉炮塔（返还70%金币） |
| `R` | 游戏结束后重开 |

## 游戏特性

- ✅ 4种防御塔（MG / Cannon / Sniper / Ice）
- ✅ 半透明射程预览圈
- ✅ Cannon 塔2倍射程（360像素）
- ✅ 右键卖掉塔（返还70%金币）
- ✅ 波次系统（自动递增难度）
- ✅ 4种敌人（普通 / 快速 / 坦克 / Boss）
- ✅ Game Over 统计 + R重开
- ✅ 深色主题 UI
- ✅ 固定地图（15×10 格子）

## 项目结构

```
GunTower/
├── guntower_refactor.py   ← 主版本（最新稳定版）
├── asset_loader.py        ← 素材加载器
├── assets/                ← 405 个 SVG 游戏素材
├── README.md              ← 本文件
└── .gitignore
```

## 素材说明

`assets/` 包含从 GunTower.sb3 提取的 405 个 SVG 素材：

- `enemy_*` — 15种敌人精灵图
- `tower_*` — 4种塔 × 动画帧
- `bullet_*` — 子弹外观
- `map_*` — 地图瓦片（草地/道路/水域/石头）
- `button_*` — UI 按钮
- `text_*` / `tip_*` / `number_*` — UI 文字

## 技术栈

- Python 3.9+
- Pygame（游戏引擎）
- cairosvg（SVG 渲染）

## License

MIT
