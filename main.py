import PySimpleGUI as sg
import json
from pathlib import Path
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

_items_dict = dict()
data = dict()
values = list()


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# if __name__ == '__main__':



# TODO Finish adding Lunar items
# TODO Add new items
# TODO End program or go to menu on plot close
