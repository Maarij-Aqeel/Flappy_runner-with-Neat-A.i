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
    screen.blit(highest_scores, (WIDTH - 200, 40))


# Calculate distance between dino and top of pipe
def distance(pos_one, pos_two):
    dx = pos_one[0] - pos_two[0]
    dy = pos_one[1] - pos_two[1]

    dx = dx**2
    dy = dy**2
    return math.sqrt(dx + dy)


# Main function for training and Testing
def main(config=None, Dino_winner=None, is_training=True, User_play=False):
    global game_speed, obstacles, scores, dinos, nets, gen, generation, highest_scr

    # Initialize the game environment
    game_speed = 10
    scores = 0
    obstacles = []
    obs_dist = 600       
    clock = pygame.time.Clock()

    if is_training:
        dinos = [Player(player_img,40,HEIGHT-player_height,jump_spd,gravity,player_height) for _ in gen]
    else:
        dino = Player(player_img,40,HEIGHT-player_height,jump_spd,gravity,player_height)

    running = True

    while running:
        screen.fill((135, 206, 250))
        clock.tick(120)

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
            else:
                if dino.rect.colliderect(obs.rect):
                    print(f"Game Over! Score: {scores}")
                    print(game_speed)
                    print(scores)
                    running = False

        # Calculating Fitness and testing 

        if User_play and not is_training:
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
                    (dino.rect.y, distance((dino.rect.x, dino.rect.y), obs.rect.midtop))
                )


                if output[0] > 0.5 and dino.rect.y >= HEIGHT - player_height:
                    dino.jump(HEIGHT)

                dino.update(HEIGHT)
                dino.draw(screen)
        else:
            if len(obstacles) == 0:
                obstacles.append(obstacle(obstacle_img, obs_dist,HEIGHT,WIDTH))

                
            output = Dino_winner.activate(
                (dino.rect.y, distance((dino.rect.x, dino.rect.y), obstacles[0].rect.midtop))
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
            print(game_speed) 
            print(scores)

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
def run_winner(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    with open("Dino_winner.pkl", "rb") as f:
        winner = pickle.load(f)

    Dino_winner = neat.nn.FeedForwardNetwork.create(winner, config)

    main(config=config, Dino_winner=Dino_winner, is_training=False)


# Function for Playing the game yourself
def User_play():
    main(is_training=False,User_play=True)


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
    run(config_file)
    # User_play() 
    # run_winner(config_file)
