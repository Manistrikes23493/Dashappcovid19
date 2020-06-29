from dash.dependencies import Input, Output,State
from app import app
from datetime import datetime as dt,timedelta
from functions import preservelayoutandoutputsunburst1
from functions import racebarchart
from functions import project_on_map
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
pd.options.mode.chained_assignment = None
import functions
from data import return_func

df_ana_1=return_func()
df_ana_1['Date']=df_ana_1['Date'].astype(str)

def update_text1(clickData,value):
        if value==[]:
            continent=','.join([str(val) for val in value])
            ##########################logic for updating subplot########################################
            if clickData==None:
                return html.Div([html.H4('Full view',style={'color':'green','textAlign': 'center', 'font-style': 'italic','position':'relative'}),
                                 html.H6('Empty tag',style={'color':'yellow','textAlign': 'center', 'font-style': 'italic','position':'relative','visibility':'hidden'})])
            else:
                if "/" not in clickData['points'][0]['id']:
                    country=clickData['points'][0]['id']
                    return html.Div([html.H4(
                         'You have selected Continent(s) as {}, country as {}'.format(continent,
                             country
                        ),style={'color':'white','textAlign': 'center', 'font-style': 'italic','position':'relative'}
                 ),html.H6('Ensure you go back to previous level by clicking on sub categories to access different continents',style={'color':'yellow','textAlign': 'center', 'font-style': 'bold','position':'relative'})])
                else:
                    country=clickData['points'][0]['id']
                    country=country.split("/")
                    return html.Div([html.H4('Full view',style={'color':'green','textAlign': 'center', 'font-style': 'italic','position':'relative'}),
                                 html.H6('Empty tag',style={'color':'yellow','textAlign': 'center', 'font-style': 'italic','position':'relative','visibility':'hidden'})])
        elif value!=[]:
            continent=','.join([str(val) for val in value])
            if clickData==None:
                return html.Div([html.H4(
                             'You have selected Continent(s) as {}'.format(
                                 continent
                            ),style={'color':'lightblue','textAlign': 'center', 'font-style': 'italic','position':'relative'}
                     ),
                       html.H6('empty tag',style={'visibility':'hidden'})])
            else:
                if "/" not in clickData['points'][0]['id']:
                    country=clickData['points'][0]['id']
                    return html.Div([html.H4(
                         'You have selected Continent(s) as {}, country as {}'.format(continent,
                             country
                        ),style={'color':'white','textAlign': 'center', 'font-style': 'italic','position':'relative'}
                 ),html.H6('Ensure you go back to previous level by clicking on sub categories to access different continents',style={'color':'yellow','textAlign': 'center', 'font-style': 'bold','position':'relative'})])
                else:
                    country=clickData['points'][0]['id']
                    country=country.split("/")
                    return html.Div([html.H4(
                         'You have selected Continent(s) as {}'.format(
                             continent
                        ),style={'color':'lightblue','textAlign': 'center', 'font-style': 'italic','position':'relative'}
                 ),
                  html.H6('empty tag',style={'visibility':'hidden'})])




    
@app.callback([Output('graph','figure'),Output('text-content', 'children')],[Input('graph', 'clickData'),Input('name-dropdown', 'value'),Input('my-date-picker-range','start_date'),Input('my-date-picker-range','end_date')],[State('graph', 'figure')])
def update_plot(selecteddata,value,start,end,fig):
    a_1=df_ana_1[(df_ana_1['Date']>=start) & (df_ana_1['Date']<=end)]
    if (value==[]):
        if selecteddata!=None:
            label=selecteddata['points'][0]['label']
            id_=selecteddata['points'][0]['id']
            if label==id_:
                return (preservelayoutandoutputsunburst1(a_1,string='Country/Region',labeller=label,flag=2),update_text1(selecteddata,value))
            else:
                return (preservelayoutandoutputsunburst1(a_1,flag=2),update_text1(selecteddata,value))
        elif (selecteddata==None):  
                return (preservelayoutandoutputsunburst1(a_1,flag=2),update_text1(selecteddata,value))
    elif (selecteddata==None) & (value!=[]):
        return (preservelayoutandoutputsunburst1(a_1,string='Continent',flag=1,continent=value),update_text1(selecteddata,value))
    elif (selecteddata!=None) & (value!=[]):
        label=selecteddata['points'][0]['label']
        id_=selecteddata['points'][0]['id']
        if id_==label:
            return (preservelayoutandoutputsunburst1(a_1,'Country/Region',label,flag=2),update_text1(selecteddata,value))
        else:
            return (preservelayoutandoutputsunburst1(a_1,string='Continent',flag=1,continent=value),update_text1(selecteddata,value))
    else:
        return (preservelayoutandoutputsunburst1(a_1,string='Continent',flag=1,continent=value),update_text1(selecteddata,value))

    
@app.callback(Output('graph1','figure'),
    [Input('graph1','selectedData'),
    Input('my-date-picker-range1', 'start_date'),Input('my-date-picker-range1', 'end_date'),Input('slider','value'),Input('my-boolean-switch', 'on'),Input('name-dropdown1','value')],
    [State('graph1', 'figure')])

