# 學習用OOP寫程式
import pygame
import os
import random
import sys

pygame.init()

window_height = 600
window_width = 1100

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("小恐龍")

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

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
BACKGROUND = pygame.image.load(os.path.join("./Assets/Other", "Track.png"))

GAMEOVER = [pygame.image.load(os.path.join("./Assets/Other", "GameOver.png")), 
            pygame.image.load(os.path.join("./Assets/Other", "Reset.png"))]

GADGET = [pygame.image.load(os.path.join("./Assets/Other", "wings.png")), 
          pygame.image.load(os.path.join("./Assets/Other", "down-arrow.png")), 
          pygame.image.load(os.path.join("./Assets/Other", "jump.png")), 
          pygame.image.load(os.path.join("./Assets/Other", "stars.png"))]

jump_sound_effect = pygame.mixer.Sound("./Assets/Music/jump_sound_effect.mp3")
death_sound_effect = pygame.mixer.Sound("./Assets/Music/death_sound_effect.mp3")
gadget_sound_effect = pygame.mixer.Sound("./Assets/Music/gadget_sound_effect.mp3")

class Text:
    def __init__(self, text, size, color, position=(0,0)):
        self.font = pygame.font.SysFont("freesansbold.ttf", size)
        self.surface = self.font.render(text, True, color)
        self.rect = self.surface.get_rect()
        self.rect.center = position
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        
class Cloud:
    def __init__(self):
        self.image = CLOUD
        self.x = window_width + random.randint(800,1000)
        self.y = random.randint(50, 100)
        self.width = self.image.get_width()
    
    def update(self):
        self.x -= game_speed
        if self.x <= -(self.width):
            self.x = window_width + random.randint(2500,3000)
            self.y = random.randint(50,100)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
