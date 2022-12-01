#%%
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:31:00 2022

@author: Reine

1. Create new env in anaconda 

2. intall packages :
    - pip install pandas (installe automatiquement numpy)
    - pip install scikit-learn
    - pip install streamlit
    - pip install streamlit-option-menu
    - pip install streamlit-aggrid
python intern package : no need to install : 
from PIL import Image
import os

    
3. check current directory : os.getcwd()   

change directory to your project folder : 
os.chdir(path)


4 for running streamlit
    - cd your path file project 
    - streamlit run reco_voyage_streamlit.py

"""
    
#%%

import streamlit as st
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from PIL import Image
import streamlit as st
import base64
import os

#%%

#change directory and check new path
os.chdir(r"C:\Users\alexi\Documents\Hackathlon_1")

#################### IMPORT DF ##################3
df=pd.read_csv(r'df_trip.csv')

st.set_page_config(page_title='Voyage culinaire', page_icon='🤤', layout="centered", initial_sidebar_state="auto", menu_items=None)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    
add_bg_from_local('cuisine2.jpg')    

st.image('logo.png')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# selection des filtres   
with st.container():
    st.markdown("<h1 style='text-align: center; font-family:Garamond; color: #ffc133;'>À la découverte de la gastronomie française</h1>", unsafe_allow_html=True)
    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left; color: white;'>Entrez vos critères : </h2>", unsafe_allow_html=True)
    #col1,col2= st.columns(2)
    col1,col2,col3 = st.columns((1,1,1))
    with col1:
        st.markdown("<p style='text-align: center; text-decoration: underline;color: white;'>Nombre d'étoiles du restaurant : </p>", unsafe_allow_html=True)
        select_etoile = st.selectbox("Nombre étoile", options=set(df.nb_Etoiles_restaurant))
    with col2:
        st.markdown("<p style='text-align: center;text-decoration: underline; color: white;'>Prix maximal pour un repas : </p>", unsafe_allow_html=True)
        prix = st.slider('prix',15,735 ,15)
        #st.write("<p style='color: white;'>Le montant sélectionné est de </p>", prix, "euros", unsafe_allow_html=True)
    with col3:
        st.markdown("<p style='text-align: center;text-decoration: underline; color: white;'>Région</p>", unsafe_allow_html=True)
        select_region = st.selectbox("Région", options=set(df['Region hotel']))
    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    if st.button('Valider'):    
        
        with st.expander("Les restaurants"):
           
            # résultats des filtres restaurants
            # map des restaurants
            
            with st.container():
                #st.header('Restaurants :')
                cond_restaurant_etoile = (df['nb_Etoiles_restaurant'] == select_etoile) & (df['Prix maximum'] <= prix) & (df['Region hotel'] == select_region)
                #df_result_resto = df.loc[cond_restaurant_etoile,'Name']
                #st.write('Restraunrants',df_result_resto)
                nb_resto = len(df.loc[cond_restaurant_etoile,'Restaurant'])
                for loop in range(nb_resto):
                    col1,col2= st.columns((2,1))
                    with col1:
                        st.markdown("<h3 style='text-align: center; color: white;'>Informations</h3>", unsafe_allow_html=True)
                        st.write('Restaurant : ',df.loc[cond_restaurant_etoile,'Restaurant'].iloc[loop])
                        st.write('Type de cuisine : ',df.loc[cond_restaurant_etoile,'Specialites culinaires'].iloc[loop])
                        etoile=df.loc[cond_restaurant_etoile,'nb_Etoiles_restaurant'].iloc[loop]
                        if etoile == 1:
                            st.write("Nombre d'étoiles : ⭐")
                        elif etoile == 2:
                            st.write("Nombre d'étoiles : ⭐⭐")
                        elif etoile == 3:
                            st.write("Nombre d'étoiles : ⭐⭐⭐")
                        else :
                            st.write("Nombre d'étoiles :✨")
                    st.markdown("<h3 style='text-align: center; color: white;'>Contacts</h3>", unsafe_allow_html=True)
                    st.write('Site du restaurant : ',df.loc[cond_restaurant_etoile,'Site restaurant'].iloc[loop])
                    st.write('Site Michelin : ',df.loc[cond_restaurant_etoile,'Site Michelin'].iloc[loop])
                    st.write('Adresse :')
                    st.write(df.loc[cond_restaurant_etoile,'Adresse restaurant'].iloc[loop])
                    st.write(str(df.loc[cond_restaurant_etoile,'Code Postal restaurant'].iloc[loop]))
                    st.write(df.loc[cond_restaurant_etoile,'Ville hotel'].iloc[loop])
                    with col2:
                        image_restaurant = Image.open('image_cuisine.png')
                        st.image(image_restaurant, caption=df.loc[cond_restaurant_etoile,'Restaurant'].iloc[loop])                     
                    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" />""", unsafe_allow_html=True)                               
                
            with st.container():
                #st.header('Nos hôtels partenaires :')
                cond_hotel = df['Region hotel'] == select_region
                #st.table(df.loc[cond_restaurant_etoile,['NOM COMMERCIAL','SITE INTERNET']])
        
        with st.expander('Localisation des restaurants'):
            with st.container():
                #st.header('Cartes')
                st.map(df.loc[cond_restaurant_etoile, ['latitude', 'longitude']])        
        
        # résultats des filtres hotels
        with st.expander("Nos hôtels partenaires"):
            with st.container():
                #st.header('Nos hôtels partenaires')
                for loop in range(nb_resto):
                    col1,col2= st.columns((2,1))
                    with col1:
                        st.markdown("<h3 style='text-align: center; color: white;'>Informations</h3>", unsafe_allow_html=True)
                        st.write("Nom de l'établissement : ",df.loc[cond_restaurant_etoile,'Hotel'].iloc[loop])
                        st.write('Prix de la nuité : ',str(df.loc[cond_restaurant_etoile,'Prix/nuitee'].iloc[loop]),'Euros')
                        
                        etoile_hotel=df.loc[cond_restaurant_etoile,'Etoiles hotel'].iloc[loop]
                        if etoile_hotel == 1:
                            st.write("Nombre d'étoiles : ⭐")
                        elif etoile_hotel == 2:
                            st.write("Nombre d'étoiles : ⭐⭐")
                        elif etoile_hotel == 3:
                            st.write("Nombre d'étoiles : ⭐⭐⭐")
                        elif etoile_hotel == 4:
                            st.write("Nombre d'étoiles : ⭐⭐⭐⭐")
                        elif etoile_hotel == 5:
                            st.write("Nombre d'étoiles : ⭐⭐⭐⭐⭐")
                        
                    st.markdown("<h3 style='text-align: center; color: white;'>Contacts</h3>", unsafe_allow_html=True)
                    st.write('Site hotel : ',df.loc[cond_restaurant_etoile,'Site restaurant'].iloc[loop])
                    st.write('E-mail : ',df.loc[cond_restaurant_etoile,'COURRIEL'].iloc[loop])
                    st.write('Adresse :')
                    st.write(df.loc[cond_restaurant_etoile,'Adresse hotel'].iloc[loop])
                    st.write(str(df.loc[cond_restaurant_etoile,'Code Postal restaurant'].iloc[loop]))
                    st.write(df.loc[cond_restaurant_etoile,'Ville hotel'].iloc[loop])
                    with col2:
                        image_restaurant = Image.open('image_hotel.jpg')
                        st.image(image_restaurant, caption = df.loc[cond_restaurant_etoile,'Hotel'].iloc[loop])                     
                    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" />""", unsafe_allow_html=True)
                                
# CSS pour le tableau
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)



