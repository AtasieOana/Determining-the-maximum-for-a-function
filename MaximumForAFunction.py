import random
import math

# reading input data
fisier = open("Input.in", "r")
evolutie = open("Evolution.txt", "w")
dimensiune_populatie = int(fisier.readline())
next_line = fisier.readline().split()
x_domeniu_functie, y_domeniu_functie = int(next_line[0]), int(next_line[1])
coeficienti_functie = [int(i) for i in fisier.readline().split()]
precizie = int(fisier.readline())
probabilitate_recombinare = float(fisier.readline())
probabilitate_mutatie = float(fisier.readline())
nr_etape = int(fisier.readline())


def function(x, coeficienti):
    return coeficienti[0] * (x ** 3) + coeficienti[1] * (x ** 2) + coeficienti[2] * x + coeficienti[3]


# function to generate random binary elements of length leng
def generate_binary(leng):
    binar = ""
    for i in range(leng):
        # we randomly generate 0 or 1
        temp = str(random.randint(0, 1))
        binar += temp
    return binar


# function that converts a number from base 2 to base 10
def baza2_baza10(numar_baza_2):
    numar_baza_10 = 0
    nr = 0
    for i in numar_baza_2[::-1]:
        numar_baza_10 += 2 ** nr * int(i)
        nr += 1
    return numar_baza_10


# function that finds the range that a number belongs to using binary search
def binarySearchInterval(intervale, stanga, dreapta, u):
    if dreapta >= stanga:
        mijloc = (stanga + dreapta) // 2
        if u > intervale[mijloc][0] and u < intervale[mijloc][1]:
            return mijloc
        elif u < intervale[mijloc][0]:
            return binarySearchInterval(intervale, stanga, mijloc - 1, u)
        else:
            return binarySearchInterval(intervale, stanga + 1, dreapta, u)

    return -1


# function to find the value in the range [x_function_domain, y_function_domain] for a chromosome
def valoare_interval(lungime_cromozom, numar_baza_2):
    # we transform the number from base 2 to base 10
    numar_baza_10 = baza2_baza10(numar_baza_2)
    # calculate the value in the range [x_function_domain, y_function_domain]
    valoare = round(
        (y_domeniu_functie - x_domeniu_functie) / (pow(2, lungime_cromozom) - 1) * numar_baza_10 + x_domeniu_functie,
        precizie)
    return valoare


# we generate the initial population
lungime_cromozom = math.ceil(math.log(((y_domeniu_functie - x_domeniu_functie) * pow(10, precizie)), 2))
valoare_din_interval = []
cromozomi = []
for i in range(dimensiune_populatie):
    # chromosomes are random numbers in base 2 with length log (b-a)*(10^accuracy)
    numar_baza_2 = generate_binary(lungime_cromozom)
    cromozomi.append(numar_baza_2)
    valoare = valoare_interval(lungime_cromozom, numar_baza_2)
    valoare_din_interval.append(valoare)


# function to display the population in the case of the initial population and to calculate the values of the function for the initial x
def afisare_populatie(cromozomi, valoare_din_interval, coeficienti, afisare):
    valori_functie = []
    for i in range(dimensiune_populatie):
        f = function(valoare_din_interval[i], coeficienti)
        valori_functie.append(f)
        if afisare:
            evolutie.write(
                str(i + 1) + ": " + cromozomi[i] + " x = " + str(valoare_din_interval[i]) + " f = " + str(f) + "\n")
    return valori_functie


# function to calculate the selection probabilities for each chromosome
def calcul_probabilitati_selectie(valori_functie, afisare):
    probabilitati_selectie = []
    suma_total_functie = sum(valori_functie)
    for i in range(dimensiune_populatie):
        probabilitate = valori_functie[i] / suma_total_functie
        probabilitati_selectie.append(probabilitate)
        if afisare:
            evolutie.write("chromosome " + str(i + 1) + " has the probability of selection " + str(probabilitate) + "\n")
    return probabilitati_selectie


