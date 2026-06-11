import chess.pgn
import pymysql

nom_fitxer_pgn="les_meves_partides.pgn"
usuari=#AFEGIR USUARI

#Considerarem només les partides on juguem en blanques les obertures Ruy López, Gambit de Dama o Anglesa
historial_obertures={ 
    "C60": {"victories": 0, "taules":0, "derrotes":0, "totals":0, "fitxer":"ruy_lopez.pgn"},
    "D30": {"victories": 0, "taules":0, "derrotes":0, "totals":0, "fitxer":"gambit_dama.pgn"},
    "A10": {"victories": 0, "taules":0, "derrotes":0, "totals":0, "fitxer": "anglesa.pgn"}
}

#Funció per agrupar les variants de les obertures que considerem
def simplificar_eco(eco_partida):
    if not eco_partida or len(eco_partida) < 3:
        return None

    lletra = eco_partida[0]

    try:
        numero = int(eco_partida[1:3])
    except ValueError:
        return None

    # Gambit de dama acceptat + gambit de dama rebutjat
    if lletra == "D" and 6 <= numero <= 69:
        return "D30" 

    # Ruy López
    elif lletra == "C" and 60 <= numero <= 99:
        return "C60"  # Ruy López
    # Obertura anglesa
    elif lletra == "A" and 10 <= numero <= 39:
        return "A10"  # Obertura anglesa

    # Si és una altra obertura, ignorem la partida
    return None

#Creem un fitxer per cada obertura per guardar-hi totes les partides 
with open("ruy_lopez.pgn", "w", encoding="utf-8") as fitxer_ruy, \
     open("gambit_dama.pgn", "w", encoding="utf-8") as fitxer_dama, \
     open("anglesa.pgn", "w", encoding="utf-8") as fitxer_anglesa:
    
    fitxers_oberts = {
        "C60": fitxer_ruy,
        "D30": fitxer_dama,
        "A10": fitxer_anglesa
    }

    partides_processades=0

    with open(nom_fitxer_pgn, "r", encoding="utf-8") as pgn_origen:
        while True:

            text_partida=chess.pgn.read_game(pgn_origen)

            if text_partida is None:
                break

            partides_processades+=1

            #Comprovem que jugàvem amb blanques
            jugador_blanc=text_partida.headers.get("White", "Desconegut")
            soc_blanques=jugador_blanc.lower()==usuari.lower()

            #Obtenim el codi eco de la partida i el simplifiquem                                      
            codi_eco=text_partida.headers.get("ECO", "")
            eco_simplificat=simplificar_eco(codi_eco)

            #Si no som blanques o no es juga una de les 3 obertures, ometem la partida
            if eco_simplificat in historial_obertures and soc_blanques:
                #Guardem la partida al fitxer corresponent
                desti=fitxers_oberts[eco_simplificat]
                desti.write(str(text_partida) + "\n\n")

                #Guardem el resultat i actualitzem comptadors
                resultat=text_partida.headers.get("Result", "*")
                historial_obertures[eco_simplificat]["totals"]+=1

                if resultat=="1/2-1/2":
                    historial_obertures[eco_simplificat]["taules"]+=1
                elif resultat=="1-0":
                    historial_obertures[eco_simplificat]["victories"]+=1
                elif resultat=="0-1":
                    historial_obertures[eco_simplificat]["derrotes"]+=1

#Imprimim resultats
print(f"S'han processat {partides_processades} partides, de les quals:\n")

print(f"Hem jugat la Ruy López {historial_obertures['C60']['totals']} vegades, amb balanç de:")
print(f"{historial_obertures['C60']['victories']} victòries, {historial_obertures['C60']['taules']} taules i {historial_obertures['C60']['derrotes']} derrotes.\n")

print(f"Hem jugat Gambit de dama {historial_obertures['D30']['totals']} vegades, amb balanç de:")
print(f"{historial_obertures['D30']['victories']} victòries, {historial_obertures['D30']['taules']} taules i {historial_obertures['D30']['derrotes']} derrotes.\n")

print(f"I hem jugat Anglesa {historial_obertures['A10']['totals']} vegades, amb balanç de:")
print(f"{historial_obertures['A10']['victories']} victòries, {historial_obertures['A10']['taules']} taules i {historial_obertures['A10']['derrotes']} derrotes.\n")

#Connectem amb la base de dades de MySQL
connexio=pymysql.connect(host="localhost", user="root", password="INTRODUIR CLAU PROPIA!", database="escacs")
cursor=connexio.cursor()

#Netegem la taula per si hi han hagut canvis en les nostres dades
cursor.execute("DELETE FROM rendiment_propi")

#Calculem el rendiment de cada obertura
rendiment_1=historial_obertures["C60"]["victories"]+0.5*historial_obertures["C60"]["taules"]
rendiment_1=rendiment_1/historial_obertures["C60"]["totals"]

rendiment_2=historial_obertures["D30"]["victories"]+0.5*historial_obertures["D30"]["taules"]
rendiment_2=rendiment_2/historial_obertures["D30"]["totals"]

rendiment_3=historial_obertures["A10"]["victories"]+0.5*historial_obertures["A10"]["taules"]
rendiment_3=rendiment_3/historial_obertures["A10"]["totals"]

#Introduim les nostres dades a la BD
dades=[("C60", rendiment_1, historial_obertures["C60"]["totals"]), 
       ("D30", rendiment_2, historial_obertures["D30"]["totals"]),
       ("A10", rendiment_3, historial_obertures["A10"]["totals"])]

cursor.executemany("INSERT INTO rendiment_propi (obertura, rendiment, partides) VALUES (%s,%s,%s)", 
                   dades)

#I tanquem la connexió
connexio.commit()
cursor.close()
connexio.close()

print("Dades guardades a la base de dades")