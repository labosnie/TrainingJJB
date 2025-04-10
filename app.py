import streamlit as st
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

# ... ici, tu définis toutes tes fonctions (ajouter_seance, generer_seance_cardio, afficher_historique, afficher_progression)

def ajouter_seance():
    st.header("Ajouter une séance")
    date_input = st.date_input("Date", value=datetime.date.today())
    type_seance = st.selectbox("Type de séance", ["Sparring", "Drilling", "Cardio", "Repos"])
    duree = st.number_input("Durée de la séance (min)", min_value=0)
    if st.button("Ajouter la séance"):
        new_data = pd.DataFrame([[date_input, type_seance, duree]], columns=["Date", "Type", "Durée (min)"])
        new_data.to_csv("log.csv", mode='a', header=False, index=False)
        st.success("Séance ajoutée avec succès !")

def generer_seance_cardio():
    import streamlit as st
import pandas as pd
import datetime
import random

def generer_seance_cardio():
    st.header("Générateur de Séance de Cardio aléatoire")
    
    # Choix du type de cardio
    type_cardio = st.selectbox("Choisissez le type de cardio", ["Rameur", "Vélo", "Course", "Assault Bike"])
    # Choix de l'intensité
    intensite = st.selectbox("Choisissez l'intensité", ["Faible", "Modéré", "Élevé"])
    # Demander la durée totale de la séance en minutes
    duree = st.number_input("Durée totale de la séance (min)", min_value=10, max_value=120, value=30)
    
    if st.button("Générer la séance"):
        plan = ""
        if intensite == "Faible":
            # Pour une intensité faible, on opte pour un travail continu
            # On choisit aléatoirement un échauffement et un cooldown (10-15% de la durée totale)
            warmup = random.randint(max(1, int(duree * 0.10)), max(1, int(duree * 0.15)))
            cooldown = random.randint(max(1, int(duree * 0.10)), max(1, int(duree * 0.15)))
            steady = duree - warmup - cooldown
            plan = (f"Votre séance de {duree} minutes en {type_cardio} sera structurée de la façon suivante :\n"
                    f"- Échauffement : {warmup} minutes\n"
                    f"- Phase principale (cardio continu à faible intensité) : {steady} minutes\n"
                    f"- Récupération : {cooldown} minutes")
        elif intensite == "Modéré":
            # Pour une intensité modérée, on propose des intervalles
            warmup = random.randint(4, 6)
            cooldown = random.randint(3, 5)
            remaining = duree - warmup - cooldown
            # On planifie des intervalles de 3 min effort + 2 min récupération (cycle de 5 min)
            interval_cycle = 5
            n_intervals = remaining // interval_cycle
            reste = remaining - n_intervals * interval_cycle
            if n_intervals > 0:
                plan = (f"Votre séance de {duree} minutes en {type_cardio} sera structurée ainsi :\n"
                        f"- Échauffement : {warmup} minutes\n"
                        f"- {n_intervals} intervalles composés de 3 minutes d'effort à intensité modérée et 2 minutes de récupération\n"
                        f"- Une phase additionnelle de {reste} minutes (à adapter entre effort et récupération selon votre ressenti)\n"
                        f"- Cooldown : {cooldown} minutes")
            else:
                plan = (f"Votre séance sera composée d'un échauffement de {warmup} minutes, "
                        f"d'une phase continue de {remaining} minutes, puis d'un cooldown de {cooldown} minutes.")
        elif intensite == "Élevé":
            # Pour une intensité élevée, on opte pour des intervalles courts et intenses
            warmup = random.randint(3, 5)
            cooldown = random.randint(3, 5)
            remaining = duree - warmup - cooldown
            # On prévoit des intervalles de 1 minute intense suivi de 1 minute de récupération (cycle de 2 minutes)
            if remaining >= 2:
                n_intervals = remaining // 2
                reste = remaining - n_intervals * 2
                plan = (f"Votre séance de {duree} minutes en {type_cardio} sera structurée comme suit :\n"
                        f"- Échauffement : {warmup} minutes\n"
                        f"- {n_intervals} intervalles composés d'1 minute à haute intensité suivie de 1 minute de récupération\n"
                        f"- Une phase complémentaire de {reste} minutes de travail continu\n"
                        f"- Cooldown : {cooldown} minutes")
            else:
                plan = (f"Votre séance sera composée d'un échauffement de {warmup} minutes, "
                        f"d'une phase de travail continu de {remaining} minutes, puis d'un cooldown de {cooldown} minutes.")
        
        # Affichage du plan généré
        st.write(plan)
        
        # Option pour enregistrer la séance générée dans l'historique
        enregistrer = st.checkbox("Enregistrer cette séance dans l'historique ?")
        if enregistrer:
            date = datetime.date.today()
            new_data = pd.DataFrame([[date, f"Cardio ({intensite})", duree]],
                                    columns=["Date", "Type", "Durée (min)"])
            new_data.to_csv("log.csv", mode='a', header=False, index=False)
            st.success("Séance de cardio enregistrée avec succès !")


def afficher_historique():
    st.header("Historique des séances")
    fichier = "log.csv"
    if os.path.exists(fichier) and os.path.getsize(fichier) > 0:
        df = pd.read_csv(fichier)
        st.dataframe(df)
    else:
        st.info("Aucune donnée disponible.")

def afficher_progression():
    st.header("Progression des séances")
    fichier = "log.csv"
    if os.path.exists(fichier) and os.path.getsize(fichier) > 0:
        df = pd.read_csv(fichier)
        durée_par_type = df.groupby("Type")["Durée (min)"].sum()
        fig, ax = plt.subplots()
        ax.bar(durée_par_type.index, durée_par_type.values, color='skyblue')
        ax.set_title("Durée d'entraînement par type de séance")
        ax.set_xlabel("Type de séance")
        ax.set_ylabel("Durée totale (minutes)")
        st.pyplot(fig)
    else:
        st.info("Aucune donnée d'entraînement disponible pour générer un graphique.")

# Ajout de la logique de navigation
page = st.sidebar.selectbox(
    "Choisissez une fonctionnalité",
    [
        "Ajouter une séance",
        "Générer une séance de cardio",
        "Afficher l'historique",
        "Afficher la progression"
    ]
)

if page == "Ajouter une séance":
    ajouter_seance()
elif page == "Générer une séance de cardio":
    generer_seance_cardio()
elif page == "Afficher l'historique":
    afficher_historique()
elif page == "Afficher la progression":
    afficher_progression()
