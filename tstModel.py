# VA A TESTARE IL METODO buildGraph nel Model
from model.model import Model

mdl = Model()
mdl.buildGraph()
print(f"Il grafo creato contiene {mdl.getNumNodes()} nodi e {mdl.getNumEdges()} archi")

mdl.getInfoCompConnessa(1224)