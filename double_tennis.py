import random
import pygame
import tkinter as tk
from tkinter import simpledialog

#Constraints
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400


BALL_SPEED = 7
BALL_RADIUS = 7


PLAYER_RADIUS = 15
PLAYER_SPEED = 5


GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


POSITIONS = {
    "A1": (0, 400, 0, 200),
    "A2": (400, 800, 0, 200),
    "B1": (0, 400, 200, 400),
    "B2": (400, 800, 200, 400),
}


BORDER_MARGIN = 5

class Player:
    def __init__(self, x, y, team, position_name):
        self.x = x
        self.y = y
        self.team = team  
        self.position_name = position_name
        self.zone = POSITIONS[position_name]

    def move(self, ball):
        zx1, zx2, zy1, zy2 = self.zone

        
        margin = PLAYER_RADIUS + 1
        zx1 += margin
        zx2 -= margin
        zy1 += margin
        zy2 -= margin

        
        net_buffer = PLAYER_RADIUS + 1
        if self.team == "A":
            zy2 = min(zy2, SCREEN_HEIGHT // 2 - net_buffer)
        else: 
            zy1 = max(zy1, SCREEN_HEIGHT // 2 + net_buffer)

        
        if zx1 <= ball.x <= zx2 and zy1 <= ball.y <= zy2:
            if ball.x < self.x:
                self.x = max(zx1, self.x - PLAYER_SPEED)
            elif ball.x > self.x:
                self.x = min(zx2, self.x + PLAYER_SPEED)
            if ball.y < self.y:
                self.y = max(zy1, self.y - PLAYER_SPEED)
            elif ball.y > self.y:
                self.y = min(zy2, self.y + PLAYER_SPEED)


    def try_hit(self, ball):
        if abs(ball.x - self.x) < 20 and abs(ball.y - self.y) < 20:
            
            ball.dy = -abs(ball.dy) if self.team == "B" else abs(ball.dy)
            ball.dx = random.choice([-BALL_SPEED, BALL_SPEED])

class Ball:
    def __init__(self):
        self.reset()

    def move(self):
        self.x += self.dx
        self.y += self.dy

        
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.dx = -self.dx
        

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = random.choice([-BALL_SPEED, BALL_SPEED])
        self.dy = random.choice([-BALL_SPEED, BALL_SPEED])

class TennisGame:
    def __init__(self):
        self.select_serving_team()
        self.players = [
            Player(100, 100, "A", "A1"),
            Player(700, 100, "A", "A2"),
            Player(100, 300, "B", "B1"),
            Player(700, 300, "B", "B2"),
        ]
        self.ball = Ball()
        self.score = {"A": 0, "B": 0}

    def select_serving_team(self):
        root = tk.Tk()
        root.withdraw()
        self.serving_team = simpledialog.askstring("Serve", "Who serves first? (A or B)").upper()
        print(f"Team {self.serving_team} serves first.")

    def check_score(self):
        if self.ball.y < 0:
            self.score["B"] += 1
            print("Team B scores!")
            self.ball.reset()
        elif self.ball.y > SCREEN_HEIGHT:
            self.score["A"] += 1
            print("Team A scores!")
            self.ball.reset()

    def draw_court(self, screen):
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 4)
        pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT//2), (SCREEN_WIDTH, SCREEN_HEIGHT//2), 2)
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT//2), (SCREEN_WIDTH, SCREEN_HEIGHT//2), 4)  # Net

    def simulate(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Doubles Tennis Simulation")
        clock = pygame.time.Clock()
        running = True

        while running:
            screen.fill(GREEN)
            self.draw_court(screen)

            
            pygame.draw.circle(screen, WHITE, (int(self.ball.x), int(self.ball.y)), BALL_RADIUS)
            self.ball.move()

            for player in self.players:
                color = RED if player.team == "A" else BLUE
                player.move(self.ball)
                player.try_hit(self.ball)
                pygame.draw.circle(screen, color, (player.x, player.y), PLAYER_RADIUS)

            self.check_score()

            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"A: {self.score['A']} | B: {self.score['B']}", True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH//2 - 80, 10))

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

if __name__ == "__main__":
    game = TennisGame()
    game.simulate()
