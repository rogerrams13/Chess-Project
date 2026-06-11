import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

#Connectem amb la BD
engine=create_engine("mysql+pymysql://root:INTRODUIRCLAUPROPIA@localhost/escacs")

#Creem els dataframe amb les nostres dades i les dels gms
df_propi=pd.read_sql_query("SELECT * FROM rendiment_propi", engine)
df_gms=pd.read_sql_query("SELECT * FROM rendiment_gms", engine)

dades_propies=df_propi.set_index("obertura").to_dict(orient="index")
#print(dades_propies)

gms_agrupats=df_gms.groupby("nom")
dades_gms={}

for nom_gm, dades_gm in gms_agrupats:

    dades_netes=dades_gm[["obertura", "rendiment", "partides"]]
    perfil_gm=dades_netes.set_index("obertura").to_dict(orient="index")

    dades_gms[nom_gm]=perfil_gm

#print(dades_gms)

#Un cop tenim les dades ben estructurades, podem passar a comparar el nostre rendiment amb els gms

distancia_user_gms=[]
obertures=["A10", "C60", "D30"]

for nom_gm, dades_gm in dades_gms.items():

    suma_distancies=0
    suma_pesos=0

    for ob in obertures:

        rendiment_propi=dades_propies[ob]["rendiment"]
        partides_propies=dades_propies[ob]["partides"]

        rendiment_gm=dades_gms[nom_gm][ob]["rendiment"]
        partides_gm=dades_gms[nom_gm][ob]["partides"]

        pes_obertura=1/(1+abs(np.log10(partides_propies)-np.log10(partides_gm)))
        distancia=(rendiment_propi-rendiment_gm)**2

        suma_distancies+=distancia*pes_obertura
        suma_pesos+=pes_obertura

    distancia_user_gm=np.sqrt(suma_distancies/suma_pesos)

    distancia_user_gms.append({"Gran Mestre": nom_gm, "Distància": distancia_user_gm})


#Guardem les distàncies i determinem la semblança entre el rendiment propi i el dels gms
#  
df_ranking=pd.DataFrame(distancia_user_gms)
df_ranking["Afinitat (%)"]=(1/(1+df_ranking["Distància"]))*100
df_ranking=df_ranking.sort_values(by="Afinitat (%)", ascending=False)

#I creem el gràfic per visualitzar els resultats
plt.figure(figsize=(8, 4))

ax=sns.barplot(
    x="Afinitat (%)",
    y="Gran Mestre",
    data=df_ranking,
    palette="Blues_r"
)

plt.title("Percentatge d'afinitat amb Grans Mestres", fontsize=14, pad=15, fontweight="bold")
plt.xlabel("Similitud d'estil (%)", fontsize=11)
plt.ylabel("Gran Mestre", fontsize=11)

plt.xlim(0,100)

plt.tight_layout()
plt.savefig("Resultats_finals.png", dpi=300)
plt.show()