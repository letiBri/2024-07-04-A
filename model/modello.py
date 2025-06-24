import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapSighting = {}
        for s in DAO.get_all_sightings():
            self._idMapSighting[s.id] = s

        self._bestPath = []
        self._bestScore = 0

    def getYears(self):
        return DAO.getYears()

    def getShapeYear(self, year):
        return DAO.getShapeYear(year)

    def buildGraph(self, year, shape):
        self._graph.clear()

        nodes = DAO.getNodes(year, shape)
        self._graph.add_nodes_from(nodes)

        allEdges = DAO.getEdges(year, shape, self._idMapSighting)
        for e in allEdges:
            self._graph.add_edge(e[0], e[1])

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getInfoConnesseDeboli(self):
        cc = nx.number_weakly_connected_components(self._graph)
        return cc

    def getLargestConnessaDebole(self):
        cc = list(nx.weakly_connected_components(self._graph))
        cc.sort(key=lambda x: len(x), reverse=True)
        return cc[0]

    # punto 2 ricorsione
    def getOptimalPath(self):
        self._bestPath = []
        self._bestScore = 0
        for node in self._graph.nodes:
            parziale = [node]
            ammissibili = self.getAmmissibili(parziale)
            self._ricorsione(parziale, ammissibili)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, ammissibili):
        if len(ammissibili) == 0:
            if self.getScore(parziale) > self._bestScore:
                self._bestScore = self.getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
        else:
            for n in ammissibili:
                parziale.append(n)
                nuovi_ammissibili = self.getAmmissibili(parziale)
                self._ricorsione(parziale, nuovi_ammissibili)
                parziale.pop()

    def getAmmissibili(self, parziale):
        ammissibili = []
        for n in list(self._graph.successors(parziale[-1])):  # successors oggetto iteratore
            if n.duration > parziale[-1].duration:
                if self.vincoloAvvistamenti(parziale, n):
                    ammissibili.append(n)
        return ammissibili

    def vincoloAvvistamenti(self, parziale, nodo):
        contaAvvistamenti = 0
        for n in parziale:
            if n.datetime.month == nodo.datetime.month:
                contaAvvistamenti += 1
        if contaAvvistamenti < 3:
            return True
        return False

    def getScore(self, parziale):
        punteggio = 0
        punteggio += 100 * len(parziale)
        for i in range(1, len(parziale)):
            if parziale[i].datetime.month == parziale[i - 1].datetime.month:
                punteggio += 200
        return punteggio

