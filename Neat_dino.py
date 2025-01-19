import neat.population
import neat
import os
import pickle
import pygame
import math
from Dino_game import *


# Essential variables
WIDTH = 1100
HEIGHT = 600
generation = 0
highest_scr = 0
player_height = 150
player_x = 40
player_y = HEIGHT - player_height
jump_spd = 14
gravity = 0.6

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Runner")


# Load the Assets
player_img = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.dirname(__file__), "assets/bird1.png")), (50, 50)
)
obstacle_img = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.dirname(__file__), "assets/pipe.png")),
    (30, 200),
)
ground_img=pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__),'assets/ground.png')),(1100,HEIGHT-500))
background_image_path = pygame.transform.smoothscale(
    pygame.image.load(os.path.join(os.path.dirname(__file__), "assets/bg.png")).convert(), 
    (WIDTH, HEIGHT)
)

# Function for Displaying generations, Dinos alive  etc 
def draw(screen, generation, alive_count, highest_score):
    font = pygame.font.SysFont("comicsans", 30)

    # Render text for generation number
    generation_text = font.render(f"Generation: {generation}", True, (0, 0, 0))
    screen.blit(generation_text, (10, 10))

    # Render text for alive dinos
    alive_text = font.render(f"Alive: {alive_count}", True, (0, 0, 0))
    screen.blit(alive_text, (10, 40))

    # Render text for Highest scores
    highest_scores = font.render(f"Highest_Score: {highest_score}", True, (0, 0, 0))
    screen.blit(highest_scores, (WIDTH - 220, 40))


# Calculate distance between dino and top of pipe
def distance(pos_one, pos_two):
    dx = pos_one[0] - pos_two[0]
    dy = pos_one[1] - pos_two[1]

    dx = dx**2
    dy = dy**2
    return math.sqrt(dx + dy)

