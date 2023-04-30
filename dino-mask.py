import pygame
import os
import random
import sys

pygame.init()

window_height = 600
window_width = 1100
# 建立視窗
window = pygame.display.set_mode((window_width, window_height))

# 顏色
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

# Load 圖檔
# mask_plus
DINO_START_DEAD = [pygame.image.load(os.path.join("./Assets/Dino", "DinoStart.png")).convert_alpha(),
                pygame.image.load(os.path.join("./Assets/Dino", "DinoDead.png")).convert_alpha()]
RUNNING_LIST = [pygame.image.load(os.path.join("./Assets/Dino", "DinoRun1.png")).convert_alpha(),
                pygame.image.load(os.path.join("./Assets/Dino", "DinoRun2.png")).convert_alpha()]
JUMPING_IMG = pygame.image.load(os.path.join("./Assets/Dino", "DinoJump.png")).convert_alpha()
DUCKING_LIST = [pygame.image.load(os.path.join("./Assets/Dino", "DinoDuck1.png")).convert_alpha(),
                pygame.image.load(os.path.join("./Assets/Dino", "DinoDuck2.png")).convert_alpha()]

SMALL_CACTUS_LIST = [pygame.image.load(os.path.join("./Assets/Cactus", "SmallCactus1.png")).convert_alpha(),
                     pygame.image.load(os.path.join("./Assets/Cactus", "SmallCactus2.png")).convert_alpha(),
                     pygame.image.load(os.path.join("./Assets/Cactus", "SmallCactus3.png")).convert_alpha()]

LARGE_CACTUS_LIST = [pygame.image.load(os.path.join("./Assets/Cactus", "LargeCactus1.png")).convert_alpha(),
                     pygame.image.load(os.path.join("./Assets/Cactus", "LargeCactus2.png")).convert_alpha(),
                     pygame.image.load(os.path.join("./Assets/Cactus", "LargeCactus3.png")).convert_alpha()]

BIRD_LIST = [pygame.image.load(os.path.join("./Assets/Bird", "Bird1.png")).convert_alpha(),
             pygame.image.load(os.path.join("./Assets/Bird", "Bird2.png")).convert_alpha()]

CLOUD = pygame.image.load(os.path.join("./Assets/Other", "Cloud.png")).convert_alpha()

# Load 步道 (background)
BG = pygame.image.load(os.path.join("./Assets/Other", "Track.png"))

GAMEOVER = [pygame.image.load(os.path.join("./Assets/Other", "GameOver.png")), 
            pygame.image.load(os.path.join("./Assets/Other", "Reset.png"))]

# Class
# 文字物件
class Text:
    def __init__(self, text: str, size: int, color: pygame.Color, position=(0, 0)):
        self.font = pygame.font.SysFont("freesansbold.ttf", size)
        self.surface = self.font.render(text, True, color)
        self.rect = self.surface.get_rect()  # 文字框起
        self.rect.center = position  # 文字的中心位置(參數)

    def draw(self, screen: pygame.display):
        screen.blit(self.surface, self.rect)

# 雲朵物件
class Cloud:
    def __init__(self):
        self.image = CLOUD  # 載入雲朵圖
        self.x = window_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:  # 若雲朵開始走到左邊視窗盡頭並消失
                self.x = window_width + random.randint(2500, 3000)  # 則將雲朵位置重新設在視窗外隨機800到1000
                self.y = random.randint(50, 100)

    def draw(self, screen : pygame.display):
        screen.blit(self.image, (self.x, self.y))

