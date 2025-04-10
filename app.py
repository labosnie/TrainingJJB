import streamlit as st
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import random

# Injecter un peu de style responsive
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Fonctions
def ajouter_seance():
    st.subheader("Ajouter une séance")
    date_input = st.date_input("Date", value=datetime.date.today())
    type_seance = st.selectbox("Type de séance", ["Sparring", "Drilling", "Cardio", "Repos"])
    duree = st.number_input("Durée de la séance (min)", min_value=0)
    if st.button("Ajouter la séance"):
        new_data = pd.DataFrame([[date_input, type_seance, duree]], columns=["Date", "Type", "Durée (min)"])
        new_data.to_csv("log.csv", mode='a', header=False, index=False)
        st.success("Séance ajoutée avec succès !")

def generer_seance_cardio():
    st.subheader("Générateur de Séance de Cardio aléatoire")
    type_cardio = st.selectbox("Type de cardio", ["Rameur", "Vélo", "Course", "Assault Bike"])
    intensite = st.selectbox("Intensité", ["Faible", "Modéré", "Élevé"])
    duree = st.number_input("Durée totale (min)", min_value=10, max_value=120, value=30)

    if st.button("Générer la séance"):
        plan = ""
        if intensite == "Faible":
            warmup = random.randint(max(1, int(duree * 0.10)), max(1, int(duree * 0.15)))
            cooldown = random.randint(max(1, int(duree * 0.10)), max(1, int(duree * 0.15)))
            steady = duree - warmup - cooldown
            plan = f"🔥 {duree} min en {type_cardio} :\n- {warmup} min échauffement\n- {steady} min continu\n- {cooldown} min récupération"
        elif intensite == "Modéré":
            warmup = random.randint(4, 6)
            cooldown = random.randint(3, 5)
            remaining = duree - warmup - cooldown
            n_intervals = remaining // 5
            reste = remaining - n_intervals * 5
            plan = f"🔥 {duree} min en {type_cardio} :\n- {warmup} min échauffement\n- {n_intervals} x (3 min effort + 2 min récup)\n- {reste} min libre\n- {cooldown} min récupération"
        else:
            warmup = random.randint(3, 5)
            cooldown = random.randint(3, 5)
            remaining = duree - warmup - cooldown
            n_intervals = remaining // 2
            reste = remaining - n_intervals * 2
            plan = f"🔥 {duree} min en {type_cardio} :\n- {warmup} min échauffement\n- {n_intervals} x (1 min sprint + 1 min récup)\n- {reste} min libre\n- {cooldown} min récupération"

        st.markdown(f"**Plan généré :**\n\n{plan}")

        if st.checkbox("Enregistrer cette séance ?"):
            date = datetime.date.today()
            new_data = pd.DataFrame([[date, f"Cardio ({intensite})", duree]],
                                    columns=["Date", "Type", "Durée (min)"])
            new_data.to_csv("log.csv", mode='a', header=False, index=False)
            st.success("Séance enregistrée.")

def afficher_historique():
    st.subheader("Historique")
    fichier = "log.csv"
    if os.path.exists(fichier) and os.path.getsize(fichier) > 0:
        df = pd.read_csv(fichier)
        st.dataframe(df)
    else:
        st.info("Aucune donnée disponible.")

def afficher_progression():
    st.subheader("Progression")
    fichier = "log.csv"
    if os.path.exists(fichier) and os.path.getsize(fichier) > 0:
        df = pd.read_csv(fichier)
        durée_par_type = df.groupby("Type")["Durée (min)"].sum()
        fig, ax = plt.subplots()
        ax.bar(durée_par_type.index, durée_par_type.values)
        ax.set_title("Durée d'entraînement par type")
        ax.set_xlabel("Type de séance")
        ax.set_ylabel("Durée (min)")
        st.pyplot(fig)
    else:
        st.info("Pas de données pour générer un graphique.")

# 🎯 Navigation mobile-friendly
page = st.radio("📲 Navigation", [
    "Ajouter une séance",
    "Générer une séance de cardio",
    "Afficher l'historique",
    "Afficher la progression"
])

if page == "Ajouter une séance":
    ajouter_seance()
elif page == "Générer une séance de cardio":
    generer_seance_cardio()
elif page == "Afficher l'historique":
    afficher_historique()
elif page == "Afficher la progression":
    afficher_progression()
