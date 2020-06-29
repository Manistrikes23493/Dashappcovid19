from datetime import datetime as dt,timedelta
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
from plotly import __version__
pd.options.mode.chained_assignment = None

def preservelayoutandoutputsunburst1(df,string='',labeller='',flag=1,continent=[]):
    from plotly.subplots import make_subplots
    df.loc[:,'pathcol']=df['Country/Region']
    L=[]
    if flag!=1:
        if string!='':
            df_1=df[df[string]==labeller]
        else:
            df_1=df
        fig = make_subplots(1, 2,vertical_spacing=10,horizontal_spacing=0.1, specs=[[{"type": "domain"}, {"type": "bar"}]],subplot_titles=("WORLD VIEW BY CONTINENT(s)",""))
        fig.update_layout(
                hoverlabel=dict(
                bgcolor="white", 
                font_size=16, 
                font_family="Rockwell"
                ))
        fig.update_layout(autosize=True,height=540, width=950)
        #fig.update_layout(clickmode =("event+select"),template='plotly_dark')
        lastval=sorted(df_1['Date'].unique())[-1]
        df_ana_=df_1[df_1['Date']==lastval]
        fig1=px.sunburst(df_ana_, path=['Country/Region','Flag'], values='Deaths/Recovered/Confirmed',color='Flag',
                         color_discrete_map={'(?)':'rgb(47,138,196)', 'Confirmed':'#00FE35', 'Deaths':'#FD3216','Recovered':'#F6F926'},hover_data=['pathcol','Continent','Date'],height=830,branchvalues='total',template='plotly_dark')
        trace1=fig1['data'][0] 
        #fig.update_layout(clickmode =("event+select"),template='plotly_dark',autosize=True)
        trace1['insidetextfont']=dict(color='white')
        b=[str(i) for i in list(fig1['data'][0]['values'])]
        a=fig1['data'][0]['customdata'].tolist()
        calculation=['See next level for cases' if (i[3]=='(?)') else j for i,j in zip(a,b)]
        fig1.data[0].customdata[:, 0] = calculation
        trace1['hovertemplate']='Cases=%{customdata[0]}<br>Continent=%{customdata[1]}<br>Date=%{customdata[2]}<br>labels=%{label}<br>parent=%{parent}<br>id=%{id}'
        fig.add_trace(trace1, row=1, col=1)
        fig['data'][0]['domain']={'x': [0.0, 0.465], 'y': [0.0,1.0]}
        Ana=df_1.groupby(['Flag','Date'])['Deaths/Recovered/Confirmed'].agg('sum').reset_index()
        Ana['Shift1']=Ana.groupby(['Flag'])['Deaths/Recovered/Confirmed'].shift(1)
        Ana['Daily no of cases']=Ana['Deaths/Recovered/Confirmed']-Ana['Shift1']
        Ana['Date'] = pd.to_datetime(Ana['Date'])
        Ana.sort_values(['Flag','Date'], inplace = True, ascending=[False, True])
