import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()            # definizione di un grafo
        self._nodes = DAO.getAllNodes()     # aggiunge i nodi

        # Un dizionario che associerà ad ogni chiave primaria l'oggetto artObject corrispondente
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n

    def getInfoCompConnessa(self, id_oggetto):
        # Cercare la componente connessa che contiene id_oggetto
        if not self.hasNode(id_oggetto):
            return None

        source = self._idMapAO[id_oggetto]

        # Strategia 1
        dfsTree = nx.dfs_tree(self._graph, source)
        print("size connessa con dfs_tree", len(dfsTree.nodes()))

        # Strategia 2
        dfsPred = nx.dfs_predecessors(self._graph, source)
        print("size connessa con dfs_predecessors", len(dfsPred.values()))      # Si scarta l'ultimo nodo

        # Strategia 3
        conn = nx.node_connected_component(self._graph, source)
        print("size connessa con node_connected_component", len(conn))

        return len(conn)

    def hasNode(self, id_oggetto):
        return id_oggetto in self._idMapAO

    def buildGraph(self):
        # aggiunge tutti i nodi presenti nella lista self._nodes dentro il grafo NetworkX.
        self._graph.add_nodes_from(self._nodes)

        # Un arco collega due oggetti se sono stati esposti contemporaneamente nella stessa exhibition
        self.addEdgesV2()                             # aggiunge gli archi

    # SISTEMA INEFFICIENTE, CI METTE MOLTO A STAMPARE
    def addEdges(self):
        for u in self._nodes:               # ciclo su tutti i nodi
            for v in self._nodes:               # ciclo su tutti i nodi
                peso  = DAO.getEdgePeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight = peso)
                    print(f"Aggiunto arco fra {u} e {v} con peso {peso}")

    # Alternativa: LAVORARE SULLA QUERY RENDENDOLA PIU' COMPLESSA
    def addEdgesV2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

