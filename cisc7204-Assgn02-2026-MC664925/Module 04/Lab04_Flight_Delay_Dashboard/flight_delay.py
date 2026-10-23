import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_utils import load_airline_data

airline_data = load_airline_data()
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Flight Delay Time Statistics', style={'textAlign':'center','color':'#503D36','fontSize':30}),
    html.Div(['Input Year: ', dcc.Input(id='input-year', value=2010, type='number', min=2010, max=2020, style={'height':'35px','fontSize':30})], style={'fontSize':30}),
    html.Div([dcc.Graph(id='carrier-plot'), dcc.Graph(id='weather-plot')], style={'display':'flex'}),
    html.Div([dcc.Graph(id='nas-plot'), dcc.Graph(id='security-plot')], style={'display':'flex'}),
    html.Div(dcc.Graph(id='late-plot'), style={'width':'65%'})
])
def compute_info(df, year):
    selected = df[df['Year'] == int(year)]
    columns = ['CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay']
    return [selected.groupby(['Month','Reporting_Airline'], as_index=False)[col].mean() for col in columns]
@app.callback([Output(x,'figure') for x in ['carrier-plot','weather-plot','nas-plot','security-plot','late-plot']], Input('input-year','value'))
def get_graph(year):
    columns = ['CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay']
    titles = ['Average carrier delay time (minutes) by airline','Average weather delay time (minutes) by airline','Average NAS delay time (minutes) by airline','Average security delay time (minutes) by airline','Average late aircraft delay time (minutes) by airline']
    frames = compute_info(airline_data, year or 2010)
    return [px.line(frame, x='Month', y=col, color='Reporting_Airline', title=title) for frame,col,title in zip(frames,columns,titles)]
if __name__ == '__main__':
    app.run(debug=False)
