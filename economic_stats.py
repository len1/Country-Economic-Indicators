import io
from turtle import color
from unicodedata import name
from matplotlib import markers, style
from matplotlib.pyplot import annotate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from fredapi import Fred
import config

# API KEYS AND OBJECT

fred_key = config.fred_api_key

fred = Fred(api_key=fred_key)

# FRED API DATA

sa_exchg_rate_usd = fred.get_series('DEXSFUS')  # SA Exchange Rate Data
sa_sample_gdp = fred.get_series('NAEXKP01ZAQ657S')  # SA GDP Growth Data
sa_sample_uemp = fred.get_series('LRUN64TTZAQ156S')  # SA Unemployment Data

# POPULATION DATAFRAME (OECD)
pop_data = pd.read_csv('sa_population.csv')

sa_pop_df = pop_data[['1990 [YR1990]','2000 [YR2000]', '2012 [YR2012]', '2013 [YR2013]',
                      '2014 [YR2014]', '2015 [YR2015]', '2016 [YR2016]', '2017 [YR2017]',
                      '2018 [YR2018]','2019 [YR2019]', '2020 [YR2020]', '2021 [YR2021]' ]]
sa_pop_df2 = sa_pop_df.T
sa_pop_df3 = sa_pop_df2[[0,1,11]]
sa_pop_df3.rename(columns={0: 'population', 1: 'growth_rate', 11: 'life_expentancy'}, inplace=True)
sa_pop_df3 = sa_pop_df3.reset_index()
sa_pop_df3.rename(columns={'index': 'year'}, inplace=True)
test = sa_pop_df3['year'].str.split(expand=True)
sa_pop_df3[['year_c', 'year_brac']] = test
sa_pop_df3.drop(['year', 'year_brac'], axis=1, inplace=True)
sa_pop_df3.drop([0,1], axis=0, inplace=True)
sa_pop_df3['year_c'] = pd.to_datetime(sa_pop_df3['year_c'])
sa_pop_df3['population'] = pd.to_numeric(sa_pop_df3['population'], errors='coerce')
sa_pop_df3['growth_rate'] = pd.to_numeric(sa_pop_df3['growth_rate'], errors='coerce')





st.set_page_config(page_title='Economic Stats Dashboard',
                   page_icon=":bar_chart:",
                   layout="wide")

# TITLE
st.markdown("<h1 style='text-align: center; color: white;'>SA Economic Overview</h1>", unsafe_allow_html=True)

#  EXCHANGE RATE CHART

fig_exchg_rate = px.line(
    sa_exchg_rate_usd,
    title="<b>South African USD Exchange Rate</b>",
    template="plotly_white",
    color_discrete_sequence=['#A7FFEB']
)

fig_exchg_rate.update_layout(
    title='<b>South African Rand to U.S. Dollar Spot Exchange Rate<b>',  # adding the title
    title_x=0.5,
    xaxis_title='Dates',  # title for x axis
    yaxis_title='SA Rand to U.S Dollar',  # title for y axis
    showlegend=False,
    xaxis=dict(  # attribures for x axis
        showline=True,
        showgrid=False,
        linecolor='black',
        tickfont=dict(
            family='Times New Roman',

        ),
        rangeslider_visible=True
    ),
    yaxis=dict(  # attribures for y axis
        showline=True,
        showgrid=True,
        linecolor='black',
        tickfont=dict(
            family='Times New Roman'
        ),
    ),

    # plot_bgcolor = 'white'  # background color for the graph
)


# SA GDP GROWTH RATE CHART

## Single plot 
gdp_figure = px.area(sa_sample_gdp,
                     template='plotly_white',
                     color_discrete_sequence=['#A7FFEB'],
                     )
# gdp_figure.add_annotation(x=sa_sample_gdp.index[220], y=8,
#                           text="COVID REBOUND",
#                           showarrow=True,
#                           arrowhead=5,
#                           yshift=10)

# gdp_figure.add_annotation(x=sa_sample_gdp.index[215], y=-25,
#                           text="COVID DOWNTURN",
#                           showarrow=True,
#                           arrowhead=5,
#                           yshift=10)
gdp_figure.add_vrect(x0="2020-03-01", x1="2021-10-01",
                     annotation_text="<b>COVID-19<b>", annotation_position="top left",
                     fillcolor="red", opacity=0.25, line_width=0)

gdp_figure.update_layout(
    title='<b>South Africa GDP Growth Rate<b>',  # adding the title
    title_x=0.5,
    xaxis_title='Dates',  # title for x axis
    yaxis_title='GDP %',  # title for y axis
    showlegend=False,
    xaxis=dict(  # attribures for x axis
        showline=False,
        showgrid=False,
        linecolor='black',
        tickfont=dict(
            family='Calibri'
        ),
        rangeslider_visible=True,
    ),

    yaxis=dict(  # attribures for y axis
        showline=True,
        showgrid=False,
        linecolor='black',
        tickfont=dict(
            family='Times New Roman'
        )
    ),


)

