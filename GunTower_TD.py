"""
GunTower 复刻 - Block TD
参考 GunTower.sb3 的素材和设计
"""
import pygame
import random
import math
import os
import sys

# ── 初始化 ──
pygame.init()
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GunTower 复刻 - Block TD")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)
font_big = pygame.font.SysFont(None, 28)

# ── 常量 ──
TILE_SIZE = 70  # GunTower的地图方块是70x70
MAP_WIDTH = 15
MAP_HEIGHT = 10
FPS = 60

# ── 颜色定义（从GunTower素材提取） ──
COLORS = {
    'bg': (30, 30, 30),
    'panel': (51, 51, 51),
    'border': (100, 100, 100),
    'text': (200, 200, 200),
    'gold': (255, 215, 0),
    'grass': (100, 200, 100),
    'path': (200, 180, 140),
    'water': (100, 150, 200),
    'stone': (150, 150, 150),
    'tower1': (0, 179, 15),
    'tower2': (230, 164, 0),
    'tower3': (255, 0, 0),
    'tower4': (128, 0, 128),
    'enemy1': (255, 100, 100),
    'enemy2': (255, 200, 100),
    'enemy3': (200, 100, 255),
    'base': (0, 255, 0),
}

# ── 地图设计（参考GunTower的路径设计） ──
# 0=grass, 1=path, 2=water, 3=stone
MAP_DESIGN = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# 敌人路径点（从左上到右下）
ENEMY_PATH = [
    (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (5, 4), (5, 5), (6, 5), (7, 5),
    (7, 6), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (11, 8), (11, 9)
]

# 防御塔类型（参考GunTower的4种塔）
TOWER_TYPES = {
    'gun': {
        'name': 'MG塔',
        'cost': 50,
        'damage': 8,
        'range': 180,
        'fire_rate': 15,  # 帧间隔
        'color': COLORS['tower1'],
        'projectile_speed': 10,
        'projectile_size': 3,
    },
    'cannon': {
        'name': 'Cannon',
        'cost': 100,
        'damage': 25,
        'range': 150,
        'fire_rate': 60,
        'color': COLORS['tower2'],
        'projectile_speed': 6,
        'projectile_size': 6,
        'splash_radius': 40,
    },
    'sniper': {
        'name': 'Sniper塔',
        'cost': 75,
        'damage': 50,
        'range': 250,
        'fire_rate': 120,
        'color': COLORS['tower3'],
        'projectile_speed': 15,
        'projectile_size': 2,
    },
    'ice': {
        'name': 'Ice',
        'cost': 60,
        'damage': 3,
        'range': 160,
        'fire_rate': 30,
        'color': (100, 200, 255),
        'projectile_speed': 8,
        'projectile_size': 4,
        'slow_factor': 0.4,
    },
}

# 敌人类
ENEMY_TYPES = {
    'normal': {'name': '普通敌人', 'hp': 30, 'speed': 1.0, 'reward': 5, 'color': COLORS['enemy1']},
    'fast': {'name': '快速敌人', 'hp': 20, 'speed': 1.8, 'reward': 8, 'color': COLORS['enemy2']},
    'tank': {'name': '坦克敌人', 'hp': 80, 'speed': 0.6, 'reward': 15, 'color': COLORS['enemy3']},
    'boss': {'name': 'Boss敌人', 'hp': 200, 'speed': 0.4, 'reward': 50, 'color': (255, 0, 255)},
}


class Game:
    """游戏主类"""
    def __init__(self):
        self.gold = 150
        self.wave = 0
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.selected_tower_type = 'gun'
        self.placing_tower = False
        self.mouse_pos = (0, 0)
        self.spawn_timer = 0
        self.enemies_to_spawn = 0
        self.spawn_interval = 60
        self.game_over = False
        self.base_health = 100
        self.wave_active = False
        self.wave_cooldown = 0
        self.difficulty = 1
        self.btn_next_wave_rect = None
        
        # 敌人路径
        self.path_points = [(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2) 
                           for x, y in ENEMY_PATH]
        
        # Base位置
        self.base_pos = ENEMY_PATH[-1]
        
        # 加载地图
        self.map_data = [row[:] for row in MAP_DESIGN]
    
    def start_wave(self):
        """开始新一波敌人"""
        if self.wave_active:
            return
        
        self.wave += 1
        self.wave_active = True
        self.enemies_to_spawn = 5 + self.wave * 2
        self.spawn_timer = 0
        self.spawn_interval = max(20, 60 - self.wave * 2)
        
        print(f"第{self.wave}波敌人开始！")
    
    def spawn_enemy(self):
        """生成敌人"""
        if self.enemies_to_spawn <= 0:
            return
        
        # 随机选择敌人类型
        rand = random.random()
        if rand < 0.6:
            enemy_type = 'normal'
        elif rand < 0.85:
            enemy_type = 'fast'
        elif rand < 0.95:
            enemy_type = 'tank'
        else:
            enemy_type = 'boss'
        
        template = ENEMY_TYPES[enemy_type]
        hp = template['hp'] * (1 + self.difficulty * 0.2)
        speed = template['speed'] * (1 + self.difficulty * 0.1)
        reward = template['reward']
        
        enemy = Enemy(self.path_points[0][0], self.path_points[0][1], hp, speed, reward, 
                     template['color'], enemy_type)
        self.enemies.append(enemy)
        self.enemies_to_spawn -= 1
    
    def update(self):
        try:
            if self.game_over:
                return
            
            # 敌人生成
            if self.enemies_to_spawn > 0:
                self.spawn_timer += 1
                if self.spawn_timer >= self.spawn_interval:
                    self.spawn_enemy()
                    self.spawn_timer = 0
            
            # 更新敌人
            for enemy in self.enemies:
                result = enemy.update(self.path_points, self.map_data)
                if result == 'reached_base':
                    self.base_health -= 10
                    if self.base_health <= 0:
                        self.game_over = True
            
            # 更新防御塔
            for tower in self.towers:
                tower.update(self.enemies, self.projectiles)
            
            # 更新子弹
            for proj in self.projectiles:
                proj.update(self.enemies)
            
            # 清理死亡实体
            self.enemies = [e for e in self.enemies if e.alive]
            self.projectiles = [p for p in self.projectiles if p.alive]
            
            # 收取奖励
            for enemy in self.enemies:
                if not enemy.alive and hasattr(enemy, 'reward'):
                    self.gold += enemy.reward
            
            # Wave结束检测
            if self.wave_active and self.enemies_to_spawn == 0 and len(self.enemies) == 0:
                self.wave_active = False
                print(f"第{self.wave}波结束！点击【Next Wave】按钮开始Next Wave")
        except Exception as e:
            import traceback
            print(f"[CRASH] {e}")
            traceback.print_exc()
            raise
    
    def draw(self, screen):
        # 清空屏幕 - 深色背景
        screen.fill(COLORS['bg'])
        
        # 绘制地图
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if y < len(self.map_data) and x < len(self.map_data[y]):
                    tile = self.map_data[y][x]
                    if tile == 0:  # 草地
                        color = COLORS['grass']
                    elif tile == 1:  # 道路
                        color = COLORS['path']
                    elif tile == 2:  # 水域
                        color = COLORS['water']
                    elif tile == 3:  # 石头
                        color = COLORS['stone']
                    else:
                        color = (0, 0, 0)
                    
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (0, 0, 0, 50), rect, 1)
        
        # 绘制Base
        base_rect = pygame.Rect(self.base_pos[0] * TILE_SIZE, self.base_pos[1] * TILE_SIZE, 
                               TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLORS['base'], base_rect)
        pygame.draw.rect(screen, (255, 255, 0), base_rect, 3)
        
        # 绘制防御塔
        for tower in self.towers:
            tower.draw(screen)
        
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # 绘制子弹
        for proj in self.projectiles:
            proj.draw(screen)
        
        # 绘制UI
        self.draw_ui(screen)
    
    def draw_ui(self, screen):
        # 顶部信息栏 - 深色面板
        pygame.draw.rect(screen, COLORS['panel'], (0, 0, WIDTH, 50))
        pygame.draw.line(screen, COLORS['border'], (0, 50), (WIDTH, 50), 2)
        
        # Gold
        gold_text = font.render(f"Gold: {self.gold}", True, COLORS['gold'])
        screen.blit(gold_text, (10, 15))
        
        # Wave
        wave_text = font.render(f"Wave: {self.wave}", True, COLORS['text'])
        screen.blit(wave_text, (150, 15))
        
        # Base生命
        hp_text = font.render(f"Base: {self.base_health}", True, (255, 80, 80))
        screen.blit(hp_text, (280, 15))
        
        # Next Wave按钮 - 居中
        btn_x = WIDTH // 2 - 50
        btn_y = 5
        btn_w, btn_h = 100, 35
        can_start = not self.wave_active and self.wave_cooldown <= 0
        btn_color = COLORS['tower1'] if can_start else (80, 80, 80)
        self.btn_next_wave_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(screen, btn_color, self.btn_next_wave_rect)
        pygame.draw.rect(screen, COLORS['border'], self.btn_next_wave_rect, 2)
        btn_text = font.render("Next Wave", True, (255, 255, 255))
        screen.blit(btn_text, (btn_x + btn_w // 2 - btn_text.get_width() // 2, btn_y + 8))
        
        # 防御塔选择 - 底部栏
        bar_y = HEIGHT - 55
        pygame.draw.rect(screen, COLORS['panel'], (0, bar_y, WIDTH, 55))
        pygame.draw.line(screen, COLORS['border'], (0, bar_y), (WIDTH, bar_y), 2)
        
        tower_keys = list(TOWER_TYPES.keys())
        for i, key in enumerate(tower_keys):
            tower = TOWER_TYPES[key]
            x = 20 + i * 150
            y = bar_y + 3
            tw, th = 140, 48
            selected = key == self.selected_tower_type
            btn_color = tower['color'] if selected else (60, 60, 60)
            pygame.draw.rect(screen, btn_color, (x, y, tw, th))
            pygame.draw.rect(screen, COLORS['border'], (x, y, tw, th), 2)
            name_txt = font.render(tower['name'], True, (255, 255, 255))
            cost_txt = font.render(f"${tower['cost']}", True, (200, 200, 200))
            dmg_txt = font.render(f"DMG:{tower['damage']}", True, (180, 180, 180))
            screen.blit(name_txt, (x + 8, y + 5))
            screen.blit(cost_txt, (x + 8, y + 22))
            screen.blit(dmg_txt, (x + 8, y + 35))
        
        # 放置模式提示
        if self.placing_tower:
            text = font.render("Click to place | ESC cancel", True, (255, 255, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 55))
        
        # Wave冷却提示
        if not self.wave_active and self.wave_cooldown > 0:
            secs = self.wave_cooldown // 60
            text = font.render(f"Next Wave将在 {secs} 秒后自动开始...", True, COLORS['text'])
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 10))
        
        # 游戏结束
        if self.game_over:
            text = font_big.render("Game Over!", True, (255, 0, 0))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.placing_tower = False
            elif event.key == pygame.K_1:
                self.selected_tower_type = 'gun'
            elif event.key == pygame.K_2:
                self.selected_tower_type = 'cannon'
            elif event.key == pygame.K_3:
                self.selected_tower_type = 'sniper'
            elif event.key == pygame.K_4:
                self.selected_tower_type = 'ice'
            elif event.key == pygame.K_SPACE:
                if not self.wave_active:
                    self.start_wave()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                mx, my = event.pos
                self.mouse_pos = (mx, my)
                # 坐标验证
                if mx < 0 or my < 0 or mx > WIDTH or my > HEIGHT:
                    print(f"[WARN] 鼠标坐标异常: ({mx},{my})")
                    return
                # 检查Next Wave按钮
                btn = getattr(self, 'btn_next_wave_rect', None)
                if btn and btn.collidepoint(mx, my):
                    if not self.wave_active:
                        self.start_wave()
                    return
                # 左键放置
                if event.button == 1:
                    if self.placing_tower:
                        self.place_tower()
                    else:
                        self.enter_placement_mode()
            except Exception as e:
                import traceback
                print(f"[CRASH in MOUSEBUTTONDOWN]: {e}")
                traceback.print_exc()
        
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        
        return True
    
    def enter_placement_mode(self):
        """进入放置模式"""
        if self.gold >= TOWER_TYPES[self.selected_tower_type]['cost']:
            self.placing_tower = True
    
    def place_tower(self):
        """放置防御塔"""
        # 将鼠标坐标转换为地图坐标
        mx, my = self.mouse_pos
        tile_x = mx // TILE_SIZE
        tile_y = my // TILE_SIZE
        
        # 检查是否可以放置
        if (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT and 
            tile_y < len(self.map_data) and tile_x < len(self.map_data[tile_y]) and
            self.map_data[tile_y][tile_x] == 0):  # 只能放在草地上
            cost = TOWER_TYPES[self.selected_tower_type]['cost']
            if self.gold >= cost:
                self.gold -= cost
                self.map_data[tile_y][tile_x] = 4  # 标记为塔位
                tower = Tower(tile_x, tile_y, self.selected_tower_type)
                self.towers.append(tower)
                self.placing_tower = False


