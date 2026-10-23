import plotly.express as px
import dash
from dash import dcc, html
from data_utils import load_airline_data

data = load_airline_data().sample(n=500, random_state=42)
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Airline Dashboard', style={'textAlign':'center', 'color':'#503D36', 'fontSize':40}),
    html.P('Proportion of distance group (250 mile distance interval group) by flights.', style={'textAlign':'center', 'color':'#F57241'}),
    dcc.Graph(figure=fig)
], style={'maxWidth':'1100px', 'margin':'0 auto'})
if __name__ == '__main__':
    app.run(debug=False)
