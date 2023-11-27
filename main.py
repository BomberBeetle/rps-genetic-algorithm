import random
import math
import matplotlib.pyplot as plt

class individuo:
    pedra = 0
    papel = 0
    tesoura = 0
    pontos = 0

    def __init__(self, pe, pa, te, po):
        self.pedra = pe
        self.papel = pa
        self.tesoura = te
        self.pontos = po

def select(population, num):
    pop_sorted = sorted(population, key=(lambda ind: -ind.pontos))
    return pop_sorted[:num]

def crossover(parents, population_size):
    n_par = len(parents)
    new_gen = []
    new_gen.extend(parents[:math.floor(n_par*0.2)]) # 20%

    for _ in range(0, population_size-len(new_gen)):
        ind1 = parents[random.randrange(0, n_par)]
        ind2 = parents[random.randrange(0, n_par)]
        pedra = (ind1.pedra+ind2.pedra)//2
        papel = (ind1.papel+ind2.papel)//2
        tesoura = (ind1.tesoura+ind2.tesoura)//2
        new_gen.append(individuo(pedra, papel, tesoura, 0))
    return new_gen

def mutate(population):
    for ind in population:
        adj_pedra= random.randint(-5, 5)
        if adj_pedra+ind.pedra >= 0: ind.pedra += adj_pedra
        adj_papel= random.randint(-5, 5)
        if adj_papel+ind.papel >= 0: ind.papel += adj_papel
        adj_tesoura= random.randint(-5, 5)
        if adj_tesoura+ind.tesoura >= 0: ind.tesoura += adj_tesoura
        
        
    return population

def set_pop_fitness(population, op, num_jogos):
    for ind in population:
        fitness = 0
        for i in range(0, num_jogos):
            fitness += sim_game(ind, op)
        ind.pontos = fitness

def sim_game(ind, op):
    seed_in = random.randint(0, 99)
    sel_in = random.choices([0,1,2], weights=[ind.pedra, ind.papel, ind.tesoura])

    seed_op = random.randint(0, 99)
    sel_op = random.choices([0,1,2], weights=[op.pedra, op.papel, op.tesoura])

    if sel_op == sel_in:
        return 0
    elif (sel_in == 0 and sel_op==1) or (sel_in == 1 and sel_op==2) or (sel_in == 2 and sel_op == 0):
        return -1
    else:
        return 1

def get_avg_fitness(pop):
    total_fit = 0
    for ind in pop:
        total_fit += ind.pontos
    return total_fit/len(pop)

def get_avg_rock(pop):
    total_fit = 0
    for ind in pop:
        total_fit += ind.pedra
    return total_fit/len(pop)

def get_avg_paper(pop):
    total_fit = 0
    for ind in pop:
        total_fit += ind.papel
    return total_fit/len(pop)

def get_avg_scissor(pop):
    total_fit = 0
    for ind in pop:
        total_fit += ind.tesoura
    return total_fit/len(pop)

def gen_initial(size):
    population = []
    for i in range(0, size):
        pedra = random.randint(0, 99)
        papel = random.randint(0, 99-pedra)
        tesoura = 99-pedra-papel
        population.append(individuo(pedra, papel, tesoura, 0))
    return population


op = individuo(49, 00, 50, -1)
pop = gen_initial(100)

avgs = []
rocks = []
papers = []
scissors = []

print(f"{pop[0].pedra}, {pop[0].papel}, {pop[0].tesoura}")

for i in range (0, 20):
    set_pop_fitness(pop, op, 100)
    avg_fitness = get_avg_fitness(pop)

    rocks.append(get_avg_rock(pop))
    papers.append(get_avg_paper(pop))
    scissors.append(get_avg_scissor(pop))

    avgs.append(avg_fitness)

    print(f"Geração {i}: {get_avg_fitness(pop)}")
    pop = mutate(crossover(select(pop, math.floor(len(pop)/2)), len(pop)))


print(f"{pop[0].pedra}, {pop[0].papel}, {pop[0].tesoura}")

plt.plot(avgs)
plt.show()
plt.plot(rocks, "-",  papers, "-", scissors, '-')
plt.show()