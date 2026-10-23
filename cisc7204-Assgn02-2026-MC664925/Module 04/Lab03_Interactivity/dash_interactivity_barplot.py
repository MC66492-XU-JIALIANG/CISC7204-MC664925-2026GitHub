import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from data_utils import load_airline_data

airline_data = load_airline_data()
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Total number of flights to the destination state split by reporting airline', style={'textAlign':'center','color':'#503D36','fontSize':40}),
    html.Div(['Input Year: ', dcc.Input(id='input-year', value=2010, type='number')]),
    dcc.Graph(id='bar-plot')
])
@app.callback(Output('bar-plot','figure'), Input('input-year','value'))
def update_bar(year):
    df = airline_data[airline_data['Year'] == int(year or 2010)]
    grouped = df.groupby(['DestState','Reporting_Airline'], as_index=False)['Flights'].sum()
    return px.bar(grouped, x='DestState', y='Flights', color='Reporting_Airline', barmode='group', title='Total number of flights to the destination state split by reporting airline')
if __name__ == '__main__':
    app.run(debug=False)
