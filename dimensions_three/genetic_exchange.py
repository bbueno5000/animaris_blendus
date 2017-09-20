import bge
import random

GENERATION = 1
N_SURVIVORS = 9
POP_SIZE = 10

print("genetic_exchange start")

cont = bge.logic.getCurrentController()
scene = bge.logic.getCurrentScene()
own = cont.owner

survivorsFile = open(bge.logic.expandPath("//survivors.csv"), 'w')
geneFileX = open(bge.logic.expandPath("//x.csv"), 'w')
geneFileY = open(bge.logic.expandPath("//y.csv"), 'w')

num = 1
list = []
for i in range(0, N_SURVIVORS):
    o = scene.objects[i]
    prop_names = o.getPropertyNames()
    survivorsFile.write(o.name + "\n")
    geneFile = open(bge.logic.expandPath("//Generation" + GENERATION + "\\" + str(num) + ".csv"), 'w')

    geneFileX.write(str(o[prop_names[0]]) + "\n")
    geneFileX.write(str(o[prop_names[1]]) + "\n")
    geneFileX.write(str(o[prop_names[2]]) + "\n")
    geneFileY.write(str(o[prop_names[3]]) + "\n")
    geneFileY.write(str(o[prop_names[4]]) + "\n")
    geneFileY.write(str(o[prop_names[5]]) + "\n")

    for n in prop_names:
        geneFile.write(str(o[n]) + "\n")
        list.append(o[n])

    geneFile.close()
    num += 1

survivorsFile.close()

for i in range(0, (POP_SIZE - N_SURVIVORS)):  # for each object

    geneFile = open(bge.logic.expandPath("//Gen1\\" + str(num) + ".txt"), 'w')

    for j in range(0, 6):  # for each property
        if random.random() < 0.5:
            x = random.randrange(-20, 20)
            geneFile.write(str(x) + "\n")
        else:
            x = random.randrange(0, len(list))
            geneFile.write(str(list[x]) + "\n")

    geneFile.close()
    num += 1

geneFileX.close()
geneFileY.close()

print("genetic_exchange end")