# 恐龍物件
class Dinosaur(pygame.sprite.Sprite):   # mask_plus
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 7
    
    def __init__(self):
        # 定義變數
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.step_index = 0 
        self.jump_vel = self.JUMP_VEL 

        # Load 圖檔
        self.duck_img_list = DUCKING_LIST
        self.run_img_list = RUNNING_LIST
        self.jump_img = JUMPING_IMG
        self.image = self.run_img_list[0]  # 第一步是跑1

        # 把恐龍腳色框列
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS

        #在最後的部分加上mask屬性
        self.mask = pygame.mask.from_surface(self.image)  # mask_plus

    def run(self):
        self.image = self.run_img_list[self.step_index // 5]  # 每五個step_index換一張圖
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1


    def duck(self):
        self.image = self.duck_img_list[self.step_index // 5]  # 依 step_index 決定恐龍的蹲下圖片，每五個step_index換一張圖
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4  # 依目前的跳躍速度來移動小恐龍的y座標值
            self.jump_vel -= 0.5  # 若jump_vel小於0則代表小恐龍逐漸往下掉
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    # 更新動作
    def update(self, user_input : pygame.key):
        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True   # 跳
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True   # 蹲
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True    # 跑
            self.dino_jump = False    
        
        # 判斷狀態
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        # 歸零 step
        if self.step_index >= 10:
            self.step_index = 0
        
    def draw(self, screen : pygame.display):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# 障礙物
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, imageList : list, typeObject : int):
        self.image_list = imageList
        self.type = typeObject  # 用序號標示
        self.rect = self.image_list[self.type].get_rect()
        self.rect.x = window_width + random.randint(800, 1000)
        
        self.image = self.image_list[self.type]
        self.mask = pygame.mask.from_surface(self.image)
        
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        self.rect.x -= game_speed

    def draw(self, screen : pygame.display):
        screen.blit(self.image_list[self.type], (self.rect.x, self.rect.y))

# 大仙人掌
class LargeCactus(Obstacle):
    def __init__(self, image_list : list):
        self.type = random.randint(0, 2)
        # pygame.sprite.Sprite.__init__(self)
        Obstacle.__init__(self,image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.y = 300

# 小仙人掌
class SmallCactus(Obstacle):
    def __init__(self, image_list : list):
        self.type = random.randint(0, 2)
        # pygame.sprite.Sprite.__init__(self)
        Obstacle.__init__(self,image_list, self.type)  # 繼承障礙物屬性與動作

        self.rect.y = 325

# 翼龍
class Bird(Obstacle):
    def __init__(self, image_list : list):
        self.type = 0   # 用不到但只是想符合class初始化
        # pygame.sprite.Sprite.__init__(self)
        Obstacle.__init__(self,image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.y = 250
        self.index = 0  # 用 index 來拍動翅膀
        
    def draw(self, screen : pygame.display):
        if self.index >= 10:    # 後寫
            self.index = 0
            
        screen.blit(self.image_list[self.index//5], self.rect)
        self.index += 1

# 開始/結算畫面
def menu(death_bool):
    death_text_position = (window_width//2, window_height//2 + 30)
    score_text_position = (window_width//2, window_height//2 + 80)
    dino_position = (window_width//2 - 20, window_height//2 - 110)
    gameover_position = (window_width//2 - 180, window_height//2 - 130)
    reset_position = (window_width//2 - 30, window_height//2 - 80)
    running = True
    while running:
        window.fill(WHITE)
        
        if death_bool == False: # false 代表 沒死(開始
            display_text = Text("Press Space to Start", 40, BLACK, death_text_position)
            window.blit(DINO_START_DEAD[0], dino_position)
        
        elif death_bool == True:
            score_text = Text("Your Score: " + str(points), 40, BLACK, score_text_position)
            score_text.draw(window)
            display_text = Text("Press Space to Restart", 40, BLACK, death_text_position)
            window.blit(GAMEOVER[0], gameover_position)
            window.blit(GAMEOVER[1], reset_position)

        
        display_text.draw(window)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                elif event.key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()
    sys.exit()

def main() :
    # 變數
    global game_speed
    game_speed = 15 # 背景移動速度
    x_pos_bg = 0    # 背景x座標
    y_pos_bg = 380  # 背景y座標

    # 分數
    global points
    points = 0

    # Clock(變數)
    clock = pygame.time.Clock()
    # 雲朵(變數)
    cloud = Cloud()
    # 小恐龍(變數)
    dinosaur = Dinosaur()
    # 障礙物(變數)
    obstacles = []

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # 塗白
        window.fill(WHITE)
        # 背景
        image_width = BG.get_width()
        window.blit(BG, (x_pos_bg, y_pos_bg))
        window.blit(BG, (x_pos_bg + image_width, y_pos_bg))
        
        x_pos_bg -= game_speed  # 背景移動
        if x_pos_bg <= -image_width:
            window.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        # 雲朵
        cloud.update()
        cloud.draw(window)
        # 分數
        points += 1
        if points % 100 == 0:
            game_speed += 1
            
        text_position = (1000, 40)
        text = Text("Points: " + str(points), 30, BLACK, text_position)
        text.draw(window)
        # 小恐龍
        user_input = pygame.key.get_pressed()  # 接收玩家指令
        dinosaur.update(user_input)  # 更新恐龍動作
        dinosaur.draw(window)  # 將恐龍換上     
        # 障礙物
        if len(obstacles) == 0:
            rand = random.randint(0, 2)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS_LIST))  
            if rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS_LIST))  
            if rand == 2:
                obstacles.append(Bird(BIRD_LIST))                
        
        # 顯示障礙物
        for obstacle in obstacles:
            obstacle.update()  # 障礙物移動
            obstacle.draw(window)  # 更新動畫
            
            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.pop()

            if pygame.sprite.collide_mask(dinosaur, obstacle):
                dinosaur.image = DINO_START_DEAD[1]
                dinosaur.draw(window)
                pygame.display.update() #加上這一行，看到更精確的畫面。
                pygame.time.delay(1000)  # 延遲0.1秒
                menu(True)

        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu(False)
