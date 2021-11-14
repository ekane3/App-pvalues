import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import streamlit.components.v1 as components
import time
import datetime


DATA_URL = ("full_2020.csv") #Connecting to endpoint to get csv file 

# Function that logs in a file the time execution interval in seconds
def log(function):
    def modified_function(df):
        time_ = time.time()
        res = function(df)
        time_ = time.time()-time_
        with open("log.txt","a") as f:
            f.write(f"{function.__name__}: execution time = {time_} s  call timestamp = {time_} s\n")
        return res
    return modified_function

# Function that loads the dataset into a dataframe

def load_data(nrows):
    df = pd.read_csv(DATA_URL,nrows=nrows)
    return df

# Function that cleans the dataframe

def clean_data(df_):
    df = df_.copy()
    df.adresse_code_voie=df.adresse_code_voie.astype(str)
    df.code_commune=df.code_commune.astype(str)
    df.code_departement=df.code_departement.astype(str)
    df.numero_volume=df.numero_volume.astype(str)
    df.lot1_numero=df.lot1_numero.astype(str)
    df.lot2_numero=df.lot2_numero.astype(str)
    df.lot3_numero=df.lot3_numero.astype(str)
    df.lot4_numero=df.lot4_numero.astype(str)
    df.lot5_numero=df.lot5_numero.astype(str)
    df.date_mutation=pd.to_datetime(df.date_mutation)
    df["prix_m2"] = df.valeur_fonciere/df.surface_terrain
    df.index = df.date_mutation
    return df


def description_analysis():
    st.title("Description analysis 📈")
    st.markdown("Les données sont recueillies pour chaque année fiscale, nous avons donc 5 jeux de données, comptabilisant plusieurs millions de transactions, constitués d'après la documentation fournie auprès du fournisseur des données des variables suivantes, nous allons juste nous interesser aux données de l'année 2020 :")
    st.markdown("""
            - **Variables financières**  
                - valeur_fonciere : Valeur foncière (séparateur décimal = point)  
            - **Variables géographiques et administratives**
                - longitude : Longitude du centre de la parcelle concernée (WGS-84)
                - latitude : Latitude du centre de la parcelle concernée (WGS-84)
                - id_mutation : Identifiant de mutation (non stable, sert à grouper les lignes)
                - date_mutation : Date de la mutation au format ISO-8601 (YYYY-MM-DD)
                - numero_disposition : Numéro de disposition
                - adresse_numero : Numéro de l'adresse
                - adresse_suffixe : Suffixe du numéro de l'adresse (B, T, Q)
                - adresse_code_voie : Code FANTOIR de la voie (4 caractères)
                - adresse_nom_voie : Nom de la voie de l'adresse
                - code_postal : Code postal (5 caractères)
                - code_commune : Code commune INSEE (5 caractères)
                - nom_commune : Nom de la commune (accentué)
                - ancien_code_commune : Ancien code commune INSEE (si différent lors de la mutation)
                - ancien_nom_commune : Ancien nom de la commune (si différent lors de la mutation)
                - code_departement : Code département INSEE (2 ou 3 caractères)
                - id_parcelle : Identifiant de parcelle (14 caractères)
                - ancien_id_parcelle : Ancien identifiant de parcelle (si différent lors de la mutation)
                - numero_volume : Numéro de volume
                - code_nature_culture : Code de nature de culture
                - nature_culture : Libellé de nature de culture
                - code_nature_culture_speciale : Code de nature de culture spéciale
                - nature_culture_speciale : Libellé de nature de culture spéciale
            - **Variables métiers**
                - lot_1_numero : Numéro du lot 1
                - lot_1_surface_carrez : Surface Carrez du lot 1
                - lot_2_numero : Numéro du lot 2
                - lot_2_surface_carrez : Surface Carrez du lot 2
                - lot_3_numero : Numéro du lot 3
                - lot_3_surface_carrez : Surface Carrez du lot 3
                - lot_4_numero : Numéro du lot 4
                - lot_4_surface_carrez : Surface Carrez du lot 4
                - lot_5_numero : Numéro du lot 5
                - lot_5_surface_carrez : Surface Carrez du lot 5
                - nombre_lots : Nombre de lots
                - code_type_local : Code de type de local
                - surface_reelle_bati : Surface réelle du bâti
                - nombre_pieces_principales : Nombre de pièces principales
                - surface_terrain : Surface du terrain
                
                """)


def title_bar():
    project_title = st.sidebar.text_input("You can change the title of this project by input")
    if project_title:
        st.title(project_title)
    else:
        st.title("Demande de valeurs foncières")

# Function that show a sample of dataframe 

def show_head(df):
    #write a streamlit markdown to show sample of data
    st.markdown(" #### Let's show a sample of our data, to see what type of data we'll be dealing with.")

    # Use checkboxes to show/hide data when you click
    if st.checkbox("Check to show raw data"):
        st.subheader("Raw data")
        st.write(df.head(10))

    st.markdown("****")

def get_communs(df):
    return df.nom_commune.value_counts().index


def type_location_by_communs(values):
    df, commune = values
    vals = df[df.nom_commune == commune].type_local.value_counts()
    labels = vals.index
    return (vals,labels)


