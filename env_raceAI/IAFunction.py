from random import randint
import pygame


#-----------------------------------------------------------------------------
#function to display every car controlled by the AI
def draw_car(win, aiCars):
    for aicar in aiCars:
        aicar.draw(win)

#function to move the aiCar randomly or create a childrenList according to the decisionList of the two parents
def move_ai(aicar):
    if len(aicar.decisionList) == 0:
        decision = randint(0,2)
        aicar.decisionList.append(decision)
    elif (len(aicar.decisionList) != 0) and (aicar.iteration != len(aicar.decisionList)-1):
        decision=aicar.decisionList[aicar.iteration]
        aicar.iteration += 1
    else:   
        decision = randint(0,2)
        aicar.decisionList.append(decision)

    if not aicar.collide:
        aicar.move_forward()
        if decision==0:
            aicar.rotate(left=True)
        elif decision==1:
            aicar.rotate(right=True)
        else:
            pass
    aicar.update()

#-----------------------------------------------------------------------------
#Genetic Algorithm function

#get the fitness value of each car controlled by the AI
def fitness(aicar):
    aicar.fitnessValue = 2000 - aicar.distTraveled + aicar.numbOfTurn/2

#create the list of the father and the mother according to the car which is parentOne or parentTwo
#According to these two parents list, create for each children a list who each cell has the same probability to have the cell of the mother or the father
def crossover(aiCars, achieveTurn):#aicar
    if not achieveTurn:
        father, mother = list(), list()
        for aicar in aiCars:
            if aicar.parentOne==True:
                father = aicar.decisionList[:len(aicar.decisionList)-3]
                aicar.decisionList = father

            elif aicar.parentTwo==True:
                mother = aicar.decisionList[:len(aicar.decisionList)-3]
                aicar.decisionList = mother

        for aicar in aiCars:
            if (aicar.parentOne==False) and (aicar.parentTwo==False):
                aicar.decisionList = list()
                for i in range(len(father)):
                    random = randint(1,2)
                    if random == 1:
                        aicar.decisionList.append(father[i])
                    elif (random == 2) and (i<len(mother)):
                        aicar.decisionList.append(mother[i])
                    else:
                        aicar.decisionList.append(father[i])
    else:
        father = list()
        for aicar in aiCars:
            if aicar.achieveFlag:
                father = aicar.decisionList
        for aicar in aiCars:
            aicar.decisionList = father

    
#each cell of each list has 0.4% to see his cell randomly changed
def mutation(aiCars):
    for aicar in aiCars:
        for i in range(len(aicar.decisionList)):
                random = randint(1,2000) #0.05%
                if random==1:
                    aicar.decisionList[i]=randint(0,2)
    



