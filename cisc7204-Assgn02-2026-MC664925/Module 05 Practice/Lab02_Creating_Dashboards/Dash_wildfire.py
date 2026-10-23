import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from data_utils import load_wildfire_data

df = load_wildfire_data()
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month_name()
df['Year'] = df['Date'].dt.year
regions = [('New South Wales','NSW'),('Northern Territory','NT'),('Queensland','QL'),('South Australia','SA'),('Tasmania','TA'),('Victoria','VI'),('Western Australia','WA')]
years = sorted(df['Year'].dropna().unique().tolist())
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Australia Wildfire Dashboard', style={'textAlign':'center','color':'#503D36','fontSize':26}),
    html.Div([
        html.Div([html.H2('Select Region:', style={'marginRight':'2em'}), dcc.RadioItems([{'label':a,'value':b} for a,b in regions], 'NSW', id='region', inline=True)]),
        html.Div([html.H2('Select Year:', style={'marginRight':'2em'}), dcc.Dropdown(options=[{'label':int(y),'value':int(y)} for y in years], value=2005 if 2005 in years else int(years[0]), id='year')])
    ], style={'display':'flex','gap':'2rem','alignItems':'center','flexWrap':'wrap'}),
    html.Div([html.Div(id='plot1',style={'width':'50%'}),html.Div(id='plot2',style={'width':'50%'})],style={'display':'flex'})
])
@app.callback([Output('plot1','children'),Output('plot2','children')],[Input('region','value'),Input('year','value')])
def reg_year_display(region, year):
    d = df[(df['Region']==region) & (df['Year']==int(year))]
    estimated = d.groupby('Month',as_index=False)['Estimated_fire_area'].mean()
    vegetation = d.groupby('Month',as_index=False)['Count'].mean()
    pie = px.pie(estimated, values='Estimated_fire_area', names='Month', title=f'{region} : Monthly Average Estimated Fire Area in year {year}')
    bar = px.bar(vegetation, x='Month', y='Count', title=f'{region} : Average Count of Pixels for Presumed Vegetation Fires in year {year}')
    return dcc.Graph(figure=pie), dcc.Graph(figure=bar)
if __name__ == '__main__':
    app.run(debug=False)
