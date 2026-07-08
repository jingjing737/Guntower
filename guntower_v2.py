"""
GunTower 复刻 - 美化版
参考 GunTower.sb3 的素材和UI设计
"""
import pygame
import random
import math
import os

# ── 初始化 ──
pygame.init()
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GunTower - 方块塔防")
clock = pygame.time.Clock()
font = pygame.font.SysFont("microsoftyahei", 16)
font_big = pygame.font.SysFont("microsoftyahei", 24)

# ── 常量 ──
TILE_SIZE = 70
MAP_WIDTH = 15
MAP_HEIGHT = 10
FPS = 60

# ── GunTower风格配色 ──
COLORS = {
    'bg': (30, 30, 30),
    'panel': (51, 51, 51),
    'panel_border': (100, 100, 100),
    'text': (200, 200, 200),
    'gold': (255, 215, 0),
    'green': (0, 179, 15),
    'green_dark': (0, 127, 11),
    'yellow': (230, 164, 0),
    'blue': (0, 164, 230),
    'red': (179, 0, 0),
    'light_blue': (178, 223, 255),
    'purple': (128, 0, 128),
    'grass': (100, 180, 100),
    'path': (180, 160, 120),
    'water': (80, 140, 200),
    'stone': (140, 140, 140),
}

# ── 地图设计 ──
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

