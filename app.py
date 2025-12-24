import streamlit as st
import pandas as pd
import numpy as np

# Titre de l’application
st.title("🚗 Estimez le prix de votre voiture d’occasion")

st.write(
    "Entrez les informations de votre voiture pour obtenir une estimation simple du prix de revente."
)

# Formulaire pour les caractéristiques de la voiture
st.header("Caractéristiques de la voiture")

year = st.number_input("Année de la voiture", min_value=1990, max_value=2025, value=2018)
km_driven = st.number_input("Kilométrage (km)", min_value=0, value=50000)

fuel = st.selectbox(
    "Carburant",
    ["Petrol", "Diesel", "CNG", "LPG", "Electric"]
)

transmission = st.selectbox(
    "Transmission",
    ["Manual", "Automatic"]
)

seller_type = st.selectbox(
    "Type de vendeur",
    ["Individual", "Dealer", "Trustmark Dealer"]
)

owner = st.selectbox(
    "Nombre de propriétaires",
    ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner"]
)

st.markdown("---")

# Bouton pour estimer
if st.button("Estimer le prix"):
    # Création d'un DataFrame (utile plus tard si tu veux brancher ton vrai modèle)
    input_data = pd.DataFrame({
        'year': [year],
        'km_driven': [km_driven],
        'fuel': [fuel],
        'transmission': [transmission],
        'seller_type': [seller_type],
        'owner': [owner]
    })

    # Modèle très simple (temporaire) pour avoir une estimation
    base_price = 1_000_000  # prix de base en INR
    price = base_price

    # Effet de l'année (plus la voiture est ancienne, plus le prix baisse)
    age = 2025 - year
    price -= age * 40_000

    # Effet du kilométrage
    price -= km_driven * 0.7

    # Ajustement carburant
    if fuel == "Diesel":
        price += 60_000
    elif fuel == "Petrol":
        price += 40_000
    elif fuel == "Electric":
        price += 150_000

    # Ajustement transmission
    if transmission == "Automatic":
        price += 80_000

    # Ajustement type de vendeur
    if seller_type == "Dealer" or seller_type == "Trustmark Dealer":
        price += 30_000

    # Ajustement nombre de propriétaires
    if owner == "Second Owner":
        price -= 30_000
    elif owner == "Third Owner":
        price -= 60_000
    elif owner == "Fourth & Above Owner":
        price -= 100_000

    # Empêcher un prix négatif
    price = max(price, 50_000)

    st.success(f"💰 Prix estimé : {price:,.0f} INR")

    st.info(
        "Cette estimation est basée sur un modèle simple écrit à la main. "
        "Quand ton vrai modèle de régression sera prêt dans Colab, tu pourras remplacer cette formule "
        "par la prédiction de ton modèle."
    )
