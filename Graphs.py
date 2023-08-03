import dash
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
from dash import Dash
from enum import unique
from matplotlib.pyplot import autoscale
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pyclbr import Class
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pio.templates.default = "plotly_dark"

from Functions_Spotify import DataManipulation

df_artist = DataManipulation.get_df_artist()
df_tracks = DataManipulation.get_df_tracks()

#####################################################################################################################################################################################################################

indicator1 = go.Indicator(
    mode = "gauge+number",
    value = sum(df_artist["Followers"]),
    domain = {"x" : [0, 0.5], "y" : [0, 1]},
    title = {"text" : f"Total Followers Top 100 Artist", "font" : {"size" : 14}}, 
    gauge = {'bar' : {'color' : "white"}})

indicator2 = go.Indicator(
    mode = "gauge+number",
    value = (df_artist["Artist_Name"].nunique()),
    domain = {"x" : [0.5, 1], "y" : [0, 1]},
    title = {"text" : f"Count of Artist", "font" : {"size" : 14}},
    gauge = {'bar' : {'color' : "white"}})

indicator3 = go.Indicator(
    mode = "gauge+number",
    value = (df_tracks["Album_Name"].nunique()),
    domain = {"x" : [0.5, 1], "y" : [0, 1]},
    title = {"text" : "Count of Album", "font" : {"size" : 14}},
    gauge = {'bar' : {'color' : "white"}})

Fig = make_subplots(rows = 1, cols = 3, specs = [[{"type" : "indicator"}, {"type" : "indicator"}, {"type" : "indicator"}]], horizontal_spacing = 0.08)
Fig.add_trace(indicator1, row = 1, col = 3)
Fig.add_trace(indicator2, row = 1, col = 2)
Fig.add_trace(indicator3, row = 1, col = 1)

Fig.update_layout(height = 300,
    xaxis_title_font = {'size' : 18, 'color' : 'white'},
    yaxis_title_font = {'size' : 18, 'color' : 'white'},
    title = {'text' : "General Information", 'x': 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font': { 'size' : 18, 'color' : 'white'}},
    plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)")

#####################################################################################################################################################################################################################

df_top5 = df_tracks.groupby('Year').apply(lambda x : x.nlargest(5, 'Popularity')).reset_index(drop = True)
df_top5 = df_tracks.groupby('Year').apply(lambda x : x.nlargest(5, 'Popularity')).reset_index(drop = True)
df_top5 = df_top5.sort_values(by = ["Year", "Popularity"], ascending = [True, False])
df_top5['Rank'] = df_top5.groupby('Year').cumcount() + 1
df_top5 = df_top5[["Rank", "Song_Name", "Album_Name", "Query_Genre", "Popularity", "Release_Date", "Year", "Album_Link"]]

#####################################################################################################################################################################################################################

df_artist_grouped = df_tracks.groupby(["Artist_Name"]) \
.agg({"Year" : "count"}) \
.reset_index().sort_values(by = "Year", ascending = False).rename(columns = {"Year" : "Sum of Track", "Artist_Name" : "Artist Name"}).reset_index(drop = True)

df_artist_grouped = df_artist_grouped.head(20)
df_artist_grouped["Artist_Name_Short"] = df_artist_grouped["Artist Name"].apply(lambda x : x[:5] if isinstance(x, str) else x)

color = ["white"]
Fig_1 = px.bar(df_artist_grouped, x = "Artist_Name_Short", y = "Sum of Track", text = "Sum of Track", color_discrete_sequence = color, 
              hover_data = {"Artist_Name_Short" : False, "Artist Name" : True})

Fig_1.update_layout(
    xaxis_title = "Artist Name",
    yaxis_title = "Sum of Track",
    xaxis_title_font = {'size': 18, 'color': 'white'},
    yaxis_title_font = {'size': 18, 'color': 'white'},
    yaxis_gridcolor = 'white',
    xaxis_gridcolor = 'white',
    title = {'text': "Top 20 Artists by Number of Hits in the Top 100", 'x': 0.5, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top', 'font': { 'size': 18, 'color': 'white'}},
    xaxis_tickangle = -45,
    hovermode = "x unified",
    hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
    plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)",
    height = 600)

#####################################################################################################################################################################################################################

df_artist_followers_grouped = df_artist.groupby(["Query_Genre", "Artist_Name"]).agg({"Followers" : "sum"}).reset_index()

Fig_2 = px.treemap(df_artist_followers_grouped, path = ["Query_Genre", "Artist_Name"],
                  values = "Followers", color = "Query_Genre", height = 600, color_continuous_scale = 'Blues')

Fig_2.update_layout (title = {'text' : "Analysis of Followers Based on Music Genres and Artist Name", 
                                 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}},
                        plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)")

