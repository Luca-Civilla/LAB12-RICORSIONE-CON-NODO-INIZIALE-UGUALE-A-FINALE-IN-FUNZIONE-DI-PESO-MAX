import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodi = []
        self._grafo = nx.Graph()
        self.idMApRetailer = {}
        #RICORSIONE
        self._bestPath = []
        self._costo = 0


    def getPercorso(self,numero):
        self._bestPath = []
        self._costo = 0
        parziale = []
        for ret in self._nodi:
            parziale.append(ret)
            self._ricorsione(parziale,numero)
            parziale.pop()

        return self._bestPath,self._costo



    def _ricorsione(self,parziale,numero):
        #condizione finale
        if len(parziale) == numero+1:#DEVO STACCARE LE CONDIZIONI AFFINCHE' POSSA ENTRARE NEL CICLO
            if parziale[0] == parziale[-1] and self._calcolaCosto(parziale)>self._costo:
                self._bestPath = copy.deepcopy(parziale)
                self._costo = self._calcolaCosto(parziale)
                print(self._costo)

            return
        #VERIFICO SE POSSO AGGIUNGERE UN ALTRO ELEMENTO
        for v in self._grafo.neighbors(parziale[-1]):#STO CONTROLLANDO I VICINI DELL'ULTIMO NODO MESSO, ALL INZIO NE HO SEMPRE UNO CHE AGGIUNGO DA SELF._NODI
            #pesoArco = self._grafo[parziale[-1]][v]["weight"]

            if len(parziale) == (numero):
                parziale.append(v)
                self._ricorsione(parziale,numero)
                parziale.pop()
            else:
                if v not in parziale:
                    parziale.append(v)
                    self._ricorsione(parziale,numero)
                    parziale.pop()
        #CONDIZIONI SONO -------> V NOT IN PARZIALE, SOMMA DEI PESI MAX

    def _calcolaCosto(self, lista):#CALCOLO DI TUTTO IL COSTO DEGLI ARCHI
        if len(lista) <=1:
            return 0

        score = 0
        for i in range(0,len(lista)-1):
            score += self._grafo[lista[i]][lista[i+1]]["weight"]
        return score



    def getAllCountries(self):
        countries = DAO.getCountry()
        return countries

    def buildGraph(self, country,anno):
        self._grafo.clear()
        self._nodi = DAO.getRetailersOfCountry(country)
        self._grafo.add_nodes_from(self._nodi)

        self.idMApRetailer = {}
        for r in self._nodi:
            self.idMApRetailer[r.Retailer_code] = r

        self.creaArchi(anno)

    def creaArchi(self,anno):
        self._grafo.clear_edges()
        for u in self._nodi:
            for v in self._nodi:
                if u!= v:
                    peso = DAO.getPesoRetailers(anno,u.Retailer_code,v.Retailer_code)
                    if peso[0] >0:
                        self._grafo.add_edge(u,v, weight=peso[0])


    def volumeRetailers(self):
        listaPesi = []
        for u in self._nodi:
            peso = 0
            vicini = self._grafo.neighbors(u)
            for v in vicini:
                peso += self._grafo[u][v]["weight"]
            if peso >0:
                listaPesi.append((u,peso))
        return listaPesi




    def printGraphDetails(self):
        return (f"Grafo creato con {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi.")

