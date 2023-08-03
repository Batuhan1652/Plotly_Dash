import jupyter_dash
import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
from matplotlib.pyplot import suptitle
import plotly.express as px, plotly.io as pio, plotly.offline as pyo
import plotly.graph_objs as go, plotly.subplots as sp
from plotly.subplots import make_subplots
import dash, dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc, html
from dash import Dash
from dash.dependencies import Input, Output, State
import os
from tkinter import Button
from jupyter_dash import JupyterDash
from enum import unique
from matplotlib.pyplot import autoscale
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pyclbr import Class
from dash import callback
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pio.templates.default = "plotly_dark"

from Functions_Spotify import DataManipulation

df_artist = DataManipulation.get_df_artist()
df_tracks = DataManipulation.get_df_tracks()

from Graphs import Fig, Fig_1, Fig_2, Fig_3, Fig_4, Fig_5, Fig_6, Fig_7, Fig_8, Fig_9, Fig_9_Copy, Fig_10, Fig_10_Copy, Fig_11, Fig_12, Fig_13, Fig_14, df_tracks_mean, df_top5, df_tracks_query_genre_top_5, df_artist_guery_genre_top5

for fig in [Fig, Fig_1, Fig_2, Fig_3, Fig_4, Fig_5, Fig_6, Fig_7, Fig_8, Fig_9, Fig_9_Copy, Fig_10, Fig_10_Copy, Fig_11, Fig_12, Fig_13, Fig_14]:
    fig.update_layout(plot_bgcolor = "rgb(4,12,38)", paper_bgcolor = "rgb(4,12,38)")
    
app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BATU EXAMPLE DASH</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div>
            <div class="row">
                <div class="col-md-5"></div>
                <div class="col-md-1"
                </div>
                <div class="col-md-5"
                </div>
            </div>
        </div>
          <style>
             body {background-color : rgb(145,148,167);}
          </style>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

info_text = "You can write the information or announcements you want to give to the users who enter the site here."

colors = ["black", "blue", "green", "purple", "black", "black"]
info_parts = info_text.split("\n")

modal_body_children = [html.P(part, style={"color" : colors[i % len(colors)]}) for i, part in enumerate(info_parts)]

info_modal = dbc.Modal([
    dbc.ModalHeader(html.H4("INFORMATION", style={'textAlign':'center'})), 
    dbc.ModalBody(modal_body_children), 
    dbc.ModalFooter(dbc.Button("Close", id = "close-info", className = "ml-auto"))],
    id = "info-modal",
    is_open = True)
info_button = dbc.Button("Show info", id = "show-info")
header = html.Div([html.H1("Your App Title"), info_button])

