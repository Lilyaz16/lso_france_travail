import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px

df = pd.read_csv("job_data_FT_final.csv", delimiter=",", encoding="utf-8")
print(df.head())

departements = ['92', '75', '91', '94', '93']
df_filtered = df[df['code_departement'].isin(departements)]

df_count = df_filtered.groupby('code_departement').size().reset_index(name='count')


pages = ["Contexte du projet", "Exploration des données", "Analyse de données", "Modélisation"]

page = st.sidebar.radio("Aller vers la page :", pages)

if page == pages[0] : 
    
    st.write("### Contexte du projet")
    
    st.write("Ce projet a pour but de mettre en avant vos compétences de Data Engineer. Vous allez regrouper des informations sur les offres d’emplois et les compagnies qui les proposent. À la fin du projet, vous aurez une meilleure vision du marché de l’emploi : quels secteurs recrutent le plus, quelles compétences sont requises, quelles sont les villes les plus actives etc ….")
    
    st.write("Nous commencerons par analyser les offres d'emploi publiées par France Travail.")
    
    st.write("Dans un premier temps, nous explorerons ce dataset. Puis nous analyserons d'autres offres d'emplois provenant d'autres sites.")
    
    st.image("job.jpg")


elif page == pages[1]:
    st.write("### Exploration des données")
    
    st.dataframe(df.head())
    
    st.write("Dimensions du dataframe :")
    
    st.write(df.shape)
    
    if st.checkbox("Afficher les valeurs manquantes") : 
        st.dataframe(df.isna().sum())
        
    if st.checkbox("Afficher les doublons") : 
        st.write(df.duplicated().sum())

elif page == pages[2]:
    st.write("### Analyse de données")
    
    fig = sns.displot(x='code_departement', data=df_filtered, kde=True)
    plt.title("Distribution de la variable cible code_dépatement")
    st.pyplot(fig)
    
    # Utilisation d'une checkbox pour sélectionner un département
    if st.checkbox("Sélectionnez les départements à afficher"):
    # Sélection multiple des départements
        selected_depts = st.multiselect(
        "Choisissez les départements",
            options=["75", "91", "92", "93", "94"],
            default=["75", "91", "92", "93", "94"]
        )
    
    # Filtrer le dataframe en fonction des départements sélectionnés
        df_filtered = df[df['code_departement'].isin(selected_depts)]
    
    # Calculer le nombre d'offres par département
        dept_offer_count = df_filtered['code_departement'].value_counts().reset_index()
        dept_offer_count.columns = ['code_departement', 'nombre_offres']
    
    # Afficher le nombre d'offres par département
        st.write("Nombre d'offres d'emploi par département sélectionné :")
        st.write(dept_offer_count)

    # Créer un graphique de barres montrant le nombre d'offres par département
        fig2 = px.bar(dept_offer_count, 
                  x="code_departement", 
                  y="nombre_offres", 
                  title="Nombre d'offres d'emploi par département",
                  labels={'code_departement': 'Département', 'nombre_offres': 'Nombre d\'offres'})

    # Afficher le graphique
        st.plotly_chart(fig2)
    else:
        st.write("Veuillez sélectionner un ou plusieurs départements.")
    
    df_count = df.groupby('code_departement').size().reset_index(name='count')

    # Créer un graphique de dispersion en fonction du nombre d'offres
    fig3 = px.scatter(df_count, x="code_departement", y="count", title="Evolution du nombre d'offres en fonction du code département")

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig3)