class Dinosaur(pygame.sprite.Sprite):
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    JUMP_VEL = 7
    gravity = 0.5
    
    def __init__(self):
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.step_index = 0 
        # Load 圖檔
        self.duck_img_list = DUCKING_LIST
        self.run_img_list = RUNNING_LIST
        self.jump_img = JUMPING_IMG
        self.image = self.run_img_list[0]  # 步伐 0 1 0 1
        # 恐龍框
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        # create mask object
        self.mask = pygame.mask.from_surface(self.image)  # mask_plus
        
    def run(self):
        self.image = self.run_img_list[self.step_index//5]
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.step_index += 1
        
    def duck(self):
        if interrupt_flag == True:
            return
        else:
            self.image = self.duck_img_list[self.step_index//5]
            self.rect = self.image.get_rect()
            self.rect.x = self.x_pos
            self.rect.y = self.y_pos_duck
            self.step_index += 1
        
    def jump(self):
        if interrupt_flag == True:
            self.jump_vel = self.JUMP_VEL
            self.dino_jump = False
            return
        else:
            self.image = self.jump_img
            self.rect = self.image.get_rect()
            self.rect.x = self.x_pos
            self.rect.y = self.y_pos

            self.y_pos -= self.jump_vel *4
            self.jump_vel -= self.gravity   # jump_vel 正上升 負下降
            
            if self.y_pos >= 310:
                self.y_pos = 310
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL 
            
    def update(self, user_input):
        if user_input[pygame.K_UP] and not self.dino_jump:
            pygame.mixer.Sound.play(jump_sound_effect)
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
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, img_list, obj_type):
        # pygame.sprite.Sprite.__init__(self)   # 換個寫法
        super(Obstacle, self).__init__()
        self.img_list = img_list
        self.type = obj_type
        self.image = self.img_list[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = window_width + random.randint(600, 1000)
        self.mask = pygame.mask.from_surface(self.image)
        
        
    def update(self):
        self.rect.x -= game_speed
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class LargeCactus(Obstacle):
    def __init__(self, img_list):
        self.type = random.randint(0,2)
        super(LargeCactus, self).__init__(img_list, self.type)
        self.rect.y = 300
        
class SmallCactus(Obstacle):
    def __init__(self, img_list):
        self.type = random.randint(0,2)
        super(SmallCactus, self).__init__(img_list, self.type)
        self.rect.y = 325
        
class Bird(Obstacle):
    def __init__(self, img_list):
        self.type = 0
        super(Bird, self).__init__(img_list, self.type)
        self.rect.y = 250
        self.index = 0  # 拍動翅膀
        
    def draw(self, screen):
        if self.index >= 10:
            self.index = 0
            
        screen.blit(self.img_list[self.index//5], self.rect)
        self.index += 1


class Gadget(pygame.sprite.Sprite):
    def __init__(self):
        super(Gadget, self).__init__()
        self.type = random.randint(0,3)
        self.image = GADGET[self.type]
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.eaten = False
        self.down_flag = False
    
        self.rect.x = window_width + random.randint(600, 1000)
        self.rect.y = 175
        
    def update(self):
        self.rect.x -= game_speed
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def eat(self, dino):
        self.rect.x = dino.rect.x
        self.rect.y = dino.rect.y - 80
    
    def action(self):
        if self.type == 0:  # wings
            return True
        elif self.type == 1:    # 中斷跳
            press = pygame.key.get_pressed()
            if press[pygame.K_DOWN]:   return True
        else:   return False
    
    def rise(self, dino):
        if dino.y_pos > 100:
            dino.y_pos -= 10
        else:
            dino.y_pos = 100
        return False
        
    def fall(self, dino):
        if dino.y_pos < 310:
            dino.y_pos += 10
        else:
            dino.y_pos= 310
        
        self.dino_jump = False
        return False
    
    def pressdown(self, dino):
        press = pygame.key.get_pressed()
        if press[pygame.K_DOWN]:
            self.down_flag = True
            
        if self.down_flag:
            if dino.y_pos < 310:
                dino.y_pos += 10
            else:
                dino.y_pos= 310
                self.down_flag = False
        return True
    
    def jumphigh(self, dino):
        dino.gravity = 0.25
        return True
        
    def end_jumphigh(self, dino):
        dino.gravity = 0.5
        return True
        
    def use_ability(self, dino):
        if self.type == 0:  # wings
            if not endding:     return self.rise(dino)
            else:   return self.fall(dino)
        if self.type == 1 :    # 中斷跳
            return self.pressdown(dino)
        elif self.type == 2:    # jumphigh shoe
            if not endding: return self.jumphigh(dino)
            else:   return self.end_jumphigh(dino)
        elif self.type == 3:    # star
            return ignore_collide()

def ignore_collide():
    return False

def reset_collide():
    return True

gadgetEnd = pygame.USEREVENT +0
gadgetTimeOut = pygame.USEREVENT +1

def main():
    global game_speed
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380
    
    global points
    points = 0
    
    toCollide = True   
    global endding
    endding = False
    
    global interrupt_flag
    interrupt_flag = False
    
    clock = pygame.time.Clock()
    cloud = Cloud()
    dinosaur = Dinosaur()
    obstacles = []  # 障礙物 (用list操作)
    gadgets = []    # 道具 (用list操作)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == gadgetEnd:
                endding = True
                
            if event.type == gadgetTimeOut: 
                endding = False
                interrupt_flag = False
                toCollide = reset_collide()
                gadgets.pop()
                pygame.time.set_timer(gadgetEnd, 0, 1)
                pygame.time.set_timer(gadgetTimeOut, 0, 1)
                        
        window.fill(WHITE)
        # 背景
        bg_image_width = BACKGROUND.get_width()
        window.blit(BACKGROUND, (x_pos_bg, y_pos_bg))
        window.blit(BACKGROUND, (x_pos_bg+bg_image_width, y_pos_bg))
        x_pos_bg -= game_speed
        if x_pos_bg <= -bg_image_width:
            window.blit(BACKGROUND, (x_pos_bg+bg_image_width, y_pos_bg))
            x_pos_bg = 0
            
        # cloud
        cloud.update()
        cloud.draw(window)
        
        points += 1
        if points % 100 == 0:
            game_speed += 0.5
        
        text_position = (1000, 40)
        text = Text("Points: " + str(points), 30, BLACK, text_position)
        text.draw(window)
            
        # 小恐龍
        user_input = pygame.key.get_pressed()  # 接收玩家指令
        dinosaur.update(user_input)  # 更新恐龍動作
        
        for gadget in gadgets:
            if gadget.eaten == True:
                toCollide = gadget.use_ability(dinosaur)  # 使用道具技能  # 回傳"True"關閉碰撞功能
                gadget.eat(dinosaur)
            
        dinosaur.draw(window)
        # 障礙物
        # generate
        if len(obstacles) == 0:
            rand = random.randint(0,2)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS_LIST))
            if rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS_LIST))
            if rand == 2:
                obstacles.append(Bird(BIRD_LIST))
        # display
        for obstacle in obstacles:
            obstacle.update()   # move (game_speed)
            obstacle.draw(window)   
            
            if obstacle.rect.x < -(obstacle.rect.width):
                obstacles.pop()
            
            if toCollide == True:
                if pygame.sprite.collide_mask(dinosaur, obstacle):
                    pygame.mixer.Sound.play(death_sound_effect)
                    dinosaur.image = DINO_START_DEAD[1]
                    dinosaur.draw(window)
                    pygame.display.update() #加上這一行，看到更精確的畫面。
                    pygame.time.delay(70)  # 延遲0.07秒
                    menu(True)
                    
        # 道具
        # generate (each 25%)
        if len(gadgets) == 0:
            rand = random.randint(1,401)
            if rand % 4 == 0:
                gadgets.append(Gadget())
        # display
        if len(gadgets) > 0:
            for gadget in gadgets:
                if not gadget.eaten:   gadget.update()  # 向左移動
                gadget.draw(window)
                
                if pygame.sprite.collide_mask(dinosaur, gadget):
                    pygame.mixer.Sound.play(gadget_sound_effect)
                    gadget.eat(dinosaur)
                    gadget.eaten = True
                    interrupt_flag = gadget.action()
                    pygame.time.set_timer(gadgetEnd, 3000, 1)
                    pygame.time.set_timer(gadgetTimeOut, 3500, 1)
                    gadget.draw(window)
                    pygame.display.update()
                elif gadget.rect.x < -(gadget.rect.width):
                    gadgets.pop()
                    
        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()
        
def menu(death_bool):
    pygame.time.set_timer(gadgetEnd, 0, 1)
    pygame.time.set_timer(gadgetTimeOut, 0, 1)
    death_text_position = (window_width//2, window_height//2 + 30)
    score_text_position = (window_width//2, window_height//2 + 80)
    dino_position = (window_width//2 - 20, window_height//2 - 110)
    gameover_position = (window_width//2 - 180, window_height//2 - 130)
    reset_position = (window_width//2 - 30, window_height//2 - 80)

    running = True
    while running:
        window.fill(WHITE)
        
        if death_bool == False: # Not dead (Start)
            display_text = Text("Press Space to Start", 40, BLACK, death_text_position)
            window.blit(RUNNING_LIST[0], dino_position)
        
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
    
if __name__ == "__main__":
    menu(False)