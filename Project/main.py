# main.py

import json
from flask import Blueprint, render_template, request
from . import cursor
from .algorithms.Graph import *

main = Blueprint('main', __name__)


# initialiser le graph

cursor.execute("Select * from nomVilles")
cities = cursor.fetchall()

cursor.execute("Select * from distances")
distances = cursor.fetchall()

edges = []
for distance in distances:
    cursor.execute("Select nom from nomVilles where id_nomVilles = %d;" % distance[0])
    cur = cursor.fetchone()
    src = str(cur[0])
    cursor.execute("Select nom from nomVilles where id_nomVilles = %d;" % distance[1])
    cur = cursor.fetchone()
    dst = str(cur[0])
    edges.append((src, dst, int(distance[2])))

# add edges and nodes to Graph
edges= [
    ("AD-DAKHLA", "FES", 524),  ("AD-DAKHLA", "LAAYOUN", 472),  ("AGADIR", "TAN TAN", 331), ("AGADIR", "ESSAOUIRA", 173),
    ("AGADIR", "OURZAZATE", 273), ("AGADIR", "MARRAKECH", 375), ("AL HOCEIMA", "TETOUAN", 278),  ("AL HOCEIMA", "OUJDA", 293),
    ("AL HOCEIMA", "FES",275),("BENIMELLAL", "CASABLANCA", 220),("BENIMELLAL", "FES", 289),("BENIMELLAL", "MARRAKECH", 194),
    ("BENIMELLAL", "MEKNES", 278),("BENIMELLAL", "RABAT", 260),("CASABLANCA", "BENIMELLAL", 220),("CASABLANCA", "EL JADIDA", 99),
    ("CASABLANCA", "MARRAKECH", 238),("CASABLANCA", "RABAT", 91),("TAN TAN", "AGADIR", 331),("TAN TAN", "LAAYOUN", 318),
    ("EL JADIDA", "CASABLANCA", 99),("EL JADIDA", "MARRAKECH", 197),("EL JADIDA", "SAFI", 157),("ESSAOUIRA", "AGADIR", 173),
    ("ESSAOUIRA", "MARRAKECH", 176),("ESSAOUIRA", "SAFI", 129),("FES", "AL HOCEIMA", 275),("FES", "BENIMELLAL", 289),
    ("FES", "MEKNES", 60),("FES", "TAZA", 120), ("FES", "TETOUAN", 285),("LAAYOUN", "AD-DAKHLA", 472),("LAAYOUN", "TAN TAN", 318),
    ("LAGWIRA", "AD-DAKHLA", 472),("MARRAKECH", "AGADIR", 273),("MARRAKECH", "BENIMELLAL", 194), ("MARRAKECH", "CASABLANCA", 238),
    ("MARRAKECH", "EL JADIDA", 197),("MARRAKECH", "ESSAOUIRA", 176),("MARRAKECH", "OURZAZATE", 204),("MARRAKECH", "SAFI", 157),
    ("MEKNES", "BENIMELLAL", 278), ("MEKNES", "FES", 60),("MEKNES", "RABAT", 138),("OURZAZATE", "AGADIR", 375),
    ("OURZAZATE", "MARRAKECH", 204),("OUJDA", "AL HOCEIMA", 293),("OUJDA", "TAZA", 223),("RABAT", "BENIMELLAL", 260),
    ("RABAT", "MEKNES", 138),("RABAT", "CASABLANCA", 91),("RABAT", "TANGER", 278),("SAFI", "EL JADIDA", 157),("SAFI", "ESSAOUIRA",129 ),
    ("SAFI", "MARRAKECH", 157),("TANGER", "RABAT", 278),("TANGER", "TETOUAN", 75),("TAZA", "FES", 120),("TAZA", "OUJDA", 223),
    ("TETOUAN", "AL HOCEIMA", 278),("TETOUAN", "FES", 285),("TETOUAN", "TANGER", 75)]
cities = list(set([city[0] for city in edges]+[city[1] for city in edges]))
myGraph2 = Graph(cities,edges)
#myGraph2 = Graph([('Tanger','Asila',3),('Asila','Larache',4),('Larache','Kenitra',5),('Kenitra','Rabat',44),('Rabat','Casa',54),('Safi','Essaouira',45),('Essaouira','Agadir',46),('Marrakech','Casa',103),('Marrakech','Safi',35),('Marrakech','Essaouira',37),('Marrakech','Agadir',354),('Marrakech','Ouarzazat',43),('Marrakech','BeniMelal',33),('Azrou','Errachidia',35),('Azrou','BeniMelal',66),('Azrou','Sfrou',56),('Azrou','Meknas',14),('Meknas','Fes',36),('Meknas','Rabat',35),('Meknas','Ouezzane',35),('Ouezzane','Fes',36),('Ouezzane','Chefchaouen',35),('Ouezzane','Larache',36),('Fes','Sfrou',53),('Fes','Taza',36),('Taza','Oujda',35),('Oujda','Nador',36),('Nador','ELHocima',36),('Chefchaouen','Tetouen',34),('Larache','Tetouen',345),('Tetouen','Tanger',43)])



@main.route('/')
def index():
    """ the Home Page
    """
    cursor.execute("Select * from nomVilles")
    cities = cursor.fetchall()
    cities = list(set([city[0] for city in edges]+[city[1] for city in edges]))
    print(cities)
    return render_template('index.html', cities=cities)


def getWeights(path,sedges):
    """ Get the list of weights lists, in the case of bellman where the target are not given
    """
    weights = list()
    for spath in path:
        sousweight = list()
        for i in range(len(spath) - 2): 
            sousweight.append(myGraph2.get_weight(spath[i],spath[i+1]))
        weights.append(sousweight)
    return weights

@main.route('/find', methods=['POST'])
def finds():
    cursor.execute("Select * from nomVilles")
    cities = cursor.fetchall()
    cities = list(set([city[0] for city in edges]+[city[1] for city in edges]))
    #get informations from the form
    sourceCity = request.form.get('source')
    targetCity = request.form.get('target')
    algorithme = request.form.get('algorithme')

    if algorithme == "dijkstra":
        path = list(myGraph2.dijkstra(sourceCity, targetCity))
        return render_template("findDijkstra.html", cities=cities, jsonpath=json.dumps(path))

    elif algorithme == "bellmanAllTargets":
        paths = list(myGraph2.Bellman(sourceCity))
        weights = getWeights(paths,edges)
        return render_template("findBellman.html", cities=cities, jsonpath=json.dumps(paths),jsonweights=json.dumps(weights))

    elif algorithme == "bellmanOneTarget":
        path = list(myGraph2.Bellman(sourceCity,targetCity))[:-1]
        return render_template("findDijkstra.html", cities=cities, jsonpath=json.dumps(path))
    