# function to calculate selection probability intervals
def calcul_intervale_probabilitati_selectie(probabilitati_selectie, afisare):
    capete_intervale_selectie = []
    nr = 0
    for i in range(len(probabilitati_selectie)):
        # for each i we add all the selection probabilities up to i
        suma = sum(probabilitati_selectie[:i])
        capete_intervale_selectie.append(suma)
        if afisare:
            evolutie.write(str(suma) + "  ")
        nr += 1
        if nr % 5 == 0 and afisare:
            evolutie.write("\n")
    capete_intervale_selectie.append(float(1))
    if afisare:
        evolutie.write(str(float(1)) + "\n")
    return capete_intervale_selectie


# function to find the elitist chromosome
def selectie_elitista(valori_functie):
    cromozom_elitist_valoare = max(valori_functie)
    cromozom_elitist = valori_functie.index(cromozom_elitist_valoare)
    return cromozom_elitist_valoare, cromozom_elitist


# function to apply the roulette method to make the selection
def selectie_metoda_ruletei(cromozomi, valoare_din_interval, valori_functie, perechi_interval, afisare,
                            cromozom_elitist):
    populatie_dupa_selectie = []
    # we generate u - uniform number in the interval [0,1) and we find the selection interval of which it is part
    for i in range(dimensiune_populatie - 1):
        u = random.uniform(0, 1)
        pozitie = binarySearchInterval(perechi_interval, 0, dimensiune_populatie - 1, u)
        # select the chromosome equivalent to the interval of which u is a part
        populatie_dupa_selectie.append(
            (pozitie, cromozomi[pozitie], valoare_din_interval[pozitie], valori_functie[pozitie]))
        if afisare:
            evolutie.write("u = " + str(u) + ", so we select the chromosome " + str(pozitie + 1) + "\n")
    populatie_dupa_selectie.append((cromozom_elitist, cromozomi[cromozom_elitist],
                                    valoare_din_interval[cromozom_elitist], valori_functie[cromozom_elitist]))
    return populatie_dupa_selectie


# function to find selected chromosomes that participate in crossover
def gaseste_cromozomii_care_participa_la_incrucisare(populatie_dupa_selectie, afisare):
    cromozomi_selectati_recombinare = []
    for i in range(len(populatie_dupa_selectie) - 1):
        u = random.uniform(0, 1)
        # if the random u uniform is less than the probability of recombination, then the current chromosome
        # will participate in the crossover
        if u < probabilitate_recombinare:
            cromozomi_selectati_recombinare.append((i, populatie_dupa_selectie[i][0]))
            if afisare:
                evolutie.write(str(i + 1) + ": chromosome " + str(populatie_dupa_selectie[i][0] + 1) + " = " + str(
                    populatie_dupa_selectie[i][1])
                               + " u = " + str(u) + " < " + str(probabilitate_recombinare) + " participate\n")
        else:
            if afisare:
                evolutie.write(str(i + 1) + ": chromosome " + str(populatie_dupa_selectie[i][0] + 1) + " = " + str(
                    populatie_dupa_selectie[i][1]) + " "
                               + " u = " + str(u) + "\n")
    if afisare:
        pozitie = len(populatie_dupa_selectie) - 1
        evolutie.write(str(pozitie + 1) + ": chromosome " + str(populatie_dupa_selectie[pozitie][0] + 1) + " = " + str(
            populatie_dupa_selectie[pozitie][1]) + " "
                       + " -> elitist chromosome \n")
    return cromozomi_selectati_recombinare


def incrucisare_2cromozomi(cromozom1, cromozom2):
    punct_rupere = random.randint(0, lungime_cromozom)
    cromozom_nou_1 = cromozom1[:punct_rupere] + cromozom2[punct_rupere:]
    cromozom_nou_2 = cromozom2[:punct_rupere] + cromozom1[punct_rupere:]
    return punct_rupere, cromozom_nou_1, cromozom_nou_2


def incrucisare_3cromozomi(cromozom1, cromozom2, cromozom3):
    punct_rupere = random.randint(0, lungime_cromozom)
    cromozom_nou_1 = cromozom1[:punct_rupere] + cromozom2[punct_rupere:]
    cromozom_nou_2 = cromozom2[:punct_rupere] + cromozom3[punct_rupere:]
    cromozom_nou_3 = cromozom3[:punct_rupere] + cromozom1[punct_rupere:]
    return punct_rupere, cromozom_nou_1, cromozom_nou_2, cromozom_nou_3


