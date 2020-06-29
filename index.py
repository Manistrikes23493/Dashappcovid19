from app import app
from layout import tab_0_layout,tab_1_layout,tab_2_layout
from app import server
from data import return_func
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
from datetime import datetime as dt,timedelta
import dash_html_components as html
import callbacks
from dash.dependencies import Output, Input, State

df_ana_1=return_func()
df_ana_1['Date']=df_ana_1['Date'].astype(str)

app.layout=html.Div(
    [
    dbc.Tabs(
            [
                dbc.Tab(label="Sunburst View", tab_id="sunburst",className="Tab1",label_style={"color": "#ff9900"},children= [
                dbc.Row([dbc.Col(  
                                        dcc.DatePickerRange(
                                            id='my-date-picker-range',
                                            updatemode='bothdates',
                                            style={"color": "red",'paper-bgcolor': "rgba(0,0,0,0)",'height':'5%'},
                                            min_date_allowed=min(sorted(df_ana_1['Date'].unique())),
                                            max_date_allowed =dt.strptime(max(df_ana_1['Date']), "%Y-%m-%d")+ timedelta(days=1),
                                            initial_visible_month=min(sorted(df_ana_1['Date'].unique())),
                                            start_date=min(sorted(df_ana_1['Date'].unique())),
                                            end_date=max(sorted(df_ana_1['Date'].unique()))
                                        ),width=4),
                          dbc.Col(
                            dcc.Dropdown(
                                id='name-dropdown',
                                options=[{'label':name,  'value':name} for name in df_ana_1["Continent"].unique()],
                                value = [],
                                multi=True,
                                style={'width': '100%','display': 'inline-block','color': 'indianred'},
                                placeholder="Select one/multiple continent"
                                ),width=4)],justify="between")]),
                
        dbc.Tab(label="Animation", tab_id="anim",className="Tab2",label_style={"color": "yellow"},children= [
                
            dbc.Row([
                dbc.Col(dcc.DatePickerRange(
                id='my-date-picker-range1',
                updatemode='bothdates',minimum_nights=10,
                style={"color": "red",'paper-bgcolor': "rgba(0,0,0,0)",'height':'5%'},
                min_date_allowed=min(sorted(df_ana_1['Date'].unique())),
                max_date_allowed =dt.strptime(max(df_ana_1['Date']), "%Y-%m-%d")+ timedelta(days=1),
                initial_visible_month=min(sorted(df_ana_1['Date'].unique())),
                start_date=sorted(df_ana_1['Date'].unique())[-30],
                end_date=sorted(df_ana_1['Date'].unique())[-1],
                                        ),width=3),
                         dbc.Col(dcc.Dropdown(
                                id='name-dropdown1',
                                options=[{'label':name,  'value':name} for name in df_ana_1["Continent"].unique()],
                                value = [],
                                multi=True,
                                style={'width': '100%','display': 'inline-block','color': 'indianred'},
                                placeholder="Select one/multiple continent"
                                ),width=3),
                         dbc.Col(daq.BooleanSwitch(
                                    label="ROTATE",
                                    labelPosition="bottom",
                                    color="maroon",
                                    className="boolean",
                                    id='my-boolean-switch',
                                    on=False
                                ),width=2),
                         dbc.Col(daq.Slider(
                                id='slider',
                                color='white',
                                className="slide",
                                min=50,
                                max=2000,
                                size=300,
                                value=50,
                                vertical=False,
                                handleLabel={'color':'red',"showCurrentValue": True,"label": "FRAMERATE",'style':{'width':'60px','height':'50px','margin':0,'padding':0,'padding-top':10}},
                                step=200,
                                disabled=False
                            ),width=2)
                        ],justify="start",no_gutters=True)]),

    dbc.Tab(label="Racebarplots", tab_id="Race",className="Tab3",label_style={"color": "green"},children= [
                dbc.Row([dbc.Col(dcc.DatePickerRange(
                                            className="Datepicker",
                                            id='my-date-picker-range2',
                                            updatemode='bothdates',
                                            style={"color": "red",'paper-bgcolor': "grey",'display':'block'},
                                            min_date_allowed=min(sorted(df_ana_1['Date'].unique())),
                                            max_date_allowed =dt.strptime(max(df_ana_1['Date']), "%Y-%m-%d")+ timedelta(days=1),
                                            initial_visible_month=min(sorted(df_ana_1['Date'].unique())),
                                            start_date=min(sorted(df_ana_1['Date'].unique())),
                                            end_date=max(sorted(df_ana_1['Date'].unique())),
                                        ),width=4),
                dbc.Col(dcc.Input(
                    id="TOP", type="number", placeholder="TOP",style={'width': '100%','display': 'inline-block','color': 'indianred','padding':10},
                    min=5, max=30, step=1,
                ),width=2),
                
                dbc.Col(dcc.Dropdown(
                                id='name-dropdown2',
                                options=[{'label':name,'value':name} for name in df_ana_1["Continent"].unique()],
                                value = [],
                                multi=True,
                                style={'width': '100%','display': 'inline-block','color': 'indianred'},
                                placeholder="Select one/multiple continent"
                                ),width=4)])
    ])
            ],
        id='tabs',
        className='Tabs',
        active_tab='anim'
    ),
        html.Div(id="content")])


@app.callback(Output('content', 'children'),
              [Input("tabs", "active_tab")])
def render_content(tab):
    if tab == 'sunburst':
        return  tab_0_layout
    elif tab == 'anim':
        return  tab_1_layout
    elif tab=='Race':
        return tab_2_layout


if __name__ == '__main__':
    app.run_server(debug=True,threaded=True)