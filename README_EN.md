# GunTower TD 🎮

A 2D tower defense game remade from *GunTower.sb3*, built with Python + Pygame.

## Quick Start

### Install Dependencies

```bash
pip install pygame cairosvg
```

> **Note for macOS**: If the game hangs at import, set this environment variable before running:
> ```bash
> export SDL_VIDEODRIVER=dummy
> ```

### Run

```bash
cd GunTower
python3 guntower_refactor.py
```

## Controls

| Key | Action |
|-----|--------|
| `1` | Select MG Tower ($50, range 180) |
| `2` | Select Cannon ($100, range 360) |
| `3` | Select Sniper Tower ($75, range 250) |
| `4` | Select Ice Tower ($60, range 160) |
| `ESC` | Cancel placement |
| `Space` | Start next wave |
| `Left Click` | Place tower / Click Next Wave |
| `Right Click` | Sell tower (70% refund) |
| `R` | Restart after game over |

## Features

- ✅ 4 tower types (MG / Cannon / Sniper / Ice)
- ✅ Semi-transparent range preview
- ✅ Cannon tower with 2× range (360px)
- ✅ Right-click to sell (70% refund)
- ✅ Wave system (auto-increasing difficulty)
- ✅ 4 enemy types (Normal / Fast / Tank / Boss)
- ✅ Game Over stats + R restart
- ✅ Dark theme UI
- ✅ Fixed map (15×10 grid)

## Project Structure

```
GunTower/
├── guntower_refactor.py   ← Main version (latest stable)
├── asset_loader.py        ← Asset loader
├── assets/                ← 405 SVG game assets
├── README.md              ← 中文说明
├── README_EN.md           ← English (this file)
└── .gitignore
```

## Assets

`assets/` contains 405 SVG assets extracted from GunTower.sb3:

- `enemy_*` — 15 enemy sprites
- `tower_*` — 4 tower types × animation frames
- `bullet_*` — Bullet appearances
- `map_*` — Map tiles (grass/road/water/rock)
- `button_*` — UI buttons
- `text_*` / `tip_*` / `number_*` — UI text

## Tech Stack

- Python 3.9+
- Pygame (game engine)
- cairosvg (SVG rendering)

## Known Issues

- macOS: SDL may hang without `SDL_VIDEODRIVER=dummy`
- Large map (2219 files) excluded from git via `.gitignore`

## License

MIT
