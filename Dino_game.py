
import random
import pygame


# Obstacle class
class obstacle:
    def __init__(self, sprite,obs_dist,HEIGHT,WIDTH):
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.rect.x = WIDTH-random.randrange(0,obs_dist)
        self.rect.y = HEIGHT-random.randrange(130,240,10) #240 for larger 200 for smaller
    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

    # Pipe run across the screen
    def update(self,game_speed,obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()


# Player class
class Player:
    
    def __init__(self, sprite,x,y,jump_spd,gravity,player_height):
        self.jump_speed = jump_spd
        self.sprite = sprite
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.rect = pygame.Rect(
            self.x, self.y, sprite.get_width(), sprite.get_height()
        )  
        self.gravity=gravity
        self.player_height=player_height

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def jump(self,HEIGHT):
        if self.rect.y >= HEIGHT - self.player_height:
            self.velocity_y = -self.jump_speed

    def update(self,HEIGHT):

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.y >= HEIGHT - self.player_height:
            self.rect.y = HEIGHT - self.player_height
            self.velocity_y = 0

# Display Score

def score(screen,scores,game_speed,highest_scr):
    # global scores, game_speed, highest_scr
    FONT = pygame.font.SysFont("comicsans", 30)

    scores += 1
    if scores % 100 == 0 and game_speed<14.3:  # Increase Game speed every 100 points
        game_speed += 0.1

    if scores > highest_scr:
        highest_scr = scores

    text = FONT.render(f"Points:  {str(scores)}", True, (0, 0, 0))  # Render Points
    screen.blit(text, (500, 50))
    return (scores,game_speed,highest_scr)

# Remove Dinos,obstacles,nets,genomes

def remove(i,dinos,gen,nets):
    dinos.pop(i)
    gen.pop(i)
    nets.pop(i)

# Draw Ground
def draw_Ground(screen,ground_img,HEIGHT) -> None:
    screen.blit(ground_img,(0,HEIGHT-100))

