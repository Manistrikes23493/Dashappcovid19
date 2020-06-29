import dash_bootstrap_components as dbc
from random import randint
import os
import dash_html_components as html
import dash
import flask
#server = app.server
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY], assets_folder='assets',server=server)
app.config['suppress_callback_exceptions'] = True
app.head=[
     html.Meta(charSet="UTF-8",name="viewport",content="width=device-width, initial-scale=1.0, maximum-scale=1.0,shrink-to-fit=yes, user-scalable=no")
]