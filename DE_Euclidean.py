import random
import cv2
import math
import imageio

MAX_NUMBER_OF_FRAMES = 100

TOTAL_KEY_FRAMES = 10

STOPPING_ITERATION = 40

NUMBER_OF_NP_CANDIDATES = 10

# Location to read images from.
# NOTE: "_" is used to follow a naming convention
# eg. _20.jpg, _21.jpg etc...
READ_LOCATION = "./frames/_"

# Location to write GIF images to.
GIF_WRITE_LOCATION = "./DE_Euclidean.GIF"

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

# Calculate AED for a chromosome.
def getAED( KF ):
    ED_sum = 0
    for i in range(1, TOTAL_KEY_FRAMES - 1):
        while True:
            try:
                im1 = cv2.imread(READ_LOCATION + str(KF[i]) + ".jpg",0)
                im2 = cv2.imread(READ_LOCATION + str(KF[i+1]) + ".jpg",0)
                ED_sum += cv2.norm(im1, im2, cv2.NORM_L2)
            except:
                print(i, KF, KF[i], KF[i+1])
                continue
            break
    return ED_sum/(TOTAL_KEY_FRAMES - 1)

# INITIALISATION : Generates population NP of 10 parent vectors (and AEDs).
def initialize_NP():
    for i in range(NUMBER_OF_NP_CANDIDATES):
        NP.append(sorted(random.sample(range(1, MAX_NUMBER_OF_FRAMES+1), TOTAL_KEY_FRAMES)))
        NP[-1].append(getAED(NP[-1]))
        print(NP[-1])

# MUTATION
def mutation(num):
    R = random.sample(NP,3)
    global MV
    MV[:] = []
    MV_value = 0
    for i in range(TOTAL_KEY_FRAMES):
        MV_value = int(NP[num][i] + F*(R[1][i] - R[2][i]))
        if(MV_value < 1):
            MV.append(1)
        elif(MV_value > MAX_NUMBER_OF_FRAMES):
            MV.append(MAX_NUMBER_OF_FRAMES)
        else:
            MV.append(MV_value)
    MV.sort()
    MV.append(getAED(MV))

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
    TV.append(getAED(TV))
    print("TV    : ", TV)

# SELECTION : Selects offspring / parent based on higher ED value.
def selection(parent, trail_vector):
    if(trail_vector[-1] > parent[-1]):
        parent[:] = trail_vector
        print("yes", parent)
    else:
        print("no")

# bestParent returns the parent with then maximum ED value.
def bestParent(population):
    Max_AED_value = population[0][-1]
    Best_Parent_Index = population[0]
    for parent in population:
        if (parent[-1] > Max_AED_value):
            Max_AED_value = parent[-1]
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