# Main Menu of game
def main_menu(Screen_Width,config_file, background_image, Screen,player_img,ground):


    button_width = 200
    button_height = 50
    button_color = (255, 22, 15) 
    button_hover_color = (254, 147, 36)
    small_font = pygame.font.Font(None, 24)

    while True:
        Screen.blit(background_image, (0, 0))
        Screen.blit(player_img,((WIDTH/2)-20,HEIGHT/4))
        Screen.blit(ground,(0,HEIGHT-100))
        

        Test_ai_rect = pygame.Rect((Screen_Width/2)-100, 220, button_width, button_height)
        Test_ai = small_font.render("Test A.i", True, (255, 255, 255))
        Test_ai_text = Test_ai.get_rect(center=Test_ai_rect.center)

        compete_ai_rect = pygame.Rect((Screen_Width/2)-100, 290, button_width, button_height)
        compete_ai = small_font.render("Compete with A.i", True, (255, 255, 255))
        compete_ai_text = compete_ai.get_rect(center=compete_ai_rect.center)
        
        Train_ai_rect = pygame.Rect((Screen_Width/2)-100, 360, button_width, button_height)
        Train_ai_sur = small_font.render("Train A.i", True, (255, 255, 255))
        Train_ai_text = Train_ai_sur.get_rect(center=Train_ai_rect.center)

        Play_alone_rect = pygame.Rect((Screen_Width/2)-100, 430, button_width, button_height)
        Play_alone_sur = small_font.render("Play yourself", True, (255, 255, 255))
        Play_alone_text = Play_alone_sur.get_rect(center=Play_alone_rect.center)

        quit_button_rect = pygame.Rect((Screen_Width/2)-100, 500, button_width, button_height)
        quit_text = small_font.render("Quit Game", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)

        mouse_pos = pygame.mouse.get_pos()
        for button_rect, button_text_rect in [
            (compete_ai_rect, compete_ai_text),
            (Train_ai_rect, Train_ai_text),
            (Play_alone_rect, Play_alone_text),
            (quit_button_rect, quit_text_rect),
            (Test_ai_rect,Test_ai_text)]:

            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(Screen, button_hover_color, button_rect)
            else:
                pygame.draw.rect(Screen, button_color, button_rect)

        Screen.blit(Test_ai, Test_ai_text)
        Screen.blit(compete_ai, compete_ai_text)
        Screen.blit(Train_ai_sur, Train_ai_text)
        Screen.blit(Play_alone_sur, Play_alone_text)
        Screen.blit(quit_text, quit_text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if compete_ai_rect.collidepoint(mouse_pos):
                    compete_with_ai(config_file)

                elif Train_ai_rect.collidepoint(mouse_pos):
                    run(config_file)

                elif Test_ai_rect.collidepoint(mouse_pos):
                    run_winner(config_file)
                    
                elif Play_alone_rect.collidepoint(mouse_pos):
                    User_play()

                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return




# Main function for training and Testing
def main(config=None, Dino_winner=None, is_training=True, User_play=False,compete=False):
    global game_speed, obstacles, scores, dinos, nets, gen, generation, highest_scr

    # Initialize the game environment
    game_speed = 10
    scores = 0
    obstacles = []
    obs_dist = 600       
    clock = pygame.time.Clock()

    if compete:
        dino_player=Player(player_img,player_x+100,player_y,jump_spd,gravity,player_height)
        dino = Player(player_img,player_x,HEIGHT-player_height,jump_spd,gravity,player_height)
        obs_dist=500    # Adjust it to make gap bigger between player and pipe

    elif is_training:
        dinos = [Player(player_img,player_x,HEIGHT-player_height,jump_spd,gravity,player_height) for _ in gen]
    else:
        dino = Player(player_img,player_x,HEIGHT-player_height,jump_spd,gravity,player_height)

    running = True

    while running:
        screen.fill((135, 206, 250))
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # Update and draw obstacles

        if len(obstacles) == 0:
            obstacles.append(obstacle(obstacle_img, obs_dist,HEIGHT,WIDTH))
        

        for obs in obstacles:
            obs.draw(screen)
            obs.update(game_speed,obstacles)

            if is_training:
                for i, dino in enumerate(dinos):
                    if dino.rect.colliderect(obs.rect):
                        gen[i].fitness -= 1
                        remove(i,dinos,gen,nets)

            elif compete:
                if dino_player.rect.colliderect(obs.rect):
                    print("You died")
                    running=False
                elif dino.rect.colliderect(obs.rect):
                    print(f"A.i Died")
                    running = False
            else:
                if dino.rect.colliderect(obs.rect):
                    print(f"Game Over! Score: {scores}")
                    running = False

        # Calculating Fitness and testing 

        if compete: # Compete with ai mode

            font = pygame.font.SysFont("comicsans", 38)
            player_label = font.render("Player", True, (255, 0, 0))  # Red plauer
            ai_label = font.render("AI", True, (0, 0, 255))  # blue Ai

            # Draw labels near the dinos
            screen.blit(player_label, (dino_player.rect.x - 10, dino_player.rect.y - 30))
            screen.blit(ai_label, (dino.rect.x - 10, dino.rect.y - 20))

            #Checking Input by player
            user_input= pygame.key.get_pressed()
            if user_input[pygame.K_SPACE]:
                dino_player.jump(HEIGHT)
            dino_player.update(HEIGHT)
            dino_player.draw(screen)


            if len(obstacles) == 0:
                obstacles.append(obstacle(obstacle_img, obs_dist,HEIGHT,WIDTH))

            #Activate A.i                
            output = Dino_winner.activate(
                (dino.rect.y, distance((dino.rect.x, dino.rect.y), obstacles[0].rect.midtop),game_speed)
            )
            if output[0] > 0.5 and dino.rect.y >= HEIGHT - player_height:
                dino.jump(HEIGHT)

            dino.update(HEIGHT)
            dino.draw(screen)


        elif User_play and not is_training:
            user_input= pygame.key.get_pressed()
            if user_input[pygame.K_SPACE]:
                dino.jump(HEIGHT)
            dino.update(HEIGHT)
            dino.draw(screen)

        elif is_training:
            for i, dino in enumerate(dinos):
                gen[i].fitness += 0.5 + (game_speed / 10)  # Reward for surviving

                if obs.rect.right < dino.rect.left:
                    gen[i].fitness += 5  # Reward for clearing pipe

                output = nets[i].activate(
                    (dino.rect.y, distance((dino.rect.x, dino.rect.y), obs.rect.midtop),game_speed)
                )


                if output[0] > 0.5 and dino.rect.y >= HEIGHT - player_height:
                    dino.jump(HEIGHT)

                dino.update(HEIGHT)
                dino.draw(screen)

        else:
            if len(obstacles) == 0:
                obstacles.append(obstacle(obstacle_img, obs_dist,HEIGHT,WIDTH))

                
            output = Dino_winner.activate(
                (dino.rect.y, distance((dino.rect.x, dino.rect.y), obstacles[0].rect.midtop),game_speed)
            )
            if output[0] > 0.5 and dino.rect.y >= HEIGHT - player_height:
                dino.jump(HEIGHT)

            dino.update(HEIGHT)
            dino.draw(screen)


        # Draw the ui elements
        draw(screen, generation if is_training else "Playing/Testing", len(dinos) if is_training else 1, highest_scr)

        scores,game_speed,highest_scr=score(screen,scores,game_speed,highest_scr)
        draw_Ground(screen,ground_img,HEIGHT)

        pygame.display.flip()

        if is_training and len(dinos) == 0:
            break


# Main eval or Fitness function
def eval_genomes(genomes, config):
    global gen, nets, generation

    generation += 1
    gen = []
    nets = []

    for _, genome in genomes:
        gen.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    main(config=config, is_training=True)

# Function for testing the best Genome(dino)
def run_winner(config_file,compete=False):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    with open(os.path.join(os.path.dirname(__file__),"winners/Dino_winner.pkl"), "rb") as f:
        winner = pickle.load(f)

    Dino_winner = neat.nn.FeedForwardNetwork.create(winner, config)

    main(config=config, Dino_winner=Dino_winner, is_training=False,compete=compete)


# Function for Playing the game yourself
def User_play():
    main(is_training=False,User_play=True)

# Functiono to Compete_with Ai
def compete_with_ai(config_file):
    run_winner(config_file,True)
    main_menu(WIDTH,config_file,background_image_path,screen,player_img,ground_img)

# Function for running the Neat algorithm
def run(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 100)

    #Save the best dino if its fitness meets the Threshold fitness
    with open("Dino_winner.pkl", "wb") as f:
        pickle.dump(winner, f)

    print(f"Best Genome: {winner}")


if __name__ == "__main__":
    
    config_file = os.path.join(os.path.dirname(__file__), "config_file.txt")
    main_menu(WIDTH,config_file,background_image_path,screen,player_img,ground_img)