# function that performs the crossover process
def proces_de_incrucisare(populatie_dupa_selectie, cromozom_elitist, cromozomi_selectati_recombinare, afisare):
    populatie_dupa_incrucisare = populatie_dupa_selectie.copy()
    nr_cromozomi_recombinati = len(cromozomi_selectati_recombinare)
    i = 0
    # we go through the chromosomes that participate in the cross and we make pairs of 2 chromosomes to cross them,
    # unless the number of chromosomes participating in the cross is odd,
    # in which case, the last 3 chromosomes will all form a pair
    while i < nr_cromozomi_recombinati - 1:
        pozitie_cromozom1, indice_cromozom1 = cromozomi_selectati_recombinare[i][0], cromozomi_selectati_recombinare[i][
            1]
        pozitie_cromozom2, indice_cromozom2 = cromozomi_selectati_recombinare[i + 1][0], \
                                              cromozomi_selectati_recombinare[i + 1][1]
        if nr_cromozomi_recombinati % 2 == 1 and nr_cromozomi_recombinati - i == 3:
            pozitie_cromozom3, indice_cromozom3 = cromozomi_selectati_recombinare[i + 2][0], \
                                                  cromozomi_selectati_recombinare[i + 2][1]
            pct_rupere, cromozom_nou_1, cromozom_nou_2, cromozom_nou_3 = incrucisare_3cromozomi(
                cromozomi[indice_cromozom1],
                cromozomi[indice_cromozom2], cromozomi[indice_cromozom3])
            populatie_dupa_incrucisare[pozitie_cromozom1] = (
            indice_cromozom1, cromozom_nou_1, valoare_interval(lungime_cromozom, cromozom_nou_1),
            function(valoare_interval(lungime_cromozom, cromozom_nou_1), coeficienti_functie))
            populatie_dupa_incrucisare[pozitie_cromozom2] = (
            indice_cromozom2, cromozom_nou_2, valoare_interval(lungime_cromozom, cromozom_nou_2),
            function(valoare_interval(lungime_cromozom, cromozom_nou_2), coeficienti_functie))
            populatie_dupa_incrucisare[pozitie_cromozom3] = (
            indice_cromozom3, cromozom_nou_3, valoare_interval(lungime_cromozom, cromozom_nou_3),
            function(valoare_interval(lungime_cromozom, cromozom_nou_3), coeficienti_functie))
            if afisare:
                evolutie.write("Recombination between chromosome " + str(indice_cromozom1 + 1) + " chromosome "
                               + str(indice_cromozom2 + 1) + " and chromosome " + str(indice_cromozom3 + 1) +
                               " with breaking point " + str(pct_rupere) + "\n")
                evolutie.write(
                    "Initial: " + str(cromozomi[indice_cromozom1]) + " and " + str(cromozomi[indice_cromozom2])
                    + " si " + str(cromozomi[indice_cromozom3]) + "\n")
                evolutie.write("Result: " + str(cromozom_nou_1) + " and " + str(cromozom_nou_2) + " and " + str(
                    cromozom_nou_3) + "\n")
            i += 3
        else:
            pct_rupere, cromozom_nou_1, cromozom_nou_2 = incrucisare_2cromozomi(cromozomi[indice_cromozom1],
                                                                                cromozomi[indice_cromozom2])
            populatie_dupa_incrucisare[pozitie_cromozom1] = (
            indice_cromozom1, cromozom_nou_1, valoare_interval(lungime_cromozom, cromozom_nou_1),
            function(valoare_interval(lungime_cromozom, cromozom_nou_1), coeficienti_functie))
            populatie_dupa_incrucisare[pozitie_cromozom2] = (
            indice_cromozom2, cromozom_nou_2, valoare_interval(lungime_cromozom, cromozom_nou_2),
            function(valoare_interval(lungime_cromozom, cromozom_nou_2), coeficienti_functie))
            if afisare:
                evolutie.write(
                    "Recombination between chromosome " + str(indice_cromozom1 + 1) + " and chromosome "
                    + str(indice_cromozom2 + 1) + " with breaking point " + str(pct_rupere) + "\n")
                evolutie.write(
                    "Initial: " + str(cromozomi[indice_cromozom1]) + " and " + str(cromozomi[indice_cromozom2]) + "\n")
                evolutie.write("Result: " + str(cromozom_nou_1) + " and " + str(cromozom_nou_2) + "\n")
            i += 2
    return populatie_dupa_incrucisare