#         Ana['Pct_change']=Ana.groupby('Flag')['Deaths/Recovered/Confirmed'].apply(pd.Series.pct_change)*100
#         Ana.loc[Ana['Pct_change']>10000,'Pct_change']=100
        figa=px.area(Ana, x="Date", y="Deaths/Recovered/Confirmed",color='Flag', color_discrete_sequence=['#F6F926','#FD3216','#00FE35'],
                             height=400,facet_row='Flag',facet_col_wrap=0,template='plotly_dark')
        fig.update_layout(clickmode =("event+select"),template='plotly_dark',autosize=True)
        figb=px.line(Ana, x="Date", y="Daily no of cases", color='Flag', color_discrete_sequence=['#F6F926','#FD3216','#00FE35'],
                             height=400,facet_row='Flag',facet_col_wrap=0,template='plotly_dark')
        fig=fig.add_trace(figa['data'][0],row=1, col=2)
        fig=fig.add_trace(figa['data'][1],row=1,col=2)
        fig=fig.add_trace(figa['data'][2],row=1,col=2)
        fig['data'][1]['xaxis']='x3'
        fig['data'][2]['xaxis']='x2'
        fig['data'][3]['xaxis']='x'
        fig['data'][1]['yaxis']='y'
        fig['data'][2]['yaxis']='y2'
        fig['data'][3]['yaxis']='y3'
        fig.update_layout(
                showlegend=False,
                legend = {'title': {'text': 'Flag'}, 'tracegroupgap': 0},
                margin = dict(r=10, t=25, b=40, l=60),
                xaxis= {'anchor': 'y', 'autorange': True,'showticklabels': True, 'domain': [0.55, 1.0], 'showgrid': False, 'title': {'text': 'Date'}},
                xaxis2= {'anchor': 'y2',
                           'autorange': True,
                           'domain': [0.55, 1.0],
                           'matches': 'x',
                           'showgrid': False,
                           'showticklabels': False},
                xaxis3= {'anchor': 'y3',
                           'autorange': True,
                           'domain': [0.55, 1.0],
                           'matches': 'x',
                           'showgrid': False,
                           'showticklabels': False},
                yaxis= {'anchor': 'x',
                          'domain': [0.0, 0.3133333333333333],
                          'mirror': True,
                          'showgrid': False,
                          'matches':None,
                          'title': {'text': 'Confirmed'}},
                yaxis2= {'anchor': 'x2',
                           'domain': [0.34333333333333327, 0.6566666666666665],
                           'mirror': True,
                            'matches':None,
                           'showgrid': False,
                           'title': {'text': 'Deaths'}},
                yaxis3= {'anchor': 'x3',
                           'autorange': True,
                           'domain': [0.6866666666666665, 0.9999999999999998],
                           'matches':None,
                           'showgrid': False,
                           'title': {'text': 'Recovered'}},
                template="plotly_dark"
                   )

        fig=fig.add_trace(figb['data'][0], row=1, col=2)
        fig=fig.add_trace(figb['data'][1],row=1,col=2)
        fig=fig.add_trace(figb['data'][2],row=1,col=2)
        fig['data'][4]['xaxis']='x3'
        fig['data'][5]['xaxis']='x2'
        fig['data'][6]['xaxis']='x'
        fig['data'][4]['yaxis']='y'
        fig['data'][5]['yaxis']='y2'
        fig['data'][6]['yaxis']='y3'
        fig.update_layout(
                showlegend=False,
                legend = {'title': {'text': 'Flag'}, 'tracegroupgap': 0},
                margin = dict(r=10, t=25, b=40, l=60),
                xaxis= {'anchor': 'y', 'autorange': True,'showticklabels': True, 'domain': [0.55, 1.0], 'showgrid': False, 'title': {'text': 'Date'}},
                xaxis2= {'anchor': 'y2',
                           'autorange': True,
                           'domain': [0.55, 1.0],
                           'matches': 'x',
                           'showgrid': False,
                           'showticklabels': False},
                xaxis3= {'anchor': 'y3',
                           'autorange': True,
                           'domain': [0.55, 1.0],
                           'matches': 'x',
                           'showgrid': False,
                           'showticklabels': False},
                yaxis= {'anchor': 'x',
                          'domain': [0.0, 0.3133333333333333],
                          'mirror': True,
                          'showgrid': False,
                          'matches':None,
                          'title': {'text': 'Recovered'}},
                yaxis2= {'anchor': 'x2',
                           'domain': [0.34333333333333327, 0.6566666666666665],
                           'mirror': True,
                            'matches':None,
                           'showgrid': False,
                           'title': {'text': 'Deaths'}},
                yaxis3= {'anchor': 'x3',
                           'autorange': True,
                           'domain': [0.6866666666666665, 0.9999999999999998],
                           'matches':None,
                           'showgrid': False,
                           'title': {'text': 'Confirmed'}},
                template="plotly_dark"
                   )
        fig.update_yaxes(matches=None)
        # Add dropdown
        fig.update_layout(
            updatemenus=[
                dict(
                    type = "buttons",
                    x=0.57,
                    y=1.2,
                    direction="right",
                    buttons=list([
#                         dict(label="Cumulative cases",
#                              method="restyle",
#                              visible=True,
#                              args=[{"visible": [True,True,True,True,False,False,False]}]),
                             #args2=[{"visible": [True,False,False,False,False,False,False]}]),
                        dict(label="Cumulative/Daily Cases",
                             method="restyle",
                             visible=True,
                             args=[{"visible": [True,False, False, False,True,True,True]}],
                             args2=[{"visible": [True,True,True,True,False,False,False]}])
                             #args2=[{"visible": [True,False, False, False,False,False,False]}])
                    ]),
                    pad={"r": 30, "t": 0},
                    showactive=True,
                    font=dict(color='black'),
                    bgcolor='grey'
                ),
            ]
        )
        #fig.update_layout(clickmode =("event+select"),template='plotly_dark')

