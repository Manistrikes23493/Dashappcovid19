from app import app
import dash_daq as daq
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from datetime import datetime as dt,timedelta
import dash_html_components as html
from data import return_func
from app import app
import numpy as np
import callbacks
import pandas as pd
from functions import preservelayoutandoutputsunburst1
from functions import racebarchart
from functions import project_on_map
df_ana_1=return_func()
df_ana_1['Date']=df_ana_1['Date'].astype(str)


colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'paper':'#111111'
}
df_ana_1=return_func()
df_ana_1['Date']=df_ana_1['Date'].astype(str)
a1=df_ana_1[(df_ana_1['Date']>=min(df_ana_1['Date'])) & (df_ana_1['Date']<=max(df_ana_1['Date']))]
fig=preservelayoutandoutputsunburst1(a1,flag=2)

tab_0_layout=html.Div(
    className="row1",
    children=[
    html.Div(
            className="three columns div-left-panelb",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-infob",
                    children=[
                        html.H2('COVID-19',style={'color':'red','textAlign': 'center'}),
                        html.H2(children="Visuals Using Dash", style={
                                    'textAlign': 'center',
                                     'overflow':'hidden',
                                     'padding-right' :10,
                                    'color': '#7FDBFF',
                                    'position':'sticky'
                                }),
                        html.Div([html.Img(src=app.get_asset_url("covid19.jpg"),
                             style={
                                'height' : '80%',
                                'width' : '100%',
                                'float':'center',
                                'position':'relative'
                            }
                           )]),
                        html.H2('''A Python Visualization Framework''', style={
                                     'font-style': 'italic',
                                    'textAlign':'center',
                                    'overflow':'hidden',
                                    'padding-right' :0,
                                    'color': 'yellow',
                                     'position':'sticky'
                                }),
                        html.Div(id='live-update-text0',
                                 style={'font-size': '10px','color':'white'}),
                        html.Div([dcc.Interval(
                                id='interval-component0',
                                interval=2*1000, # in milliseconds
                                n_intervals=0,
                    )],className='Intervals',style={'display': 'inline-block','position':'absolute','height':"110%"})
                    ],
                ),
            ],style={"display": "inline-block",'margin':0,'padding-top':0,'padding-bottom':0}
        ),
    html.Div(
            children=[html.Div(
            className="three columns div-right-panelb1",
                children=[
                   
                   html.Div(
                   className="div-infob1",
                   children=html.Div([html.Div([html.H4('Full view',style={'visibility':'hidden'}),
                                 html.H6('Empty tag',style={'visibility':'hidden'})],id='text-content'),
                             dcc.Graph(id="graph",figure=fig)
                                 ],style={'display':'inline-block','backgroundColor': '#101010'})

) 
                ],style={"display": "inline-block",'margin':0,'padding-top':0,'padding-bottom':0}),
    html.Div(id='scatter')])
    ]
)


              

              

a2=df_ana_1[(df_ana_1['Date']>=sorted(df_ana_1['Date'].unique())[-30]) & (df_ana_1['Date']<=sorted(df_ana_1['Date'].unique())[-1])]
fig1=project_on_map(a2,rotate=False,projection='natural earth',speed=50)
tab_1_layout= html.Div(
    className="row1",
    children=[
        html.Div(
            className="three columns div-left-panela",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-infoa",
                    children=[
                        html.H2('COVID-19',style={'color':'red','textAlign': 'center'}),
                        html.H2(children="Visuals Using Dash", style={
                                    'textAlign': 'center',
                                     'overflow':'hidden',
                                     'padding-right' :10,
                                    'color': '#7FDBFF',
                                    'position':'sticky'
                                }),
                        html.Div([html.Img(src=app.get_asset_url("covid19.jpg"),
                             style={
                                'height' : '80%',
                                'width' : '100%',
                                'float':'center',
                                'position':'relative'
                            }
                           )]),
                        html.H2('''A Python Visualization Framework''', style={
                                     'font-style': 'italic',
                                    'textAlign':'center',
                                    'overflow':'hidden',
                                    'padding-right' :0,
                                    'color': 'yellow',
                                     'position':'sticky'
                                }),
                       html.Div(id='live-update-text',
                                 style={'font-size': '10px','color':'white'}),
                       html.Div([dcc.Interval(
                                id='interval-component',
                                interval=2*1000, # in milliseconds
                                n_intervals=0,
                    )],className='Intervals',style={'display': 'inline-block','position':'absolute','height':"110%"})

                    ],
                ),
            ],style={"display": "inline-block",'margin':0,'padding-top':0,'padding-bottom':0}
        ),
        html.Div(
            className="three columns div-right-panela1",
            children=[
               html.Div(
               className="div-infoa1",
               children=[html.Div(dcc.Graph(id="graph1",figure=fig1))]) 
            ],style={"display": "inline-block",'margin':0,'padding-top':0,'padding-bottom':20,'float':'left'})
                       
                        ,
         
 html.Div(id='anim')

]
)

                


a2=df_ana_1
fig2=racebarchart(a2,continent='NULL',top=30)
tab_2_layout= html.Div(
    className="row",
    children=[
        html.Div(
            className="three columns div-left-panel",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-info",
                    children=[
                        html.H2('COVID-19',style={'color':'red','textAlign': 'center'}),
                        html.H2(children="Visuals Using Dash", style={
                                    'textAlign': 'center',
                                     'overflow':'hidden',
                                     'padding-right' :10,
                                    'color': '#7FDBFF',
                                    'position':'sticky'
                                }),
                        html.Div([html.Img(src=app.get_asset_url("covid19.jpg"),
                             style={
                                'height' : '80%',
                                'width' : '100%',
                                'float':'center',
                                'position':'relative'
                            }
                           )]),
                        html.H2('''A Python Visualization Framework''', style={
                                     'font-style': 'italic',
                                    'textAlign':'center',
                                    'overflow':'hidden',
                                    'padding-right' :0,
                                    'color': 'yellow',
                                     'position':'sticky'
                                }),
                       html.Div(id='live-update-text1',
                                 style={'font-size': '10px','color':'white'}),
                       html.Div([dcc.Interval(
                                id='interval-component1',
                                interval=2*1000, # in milliseconds
                                n_intervals=0,
                    )],className='Intervals',style={'display': 'inline-block','position':'absolute','height':"110%"})
                    ],
                ),
            ],style={"display": "inline-block",'margin':0,'padding-top':0,'padding-bottom':0}
        ),
        # Right Panel Div 
      html.Div(
            className="three columns div-right-panel",
            children=[
              html.Div(
               className="div-info1",
               children=[html.Div(dcc.Graph(id="graph2",figure=fig2))]) 
            ],style={"display": "inline-block",'margin':0,'padding-top':0,'padding-bottom':0,'float':'left'})
        ,html.Div(id='Race')
    ]
)

