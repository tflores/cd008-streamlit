###############################################################################
# Aluno: Tiago Porto Flores (116347)
# Tarefa 3 - Usando Streamlit
#
# Em aula vimos vários exemplos de dashboards criadas usando Streamlit. 
# Para esta tarefa pedimos que criem um novo exemplo usando Streamlit. 
# Este exemplo deve ter pelo menos um botão de escolha que modifica uma 
# das informarções mostradas nos gráficos. A nota será proporcional a 
# complexidade da solução. 
#
# Datasets utilizados:
# 1. https://www.kaggle.com/datasets/aodhanlutetiae/tour-de-france-average-speeds-1903-2018
# 2. https://www.kaggle.com/datasets/ralle360/historic-tour-de-france-dataset?resource=download
#
###############################################################################
import streamlit as st
import altair as alt
import pandas as pd

# Carga datasets
tdf_stages_df = pd.read_csv('stages_TDF.csv')
tdf_avg_spd_df = pd.read_csv('average_tourdefrance_speeds_1903_2018.csv')

# Funcoes auxiliares
def extract_year(value):
    #return pd.to_datetime(value, format='%b %d %Y').year
    return pd.to_datetime(value, format='%Y-%m-%d').year

def ajust_stage(value):
    if (len(value) == 1):
        return f"0{value}"
    return value

#movies_df["Year"] = movies_df["Release_Date"].apply(extract_year)
tdf_stages_df["Year"] = tdf_stages_df["Date"].apply(extract_year)
tdf_stages_df["Stage"] = tdf_stages_df["Stage"].apply(ajust_stage)

# Formatacao do cabecalho
st.header("CD008 - Tarefa 3")
st.subheader("Datasets sobre Tour de France")

# Formatacao da pagina
left_column, right_column = st.columns([1,3])

# Divisao em duas colunas
with left_column:    
    button_stages = left_column.button('Estágios da prova')
    button_avgspd = left_column.button('Velocidade média')    
    

# Or even better, call Streamlit functions inside a "with" block:
with right_column:

    if button_stages:
        
        slider_min = tdf_stages_df["Year"].min()
        slider_max = tdf_stages_df["Year"].max()      

        st.write(f"Estágios da Prova - de {slider_min} a {slider_max}")

        select_year = alt.selection_single(
        name='Select', fields=['Year'], init={'Year': slider_min},
        bind=alt.binding_range(min=slider_min, max=slider_max, step=1))

        #Stage,Date,Distance,Origin,Destination,Type,Winner,Winner_Country
        #y_column = st.selectbox('Select y-axis column', tdf_stages_df.select_dtypes('number').columns)

        chart = alt.Chart(tdf_stages_df).mark_bar().encode(
            x = 'Stage:N',        
            y = 'sum(Distance):Q',
            #size = alt.Size('US_Gross'),
            color = alt.Color('Type'),
            opacity = alt.OpacityValue(0.7),
            tooltip = [alt.Tooltip('Stage:N', title='Estágio'),
                    alt.Tooltip('Date:N', title='Data'),
                    alt.Tooltip('Distance:Q', title='Distância (km)'),
                    alt.Tooltip('Origin:N', title='Cidade de origem'),
                    alt.Tooltip('Destination:N', title='Cidade de destino'),
                    alt.Tooltip('Type:N', title='Tipo de percurso'),
                    alt.Tooltip('Winner_Country:N', title='País vencedor'),
                    alt.Tooltip('Winner:N', title='Atleta vencedor')
                    ]
        ).add_selection(select_year).transform_filter(select_year)

        st.altair_chart(chart, use_container_width=True)

    elif button_avgspd:       

        slider_min = tdf_avg_spd_df["Year"].min()
        slider_max = tdf_avg_spd_df["Year"].max()

        st.write(f"Evolução da velocidade Média do Pelotão (km/h) - de {slider_min} a {slider_max}")

        chart = alt.Chart(tdf_avg_spd_df).mark_line(
            point=alt.OverlayMarkDef(color="blue")
        ).encode(
            x = 'Year',
            y = 'peloton average speed (km/h)',
            tooltip = [alt.Tooltip('Year:Q', title='Estágio'),
                       alt.Tooltip('peloton average speed (km/h):Q', title='Vel. média (km/h)')]
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