#         fig.update_layout(
#             title= {'text': "Views"}
#         )
        fig.update_layout(clickmode =("event+select"),autosize=True)
        return (fig)
    elif flag==1:
        if string!='':
            df_1=df[df[string].isin(continent)]
        else:
            df_1=df
        fig = make_subplots(1, 2,vertical_spacing=10,horizontal_spacing=0.1, specs=[[{"type": "domain"}, {"type": "bar"}]],subplot_titles=("WORLD VIEW BY CONTINENT(s)",""))
        fig.update_layout(
            hoverlabel=dict(
            bgcolor="white", 
            font_size=16, 
            font_family="Rockwell"
            ))
        fig.update_yaxes(matches=None)
        fig.update_layout(autosize=True,height=540, width=950)
        #fig.update_layout(clickmode =("event+select"),template='plotly_dark')
        lastval=sorted(df_1['Date'].unique())[-1]
        df_ana_=df_1[df_1['Date']==lastval]
        #fig = make_subplots(1, 2, specs=[[{"type": "domain"}, {"type": "bar"}]],subplot_titles=("",""),shared_xaxes=True)
        fig1=px.sunburst(df_ana_, path=['Country/Region','Flag'], values='Deaths/Recovered/Confirmed',color='Flag',color_discrete_map={'(?)':'rgb(47,138,196)', 'Confirmed':'#00FE35', 'Deaths':'#FD3216','Recovered':'#F6F926'},hover_data=['pathcol','Continent','Date'],height=830,branchvalues='total',template='plotly_dark')
        trace1=fig1['data'][0]
        b=[str(i) for i in list(fig1['data'][0]['values'])]
        a=fig1['data'][0]['customdata'].tolist()
        calculation=['See next level for cases' if (i[3]=='(?)') else j for i,j in zip(a,b)]
        fig1.data[0].customdata[:, 0] = calculation
        trace1['hovertemplate']='Cases=%{customdata[0]}<br>Continent=%{customdata[1]}<br>Date=%{customdata[2]}<br>labels=%{label}<br>parent=%{parent}<br>id=%{id}'
        trace1['insidetextfont']=dict(color='white')
        fig.add_trace(trace1, row=1, col=1)
        fig['data'][0]['domain']={'x': [0.0, 0.465], 'y': [0.0,1.0]}
        Ana=df_1.groupby(['Flag','Date'])['Deaths/Recovered/Confirmed'].agg('sum').reset_index()
        Ana['Shift1']=Ana.groupby(['Flag'])['Deaths/Recovered/Confirmed'].shift(1)
        Ana['Daily no of cases']=Ana['Deaths/Recovered/Confirmed']-Ana['Shift1']
        Ana['Date'] = pd.to_datetime(Ana['Date'])
        Ana.sort_values(['Flag','Date'], inplace = True, ascending=[False, True])
        Ana['Pct_change']=Ana.groupby('Flag')['Deaths/Recovered/Confirmed'].apply(pd.Series.pct_change)*100
        Ana.loc[Ana['Pct_change']>10000,'Pct_change']=100
        figa=px.area(Ana, x="Date", y="Deaths/Recovered/Confirmed",color='Flag',color_discrete_sequence=['#F6F926','#FD3216','#00FE35'],
                             height=400,facet_row='Flag',facet_col_wrap=0,template='plotly_dark')
        fig.update_layout(clickmode =("event+select"),template='plotly_dark',autosize=True)
        figb=px.line(Ana, x="Date", y="Daily no of cases", color='Flag',color_discrete_sequence=['#F6F926','#FD3216','#00FE35'],
                             height=400,facet_row='Flag',facet_col_wrap=0,template='plotly_dark')
        fig=fig.add_trace(figa['data'][0],row=1, col=2)
        fig=fig.add_trace(figa['data'][1],row=1,col=2)
        fig=fig.add_trace(figa['data'][2],row=1,col=2)
        fig['data'][1]['xaxis']='x3'
        fig['data'][2]['xaxis']='x2'
        fig['data'][3]['xaxis']='x'
        fig['data'][1]['yaxis']='y'
        fig['data'][2]['yaxis']='y2'
        fig['data'][3]['yaxis']='y3'
        #fig.update_layout(clickmode =("event+select"),template='plotly_dark',autosize=True)
        fig.update_layout(
                showlegend=False,
                legend = {'title': {'text': 'Flag'}, 'tracegroupgap': 0},
                margin = dict(r=10, t=15, b=40, l=30),
                xaxis= {'anchor': 'y', 'autorange': True,'showticklabels': True, 'domain': [0.55, 1.0], 'showgrid': False, 'title': {'text': 'Date'}},
                xaxis2= {'anchor': 'y2',
                           'autorange': True,
                           'domain': [0.55, 1.0],
                           'matches': 'x',
                           'showgrid': False,
                           'showticklabels': False},
                xaxis3= {'anchor': 'y3',
                           'autorange': True,
                           'domain': [0.55, 1.0],
                           'matches': 'x',
                           'showgrid': False,
                           'showticklabels': False},
                yaxis= {'anchor': 'x',
                          'domain': [0.0, 0.3133333333333333],
                          'mirror': True,
                          'showgrid': False,
                          'matches':None,
                          'title': {'text': 'Confirmed(Cum)/Confirmed(Daily)'}},
                yaxis2= {'anchor': 'x2',
                           'domain': [0.34333333333333327, 0.6566666666666665],
                           'mirror': True,
                            'matches':None,
                           'showgrid': False,
                           'title': {'text': 'Deaths(Cum)/Deaths(Daily)'}},
                yaxis3= {'anchor': 'x3',
                           'autorange': True,
                           'domain': [0.6866666666666665, 0.9999999999999998],
                           'matches':None,
                           'showgrid': False,
                           'title': {'text': 'Recovered(Cum)/Recovered(Daily)'}},
                template="plotly_dark"
                   )
        fig=fig.add_trace(figb['data'][0], row=1, col=2)
        fig=fig.add_trace(figb['data'][1],row=1,col=2)
        fig=fig.add_trace(figb['data'][2],row=1,col=2)
        fig['data'][4]['xaxis']='x3'
        fig['data'][5]['xaxis']='x2'
        fig['data'][6]['xaxis']='x'
        fig['data'][4]['yaxis']='y'
        fig['data'][5]['yaxis']='y2'
        fig['data'][6]['yaxis']='y3'
        fig.update_layout(
                showlegend=False,
                legend = {'title': {'text': 'Flag'}, 'tracegroupgap': 0},
                margin = dict(r=10, t=15, b=40, l=30),
                xaxis= {'anchor': 'y', 'autorange': True,'showticklabels': True, 'domain': [0.55, 1.0], 'showgrid': False, 'title': {'text': 'Date'}},
                xaxis2= {'anchor': 'y2',
                           'autorange': True,
                           'domain': [0.55, 1.0],
                           'matches': 'x',
                           'showgrid': False,
                           'showticklabels': False},
                xaxis3= {'anchor': 'y3',
                           'autorange': True,
                           'domain': [0.55, 1.0],
                           'matches': 'x',
                           'showgrid': False,
                           'showticklabels': False},
                yaxis= {'anchor': 'x',
                          'domain': [0.0, 0.3133333333333333],
                          'mirror': True,
                          'showgrid': False,
                          'matches':None,
                          'title': {'text': 'Recovered'}},
                yaxis2= {'anchor': 'x2',
                           'domain': [0.34333333333333327, 0.6566666666666665],
                           'mirror': True,
                            'matches':None,
                           'showgrid': False,
                           'title': {'text': 'Deaths'}},
                yaxis3= {'anchor': 'x3',
                           'autorange': True,
                           'domain': [0.6866666666666665, 0.9999999999999998],
                           'matches':None,
                           'showgrid': False,
                           'title': {'text': 'Confirmed'}},
                template="plotly_dark"
                   )
        fig.update_yaxes(matches=None)
