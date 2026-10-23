import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from data_utils import load_airline_data

airline_data = load_airline_data()
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Airline Performance Dashboard', style={'textAlign':'center','color':'#503D36','fontSize':40}),
    html.Div(['Input Year: ', dcc.Input(id='input-year', value=2010, type='number', style={'height':'50px','fontSize':35})], style={'fontSize':40}),
    dcc.Graph(id='line-plot')
])
@app.callback(Output('line-plot','figure'), Input('input-year','value'))
def get_graph(year):
    df = airline_data[airline_data['Year'] == int(year or 2010)]
    line_data = df.groupby('Month', as_index=False)['ArrDelay'].mean()
    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker={'color':'green'}))
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig
if __name__ == '__main__':
    app.run(debug=False)
