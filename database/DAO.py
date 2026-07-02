from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNodes():

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """SELECT *
                from objects o """

        cursor.execute(query)

        for row in cursor:
            res.append(ArtObject(**row))

        cursor.close()
        conn.close()
        return res

    # Nel model unito a addEdges: "Quante volte queste due opere sono state esposte insieme nella stessa mostra?"
    @staticmethod
    def getEdgePeso(v1, v2):                        # data una coppia di nodi v1 e v2

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        # Per ciascuna coppia di nodi si va a prendere il peso che devo inserire nel mio grafo
        query = """Select eo.object_id as o1, eo2.object_id as o2, count(*)
                    from exhibition_objects eo, exhibition_objects eo2 
                    where eo.exhibition_id = eo2.exhibition_id            # considera solo le opere appartenenti alla stessa mostra
                    and eo.object_id < eo2.object_id                      # serve a evitare duplicati
                    and eo.object_id = %s and eo2.object_id = %s          # cerca la coppia passata alla funzione
                    group by eo.object_id, eo2.object_id"""               # deve raggruppare tutte le righe della stessa coppia

        cursor.execute(query, (v1.object_id, v2.object_id))

        for row in cursor:
            res.append(row["peso"])

        cursor.close()
        conn.close()

        if len(res) == 0:
            return None    # Se le due opere non sono mai state esposte insieme, la query non restituisce righe: NO ARCHI TRA I 2 NODI

        return res

    # Nel model è unito a addEdgesV2: "Trova TUTTE le coppie di opere che sono state esposte insieme"
    @staticmethod
    def getAllEdges(idMapAO):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """SELECT eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                   FROM exhibition_objects eo, exhibition_objects eo2
                   WHERE eo.exhibition_id = eo2.exhibition_id
                     and eo.object_id < eo2.object_id
                   group by eo.object_id, eo2.object_id
                   order by peso desc """

        cursor.execute(query)

        for row in cursor:
            # res.append((o1, o2, peso))

            # Creo un oggetto Arco
            res.append(Arco(idMapAO[row["o1"]], idMapAO[row["o2"]], row["peso"]))

        cursor.close()
        conn.close()
        return res