#         fig.update_layout(clickmode =("event+select"),template='plotly_dark',autosize=True)
        # Add dropdown
        fig.update_layout(
            updatemenus=[
                dict(
                    type = "buttons",
                    x=0.57,
                    y=1.2,
                    direction="right",
                    buttons=list([
#                         dict(label="Cumulative cases",
#                              method="restyle",
#                              visible=False,
#                              args=[{"visible": [True,True,True,True,False,False,False]}],
#                              args2=[{"visible": [False,False,False,False,False,False,False]}]),
                        dict(label="Cumulative/Daily Cases",
                             method="restyle",
                             visible=True,
                             args=[{"visible": [True,False, False, False,True,True,True]}],
                             args2=[{"visible": [True,True,True,True,False,False,False]}])
                             #args2=[{"visible": [True,False, False, False,False,False,False]}])
                    ]),
                    pad={"r": 30, "t": 0},
                    showactive=True,
                    font=dict(color='black'),
                    bgcolor='grey'
                ),
            ]
        )

#         fig.update_layout(
#             title= {'text': "Views"}
#         )
        fig.update_layout(clickmode =("event+select"),template='plotly_dark',autosize=True)
        fig.update_yaxes(matches=None)
        return fig


# In[65]:

def project_on_map(df,rotate=False,theme='plotly_dark',projection='orthographic',speed=1000,ind='special'):
    from plotly.subplots import make_subplots
    import math
    #df=df.loc[(df['Date']>=start) & (df['Date']<=end),:]
    df.loc[df['Deaths/Recovered/Confirmed']<=-1,'Deaths/Recovered/Confirmed']=0
    df=df.groupby(['Continent','Country/Region','Lat','Long','Flag','Date'])['Deaths/Recovered/Confirmed'].sum().reset_index()
    max_lat=df['Lat'].unique().max()
    min_lat=df['Lat'].unique().min()
    min_lon=df['Long'].unique().min()
    max_lon=df['Long'].unique().max()
    df=df.sort_values(by='Date')
    fig_scatter1=make_subplots(1, 2,vertical_spacing=10,horizontal_spacing=0.15,specs=[[{"type":"scattergeo"}, {"type": "scatter"}]],subplot_titles=('WORLD VIEW',"CONFIRMED Vs RECOVERED(COLOR:DEATHS)"))
    pivoted=df.groupby(['Date','Continent','Country/Region','Lat','Long','Flag'])['Deaths/Recovered/Confirmed'].sum().unstack().reset_index()
    #plotly express plots
    fig = px.scatter_geo(df,lat='Lat',lon='Long',hover_name="Country/Region",range_color=[0,1],animation_frame='Date',color='Flag',template='plotly_dark',
                     size="Deaths/Recovered/Confirmed",opacity=0.9,size_max=30,color_discrete_map={'Confirmed':'#00FE35','Recovered':'#275a61','Deaths':'#FD3216'})
    figb = px.scatter(pivoted, x="Confirmed", y="Recovered", animation_frame="Date", color="Deaths", hover_name="Country/Region",color_continuous_scale='Bluered',hover_data=['Continent','Lat',"Long"],
               size="Deaths",size_max=50,template='plotly_dark')
    #data
    fig_scatter1=fig_scatter1.add_traces(fig['data'])
    fig_scatter1=fig_scatter1.add_traces(figb['data'])
    #frames
    for i in range(0,len(fig['frames'])):
        fig['frames'][i]['data']=fig['frames'][i]['data']+figb['frames'][i]['data']
    fig_scatter1=fig_scatter1.update(frames=fig['frames'])
    #sliders
    sliders=fig['layout']['sliders']
    updatemenus=fig['layout']['updatemenus']
    #geos
    fig_scatter1.update_layout(sliders=sliders,updatemenus=updatemenus,
        coloraxis= {'colorbar': {'title': {'text': 'Deaths'}}, 'colorscale': [[0.0, 'rgb(0,0,255)'], [1.0, 'rgb(255,0,0)']]},
        legend={'itemsizing': 'constant', 'tracegroupgap': 0},template=theme
        )
    fig_scatter1.update_layout(legend=dict(x=0.4, y=1.3),xaxis= {'title': {'text': 'Confirmed'}},yaxis={'title': {'text': 'Recovered'}})
    fig_scatter1['layout']['updatemenus'][0]['buttons'][0]['args'][1]['frame']['duration']=speed
    fig_scatter1['layout']['updatemenus'][0]['buttons'][0]['args'][1]['transition']['duration']=speed
    fig_scatter1.update_geos(domain=dict(x= [0, 0.475]))
    if ((rotate==False)|(rotate==True)) & (projection!='orthographic'):
        fig_scatter1.update_geos(resolution=50,projection_type=projection,showland=True,landcolor='dimgray',showocean=False,oceancolor='lightblue',lataxis=dict(range=[min_lat,max_lat]),lonaxis=dict(range=[min_lon,max_lon]),countrywidth=0.5,countrycolor='black',showcountries=True,showframe=False)
        fig_scatter1.update_layout(margin=dict(r=10, t=25, b=40, l=60))
        #return fig_scatter1
    elif (rotate!=False) & (projection=='orthographic') & (ind!='special'):
        fig_scatter1.update_geos(resolution=50,projection_type=projection,showland=True,coastlinecolor='black',landcolor='dimgray',showocean=True,oceancolor="steelblue",countrywidth=0.5,countrycolor='black',showcountries=True,showframe=False)
        fig_scatter1.update_geos(projection = dict(
            type = projection,
            rotation = dict(
                lon =112,
                lat = 21
            )
        ))
        lon = np.arange(-180,112,round(180/len(fig_scatter1['frames'])))
        lon=lon[::-1]
        for i in range(len(fig_scatter1['frames'])):
            fig_scatter1['frames'][i]['layout']=dict(geo_center_lon=lon[i],geo_projection_rotation_lon =lon[i])
        #return fig_scatter1
    elif (rotate==True) & (projection=='orthographic') & (ind=='special'):
        fig_scatter1.update_geos(resolution=50,projection_type=projection,lataxis=dict(range=[min_lat,max_lat]),lonaxis=dict(range=[min_lon,max_lon]),showland=True,coastlinecolor='black',landcolor='dimgray',showocean=True,oceancolor="steelblue",countrywidth=0.5,countrycolor='black',showcountries=True,showframe=False)
        fig_scatter1.update_geos(projection = dict(
            type = projection,
            rotation = dict(
                lon =min_lon,
                lat =min_lat
            )
        ))
        if (abs(min_lon)>abs(max_lon)):
            a=abs(min_lon)
        elif(abs(max_lon)>abs(min_lon)):
            a=abs(max_lon)
        lon = np.arange(min_lon,max_lon,round(a/len(fig_scatter1['frames'])))
        lon=lon[::-1]
        calc=len(fig_scatter1['frames'])/len(lon)
        calc=math.ceil(calc)
        lon=np.repeat(lon,calc)
        for i in range(len(fig_scatter1['frames'])):
            fig_scatter1['frames'][i]['layout']=dict(geo_center_lon=lon[i],geo_projection_rotation_lon =lon[i])
    elif (rotate==False) & (projection=='orthographic'):
        fig_scatter1.update_geos(resolution=50,projection_type='natural earth',coastlinecolor='black',showland=True,landcolor='dimgray',showocean=True,oceancolor="steelblue",lataxis=dict(range=[min_lat,max_lat]),lonaxis=dict(range=[min_lon,max_lon]),countrywidth=0.5,countrycolor='black',showcountries=True,showframe=False)
    fig_scatter1.update_layout(autosize=True,height=690,width=960,clickmode=('event+select'))
    return fig_scatter1