def display_click_data(customdata1,start,end,value,switch,dropdown,fig):
    df_ana_2=df_ana_1[(df_ana_1['Date']>=start) & (df_ana_1['Date']<=end)]
    if dropdown==[]:
        df_ana_2=df_ana_2
    else:
        df_ana_2=df_ana_2.loc[df_ana_2['Continent'].isin(pd.Series(dropdown)),:]
    if (customdata1!=None):
        if(customdata1['points']!=[]):
            lat=[i['lat'] if 'lat' in i else 0 for i in customdata1['points']]
            lat=[i for i in lat if i!=0]     
            lon=[i['lon'] if 'lon' in i else 0 for i in customdata1['points']]
            lon=[i for i in lon if i!=0]
            if switch==True:
                if 'lassoPoints' in customdata1:
                    lon1=[i[0] for i in customdata1['lassoPoints']['geo'] if i[0]]
                    lat1=[i[1] for i in customdata1['lassoPoints']['geo'] if i[1]]
                    df_ana_3=df_ana_2[(df_ana_2['Long']>=min(lon1)) & (df_ana_2['Long']<=max(lon1)) & (df_ana_2['Lat']>=min(lat1))  & (df_ana_2['Lat']<=max(lat1))]
                    fig=project_on_map(df_ana_3,rotate=True,projection='orthographic',speed=value)
                    return (fig)
                elif 'range' in customdata1:
                    lon1=[i[0] for i in customdata1['range']['geo'] if i[0]]
                    lat1=[i[1] for i in customdata1['range']['geo'] if i[1]]
                    df_ana_3=df_ana_2[(df_ana_2['Long']>=min(lon1)) & (df_ana_2['Long']<=max(lon1)) & (df_ana_2['Lat']>=min(lat1))  & (df_ana_2['Lat']<=max(lat1))]
                    fig=project_on_map(df_ana_3,rotate=True,projection='orthographic',speed=value)
                    return (fig) 
                else:
                    df_ana_3=df_ana_2[(df_ana_2['Lat'].isin(list(set(lat)))) & (df_ana_2['Long'].isin(list(set(lon))))]
                    fig=project_on_map(df_ana_3,rotate=False,projection='orthographic',speed=value)
                    return (fig)
            else:
                df_ana_3=df_ana_2[(df_ana_2['Lat'].isin(list(set(lat)))) & (df_ana_2['Long'].isin(list(set(lon))))]
                fig=project_on_map(df_ana_3,rotate=False,projection='natural earth',speed=value)
                return (fig)
        elif (customdata1['points']==[]):
            if switch==True:
                fig=project_on_map(df_ana_2,rotate=True,projection='orthographic',speed=value)
                return (fig)
            else:
                fig=project_on_map(df_ana_2,rotate=False,projection='natural earth',speed=value)
                return (fig)   
    elif(customdata1==None):
        if switch==True:
            if dropdown==[]:
                fig=project_on_map(df_ana_2,rotate=True,projection='orthographic',speed=value,ind='sodo')
                return (fig)
            elif dropdown!=[]:
                fig=project_on_map(df_ana_2,rotate=True,projection='orthographic',speed=value,ind='special')
                return (fig)  
        else:
            fig=project_on_map(df_ana_2,rotate=False,projection='natural earth',speed=value)
            return (fig)
    #customdata1=None
    
@app.callback (Output('graph2','figure'),
[Input('my-date-picker-range2', 'start_date'),Input('my-date-picker-range2', 'end_date'),Input('name-dropdown2','value'),Input("TOP",'value')],
[State('graph2','figure')])

def display_click_data1(start,end,dropdown,top,fig):
    df_ana_2=df_ana_1[(df_ana_1['Date']>=start) & (df_ana_1['Date']<=end)]
    if dropdown==[]:
        if top==None:
            fig=racebarchart(df_ana_2,continent='NULL',top=30)
        else:
            fig=racebarchart(df_ana_2,continent='NULL',top=top)
    elif dropdown!=[]:
        if top==None:
            fig=racebarchart(df_ana_2,continent=dropdown,top=30)
        else:
            fig=racebarchart(df_ana_2,continent=dropdown,top=top)
    return fig
    #customdata1=None

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_date(n):
      return [html.P('Current Date & Time: ' +str(dt.now()),style={'font-family': 'Times New Roman','color':'white','backgroundColor':'black','opacity': '0.6','fontSize': 15,'height' : '30%',
                    'width' : '100%',
                    'float' : 'left',
                    'position' : 'bottom',
                    'padding-top' : 0,
                    'padding-right' : 0})]


@app.callback(Output('live-update-text1', 'children'),
              [Input('interval-component1', 'n_intervals')])
def update_date(n):
      return [html.P('Current Date & Time: ' +str(dt.now()),style={'font-family': 'Times New Roman','color':'white','backgroundColor':'black','opacity': '0.6','fontSize': 15,'height' : '30%',
                    'width' : '100%',
                    'float' : 'left',
                    'position' : 'bottom',
                    'padding-top' : 0,
                    'padding-right' : 0})]

@app.callback(Output('live-update-text0', 'children'),
              [Input('interval-component0', 'n_intervals')])
def update_date(n):
      return [html.P('Current Date & Time: ' +str(dt.now()),style={'font-family': 'Times New Roman','color':'white','backgroundColor':'black','opacity': '0.6','fontSize': 15,'height' : '30%',
                    'width' : '100%',
                    'float' : 'left',
                    'position' : 'bottom',
                    'padding-top' : 0,
                    'padding-right' : 0})]



