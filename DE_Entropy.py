import random
import cv2
import math
import imageio
from sklearn.metrics.cluster import entropy

MAX_NUMBER_OF_FRAMES = 100

TOTAL_KEY_FRAMES = 10

STOPPING_ITERATION = 40

NUMBER_OF_NP_CANDIDATES = 10

# Location to read images from.
# NOTE: "_" is used to follow a naming convention
# eg. _20.jpg, _21.jpg etc...
READ_LOCATION = "./frames/_"

# Location to write GIF images to.
GIF_WRITE_LOCATION = "./DE_Entropy.GIF"

# Population matrix.
NP = []

# Mutation vector.
MV = []

# Trail vector.
TV = []

# Scale factor.
F = 0.9

# Cr probability value.
Cr = 0.6

# Calculate Average Entropy Difference for a chromosome.
def getEntropy( KF ):
    entropy_sum = 0
    for i in range(1, TOTAL_KEY_FRAMES - 1):
        while True:
            try:
                im1 = cv2.imread(READ_LOCATION + str(KF[i]) + ".jpg",0)
                im2 = cv2.imread(READ_LOCATION + str(KF[i+1]) + ".jpg",0)
                entropy_sum += abs(entropy(im1) - entropy(im2))
            except:
                print(i, KF, KF[i], KF[i+1])
                continue
            break
    return entropy_sum/(TOTAL_KEY_FRAMES - 1)

# INITIALISATION : Generates population NP of 10 parent vectors (and Average Entropy Differences).
def initialize_NP():
    for i in range(NUMBER_OF_NP_CANDIDATES):
        NP.append(sorted(random.sample(range(1, MAX_NUMBER_OF_FRAMES+1), TOTAL_KEY_FRAMES)))
        NP[-1].append(getEntropy(NP[-1]))
        print(NP[-1])

# MUTATION
def mutation(parent):
    R = random.sample(NP,2)
    global MV
    MV[:] = []
    MV_value = 0
    print(NP[parent])
    for i in range(TOTAL_KEY_FRAMES):
        MV_value = int(NP[parent][i] + F*(R[0][i] - R[1][i]))
        if(MV_value < 1):
            MV.append(1)
        elif(MV_value > MAX_NUMBER_OF_FRAMES):
            MV.append(MAX_NUMBER_OF_FRAMES)
        else:
            MV.append(MV_value)
    MV.sort()
    MV.append(getEntropy(MV))

# CROSSOVER (uniform crossover with Cr = 0.6).
def crossover(parent, mutant):
    print("mutant: ", mutant)
    print("parent: ", parent)
    for j in range(TOTAL_KEY_FRAMES) :
        if(random.uniform(0,1) < Cr) :
            TV.append(mutant[j])
        else:
            TV.append(parent[j])
    TV.sort()
    TV.append(getEntropy(TV))
    print("TV    : ", TV)

# SELECTION : Selects offspring / parent based on higher Entropy diff. value.
def selection(parent, trail_vector):
    if(trail_vector[-1] > parent[-1]):
        parent[:] = trail_vector
        print("yes", parent)
    else:
        print("no")

# bestParent returns the parent with then maximum Entropy diff. value.
def bestParent(population):
    Max_Entropy_value = population[0][-1]
    Best_Parent_Index = population[0]
    for parent in population:
        if (parent[-1] > Max_Entropy_value):
            Max_Entropy_value = parent[-1]
            Best_Parent_Index = parent
    return Best_Parent_Index

initialize_NP()
for GENERATION in range(STOPPING_ITERATION):
    for i in range(NUMBER_OF_NP_CANDIDATES):
        print("---------------------", "PARENT:", i+1 , "GENERATION:", GENERATION+1, "---------------------")
        mutation(i)
        crossover(NP[i], MV)
        selection(NP[i], TV)
        print(NP[i])
        TV[:] = []
        print("")
    print("")
best_parent = bestParent(NP)
print("best solution is: ", best_parent)
images_for_gif = []
for frame_number in best_parent[:-1]:
        images_for_gif.append(imageio.imread(READ_LOCATION + str(frame_number) + '.jpg'))
imageio.mimsave(GIF_WRITE_LOCATION, images_for_gif)