# In[66]:


def racebarchart(dataframe,continent="NULL",top=10):
    df=dataframe.groupby(['Country/Region','Date','Flag','Continent'])['Deaths/Recovered/Confirmed'].sum().reset_index()
    if continent=="NULL":
        df['Date']=df['Date'].astype(str)
    else:
        df['Date']=df['Date'].astype(str)
        df=df[df['Continent'].isin(continent)]
    maindf=pd.DataFrame()
    for i in df['Date'].unique():
        gp1=df[df['Date']==i]
        gp1=gp1.sort_values(by=['Flag','Deaths/Recovered/Confirmed'],ascending=False)
        a=gp1[gp1['Flag']=='Confirmed']
        a=a.sort_values(by='Deaths/Recovered/Confirmed',ascending=False)[0:top]
        a=a.sort_values(by='Deaths/Recovered/Confirmed')
#         b=gp1[gp1['Flag']=='Recovered']
#         b=b.sort_values(by='Deaths/Recovered/Confirmed',ascending=False)[0:top]
#         b=b.sort_values(by='Deaths/Recovered/Confirmed')
        c=gp1[gp1['Flag']=='Deaths']
        c=c.sort_values(by='Deaths/Recovered/Confirmed',ascending=False)[0:top]
        c=c.sort_values(by='Deaths/Recovered/Confirmed')
        maindf=maindf.append([a,c])
        maindf=maindf.reset_index(drop=True)
    df=maindf
    from plotly.subplots import make_subplots
    #print(pd.concat(List))
    fig=make_subplots(1,2,specs=[[{"type":"bar"}, {"type": "bar"}]],vertical_spacing=10,horizontal_spacing=0.1,subplot_titles=("CONFIRMED","DEATHS"))
    maindf1=df[df['Flag']=='Confirmed']
    figa=px.bar(maindf1, x="Deaths/Recovered/Confirmed", y="Country/Region",animation_frame='Date',orientation='h',hover_data=['Flag'],template='plotly_dark',barmode='group',color='Deaths/Recovered/Confirmed',color_continuous_scale='greens')
