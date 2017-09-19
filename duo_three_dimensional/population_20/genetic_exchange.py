""" change gen number """
import bge
import random

print("genetic_exchange start")

gen = 1

cont = bge.logic.getCurrentController()
scene = bge.logic.getCurrentScene()
own = cont.owner

survivorsFile = open(bge.logic.expandPath("//survivors.csv"), 'w')

num = 1
list = []

for i in range(0, 9):
    o = scene.objects[i]
    prop_names = o.getPropertyNames()

    survivorsFile.write(o.name + "\n")
    geneFile = open(bge.logic.expandPath("//Gen" + str(gen) + "/" + str(num) + ".csv"), 'w')

    for n in prop_names:
        geneFile.write(str(o[n]) + "\n")
        list.append(o[n])

    geneFile.close()
    num += 1

survivorsFile.close()

for o in range(0, 11):  # for each object
    geneFile = open(bge.logic.expandPath("//Gen" + str(gen) + "/" + str(num) + ".csv"), 'w')

    for p in range(0, 6):  # for each property
        if random.random() < 0.5:
            x = random.randrange(-20, 20)
            geneFile.write(str(x) + "\n")
        else:
            x = random.randrange(0, len(list))
            geneFile.write(str(list[x]) + "\n")

    geneFile.close()
    num += 1

print("genetic_exchange end")
