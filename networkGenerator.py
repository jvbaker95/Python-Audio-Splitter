import networkx as nx
import matplotlib.pyplot as plt

def convertName(name):
    namelist = name.split(" ")
    firstname = namelist.pop(0)
    lastname = " ".join(namelist)
    processedname = "%s\n%s" % (firstname, lastname)
    return processedname


file = "relationships.csv"
file = open(file)
rawtext = file.read().split("\n")
rawtext.pop(0)

relationset = set()
namelist = set()

for nameset in rawtext:
    cleanednameset = nameset.replace("\t\t","")
    person = cleanednameset.split(",")

    #Take each relationship and turn it into a tuple, and add it to a relationship set.

    person1 = convertName(person[0])
    person2 = convertName(person[1])

    tuple = (person1,person2)
    relationset.add(tuple)

G = nx.Graph()
G.add_edges_from(relationset)

nodelist = G.nodes
#G = nx.convert_node_labels_to_integers(G)

nx.draw_networkx(G,font_color="white",font_size="7",node_size=1500,edge_color="grey",node_shape="o")

plt.show()
nx.write_graphml(G,'SNA.graphml')