ENEMY_PATH = [
    (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (5, 4), (5, 5), (6, 5), (7, 5),
    (7, 6), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (11, 8), (11, 9)
]

# ── 防御塔定义 ──
TOWER_TYPES = {
    'gun': {
        'name': '机枪',
        'cost': 50,
        'damage': 8,
        'range': 180,
        'fire_rate': 15,
        'color': COLORS['green'],
        'dark_color': COLORS['green_dark'],
        'projectile_speed': 10,
        'projectile_size': 3,
    },
    'cannon': {
        'name': '炮塔',
        'cost': 100,
        'damage': 25,
        'range': 150,
        'fire_rate': 60,
        'color': COLORS['yellow'],
        'dark_color': (178, 128, 0),
        'projectile_speed': 6,
        'projectile_size': 6,
        'splash_radius': 40,
    },
    'sniper': {
        'name': '狙击',
        'cost': 75,
        'damage': 50,
        'range': 250,
        'fire_rate': 120,
        'color': COLORS['red'],
        'dark_color': (127, 0, 0),
        'projectile_speed': 15,
        'projectile_size': 2,
    },
    'ice': {
        'name': '冰塔',
        'cost': 60,
        'damage': 3,
        'range': 160,
        'fire_rate': 30,
        'color': COLORS['light_blue'],
        'dark_color': (80, 160, 200),
        'projectile_speed': 8,
        'projectile_size': 4,
        'slow_factor': 0.4,
    },
}

ENEMY_TYPES = {
    'normal': {'hp': 30, 'speed': 1.0, 'reward': 5, 'color': (200, 100, 100)},
    'fast': {'hp': 20, 'speed': 1.8, 'reward': 8, 'color': (255, 180, 100)},
    'tank': {'hp': 80, 'speed': 0.6, 'reward': 15, 'color': (150, 100, 200)},
    'boss': {'hp': 200, 'speed': 0.4, 'reward': 50, 'color': (255, 0, 255)},
}


class Game:
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
        self.path_points = [(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                           for x, y in ENEMY_PATH]
        self.base_pos = ENEMY_PATH[-1]
        self.map_data = [row[:] for row in MAP_DESIGN]
        self.hover_tile = None
        self.btn_next_wave_rect = None
        self.btn_buy_rect = None
        self.btn_sell_rect = None
        self.btn_speed_rect = None
        self.build_menu_open = False
        self.build_menu_pos = (0, 0)
        self.selected_tower_for_sell = None
        self.speed_up = False
    
    def start_wave(self):
        if self.wave_active:
            return
        self.wave += 1
        self.wave_active = True
        self.enemies_to_spawn = 5 + self.wave * 2
        self.spawn_timer = 0
        self.spawn_interval = max(20, 60 - self.wave * 2)
    
    def spawn_enemy(self):
        if self.enemies_to_spawn <= 0:
            return
        rand = random.random()
        if rand < 0.6:
            etype = 'normal'
        elif rand < 0.85:
            etype = 'fast'
        elif rand < 0.95:
            etype = 'tank'
        else:
            etype = 'boss'
        tmpl = ENEMY_TYPES[etype]
        hp = tmpl['hp'] * (1 + self.difficulty * 0.2)
        speed = tmpl['speed'] * (1 + self.difficulty * 0.1)
        enemy = Enemy(self.path_points[0][0], self.path_points[0][1], hp, speed,
                     tmpl['reward'], tmpl['color'], etype)
        self.enemies.append(enemy)
        self.enemies_to_spawn -= 1
    
    def update(self):
        if self.game_over:
            return
        if self.enemies_to_spawn > 0:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_enemy()
                self.spawn_timer = 0
        for enemy in self.enemies:
            result = enemy.update(self.path_points, self.map_data)
            if result == 'reached_base':
                self.base_health -= 10
                if self.base_health <= 0:
                    self.game_over = True
        for tower in self.towers:
            tower.update(self.enemies, self.projectiles)
        for proj in self.projectiles:
            proj.update(self.enemies)
        self.enemies = [e for e in self.enemies if e.alive]
        self.projectiles = [p for p in self.projectiles if p.alive]
        for enemy in self.enemies:
            if not enemy.alive and hasattr(enemy, 'reward'):
                self.gold += enemy.reward
        if self.wave_active and self.enemies_to_spawn == 0 and len(self.enemies) == 0:
            self.wave_active = False
            self.wave_cooldown = 180
    
    def draw(self, screen):
        screen.fill(COLORS['bg'])
        self.draw_map(screen)
        self.draw_base(screen)
        for tower in self.towers:
            tower.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for proj in self.projectiles:
            proj.draw(screen)
        self.draw_hover(screen)
        self.draw_build_menu(screen)
        self.draw_ui(screen)
    
    def draw_map(self, screen):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if y < len(self.map_data) and x < len(self.map_data[y]):
                    tile = self.map_data[y][x]
                    if tile == 0:
                        color = COLORS['grass']
                    elif tile == 1:
                        color = COLORS['path']
                    elif tile == 2:
                        color = COLORS['water']
                    elif tile == 3:
                        color = COLORS['stone']
                    elif tile == 4:
                        color = (80, 80, 80)
                    else:
                        color = (0, 0, 0)
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (0, 0, 0, 80), rect, 1)
    
    def draw_base(self, screen):
        bx, by = self.base_pos
        rect = pygame.Rect(bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLORS['green'], rect)
        pygame.draw.rect(screen, (255, 255, 0), rect, 3)
        txt = font.render("基地", True, (255, 255, 255))
        screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))
    
    def draw_hover(self, screen):
        if self.hover_tile and self.placing_tower:
            tx, ty = self.hover_tile
            rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            can_place = (0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT and
                        ty < len(self.map_data) and tx < len(self.map_data[ty]) and
                        self.map_data[ty][tx] == 0)
            color = (0, 255, 0, 100) if can_place else (255, 0, 0, 100)
            hover_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(hover_surf, color, (0, 0, TILE_SIZE, TILE_SIZE))
            screen.blit(hover_surf, rect.topleft)
            if can_place:
                tower = TOWER_TYPES[self.selected_tower_type]
                range_surf = pygame.Surface((tower['range'] * 2, tower['range'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(range_surf, (255, 255, 0, 30), (tower['range'], tower['range']), tower['range'])
                screen.blit(range_surf, (rect.centerx - tower['range'], rect.centery - tower['range']))
    
    def draw_build_menu(self, screen):
        if not self.build_menu_open:
            return
        mx, my = self.build_menu_pos
        menu_w, menu_h = 220, 200
        rect = pygame.Rect(mx, my, menu_w, menu_h)
        pygame.draw.rect(screen, COLORS['panel'], rect)
        pygame.draw.rect(screen, COLORS['panel_border'], rect, 2)
        title = font_big.render("建造菜单", True, COLORS['text'])
        screen.blit(title, (mx + 10, my + 10))
        y = my + 40
        for i, (key, tower) in enumerate(TOWER_TYPES.items()):
            ty = y + i * 35
            selected = key == self.selected_tower_type
            btn_color = tower['color'] if selected else (80, 80, 80)
            btn_rect = pygame.Rect(mx + 10, ty, menu_w - 20, 30)
            pygame.draw.rect(screen, btn_color, btn_rect)
            pygame.draw.rect(screen, COLORS['panel_border'], btn_rect, 1)
            txt = font.render(f"{tower['name']} (${tower['cost']})", True, (255, 255, 255))
            screen.blit(txt, (mx + 15, ty + 7))
    
    def draw_ui(self, screen):
        # 顶部栏
        pygame.draw.rect(screen, COLORS['panel'], (0, 0, WIDTH, 45))
        pygame.draw.line(screen, COLORS['panel_border'], (0, 45), (WIDTH, 45), 2)
        
        # 金币
        gold_txt = font.render(f"金币: {self.gold}", True, COLORS['gold'])
        screen.blit(gold_txt, (10, 12))
        
        # 波次
        wave_txt = font.render(f"波次: {self.wave}", True, COLORS['text'])
        screen.blit(wave_txt, (150, 12))
        
        # 基地生命
        hp_txt = font.render(f"基地: {self.base_health}", True, COLORS['red'])
        screen.blit(hp_txt, (280, 12))
        
        # 下一波按钮
        btn_w, btn_h = 120, 35
        btn_x = WIDTH // 2 - btn_w // 2
        btn_y = 5
        can_start = not self.wave_active and self.wave_cooldown <= 0
        btn_color = COLORS['green'] if can_start else (80, 80, 80)
        self.btn_next_wave_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(screen, btn_color, self.btn_next_wave_rect)
        pygame.draw.rect(screen, COLORS['panel_border'], self.btn_next_wave_rect, 2)
        btn_txt = font.render("下一波", True, (255, 255, 255))
        screen.blit(btn_txt, (btn_x + btn_w // 2 - btn_txt.get_width() // 2, btn_y + 8))
        
        # 建造按钮
        build_btn_rect = pygame.Rect(btn_x + btn_w + 10, btn_y, 100, btn_h)
        self.btn_buy_rect = build_btn_rect
        pygame.draw.rect(screen, COLORS['yellow'], build_btn_rect)
        pygame.draw.rect(screen, COLORS['panel_border'], build_btn_rect, 2)
        build_txt = font.render("建造", True, (0, 0, 0))
        screen.blit(build_txt, (build_btn_rect.centerx - build_txt.get_width() // 2, btn_y + 8))
        
        # 加速按钮
        speed_btn_rect = pygame.Rect(btn_x + btn_w + 120, btn_y, 80, btn_h)
        self.btn_speed_rect = speed_btn_rect
        speed_color = COLORS['blue'] if self.speed_up else (60, 60, 100)
        pygame.draw.rect(screen, speed_color, speed_btn_rect)
        pygame.draw.rect(screen, COLORS['panel_border'], speed_btn_rect, 2)
        speed_txt = font.render("加速" if self.speed_up else "正常", True, (255, 255, 255))
        screen.blit(speed_txt, (speed_btn_rect.centerx - speed_txt.get_width() // 2, btn_y + 8))
        
        # 底部栏 - 防御塔快捷选择
        bar_y = HEIGHT - 50
        pygame.draw.rect(screen, COLORS['panel'], (0, bar_y, WIDTH, 50))
        pygame.draw.line(screen, COLORS['panel_border'], (0, bar_y), (WIDTH, bar_y), 2)
        
        for i, (key, tower) in enumerate(TOWER_TYPES.items()):
            bx = 20 + i * 150
            by = bar_y + 5
            bw, bh = 140, 40
            selected = key == self.selected_tower_type
            btn_color = tower['color'] if selected else (60, 60, 60)
            btn_rect = pygame.Rect(bx, by, bw, bh)
            pygame.draw.rect(screen, btn_color, btn_rect)
            pygame.draw.rect(screen, COLORS['panel_border'], btn_rect, 2)
            name_txt = font.render(tower['name'], True, (255, 255, 255))
            cost_txt = font.render(f"${tower['cost']}", True, (200, 200, 200))
            screen.blit(name_txt, (bx + 5, by + 5))
            screen.blit(cost_txt, (bx + 5, by + 22))
        
        # 波次冷却提示
        if not self.wave_active and self.wave_cooldown > 0:
            secs = self.wave_cooldown // 60
            txt = font.render(f"下一波将在 {secs} 秒后开始...", True, COLORS['text'])
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 20))
        
        # 游戏结束
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            text = font_big.render("游戏结束!", True, COLORS['red'])
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
            restart = font.render("按R重新开始", True, COLORS['text'])
            screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.placing_tower = False
                self.build_menu_open = False
            elif event.key == pygame.K_1:
                self.selected_tower_type = 'gun'
            elif event.key == pygame.K_2:
                self.selected_tower_type = 'cannon'
            elif event.key == pygame.K_3:
                self.selected_tower_type = 'sniper'
            elif event.key == pygame.K_4:
                self.selected_tower_type = 'ice'
            elif event.key == pygame.K_b:
                self.build_menu_open = not self.build_menu_open
            elif event.key == pygame.K_r and self.game_over:
                self.__init__()
            elif event.key == pygame.K_SPACE:
                if not self.wave_active and self.wave_cooldown <= 0:
                    self.start_wave()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            self.mouse_pos = (mx, my)
            # 下一波按钮
            if self.btn_next_wave_rect and self.btn_next_wave_rect.collidepoint(mx, my):
                if not self.wave_active and self.wave_cooldown <= 0:
                    self.start_wave()
                return
            # 建造按钮
            if self.btn_buy_rect and self.btn_buy_rect.collidepoint(mx, my):
                self.build_menu_open = not self.build_menu_open
                self.build_menu_pos = (mx - 110, my + 10)
                return
            # 加速按钮
            if self.btn_speed_rect and self.btn_speed_rect.collidepoint(mx, my):
                self.speed_up = not self.speed_up
                return
            # 建造菜单
            if self.build_menu_open:
                menu_w, menu_h = 220, 200
                mmx, mmy = self.build_menu_pos
                for i, key in enumerate(TOWER_TYPES.keys()):
                    ty = mmy + 40 + i * 35
                    btn_rect = pygame.Rect(mmx + 10, ty, menu_w - 20, 30)
                    if btn_rect.collidepoint(mx, my):
                        self.selected_tower_type = key
                        self.build_menu_open = False
                        self.placing_tower = True
                        return
                return
            # 左键放置
            if event.button == 1:
                if self.placing_tower:
                    self.place_tower()
                else:
                    tile_x = mx // TILE_SIZE
                    tile_y = my // TILE_SIZE
                    if (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT and
                        tile_y < len(self.map_data) and tile_x < len(self.map_data[tile_y])):
                        if self.map_data[tile_y][tile_x] == 4:  # 已有塔
                            # 卖塔
                            for tower in self.towers:
                                if tower.x == tile_x and tower.y == tile_y:
                                    refund = int(TOWER_TYPES[tower.tower_type]['cost'] * 0.7)
                                    self.gold += refund
                                    self.map_data[tile_y][tile_x] = 0
                                    self.towers.remove(tower)
                                    self.placing_tower = False
                                    break
                            return
                    self.enter_placement_mode()
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self.hover_tile = (event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE)
        return True
    
    def enter_placement_mode(self):
        if self.gold >= TOWER_TYPES[self.selected_tower_type]['cost']:
            self.placing_tower = True
    
    def place_tower(self):
        mx, my = self.mouse_pos
        tile_x = mx // TILE_SIZE
        tile_y = my // TILE_SIZE
        if (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT and
            tile_y < len(self.map_data) and tile_x < len(self.map_data[tile_y]) and
            self.map_data[tile_y][tile_x] == 0):
            cost = TOWER_TYPES[self.selected_tower_type]['cost']
            if self.gold >= cost:
                self.gold -= cost
                self.map_data[tile_y][tile_x] = 4
                tower = Tower(tile_x, tile_y, self.selected_tower_type)
                self.towers.append(tower)
                self.placing_tower = False


class Enemy:
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
        current_speed = self.speed
        if self.slow_timer > 0:
            current_speed *= 0.5
            self.slow_timer -= 1
        if self.path_index < len(path_points) - 1:
            tx, ty = path_points[self.path_index + 1]
            dx = tx - self.x
            dy = ty - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 5:
                self.path_index += 1
            else:
                self.x += (dx / dist) * current_speed
                self.y += (dy / dist) * current_speed
        else:
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
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        bar_w = 24
        bar_h = 4
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (200, 0, 0), (int(self.x) - bar_w // 2, int(self.y) - 20, bar_w, bar_h))
        pygame.draw.rect(screen, (0, 200, 0), (int(self.x) - bar_w // 2, int(self.y) - 20, int(bar_w * hp_ratio), bar_h))


class Tower:
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
            px = self.x * TILE_SIZE + TILE_SIZE // 2
            py = self.y * TILE_SIZE + TILE_SIZE // 2
            projectiles.append(Projectile(px, py, target, self))
            self.cooldown = self.stats['fire_rate']
    
    def draw(self, screen):
        color = self.stats['color']
        dark = self.stats.get('dark_color', color)
        rect = pygame.Rect(self.x * TILE_SIZE + 4, self.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8)
        pygame.draw.rect(screen, dark, rect)
        pygame.draw.rect(screen, color, (rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4))
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)


class Projectile:
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
            if self.splash_radius > 0:
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
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
    
    def draw(self, screen):
        if not self.alive:
            return
        color = self.tower.stats['color']
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)


game = Game()
running = True
while running:
    for event in pygame.event.get():
        if not game.handle_event(event):
            running = False
    if game.speed_up:
        for _ in range(3):
            game.update()
    else:
        game.update()
    game.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
