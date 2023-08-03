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
from jupyter_dash import JupyterDash
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


class DataManipulation:
    
    @staticmethod
    def Fix_Year_Only_Dates(date):
        
          if '-' not in date:
              return date + '-06-15'
          else:
             return date
       
    @staticmethod  
    def Ms_To_Min_Sec(ms):
         total_seconds = int(ms / 1000)
         minutes = total_seconds // 60
         seconds = total_seconds % 60
         return f"{minutes}:{seconds:02}"

    @staticmethod
    def Artist_Data(path):
        
        df = pd.read_csv(path)
        df.drop("Unnamed: 0", axis = 1, inplace = True)
        num_cols = len(df.columns)
        threshold = num_cols - 4
        df = df.dropna(thresh = threshold, axis = 0)
        df.rename(columns = {"artist_name" : "Artist_Name",
                                  "popularity" : "Popularity",
                                  "followers" : "Followers",
                                  "artist_link" : "Artist_Link",
                                  "genres" : "Genres",
                                  "top_track" : "Top_Track",
                                  "top_track_album" : "Top_Track_Album",
                                  "top_track_popularity" : "Top_Track_Popularity",
                                  "top_track_release_date" : "Top_Track_Release_Date",
                                  "top_track_duration_ms" : "Top_Track_Duration_Ms",
                                  "top_track_explicit" : "Top_Track_Explicit",
                                  "top_track_album_link" : "Top_Track_Album_Link",
                                  "top_track_link" : "Top_Track_Link",
                                  "query_genre" : "Query_Genre"}, inplace = True)
        
        df['Top_Track_Release_Date'] = df['Top_Track_Release_Date'].apply(DataManipulation.Fix_Year_Only_Dates)
        df['Top_Track_Release_Date'] = pd.to_datetime(df['Top_Track_Release_Date'])
                
        df = df.astype({"Top_Track_Popularity" : "int64", "Top_Track_Duration_Ms" : "int64"})
        
        df["Year"] = pd.to_datetime(df["Top_Track_Release_Date"], format = "%y-%m-%d").dt.year
        df["Months"] = pd.to_datetime(df["Top_Track_Release_Date"], format = "%Y-%m-%d").dt.month
        df["Day"] = pd.to_datetime(df["Top_Track_Release_Date"], format = "%Y-%m-%d").dt.day
        df["Months_Cat"] = df["Months"].replace({1 : "January", 2 : "February", 3 : "March", 4 : "April",
                                             5 : "May", 6 : "June", 7 : "July", 8 : "August",
                                             9 : "September", 10 : "October", 11 : "November", 12 : "December"})
        
        df['Top_Track_Duration'] = df['Top_Track_Duration_Ms'].apply(DataManipulation.Ms_To_Min_Sec)
        
        df = df.sort_values(by = "Popularity").reset_index(drop = True)
        
        season_mapping = {"December" : "Winter", "January" : "Winter", "February" : "Winter",
                          "March" : "Spring", "April" : "Spring", "May" : "Spring", 
                          "June" : "Summer", "July" : "Summer", "August" : "Summer",
                          "September" : "Autumn", "October" : "Autumn", "November" : "Autumn"}

        df["Season"] = df["Months_Cat"].map(season_mapping)
        
        df["Top_Track_Duration"] = df["Top_Track_Duration"].str.replace(":", ".")
        df["Top_Track_Duration"] = df["Top_Track_Duration"].astype("float64")
        df['Top_Track_Duration'] = df['Top_Track_Duration'].round(2).astype(str).replace('\.0+$', '', regex=True)
        
        df["Top_Track_Duration"] = df["Top_Track_Duration"].astype("float64")
        labels = ["0 - 1", "1 - 2", "2 - 3", "3 - 4"]
        bins = [0, 1, 2, 3, 4.99]
        df["Top_Track_Duration_Cat"] = pd.cut(df["Top_Track_Duration"], labels = labels, bins = bins)

        return df
    
    
    def Tracks(path):
        df = pd.read_csv(path)
        
        df = df.drop("Unnamed: 0", axis = 1)
        df.rename(columns = {"song_name" : "Song_Name", "album_name" : "Album_Name", "album_link" : "Album_Link", "artist_name" : "Artist_Name", "popularity" : "Popularity",
                             "release_date" : "Release_Date", "song_link" : "Song_Link", "duration_ms" : "Duration_Ms", "explicit" : "Explicit", "query_genre" : "Query_Genre"},
                  inplace = True)
        
        df['Duration'] = df['Duration_Ms'].apply(DataManipulation.Ms_To_Min_Sec)
        df["Duration"] = df["Duration"].str.replace(":", ".")
        df["Duration"] = df["Duration"].astype("float64")
        df['Duration'] = df['Duration'].round(2).astype(str).replace('\.0+$', '', regex=True)
        df['Release_Date'] = df['Release_Date'].apply(DataManipulation.Fix_Year_Only_Dates)
        df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors = 'coerce')
        df = df.dropna()
        df["Year"] = pd.to_datetime(df["Release_Date"], format = "%y-%m-%d").dt.year
        df["Months"] = pd.to_datetime(df["Release_Date"], format = "%Y-%m-%d").dt.month
        df["Day"] = pd.to_datetime(df["Release_Date"], format = "%Y-%m-%d").dt.day
        df["Months_Cat"] = df["Months"].replace({1 : "January", 2 : "February", 3 : "March", 4 : "April",
                                             5 : "May", 6 : "June", 7 : "July", 8 : "August",
                                             9 : "September", 10 : "October", 11 : "November", 12 : "December"})
        
        season_mapping = {"December" : "Winter", "January" : "Winter", "February" : "Winter",
                          "March" : "Spring", "April" : "Spring", "May" : "Spring", 
                          "June" : "Summer", "July" : "Summer", "August" : "Summer",
                          "September" : "Autumn", "October" : "Autumn", "November" : "Autumn"}

        df["Season"] = df["Months_Cat"].map(season_mapping)
        
        df["Duration"] = df["Duration"].astype("float64")
        labels = ["0 - 1", "1 - 2", "2 - 3", "3 - 4"]
        bins = [0, 1, 2, 3, 4.99]
        df["Duration_Cat"] = pd.cut(df["Duration"], labels = labels, bins = bins) 

        return df
    
    @staticmethod
    def get_df_artist():
        return DataManipulation.Artist_Data(r"C:\Users\rocks\OneDrive\Masaüstü\Python\east_asia_top_artists.csv")
    
    @staticmethod
    def get_df_tracks():
        return DataManipulation.Tracks(r"C:\Users\rocks\OneDrive\Masaüstü\Python\east_asia_top_tracks.csv")

    

