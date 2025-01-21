from Neat_dino import *


#   Funciton for Fine tuning
def fine_tune(config_file, winner_file, generations=50):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    # Load Winner
    with open(winner_file, "rb") as f:
        winner = pickle.load(f)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Replace all genomes with clones of the pre-trained winner 
    new_population = {}
    for genome_id in population.population.keys():
        new_genome = pickle.loads(pickle.dumps(winner))  # Deep copy 
        new_genome.key = genome_id 
        new_population[genome_id] = new_genome

    # Update the population with the new genomes
    population.population = new_population

    for genome in population.population.values():
        genome.fitness = 0

    population.species.speciate(
        config=population.config,
        population=population.population,
        generation=population.generation,
    )

    # fine-tune the population
    fine_tuned_winner = population.run(eval_genomes, generations) 

    # Save the fine-tuned genome
    fine_tuned_file = "Dino_winner_fine_tuned.pkl"
    with open(fine_tuned_file, "wb") as f:
        pickle.dump(fine_tuned_winner, f)

    print(f"Fine-tuned genome saved to {fine_tuned_file}")

if __name__ == "__main__":
        config_file = os.path.join(os.path.dirname(__file__), "config_file.txt")
        fine_tune(config_file,os.path.join(os.path.dirname(__file__),"winners/Dino_winner.pkl"),50)
