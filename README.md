# Determining the maximum for a function
**Project developed in Python, using using a genetic algorithm**

## Input data
* population size;
* domain of the function;
* parameters for the maximize function;
* the accuracy with which the interval is discretized;
* probability of recombination;
* probability of mutation;
* number of steps of the algorithm;

## Algorithm steps
1. Creation of the initial population: the population consists of chromosomes with genes equal to 1 or 0, of length: \
[![Formula-lungime.gif](https://i.postimg.cc/76gwDRg8/Formula-lungime.gif)](https://postimg.cc/vgHpt3q3)
2. Calculating the selection probabilities for each chromosome, where: \
[![Prob-Selectie.gif](https://i.postimg.cc/nrD7Hp3V/Prob-Selectie.gif)](https://postimg.cc/tn97kQ08)
3. Calculating the cumulative probabilities that give the intervals for selection
4. Using the elitist type selection, ie the chromosome with the highest fitness index will automatically pass to the next generation
5. Using the selection by the roulette method which consists in generating a random number u uniform on [0,1) and determining the selection interval to which this number belongs; the chromosome corresponding to the interval of which u is a part will be selected. The process is repeated until the desired number of chromosomes is selected.

 
