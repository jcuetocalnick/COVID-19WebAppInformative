import streamlit as st
from datetime import time, date
import pandas as pd
import requests
import io
import os
from io import BytesIO , StringIO
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="COVID-19 Data Analyzer",
    layout="wide",
    page_icon= ":microscope:",
    menu_items={
        'Get Help' : 'https://docs.streamlit.io//',
        'About': '#Welcome to Covid-19 Analyzer developed by Janet Cueto & Julio Padron'


    }
)
st.title(":microscope: Covid-19 Informative ")
st.header("Developed by Janet Cueto & Julio Padron")

add_selectbox = st.sidebar.selectbox(
    "Menu",
    ["Homepage","Interactive Map","Statistics USA","Personal Information","Live data for Covid-19"]
)

if add_selectbox == "Interactive Map":
        st.subheader(":earth_americas: Worldwide Map COVID most affected countries")

        map_data = pd.DataFrame(
            np.array([
                [37.0902, -95.7129],
                [46.2276, 2.2137],
                [51.1657, 10.4515],
                [-14.2350, -51.9253],
                [35.9078, 127.7669],
                [55.3781, -3.4360],
                [41.8719, 12.5674],
                [37.0902, 95.7129],
                [20.5937, 78.9629],
                [36.2048, 138.2529],
                [61.5240, 105.3188],
                [40.4637, -3.7492]]),

            columns=['lat', 'lon'])
        st.map(map_data)
        st.caption("Countries most affected by COVID-19 ")

elif add_selectbox == "Statistics USA":

    st.subheader(":us: USA COVID-19 statistics")

    uploaded_file=st.file_uploader("Please upload a CSV file containing the latest COVID report so"
                                   " an interactive table can be displayed , if none then pre-set CSV file data "
                                   "will be shown ")
    if uploaded_file is not None:
        df:pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("csv/usacoviddata.csv")
        st.dataframe(df)

elif add_selectbox == "Live data for Covid-19":
    st.header(":bar_chart: Find the latest data for covid-19 here")

    url = "https://covid-193.p.rapidapi.com/countries"

    headers = {
        "X-RapidAPI-Key": "6bcbf8202amshe78346f4d19fc85p10e53ejsn370a0502495b",
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers).json()

    country_value = [""]
    for asset in response["response"]:
        country_value.append(asset)
    country = st.selectbox('Select country', options=country_value)

    url2 = "https://covid-193.p.rapidapi.com/statistics"

    headers2 = {
        "X-RapidAPI-Key": "6bcbf8202amshe78346f4d19fc85p10e53ejsn370a0502495b",
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
    }

    response2 = requests.request("GET", url2, headers=headers2).json()
    if not country:
        continents = []
        countries = []
        populations = []
        new_cases = []
        active_cases = []
        critical_cases = []
        recovered_cases = []
        million_population_cases = []
        total_cases = []
        new_deaths = []
        million_population_deaths = []
        total_deaths = []
        million_population_tests = []
        total_tests = []
        current_day = []
        current_time = []
        for asset in response2["response"]:
            if asset['continent'] != "All" and asset['continent'] != asset['country']:
                continents.append(asset['continent'])
                countries.append(asset['country'])
                populations.append(asset['population'])
                new_cases.append(asset['cases']['new'])
                active_cases.append(asset['cases']['active'])
                critical_cases.append(asset['cases']['critical'])
                recovered_cases.append(asset['cases']['recovered'])
                million_population_cases.append(asset['cases']['1M_pop'])
                total_cases.append(asset['cases']["total"])
                new_deaths.append(asset['deaths']['new'])
                million_population_deaths.append(asset['deaths']['1M_pop'])
                total_deaths.append(asset['deaths']['total'])
                million_population_tests.append(asset['tests']['1M_pop'])
                total_tests.append(asset['tests']['total'])
                current_day.append(asset['day'])
                current_time.append(asset['time'])

        covid_19_statistics = pd.DataFrame(
            {
                "Country": countries,
                "Continent": continents,
                "Population": populations,
                "New cases": new_cases,
                "Active cases": active_cases,
                "Critical cases": critical_cases,
                "Recovered cases": recovered_cases,
                "Million population for cases": million_population_cases,
                "Total cases": total_cases,
                "New deaths": new_deaths,
                "Million population for deaths": million_population_deaths,
                "Total deaths": total_deaths,
                "Million population for people tested": million_population_tests,
                "Total people tested": total_tests
            }
        )
        # displaying the dataframe
        st.dataframe(covid_19_statistics)
        checkbox = st.checkbox("See line chart")
        if checkbox:
            st.subheader("COVID-19 Statistics")
            col1, col2 = st.columns(2)

            with col1:
                covid_parameter = st.radio(
                    "Select a COVID-19 parameter",
                    ["Total cases", "Total deaths", "Total people tested"]
                )
            with col2:
                color = st.color_picker("Pick a color", "#00f900")
                st.write("The chosen color is", color)
            if covid_parameter:
                fig = px.line(
                    covid_19_statistics,
                    x=covid_parameter,
                    y=covid_19_statistics["Country"],
                    title=covid_parameter
                )
                fig.update_traces(line_color=color)
                st.plotly_chart(fig, use_container_width=True)

            checkbox2 = st.checkbox("See bar chart")
            if checkbox2:
                if covid_parameter:
                    fig2 = px.bar(
                        covid_19_statistics,
                        x=covid_19_statistics["Continent"],
                        y=covid_parameter,
                        title=covid_parameter
                    )
                    st.plotly_chart(fig2)
    else:
        for asset in response2["response"]:
            if asset['country'] == country:
                continent = f"{asset['continent']}"
                population = f"{asset['population']}"
                new_cases = f"{asset['cases']['new']}"
                cases = f"{asset['cases']}"
                active_cases = f"{asset['cases']['active']}"
                critical_cases = f"{asset['cases']['critical']}"
                recovered_cases = f"{asset['cases']['recovered']}"
                million_population_cases = f"{asset['cases']['1M_pop']}"
                total_cases: float = f"{asset['cases']['total']}"
                deaths = f"{asset['deaths']}"
                new_deaths = f"{asset['deaths']['new']}"
                million_population_deaths = f"{asset['deaths']['1M_pop']}"
                total_deaths = f"{asset['deaths']['total']}"
                million_population_tests = f"{asset['tests']['1M_pop']}"
                tests = f"{asset['tests']}"
                total_tests = f"{asset['tests']['total']}"
                current_day = f"{asset['day']}"
                current_time = f"{asset['time']}"
        covid_19_statistics2 = pd.DataFrame(
            {
                "Country": [country],
                "Continent": [continent],
                "Population": [population],
                "New cases": [new_cases],
                "Active cases": [active_cases],
                "Critical cases": [critical_cases],
                "Recovered cases": [recovered_cases],
                "Million population for cases": [million_population_cases],
                "Total cases": [total_cases],
                "New deaths": [new_deaths],
                "Million population for deaths": [million_population_deaths],
                "Total deaths": [total_deaths],
                "Million population for people tested": [million_population_tests],
                "Total people tested": [total_tests]
            }
        )
        st.dataframe(covid_19_statistics2)

