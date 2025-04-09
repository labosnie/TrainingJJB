import random
import streamlit as st


# Configuration de la page Streamlit
st.set_page_config(page_title="Générateur Cardio JJB", page_icon="🔥", layout="centered")

st.title("🔥 Générateur de séances cardio JJB")
st.markdown("**Optimise ton rameur ou assault bike pour devenir un monstre sur le tatami.**")

machines = ["Rameur", "Assault Bike"]
fromats = {
    "HIIT Explosive": {
        "echauffement": "5 min en progressif",
        "bloc": lambda: f"{random.randint(5, 10)} rounds :\n - 30s a fond\n  - 90s récup actif ",
        "cooldown": "5 min tranquille",
    },
    "Intervalle Tactiques": {
        "echauffement": "5 min en progressif",
        "bloc": lambda: f"{random.randint(4,6)} rounds :\n - 90s a 85-90% efforts\n - 2min récup active",
        "cooldown": "5 min tranquille",
    },

} 

#Choix aléatoire
machine = random.choice(machines)
format_nom = random.choice(list(fromats.keys()))
format_data = fromats[format_nom]

#Affichage de la séance
print(f"\n Séance générée pour toi" )
print(f"Machine choisie : {machine}")
print(f"Format choisi : {format_nom}\n")

print(f"Echauffement : {format_data['echauffement']}")
print(f"\nBloc principal : {format_data['bloc']()}")
print(f"\nRetour au calme : {format_data['cooldown']}")

# Choix de la machine et du format
st.subheader("🛠️ Personnalise ta séance")
machine = st.selectbox("Choisis ta machine", ["Aléatoire"] + machines)
format_nom = st.selectbox("Choisis le format", ["Aléatoire"] + list(fromats.keys()))


# Génération de la séance

if st.button("🎲 Générer la séance"):
    chosen_machine = random.choice(machines) if machine == "Aléatoire" else machine
    chosen_format = random.choice(list(fromats.keys())) if format_nom == "Aléatoire" else format_nom
    format_data = fromats[chosen_format]

    st.success(f"**Machine :** {chosen_machine}")
    st.info(f"**Format :** {chosen_format}")

    st.write(f"**Échauffement :** {format_data['echauffement']}")
    st.write("**Bloc principal :**")
    st.code(format_data["bloc"](), language="markdown")
    st.write(f"**Retour au calme :** {format_data['cooldown']}")