app.layout = dbc.Container(fluid = True, children = [
    html.Img(src = "/assets/data.jpeg", style = {"width" : "100%", "height" : "350px", "border" : "3px solid white", "border-radius" : "10px", 
                                       "background-color" : "rgb(4,12,38)", "display": "block", "margin-bottom" : "5px"}),
    
    info_modal,
    html.Div(children = [html.Div(children=[html.H4(children = [html.A("PLEASE CLICK ON THE LINK TO VISIT MY LINKEDIN PROFILE", href = "https://www.linkedin.com/in/batuhanmtn/",  target = "_blank", 
                                                    style = {"color" : "white", "textAlign" : "left", "width" : "40%"})])],
                 style={"width" : "50%", "color" : "white", "textAlign" : "left", "font-size" : "5px", "display" : "flex",
                        "align-items" : "center", "margin-bottom" : "5px", "margin-top" : "5px", "line-height" : "30px", "justify-content" : "flex-start"}),
        
    html.Div(children = [info_button], style = {"width" : "20%", "display" : "flex", "justify-content" : "center", "align-items" : "center"}),
        
    html.Div(children = [html.H4(children=[html.A("PLEASE CLICK TO VIEW THE SOURCE CODE OF THIS DASH", href = "https://github.com/Batuhan1652", target = "_blank", style = {"color" : "white", "textAlign" : "right", "width" : "30%"})])],
                 style = {"width" : "50%", "color" : "white", "textAlign" : "right", "font-size" : "5px", "display" : "flex",
                          "align-items" : "center", "margin-bottom" : "5px", "margin-top" : "5px", "line-height" : "30px", "justify-content" : "flex-end"})], 
             style = {"display" : "flex", "justify-content" : "space-around", "align-items" : "center", "width" : "100%", "backgroundColor" : "rgb(4,12,38)", "margin-bottom" : "1px", "font-size" : "20px", "margin-top" : "10px"}),

    html.Div(html.H1(children = [html.A("CLICK HERE TO GO TO THE END OF THE DASH APPLICATION", href = "#Fig_14", style = {"color" : "white", "textAlign" : "center"})], 
        style = {"backgroundColor" : "rgb(4,12,38)", "color" : "white", "textAlign" : "center", "font-size" : "20px", "width" : "100%", "margin-right" : "auto", "display" : "flex", 
               "align-items" : "center", "justify-content" : "center", "margin-bottom" : "5px", "margin-top" : "10px", "height" : "40px"})),

    dbc.Row(dbc.Col(children = html.Div(children = [dcc.Graph(id = "Fig", figure = Fig)], style = {"width": "100%", "margin-bottom" : "5px", "margin-top": "5px"}), align = "center")),
    
    html.H6(children = "TO VIEW THE MOST POPULAR SONG ACCORDING TO THE RELEASE YEARS, PLEASE SELECT THE YEAR FROM THE TABLE.", 
        style = {"backgroundColor": "white", "color": "rgb(4,12,38)", "textAlign" : "center", "font-size": "30px", "width" : "100%", "height" : "40px", "display" : "block", "margin-top" : "5px"}),
    dcc.Dropdown(id = 'year-dropdown',options = [{'label' : i, 'value' : i} for i in df_top5['Year'].unique()], value = df_top5['Year'].min(), 
                 style = {"backgroundColor" : "white", "color" : "rgb(4,12,38)", "margin-bottom" : "10px"}),
    dash_table.DataTable(id = 'table', columns = [{"name": i, "id": i} for i in df_top5.columns], 
                         style_header = {"backgroundColor" : "rgb(4,12,38)",  "fontWeight" : "bold",  "color" : "white", "textAlign" : "center", "border-radius" : "15px"}, 
                         style_cell={'backgroundColor' : 'rgb(4,12,38)', 'color' : 'white', "textAlign" : "center", "border-radius" : "15px"}),
    
    html.Div([
    html.Div(children=dcc.Graph(id = "Fig_1", figure = Fig_1), style = {"flex" : "1", "height" : "600px", "margin-right" : "5px", "border-radius" : "15px", "overflow" : "hidden"}),
    html.Div(children=dcc.Graph(id = "Fig_2", figure = Fig_2), style = {"flex" : "1", "height" : "600px", "margin-left" : "5px",  "border-radius" : "15px", "overflow" : "hidden"})]
            ,style={"display" : "flex", "flex-direction" : "row", "justify-content" : "space-between", "margin-top" : "15px",  "border-radius" : "15px", "margin-bottom" : "10px"}),
    
    html.Div([
    html.Div(children = dcc.Graph(id = "Fig_3", figure = Fig_3), style = {"flex" : "1", "height" : "600px", "margin-right" : "5px", "border-radius" : "15px", "overflow" : "hidden"}),
    html.Div(children = dcc.Graph(id = "Fig_4", figure = Fig_4), style = {"flex" : "1", "height" : "600px", "margin-left" : "5px", "border-radius" : "15px", "overflow" : "hidden"})]
            ,style = {"display" : "flex", "flex-direction" : "row", "justify-content" : "space-between", "margin-top" : "15px",  "border-radius" : "15px"}),
    
    html.H6(children = "TO VIEW THE GRAPH OF THE SECTION YOU WANT, PLEASE SELECT THE SECTION YOU WANT TO SEE FROM THE BOX BELOW.", 
        style = {"backgroundColor": "white", "color": "rgb(4,12,38)", "textAlign" : "center", "font-size": "30px", "width" : "100%", "height" : "40px", "display" : "block", "margin-top" : "15px"}),
    html.Div(children = dcc.Dropdown(id = "Fig_5_Genre", options = [{"label" : col, "value" : col} for col in df_tracks_mean["Query_Genre"].unique()], value = df_tracks_mean["Query_Genre"].unique()[0]),          
                                style = {"margin-top" : "5px"}),
    html.Div(children = dcc.Dropdown(id = "Fig_5_Years_Cat", options = [{"label" : col, "value" : col} for col in df_tracks_mean["Years_Cat"].unique()], value = None),
                                style = {"margin-top" : "5px"}),
    html.Button('CLICK HERE FOR RESET THE YEARS CATEGORY', id = 'reset-button', n_clicks = 0, style = {"backgroundColor": "white", "color": "rgb(4,12,38)", "textAlign" : "center", 
                                                                         "font-size": "30px", "width" : "100%", "height" : "40px", "display" : "block", "margin-top" : "5px", "line-height": "0px"}),
    html.Div(children = dcc.Graph(id = "Fig_5", figure = Fig_5), style = {"width" : "100%", "height": "600px", "display": "inline-block", "margin-top" : "10px"}),
    
    html.Div([
    html.Div(children=dcc.Graph(id = "Fig_6", figure = Fig_6), style = {"flex" : "1", "height" : "600px", "margin-right" : "5px", "border-radius" : "15px", "overflow" : "hidden"}),
    html.Div(children=dcc.Graph(id = "Fig_7", figure = Fig_7), style = {"flex" : "1", "height" : "600px", "margin-left" : "5px",  "border-radius" : "15px", "overflow" : "hidden"})]
            ,style = {"display" : "flex", "flex-direction" : "row", "justify-content" : "space-between", "margin-top" : "10px",  "border-radius" : "15px", "margin-bottom" : "10px"}),
    
    dbc.Row(children = dbc.Col(children = html.Div(children = [dcc.Graph(id = "Fig_8", figure = Fig_8)], style = {"margin-top" : "10px", "width" : "100%", "border-radius" : "15px", "overflow" : "hidden"}), align = "center")),
    
    html.H6(children = "TO VIEW THE GRAPH OF THE SECTION YOU WANT, PLEASE SELECT THE SECTION YOU WANT TO SEE FROM THE BOX BELOW.", 
        style = {"backgroundColor": "white", "color": "rgb(4,12,38)", "textAlign" : "center", "font-size": "30px", "width" : "100%", "height" : "40px", "display" : "block", "margin-top" : "15px"}),
    html.Div(children = dcc.Dropdown(id = "Fig_9_10_Genre", options = ["Reset The Figures", 'j-pop', 'japanese', 'korean', 'j-dance', 'chinese', 'j-idol', 'k-pop'],
                                     value = ["Reset The Figures", 'j-pop', 'japanese', 'korean', 'j-dance', 'chinese', 'j-idol', 'k-pop']), style = {"margin-top" : "3px"}),
    
    html.Div([
    html.Div(children=dcc.Graph(id = "Fig_9", figure = Fig_9), style = {"flex" : "1", "height" : "600px", "margin-right" : "5px", "border-radius" : "15px", "overflow" : "hidden"}),
    html.Div(children=dcc.Graph(id = "Fig_10", figure = Fig_10), style = {"flex" : "1", "height" : "600px", "margin-left" : "5px",  "border-radius" : "15px", "overflow" : "hidden"})],
             style = {"display" : "flex", "flex-direction" : "row", "justify-content" : "space-between", "margin-top" : "10px",  "border-radius" : "15px", "margin-bottom" : "10px"}),
    
    html.Div([
    html.Div(children=dcc.Graph(id = "Fig_11", figure = Fig_11), style = {"flex" : "1", "height" : "600px", "margin-right" : "5px", "border-radius" : "15px", "overflow" : "hidden"}),
    html.Div(children=dcc.Graph(id = "Fig_12", figure = Fig_12), style = {"flex" : "1", "height" : "600px", "margin-left" : "5px",  "border-radius" : "15px", "overflow" : "hidden"})],
             style = {"display" : "flex", "flex-direction" : "row", "justify-content" : "space-between", "margin-top" : "10px",  "border-radius" : "15px", "margin-bottom" : "10px"}),
    
    html.Div([
    html.Div(children=dcc.Graph(id = "Fig_13", figure = Fig_13, responsive = True), style = {"width" : "50%", "height" : "500px", "margin-right" : "5px", "border-radius" : "15px", "overflow" : "hidden"}),
    html.Div(children=dcc.Graph(id = "Fig_14", figure = Fig_14, responsive = True), style = {"width" : "50%", "height" : "500px" ,"margin-left" : "5px",  "border-radius" : "15px", "overflow" : "hidden"})],
    style = {"display" : "flex", "flex-direction" : "row", "justify-content" : "space-between", "margin-top" : "10px",  "border-radius" : "15px"}),
    
    html.Div(html.H1(children = [html.A("CLICK HERE TO GO TO THE START OF THE DASH APPLICATION", href = "#Fig", style = {"color" : "white", "textAlign" : "center"})], 
        style = {"backgroundColor" : "rgb(4,12,38)", "color" : "white", "textAlign" : "center", "font-size" : "20px", "width" : "100%", "margin-right" : "auto", "display" : "flex", 
               "align-items" : "center", "justify-content" : "center", "margin-bottom" : "5px", "margin-top" : "-40px", "height" : "40px"})),

    
])
    