#     maindf2=maindf[maindf['Flag']=='Recovered']
#     figb=px.bar(maindf2, x="Deaths/Recovered/Confirmed", y="Country/Region",animation_frame='Date',orientation='h',hover_data=['Flag'],template='plotly_dark',color='Deaths/Recovered/Confirmed',color_continuous_scale='spectral')
    maindf3=df[df['Flag']=='Deaths']
    figc=px.bar(maindf3, x="Deaths/Recovered/Confirmed", y="Country/Region",animation_frame='Date',color="Deaths/Recovered/Confirmed",orientation='h',hover_data=['Flag'],template='plotly_dark',color_continuous_scale='reds')
    fig=fig.add_trace(figa['data'][0],row=1,col=1)
    fig.update_layout(coloraxis=dict(colorscale='tealgrn_r'))
    fig=fig.update_traces(marker=dict(colorscale='tealgrn_r',coloraxis='coloraxis'),row=1,col=1)
    fig=fig.add_trace(figc['data'][0],row=1,col=2)
    fig.update_layout(coloraxis2=dict(colorscale='peach'))
    fig=fig.update_traces(marker=dict(colorscale='peach',coloraxis='coloraxis2'),row=1,col=2)
    fig.update_layout(template='plotly_dark')
    for i in range(0,len(figa['frames'])):
        figa['frames'][i]['data']=figa['frames'][i]['data']+figc['frames'][i]['data']
        figa['frames'][i]['data'][1]['xaxis']='x2'
        figa['frames'][i]['data'][1]['yaxis']='y2'
        figa['frames'][i]['data'][0]['marker']['coloraxis']='coloraxis'
        figa['frames'][i]['data'][1]['marker']['coloraxis']='coloraxis2'
    fig=fig.update(frames=figa['frames'])
    sliders=figa['layout']['sliders']
    updatemenus=figa['layout']['updatemenus']
    fig=fig.update_layout(sliders=sliders,updatemenus=updatemenus,autosize=True,height=710,width=950)
    fig.update_layout(coloraxis_showscale=False,coloraxis2_showscale=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return (fig)