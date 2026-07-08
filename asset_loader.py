"""
Asset Loader - 从 assets/ 加载 SVG 并转为 pygame Surface
修复：不再强制添加系统 Python 3.9 的 site-packages（会破坏 Hermes venv 的 PIL）
改为只添加当前 Python 版本的 site-packages（如果存在且没在 sys.path 里）
"""
import os
import sys
import pygame
from io import BytesIO

# 只添加当前 Python 版本的 site-packages（不强制跨版本污染）
import site
for _sp in site.getsitepackages():
    if _sp not in sys.path and os.path.exists(_sp):
        sys.path.insert(0, _sp)

# 延迟导入cairosvg，失败则使用纯色fallback
CAIROSVG_AVAILABLE = False
try:
    import cairosvg as _cairosvg_module
    CAIROSVG_AVAILABLE = True
except Exception:
    pass

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
CACHE = {}

def _load_svg(filename, size=(64, 64)):
    """加载SVG文件并转为指定尺寸的Surface"""
    if filename in CACHE:
        return CACHE[filename]
    
    if not CAIROSVG_AVAILABLE:
        return None
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        return None
    
    try:
        # 确保pygame.display已初始化
        if not pygame.display.get_init():
            pygame.init()
            pygame.display.set_mode((1, 1))
        png_data = _cairosvg_module.svg2png(url=path, output_width=size[0], output_height=size[1])
        img = pygame.image.load(BytesIO(png_data)).convert_alpha()
        CACHE[filename] = img
        return img
    except Exception as e:
        print(f"Failed to load {filename}: {e}")
        return None

def get_enemy(enemy_type, size=(72, 72)):
    """获取敌人图片"""
    mapping = {
        'normal': 'enemy_1.svg',
        'fast': 'enemy_2.svg',
        'tank': 'enemy_3.svg',
        'boss': 'enemy_4.svg',
        'slow': 'enemy_5.svg',
    }
    filename = mapping.get(enemy_type, 'enemy_1.svg')
    return _load_svg(filename, size)

def get_tower(tower_type, size=(96, 96)):
    """获取炮塔图片"""
    mapping = {
        'gun': 'tower_1-1-0.svg',
        'cannon': 'tower_2-1-0.svg',
        'sniper': 'tower_3-1-0.svg',
        'ice': 'tower_4-1-0.svg',
    }
    filename = mapping.get(tower_type, 'tower_1-1-0.svg')
    return _load_svg(filename, size)

def get_bullet(bullet_type, size=(32, 32)):
    """获取子弹图片"""
    mapping = {
        'gun': 'bullet_1.svg',
        'cannon': 'bullet_2.svg',
        'sniper': 'bullet_3.svg',
        'ice': 'bullet_4.svg',
    }
    filename = mapping.get(bullet_type, 'bullet_1.svg')
    return _load_svg(filename, size)

def get_map_tile(tile_type, size=(64, 64)):
    """获取地图瓦片"""
    mapping = {
        0: 'map_0.svg',   # 草地
        1: 'map_1.svg',   # 道路
        2: 'map_2.svg',   # 水域
        3: 'map_3.svg',   # 石头
    }
    filename = mapping.get(tile_type, 'map_0.svg')
    return _load_svg(filename, size)