@app.callback(Output('table', 'data'), Input('year-dropdown', 'value'))
def update_table(selected_year):
    filtered_df = df_top5[df_top5['Year'] == selected_year]
    return filtered_df.to_dict('records')

@app.callback(Output("Fig_5", "figure"), Input("Fig_5_Genre", "value"), Input("Fig_5_Years_Cat", "value"))
def update_graphs(selected_genre, selected_years):
    if selected_genre and selected_years:
        filtered_df = df_tracks_mean.loc[(df_tracks_mean["Query_Genre"] == selected_genre) & (df_tracks_mean["Years_Cat"] == selected_years)]
        
    elif selected_genre and not selected_years:
        filtered_df = df_tracks_mean.loc[df_tracks_mean["Query_Genre"] == selected_genre]
        
    elif selected_years:
        filtered_df = df_tracks_mean.loc[df_tracks_mean["Years_Cat"] == selected_years]
        
    else :
        filtered_df = df_tracks_mean
        
    Fig_5 = px.area(filtered_df, x = "Year", y = "Popularity", color_discrete_sequence = ['white'])
    scatter = go.Scatter(x = filtered_df["Year"], y = filtered_df["Popularity"], mode = 'markers', marker_color = 'black')
    Fig_5.add_trace(scatter)
    
    Fig_5.update_layout(
        plot_bgcolor = "rgb(4,12,38)", paper_bgcolor = "rgb(4,12,38)", height = 600, hovermode = "x unified",
        hoverlabel=dict(bgcolor = "white", font_size = 16, font_family = "Rockwell", font_color = "black"),
        legend=dict(x = 1, y = 0.5),
        title={"text" : "Average popularity of the top 100 songs according to their release dates", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : {'size' : 18, 'color' : 'white'}})

    Fig_5.update_yaxes(gridcolor = "white", autorange = False, range = [filtered_df["Popularity"].min(), df_tracks_mean["Popularity"].max() + 10])
    Fig_5.update_xaxes(gridcolor = "white", autorange = False, range = [filtered_df["Year"].min() - 3, df_tracks_mean["Year"].max()])

    return Fig_5