elif add_selectbox == "Personal Information":
    st.subheader(":page_facing_up: Personal Info")

    first_name= st.text_input('First Name')
    last_name= st.text_input('Last Name')
    continent=st.selectbox('In what continent do you live?',
                       ["","North America","Antarctica", "Asia","Europe","South America","Africa","Oceania"])
    covid_vaccine= st.radio('What COVID-19 vaccine did you get?',
                     ["None","Pfizer","Moderna","Johnson & Johnson" ,"Novavax"])
    date_started=st.date_input("Please insert the date you last got vaccinated")
    today = date.today().year

    if first_name and last_name and continent and covid_vaccine and date_started:
        st.write("Hi", first_name, "! You have been vaccinated with", covid_vaccine, "for", str(today - date_started.year), "years "
                 "in", continent, ".")

    input = st.radio('Do you have your COVID-19 vaccine card?',
             ["Yes","No"])
    if input == "Yes":
        uploaded_file = st.file_uploader("Choose a file to upload your card",type=["jpg","jpeg","png"])
        show_file= st.empty()

        if not uploaded_file:
            show_file.error("Please upload a file".format(''.join(["jpg","jpeg","png"])))


        if isinstance(uploaded_file,BytesIO):
            show_file.image(uploaded_file)


    boxes = st.checkbox("Why should I get vaccinated?")

    if boxes:

        st.info("COVID-19 vaccination helps protect you by creating an antibody response without you having "
                "to experience potentially severe illness or post-COVID conditions. Getting sick with COVID-19"
                " can cause severe illness or death, even in children, and we can't reliably predict who will "
                "have mild or severe illness.")

    if st.button('Press here for a COVID fact'):
        st.write('1/10 people in the world have contracted COVID-19 ')
else:

    st.subheader("What is COVID-19?")


    col1, col2 =st.columns(2)

    with col1:

        st.image("media/covidimage1.jpg")
        st.video("media/covid-19prevent.mp4")

    with col2:
        st.info("Coronavirus disease (COVID-19) is an infectious disease caused by the SARS-CoV-2 virus."
            "Most people infected with the virus will experience mild to moderate respiratory illness and "
            "recover without requiring special treatment. However, some will become seriously ill and require "
            "medical attention. Older people and those with underlying medical conditions like cardiovascular disease,"
            " diabetes, chronic respiratory disease, or cancer are more likely to develop serious illness."
            " Anyone can get sick with COVID-19 and become seriously ill or die at any age. ")


        st.info("The best way to prevent "
                 "and slow down transmission is to be well informed about the disease and how the virus spreads. "
                 "Protect yourself and others from infection by staying at least 1 metre apart from others, "
                 "wearing a properly fitted mask, and washing your hands or using an alcohol-based rub frequently. "
                 "Get vaccinated when it’s your turn and follow local guidance."
                 "The virus can spread from an infected person’s mouth or nose in small liquid particles when they cough,"
                 " sneeze, speak, sing or breathe. These particles range from larger respiratory droplets to smaller"
                 " aerosols. It is important to practice respiratory etiquette, for example by coughing into a flexed elbow, "
                 "and to stay home and self-isolate until you recover if you feel unwell.")


