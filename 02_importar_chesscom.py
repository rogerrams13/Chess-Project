import requests

headers = {"User-Agent": "ProjecteEscacs/1.0 (contacte: #AFEGIR EMAIL)"}
NOM_FITXER = "les_meves_partides.pgn"
usuari=#AFEGIR USUARI

url_arxius = f"https://api.chess.com/pub/player/{usuari}/games/archives"
resposta_arxius = requests.get(url_arxius, headers=headers)

if resposta_arxius.status_code == 200:
    llista_mesos = resposta_arxius.json().get("archives", [])
    print(f"S'han trobat {len(llista_mesos)} mesos amb partides.")

    partides_totals_comptades = 0

    with open(NOM_FITXER, "w", encoding="utf-8") as fitxer_pgn:
        for url_mes in llista_mesos:
            fragments = url_mes.split("/")
            any_mes = f"{fragments[-2]}-{fragments[-1]}"

            print(f"Descarregant i desant partides de {any_mes}...")

            resposta_mes = requests.get(url_mes, headers=headers)
            if resposta_mes.status_code == 200:
                partides_del_mes = resposta_mes.json().get("games", [])

                for partida in partides_del_mes:
                    text_pgn_partida = partida.get("pgn")

                    if text_pgn_partida:
                        fitxer_pgn.write(text_pgn_partida + "\n\n")
                        partides_totals_comptades += 1

        print(f"Procés finalitzat amb èxit!")
    print(
        f"S'han desat {partides_totals_comptades} partides a: '{NOM_FITXER}'"
    )
    
else:
    print(
        f"No s'ha pogut accedir als teus arxius (Codi: {resposta_arxius.status_code})"
    )