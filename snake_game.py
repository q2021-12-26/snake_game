import pygame
import random
import sys
import os

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
GAME_SPEED = 15

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')
clock = pygame.time.Clock()

def get_font(size):
    """获取支持中文的字体"""
    # 尝试使用系统中的中文字体
    chinese_fonts = [
        'Microsoft YaHei', # 微软雅黑
        'SimHei', # 黑体
        'SimSun', # 宋体
        'NSimSun', # 新宋体
        'FangSong', # 仿宋
        'KaiTi', # 楷体
        'Arial Unicode MS'
    ]
    
    # 尝试从系统字体中查找可用的中文字体
    for font_name in chinese_fonts:
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            continue
    
    # 如果没有找到中文字体，使用默认字体
    return pygame.font.Font(None, size)

class Snake:
    def __init__(self):
        self.color = GREEN
        self.reset()

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + (x*BLOCK_SIZE), cur[1] + (y*BLOCK_SIZE))
        
        # 检查是否撞到边界
        if (new[0] < 0 or new[0] >= WINDOW_WIDTH or 
            new[1] < 0 or new[1] >= WINDOW_HEIGHT):
            return False
            
        # 检查是否撞到自己
        if new in self.positions[3:]:
            return False
            
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.game_over = False

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# 定义方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_button(surface, text, x, y, width, height, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))
    
    font = get_font(24)  # 按钮文字大小从36减小到24
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    surface.blit(text_surface, text_rect)
    return False

def main():
    snake = Snake()
    food = Food()
    font = get_font(32)  # 将游戏中的主要字体从48减小到32
    game_state = "playing"  # playing, game_over

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and game_state == "playing":
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        # 绘制游戏界面
        screen.fill(BLACK)
        
        if game_state == "playing":
            # 更新蛇的位置
            if not snake.update():
                game_state = "game_over"
            
            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()
            
            # 绘制蛇和食物
            snake.render(screen)
            food.render(screen)
            
            # 显示分数
            score_text = font.render(f'分数: {snake.score}', True, WHITE)
            screen.blit(score_text, (10, 10))
            
        elif game_state == "game_over":
            # 显示游戏结束信息
            game_over_font = get_font(40)  # 游戏结束字体稍大一些
            normal_font = get_font(28)  # 其他文字更小一些
            
            game_over_text = game_over_font.render('游戏结束!', True, RED)
            score_text = normal_font.render(f'最终分数: {snake.score}', True, WHITE)
            
            # 计算文字位置，使其居中显示
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            
            # 绘制文字
            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_text, score_rect)
            
            # 绘制重新开始按钮
            button_width = 160  # 减小按钮宽度
            button_height = 40  # 减小按钮高度
            button_x = WINDOW_WIDTH//2 - button_width//2
            button_y = WINDOW_HEIGHT//2 + 50
            
            if draw_button(screen, "重新开始", button_x, button_y, button_width, button_height, GRAY, (100, 100, 100)):
                snake.reset()
                food.randomize_position()
                game_state = "playing"

        pygame.display.update()
        clock.tick(GAME_SPEED)

if __name__ == '__main__':
    main() 