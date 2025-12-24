import streamlit as st
import pandas as pd
import numpy as np
import joblib
@st.cache_resource
def load_model():
    model = joblib.load('car_price_model.pkl')
    encoder = joblib.load('encoder.pkl')
    return model, encoder

model, encoder = load_model()

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
      # Préparer les données comme dans le notebook
    input_df = pd.DataFrame({
        'year': [year],
        'km_driven': [km_driven],
        'fuel': [fuel],
        'transmission': [transmission],
        'seller_type': [seller_type],
        'owner': [owner]
    })

    # Séparer numériques et catégorielles
    X_num_new = input_df[['year', 'km_driven']]
    X_cat_new = input_df[['fuel', 'transmission', 'seller_type', 'owner']]

    # Encoder les catégorielles avec le même encodeur qu'en entraînement
    X_cat_encoded_new = encoder.transform(X_cat_new)

    # Concaténer
    X_new = np.hstack([X_num_new.values, X_cat_encoded_new])

    # Prédiction du prix (unité = même que dans ton dataset, INR si CarDekho)
    predicted_price_inr = model.predict(X_new)[0]

    # Conversion simple INR -> MAD (à ajuster si tu veux)
    predicted_price_mad = predicted_price_inr / 1.4
    predicted_price_mad = max(predicted_price_mad, 5000)  # éviter < 0
    predicted_price_mad = int(round(predicted_price_mad, -2))  # arrondi à la centaine

    st.success(f"💰 Prix estimé : **{predicted_price_mad:,.0f} MAD**".replace(",", " "))

    low = int(predicted_price_mad * 0.9)
    high = int(predicted_price_mad * 1.1)
    st.write(
        f"Fourchette indicative : entre **{low:,.0f} MAD** et **{high:,.0f} MAD**."
        .replace(",", " ")
    )

    st.info(
        "Estimation basée sur un modèle de régression entraîné sur des données de voitures d’occasion. "
        "Les prix réels peuvent varier selon la marque, le modèle, l’état et la région."
    )
else:
    st.write("Cliquez sur le bouton ci‑dessus après avoir renseigné toutes les informations.")