Fig_2.update_traces(hoverlabel = dict(bgcolor = "white", font = dict(family = "Arial", color = "black", size = 20)), marker = {'line' : {'color' : 'black', 'width': 2}},
                       hovertemplate = '<b>Query_Genre : </b> %{parent}<br> \
                       <b>Top_Track_Album : </b> %{label}<br> \
                       <b>Followers : </b> %{value:,}<extra></extra>')

#####################################################################################################################################################################################################################

df_tracks_year = df_tracks.groupby(["Album_Name", "Year"]).agg({"Album_Link" : "count"}).reset_index().sort_values(by = "Album_Link", ascending = False)
df_tracks_year = df_tracks_year.groupby(["Year"]).agg({"Album_Link" : "sum"}).reset_index().rename(columns = {"Album_Link" : "Count of Album"})

Fig_3 = px.area(df_tracks_year, x = "Year", y = "Count of Album", color_discrete_sequence = ['white'])
Fig_3.update_layout(plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)")
Fig_3.update_yaxes(range = [0, 1600], gridcolor = "white")
Fig_3.update_xaxes(gridcolor = "white")
scatter = go.Scatter(x = df_tracks_year["Year"], y = df_tracks_year["Count of Album"], mode = 'markers', marker_color = 'black')
Fig_3.add_trace(scatter)
Fig_3.update_layout(hovermode = "x unified", 
                    hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"), height = 600,
                    title = {'text' : "Albums Count by Published Year", 
                                 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})

#####################################################################################################################################################################################################################

df_tracks_heat_map = df_tracks.groupby(["Months_Cat", "Year"]).agg({"Day" : "count"}).reset_index().sort_values(by = "Year").rename(columns = {"Months_Cat" : "Months", "Day" : "Tracks"})

Fig_4 = px.density_heatmap(df_tracks_heat_map, x = "Year", y = "Months", z = "Tracks", color_continuous_scale = "Blues", text_auto = True)
Fig_4.update_xaxes(tickmode = 'array', tickvals = list(range(min(df_tracks_heat_map["Year"]), max(df_tracks_heat_map["Year"]) + 1, 10)), gridcolor = 'LightGray', gridwidth = 1)
Fig_4.update_layout(plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)", height = 600,
                     title = {'text' : "Tracks Count by Year and Month According to Release Date", 
                                 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})

#####################################################################################################################################################################################################################

df_tracks_mean = df_tracks.groupby(["Year", "Season", "Query_Genre"]).agg({"Popularity" : "mean"}).reset_index().sort_values(by = ["Year", "Popularity"])
bins = [1900, 1990, 2000, 2010, 2023]
labels = ["1970 - 1990", "1990 - 2000", "2000 - 2010", "2010 - 2023"]
df_tracks_mean["Years_Cat"] = pd.cut(df_tracks_mean["Year"], labels = labels, bins = bins)
df_tracks_mean2 = df_tracks_mean.groupby(["Years_Cat", "Query_Genre"]).agg({"Popularity" : "mean"}).reset_index()
df_tracks_mean2["Popularity"].fillna(0, inplace = True)
df_tracks_mean2["Average_Popularity of Years Category"] = df_tracks_mean2["Popularity"]
df_tracks_mean2 = df_tracks_mean2[["Average_Popularity of Years Category", "Years_Cat", "Query_Genre"]]
df_tracks_mean = pd.merge(df_tracks_mean, df_tracks_mean2, how = "left", on = ["Years_Cat", "Query_Genre"])


Fig_5 = px.area(df_tracks_mean, x = "Year", y = "Popularity", color_discrete_sequence = ['white'])

scatter = go.Scatter(x = df_tracks_mean["Year"], y = df_tracks_mean["Popularity"], mode = 'markers', marker_color = 'black')
Fig_5.add_trace(scatter)

Fig_5.update_layout(plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)", height = 600, hovermode = "x unified", 
    hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
    legend = dict(x = 1, y = 0.5),
    title = {"text" : "Average popularity of the top 100 songs according to their release dates", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}}) 

Fig_5.update_yaxes(gridcolor = "white", autorange = False, range = [df_tracks_mean["Popularity"].min(), df_tracks_mean["Popularity"].max() + 10])
Fig_5.update_xaxes(gridcolor = "white", autorange = False, range = [df_tracks_mean["Year"].min(), df_tracks_mean["Year"].max()])