@app.callback(Output('Fig_5_Years_Cat', 'value'), Input('reset-button', 'n_clicks'))
def reset_years(n_clicks):
    if n_clicks > 0:
        return None
        
@app.callback(Output("Fig_9", "figure"), Input("Fig_9_10_Genre", "value"))
def update_graphs(selected_values):
    
    if not selected_values:
        return Fig_9_Copy
    
    if not isinstance(selected_values, list):
        selected_values = [selected_values]
    
    if "Reset The Figures" in selected_values:
        return Fig_9_Copy
        
    filtered_df = df_artist_guery_genre_top5[df_artist_guery_genre_top5["Query_Genre"].isin(selected_values)]
    
    Fig_9 = px.bar(filtered_df, x = "Artist_Name", y = "Followers", color = "Query_Genre", text = "Artist_Name")

    Fig_9.update_layout(height = 600,
                  plot_bgcolor = "rgb(4,12,38)", paper_bgcolor = "rgb(4,12,38)",
                  hovermode = "x unified", hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
                  title = {"text" : "TOP 5 IN FOLLOWERS FOR ARTIST NAME, ACCORDING TO QUERY GENRE", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})

    return Fig_9 
   
@app.callback(Output("Fig_10", "figure"), Input("Fig_9_10_Genre", "value"))
def update_graphs(selected_values):
    
    if not selected_values:
        return Fig_10_Copy
    
    if not isinstance(selected_values, list):
        selected_values = [selected_values]
    
    if "Reset The Figures" in selected_values:
        return Fig_10_Copy
    
    filtered_df = df_tracks_query_genre_top_5[df_tracks_query_genre_top_5["Query_Genre"].isin(selected_values)]
    
    Fig_10 = px.bar(filtered_df, x = "Artist_Name", y = "Popularity", color = "Query_Genre", text = "Artist_Name")
    Fig_10.update_layout(height = 600,
                  plot_bgcolor = "rgb(4,12,38)", paper_bgcolor = "rgb(4,12,38)",
                  hovermode = "x unified", hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
                  title = {"text" : "TOP 5 IN POPULARITY FOR ARTIST NAME, ACCORDING TO QUERY GENRE", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})
    
    return Fig_10

@app.callback(Output("info-modal", "is_open"), [Input("show-info", "n_clicks"), Input("close-info", "n_clicks")], [State("info-modal", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
                                
if __name__ == '__main__':

    app.run_server(debug = True, host = "192.168.1.45", port = 7021)