def communes_highest_num_transactions(df):
    st.subheader("20 first communes with the highest number of real estates")
    df_ = df.groupby("nom_commune").count()
    df_ = df_.sort_values(by='id_mutation',ascending=False)[:20]
    return df_

# departments with the highest number of real estate transactions

def departments_highest_num_transactions(df):
    st.subheader("20 first departments with the highest number of real estate transactions")
    df_ = df.groupby('code_departement').count()
    df_ = df_.sort_values(by='id_mutation',ascending=False)[:20]
    #df_ = df_.drop(['id_mutation','prix_m2','date_mutation','code_departement','code_commune','adresse_code_voie','nature_mutation','surface_terrain','valeur_fonciere'],axis=1)
    return df_

# Given a region or a department, what are the communes with the highest and the lowest prices per square meter ?

def communes_highest_price_sqmeter(df):
    st.subheader("Communes with the highest and the lowest prices per square meter")
    department = st.selectbox("Select a department", df["code_departement"].unique())
    if department:
        df_ = df[(df['code_departement']==department)]
        df_ = df_.groupby('code_commune').mean()
        df_ = df_.sort_values(by='prix_m2',ascending=False)[:20]    
        return df_

# departments that have the biggest price increase this year

def department_highest_price_increase(df):
    st.subheader("Departments that have experienced the biggest price increase this year")
    df_ = df.groupby('code_departement').count()
    df_ = df_.sort_values(by='id_mutation',ascending=False)[:20]
    return df_


def average_transactionValue_perMonth(df):
    data = df.loc[:,"valeur_fonciere"].resample("M").mean()
    return pd.DataFrame({"valeurs": data.values, "mois": data.index.month})



def get_points_by_months(values):
    df, start_date, end_date = values
    points = df[["valeur_fonciere","latitude","longitude"]]

    points = points.loc[f"{start_date}": f"{end_date}",:]
    return points[~(points.latitude.isna() & points.longitude.isna())][["latitude","longitude"]]


def month_to_index(month):
    months = {"Janvier": 1, "Février": 2, "Mars": 3, "Avril":4, "Mai":5, "Juin":6, "Juillet":7, "Aout":8, "Septembre": 9, "Octobre":10, "Novembre":11, "Décembre":12}
    return months[month]


def plot_map(df_):
    st.subheader("Map Chart")
    st.markdown(" ##### Map des transactions immobilières selon la période de l'année 2020")
    st.markdown("Choisissez une date de debut et une date de fin en cliquant sur les listes déroulantes")
    col1, col2 =  st.columns(2)
    min_date = datetime.date(df_.index.min().year, df_.index.min().month, df_.index.min().day)
    max_date = datetime.date(df_.index.max().year, df_.index.max().month, df_.index.max().day)
    start_date = col1.date_input('Date de debut', min_date, min_date, max_date)
    end_date = col2.date_input('Date de fin', max_date, min_date, max_date)
    points = get_points_by_months((df_,start_date, end_date))
    col1, col2 = st.columns(2)
    #col1.st.write("")
    col1.metric("Nombre de transactions sur cette période :", len(points))
    st.map(points)


def nullity_plot(df):
    st.subheader("Nullity plot : checking missing values by column")
    data = df.isnull().sum()
    st.bar_chart(data)

def main():
    st.sidebar.title("Currently streaming with ❤")
    genre = st.sidebar.radio("👇",('Analysis description', 'Lookup Analysis'))
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    st.sidebar.markdown("Made by [Emile.E](https://github.com/ekane3)")

    if genre == 'Analysis description':
        description_analysis()
    else:
        title_bar()

        #Let's load 1 000 000 rows of data
        df1 = load_data(1000000)
        df_ = clean_data(df1)
        # Montrer les 10 premieres lignes du dataframe
        show_head(df_)
        #Montrer le nombre de valeurs nulles par colonne
        nullity_plot(df_)
        
        # Localisation des transactions immobilières par période de l'année
        plot_map(df_)
        
        # plot the communes with the highest number of real estate transactions
        data = communes_highest_num_transactions(df_)
        st.bar_chart(data, height=500)

        # plot the departments with the highest number of real estate transactions
        data = departments_highest_num_transactions(df_)    
        st.bar_chart(data, height=500)

        # plot the communes with the highest and the lowest prices per square meter
        data = communes_highest_price_sqmeter(df_)
        st.bar_chart(data, height=500)

        # plot the departments that have the biggest price increase this year
        data = department_highest_price_increase(df_)
        st.line_chart(data, height=500)


        # Valeur moyenne des transactions par mois
        st.markdown("***")
        st.subheader("Valeur moyenne des transactions par mois")
        data = average_transactionValue_perMonth(df_)
        fig, ax= plt.subplots(figsize=(10,6))
        ax = sns.barplot(data=data, x="mois", y="valeurs")
        ax.set_xticklabels('Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec'.split(","))
        ax.set_xticks(np.arange(12))
        st.pyplot(fig)

        # Les types de location les plus demandées selon les communes
        
        st.subheader("Les types de location les plus demandées selon les communes")

        fig, ax = plt.subplots(figsize=(10,6))
        commune=st.selectbox(
                "Choissisez une commune",
                tuple(get_communs(df_))
            )
        data, labels = type_location_by_communs((df_,commune))
        ax = plt.pie(data, labels=labels, autopct="%.0f%%")
        st.pyplot(fig)


if __name__ == "__main__":
    main()