#####################################################################################################################################################################################################################

df_artist_top_10 = df_artist.groupby(["Artist_Name"]).agg({"Followers" : "sum"}).reset_index().sort_values(by = "Followers", ascending = False).rename(columns = {"Artist_Name" : "Artist Name"})
df_artist_top_10 = df_artist_top_10.head(10)
Fig_6 = px.funnel(df_artist_top_10, x = "Followers", y = "Artist Name", color_discrete_sequence = ['white'])
Fig_6.update_layout(plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)", height = 600, hovermode = "y unified", 
    hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
    legend = dict(x = 1, y = 0.5),
    title = {"text" : "Elite Artists : The Top 10 Groups by Followers", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})
Fig_6.update_yaxes(gridcolor = "white")

#####################################################################################################################################################################################################################

df_artist_popularity_global_mean = df_tracks.groupby(["Query_Genre"]).agg({"Popularity" : "mean"}).reset_index().rename(columns = {"Popularity" : "Popularity Mean", "Query_Genre" : "Query Genre"})

colors = plt.cm.viridis(np.linspace(0, 1, len(df_artist_popularity_global_mean["Query Genre"])))
colors_hex = [mcolors.to_hex(c) for c in colors]

Fig_7 = go.Figure(data = [go.Pie(labels = df_artist_popularity_global_mean["Query Genre"],
                                 values = df_artist_popularity_global_mean["Popularity Mean"],
                                 hole = 0.3,
                                 hoverinfo = "none",
                                 hovertemplate = 'Query Genre : %{label}<br>Popularity Mean : %{value}',
                                 textinfo = "value",
                                 textfont = dict(size = 20),
                                 marker = dict(colors = colors_hex))])

Fig_7.update_layout(
    font = dict(color = 'white', size = 18),
    height = 600,
    title_text = "Average Popularity by Query Genre",
    title_x = 0.5,
    title_font = dict(size = 24, color = 'white'),
    legend = dict(
    yanchor = "top",
    y = 0.97,
    xanchor = "left",
    x = 0.95,
    font = dict(color = 'white', size = 10)),
    annotations = [dict(text = 'Query Genre', x = 0.50, y = 0.5, font_size = 16, showarrow = False)],
    plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)")

Fig_7.update_traces(marker = {'line': {'color': 'white', 'width': 2}})

#####################################################################################################################################################################################################################

df_season_artist = df_artist.groupby(["Season", "Artist_Name"]).agg({"Popularity" : "mean"}).reset_index()
df_season_artist = df_season_artist.groupby("Season").apply(lambda x: x.nlargest(5, 'Popularity')).reset_index(drop = True)
df_season_artist["Popularity"] = df_season_artist["Popularity"].astype("int64")
df_season_artist["Artist_Name_Short"] = df_season_artist["Artist_Name"].apply(lambda x : x[:7] if isinstance(x, str) else x)

df_season_tracks = df_tracks.groupby(["Season", "Album_Name"]).agg({"Popularity" : "mean"}).reset_index()
df_season_tracks = df_season_tracks.groupby("Season").apply(lambda x: x.nlargest(5, 'Popularity')).reset_index(drop = True)
new_values = [1, 2, 4, 5, 7]
df_season_tracks.loc[[10, 11, 12, 13, 14], 'Popularity'] = new_values
df_season_tracks["Popularity"] = df_season_tracks["Popularity"].astype("int64")
df_season_tracks["Album_Name_Short"] = df_season_tracks["Album_Name"].apply(lambda x: x[:7] if isinstance(x, str) else x)

unique_categories = ["Spring", "Summer", "Autumn", "Winter"]
category_orders = {"Season" : unique_categories}

fig_artist = px.bar(df_season_artist, y = 'Artist_Name_Short', x = 'Popularity', color = 'Season', 
                    hover_data = {"Artist_Name_Short" : False, "Artist_Name" : True}, category_orders = {"Season" : unique_categories})

fig_track = px.bar(df_season_tracks, y = 'Album_Name_Short', x = 'Popularity', color = 'Season', 
                   hover_data = {"Album_Name_Short" : False, "Album_Name" : True}, category_orders = {"Season" : unique_categories})

Fig_8 = make_subplots(rows = 1, cols = 2, subplot_titles = ("ARTİST", "TRACK"))

for trace in fig_artist.data:
    Fig_8.add_trace(trace, row = 1, col = 1)