# function that performs the mutation process
def proces_mutatie(populatie_dupa_incrucisare, afisare):
    populatie_dupa_mutatie = populatie_dupa_incrucisare.copy()
    for i in range(len(populatie_dupa_incrucisare) - 1):
        u = random.uniform(0, 1)
        # if the random u uniform is less than the probability of mutation, then the current chromosome will
        # change its gene from position p
        if u < probabilitate_mutatie:
            p = random.randint(0, lungime_cromozom - 1)
            if populatie_dupa_incrucisare[i][1][p] == '0':
                cromozom_nou = populatie_dupa_incrucisare[i][1][:p] + '1' + populatie_dupa_incrucisare[i][1][p + 1:]
            else:
                cromozom_nou = populatie_dupa_incrucisare[i][1][:p] + '0' + populatie_dupa_incrucisare[i][1][p + 1:]
            populatie_dupa_mutatie[i] = (i, cromozom_nou, valoare_interval(lungime_cromozom, cromozom_nou),
                                         function(valoare_interval(lungime_cromozom, cromozom_nou),
                                                  coeficienti_functie))
            if afisare:
                evolutie.write("chromosome " + str(i + 1) + "  " + str(populatie_dupa_incrucisare[i][1])
                               + " u = " + str(u) + " < " + str(probabilitate_mutatie) + " participate\n")
        else:
            if afisare:
                evolutie.write("chromosome " + str(i + 1) + "  " + str(populatie_dupa_incrucisare[i][1]) + " "
                               + " u = " + str(u) + "\n")
    if afisare:
        pozitie = len(populatie_dupa_selectie) - 1
        evolutie.write("chromosome " + str(pozitie + 1) + "  " + str(populatie_dupa_incrucisare[pozitie][1]) + " "
                       + " -> elitist chromosome \n")
    return populatie_dupa_mutatie


# function to display, if necessary, the population after the mutation process has taken place
# and retain chromosomes for the final population that will participate in the next stage
def populatie_finala(populatie_dupa_mutatie, afisare):
    nr = 1
    populatie_finala = []
    valoare_din_interval = []
    maxi = -1
    x_maxi = -1
    valoare_performanta = 0
    for i in populatie_dupa_mutatie:
        populatie_finala.append(i[1])
        valoare_din_interval.append(valoare_interval(lungime_cromozom, i[1]))
        if afisare:
            evolutie.write(str(nr) + ": " + str(i[1]) + " x = " + str(i[2]) + " f = " + str(i[3]) + "\n")
        if i[3] > maxi:
            maxi = i[3]
            x_maxi = i[2]
        valoare_performanta += i[3]
        nr += 1
    return populatie_finala, maxi, valoare_performanta, valoare_din_interval, x_maxi


# displaying steps for the initial population
evolutie.write("Initial population\n")
valori_functie = afisare_populatie(cromozomi, valoare_din_interval, coeficienti_functie, 1)

evolutie.write("\nProbability selection\n")
probabilitati_selectie = calcul_probabilitati_selectie(valori_functie, 1)

evolutie.write("\nSelection probability intervals\n")
capete_intervale_selectie = calcul_intervale_probabilitati_selectie(probabilitati_selectie, 1)

cromozom_elitist_valoare, cromozom_elitist = selectie_elitista(valori_functie)
evolutie.write("\nUsing elitist selection, the chromosome " + str(cromozom_elitist + 1) + " is selected.\n")