# fig.add_hline(y=0, line_dash="dot", line_color="red", line_width=2),

# fig.add_vrect(x0="2020-03-01", x1="2021-10-01", 
#               annotation_text="<b>COVID-19<b>", annotation_position="top left",
#               fillcolor="red", opacity=0.25, line_width=0),
# fig.update_traces(showlegend=False)

# SA UNEMPLOYMENT CHART

unemployment_chart = px.line(sa_sample_uemp,
                             template='plotly_white',
                             color_discrete_sequence=['#A7FFEB'])
unemployment_chart.update_layout(
    title='<b>South Africa Unemployment Rate<b>',  # adding the title
    title_x=0.5,
    xaxis_title='Dates',  # title for x axis
    yaxis_title='Unemployment %',  # title for y axis
    xaxis=dict(  # attribures for x axis
        showline=False,
        showgrid=False,
        linecolor='black',
        tickfont=dict(
            family='Calibri'
        ),
        rangeslider_visible=True,
    ),
    yaxis=dict(  # attribures for y axis
        showline=True,
        showgrid=True,
        linecolor='black',
        tickfont=dict(
            family='Times New Roman'
        ),

    ),
    # plot_bgcolor='white'  # background color for the graph
)

unemployment_chart.add_vrect(x0="2020-03-01", x1="2021-10-01",
                             annotation_text="<b>COVID-19<b>", annotation_position="top left",
                             fillcolor="red", opacity=0.25, line_width=0)
unemployment_chart.update_traces(showlegend=False)

unemployment_chart.update_traces(showlegend=False)

# POPULATION GROWTH CHART

# Create figure with secondary y-axis
pop_chart = make_subplots(specs=[[{"secondary_y": True}]])

pop_chart.add_trace(
    go.Scatter(
        x=sa_pop_df3.year_c,
        y=sa_pop_df3.growth_rate,
        text=sa_pop_df3.growth_rate,
        mode="lines+markers+text",
        line=dict(color='#A7FFEB', width=2),
        name='growth_rate',
        marker=dict(
            color='LightSkyBlue',
            size=120,
            line=dict(
                color='MediumPurple',
                width=4
            )
    )
)
    )

pop_chart.add_trace(go.Scatter(x=sa_pop_df3.year_c, y=sa_pop_df3.population,text=sa_pop_df3.population,
                           mode="lines+markers+text",
                           line=dict(color='#A7FFEB', width=4),
                           name='population',
                           
                           
                           ),
                )

pop_chart.update_layout(
    template="plotly_white",
)
# fig.update_traces(textposition='top center',
# )

pop_chart.update_traces(texttemplate='%{text:.3s}', textposition='top center',
                  textfont_size=12, textfont_color="white",
                  marker=dict(size=12, color='orange'),
                  marker_symbol='diamond',
                  #mode='markers'
                  
                  )
# fig.add_trace(go.Scatter(x=sa_pop_df3.year_c, y=sa_pop_df3.growth_rate,
#                     mode='markers',
#                     name='growth_rate'))

pop_chart.update_layout(
    title='<b>Total Population by Years<b>',  # adding the title
    title_x=0.5,
    xaxis_title='Dates',  # title for x axis
    yaxis_title='Population',  # title for y axis
    xaxis=dict(  # attribures for x axis
        showline=False,
        showgrid=False,
        linecolor='black',
        tickfont=dict(
            family='Calibri'
        ),
        rangeslider_visible=False,
    ),
    yaxis=dict(  # attribures for y axis
        showline=True,
        showgrid=True,
        linecolor='black',
        tickfont=dict(
            family='Times New Roman'
        ),
    ),
)

st.info('💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸\
        💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸')

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Population Growth Rate", value="1.2 %", delta="-0.05")
col2.metric(label="Projected GDP Growth Rate (OECD)", value="1.6 %", delta="-1.6")
col3.metric(label="Income Inequality (Gini coefficient)", value=0.62, delta=0.62,
     delta_color="off")
col4.metric(label="CO2 emissions per capita", value="7.4 tonnes")

left_column, right_column = st.columns(2)
left_column.plotly_chart(pop_chart, use_container_width=True)
right_column.plotly_chart(unemployment_chart, use_container_width=True)

bottom_left_column, bottom_right_column = st.columns(2)
bottom_left_column.plotly_chart(fig_exchg_rate, use_container_width=True)
bottom_right_column.plotly_chart(gdp_figure, use_container_width=True)





