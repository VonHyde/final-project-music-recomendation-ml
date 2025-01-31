import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import os
from PIL import Image


# Cargar modelo
model_path = os.path.join("models", "xgbclassifier_lr-0.5_md-6_subsample_0.6.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

# Cargar dataset
data_path = os.path.join("data", "processed", "total_data_final.csv")

total_data = pd.read_csv(data_path)

def main():
   

    # Mostrar imagen de fondo
    img_path = "./images/nba-header.jpeg"
    img = Image.open(img_path)
    st.image(img, width=800)

    # Contenido del resto de tu aplicación Streamlit...
    st.title("Predicciones NBA")
    # Crear una barra de pestañas con tres opciones
    tab1, tab2, tab3 = st.tabs(["Informacion a resaltar", "Contexto y Limitaciones", "Formulario"])

    # Contenido de la primera pestaña
    with tab1:
        st.write("Informacion a resaltar")
        st.write("Dentro del analisis realizado se pueden resaltar lo siguiente")
        st.image("./images/Distribucion de Victorias y Derrotas.png")
        st.write("Podemos observar que cuando juegan en local los equipos tienden a ganar mas veces")
        st.write('')
        st.image("./images/Cantidad de victorias y derrotas por año en Local.png", caption="Victorias y Derrotas")
        st.write("Aqui podemos observar la cantidad de Victorias y Derrotas por años en Local")
        st.write('')
        st.image("./images/Porcentaje de victorias y derrotas por equipo local.png")
        st.write("Aqui vemos el porcentaje de Victorias y Derrotas por equipos cuando juegan en local")




# Contenido de la segunda pestaña
    with tab2:
      with tab2:
        st.header("Contexto y Limitaciones")
        st.subheader("Contexto")
        st.image("./images/basketball.png", caption="Basketball")

        st.write("El basketball es un deporte de equipo que se juega con dos equipos de cinco jugadores cada uno. El objetivo principal del juego es anotar puntos lanzando la pelota en la canasta del equipo contrario. El equipo con más puntos al final del partido gana.")
        st.write("El juego se lleva a cabo en una cancha rectangular con una canasta en cada extremo. Los jugadores pueden moverse por la cancha driblando la pelota (botándola en el suelo mientras se mueven) o pasándola entre ellos. El equipo en posesión de la pelota intenta encontrar una posición de tiro favorable para anotar, mientras que el equipo defensor intenta evitar que esto suceda bloqueando tiros, robando la pelota o forzando pérdidas de posesión.")
        st.write("El análisis de datos en el basketball puede abordar una variedad de aspectos del juego, para este análisis específico, se utilizó un conjunto de datos relacionados con partidos de basketball para predecir el resultado de un partido en función de diversas variables, como estadísticas de equipo y características del partido. Se empleó un modelo de aprendizaje automático (XGBoost) entrenado previamente para realizar estas predicciones. El objetivo es proporcionar información útil para equipos, entrenadores y aficionados sobre qué factores pueden influir en el resultado de un partido y cómo pueden aprovecharse para mejorar el desempeño del equipo.")

        st.subheader("Limitaciones")
        st.write("Al momento de realizar este analisis nos encontramos con varias limitaciones, las cuales seran mencionadas a continuacion")

        st.image("./images/NaN.png")

        st.image("./images/Porcentaje de nulidad.png", caption="El dataset posee una gran cantidad de datos nulos")
        
        st.write('Como se puede observar, el dataset original posee una gran cantidad de nulos. Esto se debe a que estos nulos pertenecen a partidos que se celebraron en una epoca en la que no existia ni la tecnologia ni los medios necesarios para recopilar dicha informacion')

        st.image("./images/Equipos_Perdiendo.png", caption="Equipos que siempre pierden o ganan")
        st.write('En el dataset tambien aparecen equipos que solo pierden o ganan, lo cual puede generar un sesgo a la hora de intentar predecir. Esto puede deberse a una falta de datos en el dataset o que simplemente el desempeño de dichos equipos siempre ha sido mediocre')


# Contenido de la tercera pestaña
    with tab3:
        st.write("Formulario")

        st.sidebar.image("./images/nba-logo-1.png", caption="NBA")

        #Creamos listas de los equipos y sus abreviaciones
        team_list = total_data["team_name_home"].to_list()
        team_abb_list = total_data["team_abbreviation_home"].to_list()

        #Creamos una lista para mostrar al equipo y su abreviatura juntas
        complete_team_list = []
        for index, row in total_data.iterrows():
            equipo = f"{row['team_name_home']} ({row['team_abbreviation_home']})"
            complete_team_list.append(equipo)

        #Con las listas anteriores creamos un Dataframe para agrupar todos los valores
        team_df = pd.DataFrame({'team_abbreviation_home': team_abb_list, 'team_name_home': team_list, 'final_team_home': complete_team_list})
        team_df= team_df.drop_duplicates()

        #Lista final de equipos
        final_team_list = team_df['final_team_home']
        input_team_list = st.sidebar.selectbox("Selecciona tu Equipo", final_team_list)

        #Localizar valores en funcion del equipo que ha sido seleccionado
        valor_abb = team_df.loc[team_df['final_team_home'] == input_team_list, 'team_abbreviation_home'].iloc[0]
        valor_team = team_df.loc[team_df['final_team_home'] == input_team_list, 'team_name_home'].iloc[0]
    
        #Lista de Matches
        matchup_data = total_data['matchup_home']
        matchup_data = matchup_data.drop_duplicates()
        matchup_list = matchup_data.to_list()
        local_matches = [element for element in matchup_list if element.startswith(valor_abb)]
        match_team_input = st.sidebar.selectbox("Selecciona tu Match", local_matches)


        #Lista de Temporadas
        season_list = total_data["season_type"].to_list()
        season_list_clean = set(season_list)
        season_list_f = list(season_list_clean)
        input_season_list = st.sidebar.selectbox("Temporada", season_list_f)

        #Creamos un diccionario con los datos categoricos introducidos por el usuario

        data_cat = {'team_abbreviation_home': valor_abb, 
    'team_name_home': valor_team,'matchup_home' : match_team_input, 'season_type': input_season_list }
    
        #Convertimos este diccionario en un dataframe para luego preprocesarlos
        data_cat_df = pd.DataFrame(data_cat, index =[0])

        # Preprocesamiento de datos categóricos

        #Primero una lista con las columnas categoricas que estamos manejando
        categorical_cols = ['team_abbreviation_home', 'team_name_home', 'matchup_home', 'season_type']
    
        encode_path = os.path.join("data", "processed", "encode_data.pkl")

        with open(encode_path, 'rb') as f:
            encoding_info = pickle.load(f)

        # Aplicar el 
        data_cat_encoded = data_cat_df.copy()
        for col in categorical_cols:
        # Map labels from encoding information to the new data
            data_cat_encoded[col] = data_cat_encoded[col].map(lambda x: encoding_info[col].tolist().index(x) if x in encoding_info[col] else -1)

        #Empezamos con la insercion de datos numericos


        with st.form("my_form"):
            
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Equipo local")

                fga_home = st.number_input("Tiros de campo intentados en casa", min_value=0)
                fg3a_home = st.number_input("Tiros de campo de tres puntos intentados en casa", min_value=0)
                fta_home = st.number_input("Tiros de campo libres intentados en casa", min_value=0)
                oreb_home = st.number_input("Rebotes Ofensivos en casa", min_value=0)
                dreb_home = st.number_input("Rebotes Defensivos en casa", min_value=0)
                ast_home = st.number_input("Asistencias en casa", min_value=0)
                stl_home = st.number_input("Robos en casa", min_value=0)
                blk_home = st.number_input("Bloqueos en casa", min_value=0)
                tov_home = st.number_input("Perdidas de balón en casa", min_value=0)

            with col2:
                st.subheader("Equipo Visitante")

                fga_away = st.number_input("Tiros de campo intentados visitante", min_value=0)
                fg3a_away = st.number_input("Tiros de campo de tres puntos intentados visitante", min_value=0)
                fta_away = st.number_input("Tiros de campo libres intentados visitante", min_value=0)
                oreb_away = st.number_input("Rebotes Ofensivos visitante", min_value=0)
                dreb_away = st.number_input("Rebotes Defensivos visitante", min_value=0)
                ast_away = st.number_input("Asistencias visitante", min_value=0)
                stl_away = st.number_input("Robos visitante", min_value=0)
                blk_away = st.number_input("Bloqueos visitante", min_value=0)
                tov_away = st.number_input("Perdidas de balón visitante", min_value=0)


            button = st.form_submit_button(label="Submit")


    #Creamos un diccionario y un DataFrame de los datos numericos
        data_num = {'fga_home': fga_home, 
    'fg3a_home': fg3a_home, 'fta_home' : fta_home, 'oreb_home': oreb_home, 'dreb_home': dreb_home, 
    'ast_home': ast_home, 'stl_home': stl_home, 'blk_home': blk_home, 'tov_home':tov_home, 
    'fga_away': fga_away, 'fg3a_away': fg3a_away, 'fta_away': fta_away, 'oreb_away': oreb_away, 'dreb_away': dreb_away,
    'ast_away': ast_away, 'stl_away': stl_away, 'blk_away': blk_away, 'tov_away': tov_away }

    
        if button:
            data_num_df = pd.DataFrame(data_num, index=[0])
            data_final = pd.concat([data_num_df, data_cat_encoded], axis=1)
            data_final = data_final.values.tolist()
            prediccion = model.predict(data_final)
        
        # Mostrar los datos seleccionados y la predicción en Streamlit
            col1, col2 = st.columns(2)

            with col1:
                st.subheader('Prediccion')
                st.write(prediccion)
        
            if prediccion == 0:
                st.subheader("Este equipo tiene muchas probabilidades de ganar")
            else:
                st.subheader('Este equipo tiene las de perder')

        else:
            st.write("Aqui aparecera la prediccion")

if __name__ == "__main__":
    main()