for trace in fig_track.data:
    Fig_8.add_trace(trace, row = 1, col = 2)

Fig_8.update_layout(height = 600,
                  plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)",
                  hovermode = "y unified", hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
                  title = {"text" : "Top 5 in popularity for tracks and artists, according to seasons", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})

#####################################################################################################################################################################################################################

df_artist_guery_genre_top5 = df_artist.groupby(["Query_Genre", "Artist_Name"]).agg({"Followers" : "mean"}).reset_index()
df_artist_guery_genre_top5 = df_artist_guery_genre_top5.groupby("Query_Genre").apply(lambda x : x.nlargest(5, "Followers")).reset_index(drop=True) 
Fig_9 = px.bar(df_artist_guery_genre_top5, x = "Artist_Name", y = "Followers", color = "Query_Genre")

Fig_9.update_layout(height = 600,
                  plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)",
                  hovermode = "x unified", hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
                  title = {"text" : "Top 5 artists with the most followers, categorized by query genre", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})

Fig_9_Copy = Fig_9

#####################################################################################################################################################################################################################

df_tracks_query_genre_top_5 = df_tracks.groupby(["Query_Genre", "Artist_Name"]).agg({"Popularity" : "mean"}).reset_index()
df_tracks_query_genre_top_5 = df_tracks_query_genre_top_5.groupby("Query_Genre").apply(lambda x : x.nlargest(5, "Popularity")).reset_index(drop = True)

Fig_10 = px.bar(df_tracks_query_genre_top_5, x = "Artist_Name", y = "Popularity", color = "Query_Genre")
Fig_10.update_layout(height = 600,
                  plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)",
                  hovermode = "x unified", hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
                  title = {"text" : "Top 5 artists in popularity, categorized by query genre", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})
Fig_10_Copy = Fig_10

#####################################################################################################################################################################################################################

df_tracks_duration_count = df_tracks.groupby(["Query_Genre", "Duration_Cat"]).agg({"Song_Link" : "count"}).reset_index().rename(columns = {"Song_Link" : "Count_of_Song"})
df_tracks_duration_count["Count_of_Song"].fillna(0, inplace = True)
category_orders = {"Duration_Cat" : ["3 - 4", "2 - 3", "1 - 2", "0 - 1"]}


unique_duration_cats = df_tracks_duration_count['Duration_Cat'].unique()
buttons = [dict(label = 'All', method = 'update', args = [{'visible' : df_tracks_duration_count['Duration_Cat'].isin(unique_duration_cats)}, {'title' : 'Total Number of Hit Songs by Query Genre and Song Duration'}])]

for cat in unique_duration_cats:
    buttons.append(dict(label = cat, method = 'update', args = [{'visible' : df_tracks_duration_count['Duration_Cat'] == cat}, {'title' : f" {cat} Total Number of Hit Songs by Query Genre and Song Duration"}]))

Fig_11 = go.Figure()

for cat in unique_duration_cats:
    Fig_11.add_trace(go.Bar(
        x = df_tracks_duration_count[df_tracks_duration_count['Duration_Cat'] == cat]["Query_Genre"], 
        y = df_tracks_duration_count[df_tracks_duration_count['Duration_Cat'] == cat]["Count_of_Song"],
        text = df_tracks_duration_count[df_tracks_duration_count['Duration_Cat'] == cat]["Count_of_Song"],
        textposition = 'outside',
        hovertemplate = '<b>Query Genre</b>: %{x}'+
                        '<br><b>Duration Category</b>: '+cat+
                        '<br><b>Count of Song</b>: %{y}<br>',
        name = cat))

Fig_11.update_layout(updatemenus = [go.layout.Updatemenu(active = 0, buttons = buttons)])

Fig_11.update_layout(height = 600,
                  plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)",
                  hovermode = "x unified", hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
                  title = {"text" : "Total Number of Hit Songs by Query Genre and Song Duration", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})

#####################################################################################################################################################################################################################

df_tracks_duration_genre = df_tracks.groupby(["Query_Genre", "Duration_Cat"]).agg({"Popularity" : "mean"}).reset_index()
df_tracks_duration_genre["Popularity"].fillna(0, inplace = True)
category_orders = {"Duration_Cat" : ["3 - 4", "2 - 3", "1 - 2", "0 - 1"]}

unique_duration_cats = df_tracks_duration_genre['Duration_Cat'].unique()

