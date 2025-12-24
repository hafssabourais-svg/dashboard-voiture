import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
#  Titre et description générale
# -----------------------------
st.title("🚗 Estimez le prix de votre voiture d’occasion au Maroc")

st.write(
    """
Cet outil vous permet d’obtenir une **estimation approximative** du prix de revente
d’une voiture d’occasion au Maroc, en dirhams marocains (MAD).

Il ne remplace pas une expertise professionnelle, mais donne un ordre de grandeur
à partir de quelques caractéristiques simples du véhicule.
"""
)

st.markdown("---")

# -----------------------------
#  Saisie des caractéristiques
# -----------------------------
st.header("Caractéristiques de la voiture")

# Année et kilométrage
col1, col2 = st.columns(2)
with col1:
    year = st.number_input("Année de mise en circulation", min_value=1990, max_value=2025, value=2016)
with col2:
    km_driven = st.number_input("Kilométrage (km)", min_value=0, value=120000)

# Type de carburant
fuel = st.selectbox(
    "Type de carburant",
    ["Essence", "Diesel", "Hybride", "Électrique", "GPL"]
)

# Transmission
transmission = st.selectbox(
    "Boîte de vitesses",
    ["Manuelle", "Automatique"]
)

# Type de vendeur
seller_type = st.selectbox(
    "Type de vendeur",
    ["Particulier", "Professionnel (garage, concession)", "Autre"]
)

# Nombre de propriétaires
owner = st.selectbox(
    "Nombre de propriétaires précédents",
    ["Premier propriétaire", "Deuxième propriétaire", "Troisième propriétaire ou plus"]
)

st.markdown("---")

# -----------------------------
#  Estimation du prix (modèle simple)
# -----------------------------
st.subheader("Estimation du prix en MAD")

if st.button("Estimer le prix"):
    # DataFrame pour une future intégration avec un vrai modèle ML
    input_data = pd.DataFrame({
        'year': [year],
        'km_driven': [km_driven],
        'fuel': [fuel],
        'transmission': [transmission],
        'seller_type': [seller_type],
        'owner': [owner]
    })

    # -------- Modèle simplifié "à la main" --------
    # Base : voiture moyenne autour de 120 000 MAD
    base_price = 120_000

    price = base_price

    # Effet de l'âge : plus la voiture est ancienne, plus le prix baisse
    current_year = 2025
    age = current_year - year
    price -= age * 7_000  # -7 000 MAD par année d'ancienneté (à ajuster)

    # Effet du kilométrage : plus de km => prix plus bas
    # Réduction d'environ 0,3 MAD par km
    price -= km_driven * 0.3

    # Effet du carburant
    if fuel == "Diesel":
        price += 15_000   # diesel encore très répandu au Maroc
    elif fuel == "Hybride":
        price += 25_000
    elif fuel == "Électrique":
        price += 35_000
    elif fuel == "GPL":
        price -= 5_000    # peut faire baisser un peu la valeur perçue
    # Essence : pas de modification

    # Effet de la boîte de vitesses
    if transmission == "Automatique":
        price += 12_000   # voitures auto souvent plus chères

    # Effet du type de vendeur
    if seller_type == "Professionnel (garage, concession)":
        price += 5_000    # garantie, préparation, etc.
    # Particulier / Autre : pas de modification

    # Effet du nombre de propriétaires
    if owner == "Deuxième propriétaire":
        price -= 8_000
    elif owner == "Troisième propriétaire ou plus":
        price -= 15_000

    # Éviter un prix trop bas ou négatif
    price = max(price, 10_000)

    # Arrondir
    price = int(round(price, -2))  # arrondi à la centaine

    # Affichage du résultat
    st.success(f"💰 Prix estimé : **{price:,.0f} MAD**".replace(",", " "))

    # Intervalle de confiance grossier (+/- 15 %)
    low = int(price * 0.85)
    high = int(price * 1.15)
    st.write(
        f"Fourchette indicative : entre **{low:,.0f} MAD** et **{high:,.0f} MAD** "
        f"(en fonction de l’état, de la région, des options, etc.).".replace(",", " ")
    )

    st.info(
        """
⚠️ Cette estimation est basée sur un modèle simplifié, uniquement à des fins pédagogiques.
Pour un prix plus précis, il faut tenir compte de la marque, du modèle, de la finition,
de l’état réel du véhicule et des prix du marché local (sites d’annonces marocains, garages, experts)."""
    )

else:
    st.write("Cliquez sur le bouton ci‑dessus après avoir renseigné toutes les informations.")
