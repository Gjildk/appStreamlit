import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Titre de l'application
st.title('Cars Streamlit')

# Chargement des données depuis GitHub
link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df_cars = pd.read_csv(link)

# Supprimer les lignes avec des valeurs manquantes
df_cars.dropna(inplace=True)

# Sélection des colonnes numériques pour l'analyse
numeric_columns = ['mpg', 'cylinders', 'cubicinches', 'hp', 'weightlbs', 'time-to-60', 'year']

# Sélection de la région à partir de la barre latérale
selected_region = st.sidebar.selectbox("Sélectionnez une région",
                                       ('Toutes les régions', 'US', 'Europe', 'Japan'))

# Filtrer les données en fonction de la région sélectionnée
if selected_region == 'Toutes les régions':
    df_region = df_cars.copy()
    st.write('Données pour toutes les régions')
else:
    df_region = df_cars[df_cars['continent'].str.contains(selected_region)]
    st.write(f'Données pour la région {selected_region}')

# Heatmap de la corrélation
fig, ax = plt.subplots()
plt.figure(figsize=(10, 8))
sns.heatmap(df_region[numeric_columns].corr(),
            ax=ax, cmap='coolwarm',
            annot=True, fmt='.2f')
st.write(fig)

# Histogrammes pour chaque colonne numérique
for col in numeric_columns:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(df_region[col], kde=True)
    plt.title(f'Distribution de {col} - {selected_region}')
    st.pyplot(fig)

# Boxplots pour chaque colonne numérique avec Plotly Express
for col in numeric_columns:
    fig = px.box(df_region, y=col)
    fig.update_layout(title=f'Boxplot de {col} - {selected_region}', yaxis=dict(title=f'{col}'))
    st.plotly_chart(fig)