buttons = [dict(label = 'All', method = 'update', args = [{'visible' : df_tracks_duration_genre['Duration_Cat'].isin(unique_duration_cats)}, {'title' : 'Average Popularity by Query Genre and Song Duration'}])]

for cat in unique_duration_cats:
    buttons.append(dict(label = cat, method = 'update', args = [{'visible' : df_tracks_duration_genre['Duration_Cat'] == cat}, {'title' : f"{cat} Average Popularity by Query Genre and Song Duration"}]))

Fig_12 = go.Figure()

for cat in unique_duration_cats:
    Fig_12.add_trace(go.Bar(
        x = df_tracks_duration_genre[df_tracks_duration_genre['Duration_Cat'] == cat]["Query_Genre"], 
        y = df_tracks_duration_genre[df_tracks_duration_genre['Duration_Cat'] == cat]["Popularity"],
        text = round(df_tracks_duration_genre[df_tracks_duration_genre['Duration_Cat'] == cat]["Popularity"], 2),
        textposition = 'outside',
        hovertemplate = '<b>Query Genre</b>: %{x}'+
                        '<br><b>Duration Category</b>: '+cat+
                        '<br><b>Avg Popularity</b>: %{y}<br>',
        name = cat))

Fig_12.update_layout(updatemenus = [go.layout.Updatemenu(active = 0, buttons = buttons)])

Fig_12.update_layout(height = 600,
                  plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)",
                  hovermode = "x unified", hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
                  title = {"text" : "Average Popularity by Query Genre and Song Duration", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})

#####################################################################################################################################################################################################################

df_tracks_duration = df_tracks.groupby(["Duration_Cat"]).agg({"Popularity" : "mean"}).reset_index().rename(columns = {"Popularity" : "Popularity Mean"})
Fig_13 = go.Figure(data = [go.Pie(labels = df_tracks_duration['Duration_Cat'],
                            values = df_tracks_duration['Popularity Mean'],
                            hovertemplate = '<b>Duration Category</b>: %{label}'+
                                             '<br><b>Average Popularity</b>: %{value}<br>',
                            textinfo = 'value')])

Fig_13.update_layout(height = 600,
                  plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)",
                  hovermode = "x unified", hoverlabel = dict(bgcolor = "white",  font_size = 16, font_family = "Rockwell", font_color = "black"),
                  title = {"text" : "Average Popularity by Duration Category", 'x' : 0.5, 'xanchor' : 'center', 'y' : 0.95, 'yanchor' : 'top', 'font' : { 'size' : 18, 'color' : 'white'}})

#####################################################################################################################################################################################################################

query_genre = {"k-pop": 1000, "j-pop": 1000, "japanese": 1000, "korean": 1000, "j-dance": 1000, "chinese": 1000, "j-idol": 999}

data = {
    "country": ["China", "Japan", "South Korea", "North Korea", "Mongolia", "Taiwan"],
    "value": [query_genre.get("chinese", 0),
              query_genre.get("japanese", 0) + query_genre.get("j-pop", 0),
              query_genre.get("korean", 0) + query_genre.get("k-pop", 0),
              0, 0, 0]}

colorscale = "RdYlBu"
df = pd.DataFrame(data)

background_world = go.Scattergeo(
    lon = [180, -180], lat = [90, -90], mode = "text", text = [""],
    showlegend = False, hoverinfo = "none",
    marker = dict(size = 0, cmin = 0, cmax = 0,
    colorscale = [[0, "rgba(28, 107, 160, 0.6)"], [1, "rgba(28, 107, 160, 0.6)"]], showscale = False,
    colorbar = dict(lenmode = "fraction", len = 0.1, yanchor = "top", y = 1, xanchor = "left", x = 0.01, bgcolor = None),))

main_map = go.Choropleth(
    locations = df["country"], z = df["value"], locationmode = "country names",
    colorscale = colorscale, colorbar_title = "Total Song Count", hoverinfo = "location+z", 
    marker_line_color = "darkgray", marker_line_width = 1)

Fig_14 = go.Figure(data=[background_world, main_map])

Fig_14.update_layout(title = {"text" : "Highlighted Countries of Interest", "y" : 0.92, "x" : 0.5, "xanchor" : "center", "yanchor" : "top"},
    geo = dict(scope = "world",  showland = True, landcolor = "lightgray", showocean = True, oceancolor = "rgba(28, 107, 160, 0.6)"),
    autosize = False, height = 600, plot_bgcolor = "rgb(84,52,107)", paper_bgcolor = "rgb(84,52,107)")

#####################################################################################################################################################################################################################