class Enemy:
    """敌人"""
    def __init__(self, x, y, hp, speed, reward, color, enemy_type):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.reward = reward
        self.color = color
        self.enemy_type = enemy_type
        self.alive = True
        self.path_index = 0
        self.slow_timer = 0
        self.size = 12
    
    def update(self, path_points, map_data):
        if not self.alive:
            return None
        
        # 减速效果
        current_speed = self.speed
        if self.slow_timer > 0:
            current_speed *= 0.5
            self.slow_timer -= 1
        
        # 沿路径移动
        if self.path_index < len(path_points) - 1:
            target_x, target_y = path_points[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist < 5:
                self.path_index += 1
            else:
                self.x += (dx / dist) * current_speed
                self.y += (dy / dist) * current_speed
        else:
            # 到达终点
            self.alive = False
            return 'reached_base'
        
        return None
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            return True
        return False
    
    def draw(self, screen):
        if not self.alive:
            return
        
        # 身体
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        
        # 血条
        bar_width = 24
        bar_height = 4
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (255, 0, 0), 
                        (int(self.x) - bar_width // 2, int(self.y) - 20, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                        (int(self.x) - bar_width // 2, int(self.y) - 20, 
                         int(bar_width * hp_ratio), bar_height))


class Tower:
    """防御塔"""
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.stats = TOWER_TYPES[tower_type].copy()
        self.cooldown = 0
        self.level = 1
    
    def update(self, enemies, projectiles):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        
        # 寻找目标
        target = None
        min_dist = float('inf')
        
        for enemy in enemies:
            if not enemy.alive:
                continue
            
            dx = enemy.x - (self.x * TILE_SIZE + TILE_SIZE // 2)
            dy = enemy.y - (self.y * TILE_SIZE + TILE_SIZE // 2)
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist <= self.stats['range'] and dist < min_dist:
                min_dist = dist
                target = enemy
        
        if target:
            # 发射子弹
            proj_x = self.x * TILE_SIZE + TILE_SIZE // 2
            proj_y = self.y * TILE_SIZE + TILE_SIZE // 2
            projectiles.append(Projectile(proj_x, proj_y, target, self))
            self.cooldown = self.stats['fire_rate']
    
    def draw(self, screen):
        # 塔基座
        color = self.stats['color']
        rect = pygame.Rect(self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 5, 
                          TILE_SIZE - 10, TILE_SIZE - 10)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        
        # 等级标记
        if self.level > 1:
            pygame.draw.circle(screen, (255, 255, 0), 
                             (int(self.x * TILE_SIZE + TILE_SIZE // 2), 
                              int(self.y * TILE_SIZE + TILE_SIZE // 2)), 
                             3)


class Projectile:
    """子弹"""
    def __init__(self, x, y, target, tower):
        self.x = x
        self.y = y
        self.target = target
        self.tower = tower
        self.speed = tower.stats['projectile_speed']
        self.damage = tower.stats['damage']
        self.alive = True
        self.slow_factor = tower.stats.get('slow_factor', 0)
        self.splash_radius = tower.stats.get('splash_radius', 0)
        self.size = tower.stats['projectile_size']
    
    def update(self, enemies):
        if not self.alive:
            return
        
        if not self.target.alive:
            self.alive = False
            return
        
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist < 10:
            # 命中
            if self.splash_radius > 0:
                # 范围DMG
                for enemy in enemies:
                    if not enemy.alive:
                        continue
                    edx = enemy.x - self.target.x
                    edy = enemy.y - self.target.y
                    edist = math.sqrt(edx * edx + edy * edy)
                    if edist <= self.splash_radius:
                        enemy.take_damage(self.damage * (1 - edist / self.splash_radius))
            else:
                self.target.take_damage(self.damage)
                if self.slow_factor > 0:
                    self.target.slow_timer = 60
            
            self.alive = False
        else:
            # 移动
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
    
    def draw(self, screen):
        if not self.alive:
            return
        
        color = self.tower.stats['color']
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)


# ── 主循环 ──
game = Game()
running = True

# 测试模式：从stdin读取命令
import threading
def read_input():
    try:
        for line in sys.stdin:
            line = line.strip()
            if line == 'next_wave':
                game.start_wave()
            elif line == 'place_gun':
                game.selected_tower_type = 'gun'
                game.placing_tower = True
            elif line == 'place_cannon':
                game.selected_tower_type = 'cannon'
                game.placing_tower = True
            elif line == 'place_sniper':
                game.selected_tower_type = 'sniper'
                game.placing_tower = True
            elif line == 'place_ice':
                game.selected_tower_type = 'ice'
                game.placing_tower = True
            elif line == 'cancel':
                game.placing_tower = False
            elif line.startswith('place_at '):
                parts = line.split()
                if len(parts) >= 3:
                    x, y = int(parts[1]), int(parts[2])
                    game.mouse_pos = (x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2)
                    game.place_tower()
            elif line == 'quit':
                running = False
    except:
        pass

threading.Thread(target=read_input, daemon=True).start()

while running:
    for event in pygame.event.get():
        if not game.handle_event(event):
            running = False
    
    game.update()
    game.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