evolutie.write("\nThe selection process\n")
perechi_interval = tuple(zip(capete_intervale_selectie[:len(capete_intervale_selectie)], capete_intervale_selectie[1:]))
populatie_dupa_selectie = selectie_metoda_ruletei(cromozomi, valoare_din_interval, valori_functie, perechi_interval, 1,
                                                  cromozom_elitist)

evolutie.write("\nAfter selection we have chromosomes:\n")
nr = 1
for i in populatie_dupa_selectie:
    evolutie.write(str(nr) + ": chromosome " + str(i[0] + 1) + "  " + str(i[1]) + "  x = " + str(i[2])
                   + "  f = " + str(i[3]) + "\n")
    nr += 1

evolutie.write("\nHaving the probability of crossing:  " + str(probabilitate_recombinare) +
               ", the chromosomes that participate in the crossing are:\n")
cromozomi_selectati_recombinare = gaseste_cromozomii_care_participa_la_incrucisare(populatie_dupa_selectie, 1)

evolutie.write("\nThe crossover process:\n")
populatie_dupa_incrucisare = proces_de_incrucisare(populatie_dupa_selectie, cromozom_elitist,
                                                   cromozomi_selectati_recombinare, 1)

evolutie.write("\nPopulation after crossing:\n")
nr = 1
for i in populatie_dupa_incrucisare:
    evolutie.write(str(nr) + ": " + str(i[1]) + " x = " + str(i[2]) + " f = " + str(i[3]) + "\n")
    nr += 1

evolutie.write("\nThe mutation probability for each gene is: " + str(probabilitate_mutatie) + "\n")
populatie_dupa_mutatie = proces_mutatie(populatie_dupa_incrucisare, 1)

evolutie.write("\nPopulation after mutation:\n")
populatia_finala, maxi, valoare_performanta, valoare_din_interval, x_maxi = populatie_finala(populatie_dupa_mutatie, 1)
valoare_medie_performanta = valoare_performanta / dimensiune_populatie

evolutie.write("\nThe evolution of the maximum:\n")
evolutie.write("Generation " + str(1) + "\n")
evolutie.write(
    "Maximul: " + str(maxi) + "; The average value of performance: " + str(valoare_medie_performanta) + ", x =" + str(
        x_maxi) + "\n")

maxim_anterior = maxi
nr = 1

for i in range(2, nr_etape + 1):
    evolutie.write("Generation " + str(i) + "\n")

    valori_functie = afisare_populatie(populatia_finala, valoare_din_interval, coeficienti_functie, 0)

    probabilitati_selectie = calcul_probabilitati_selectie(valori_functie, 0)

    capete_intervale_selectie = calcul_intervale_probabilitati_selectie(probabilitati_selectie, 0)

    cromozom_elitist_valoare, cromozom_elitist = selectie_elitista(valori_functie)

    perechi_interval = tuple(
        zip(capete_intervale_selectie[:len(capete_intervale_selectie)], capete_intervale_selectie[1:]))
    populatie_dupa_selectie = selectie_metoda_ruletei(populatia_finala, valoare_din_interval, valori_functie,
                                                      perechi_interval, 0, cromozom_elitist)

    cromozomi_selectati_recombinare = gaseste_cromozomii_care_participa_la_incrucisare(populatie_dupa_selectie, 0)

    populatie_dupa_incrucisare = proces_de_incrucisare(populatie_dupa_selectie, cromozom_elitist,
                                                       cromozomi_selectati_recombinare, 0)

    populatie_dupa_mutatie = proces_mutatie(populatie_dupa_incrucisare, 0)

    populatia_finala, maxi, valoare_performanta, valoare_din_interval, x_maxi = populatie_finala(populatie_dupa_mutatie,
                                                                                                 0)
    valoare_medie_performanta = valoare_performanta / dimensiune_populatie

    evolutie.write(
        "Maximum: " + str(maxi) + "; The average value of performance: " + str(valoare_medie_performanta) + ", x =" + str(
            x_maxi) + "\n")

    if maxi == maxim_anterior:
        nr += 1
    else:
        nr = 1

    maxim_anterior = maxi

    if nr == 10:
        break
