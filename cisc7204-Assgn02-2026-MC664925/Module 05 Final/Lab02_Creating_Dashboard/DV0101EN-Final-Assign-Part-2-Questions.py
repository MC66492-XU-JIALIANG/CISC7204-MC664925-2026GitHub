import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_utils import load_automobile_data

data = load_automobile_data()
data['Year'] = pd.to_numeric(data['Year'], errors='coerce')
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
data['Month'] = pd.Categorical(data['Month'].astype(str).str.strip(), categories=month_order, ordered=True)
years = sorted(data['Year'].dropna().astype(int).unique())
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Automobile Sales Statistics Dashboard', style={'textAlign':'center','color':'#503D36','fontSize':24}),
    html.Label('Select Statistics:'),
    dcc.Dropdown(id='dropdown-statistics', options=[
        {'label':'Yearly Statistics','value':'Yearly Statistics'},
        {'label':'Recession Period Statistics','value':'Recession Period Statistics'}
    ], value='Select Statistics', placeholder='Select a report type', style={'width':'80%','padding':'3px','fontSize':'20px','textAlignLast':'center'}),
    html.Label('Select Year:'),
    dcc.Dropdown(id='select-year', options=[{'label':y,'value':y} for y in years], value='Select-year', placeholder='Select-year', style={'width':'80%','padding':'3px','fontSize':'20px','textAlignLast':'center'}),
    html.Div(id='output-container', className='chart-grid', style={'display':'flex','flexDirection':'column'})
], style={'maxWidth':'1450px','margin':'0 auto','padding':'12px'})

@app.callback(Output('select-year','disabled'), Input('dropdown-statistics','value'))
def update_input_container(statistics):
    return statistics != 'Yearly Statistics'

@app.callback(Output('output-container','children'), [Input('dropdown-statistics','value'),Input('select-year','value')])
def update_output_container(statistics, year):
    if statistics == 'Recession Period Statistics':
        d = data[data['Recession']==1]
        a = d.groupby('Year',as_index=False)['Automobile_Sales'].mean()
        b = d.groupby('Vehicle_Type',as_index=False)['Automobile_Sales'].mean()
        c = d.groupby('Vehicle_Type',as_index=False)['Advertising_Expenditure'].sum()
        u = d.groupby(['unemployment_rate','Vehicle_Type'],as_index=False)['Automobile_Sales'].mean()
        figs = [
            px.line(a,x='Year',y='Automobile_Sales',title='Average Automobile Sales Fluctuation Over Recession Period'),
            px.bar(b,x='Vehicle_Type',y='Automobile_Sales',title='Average Number of Vehicles Sold by Vehicle Type During Recessions'),
            px.pie(c,values='Advertising_Expenditure',names='Vehicle_Type',title='Total Expenditure Share by Vehicle Type During Recessions'),
            px.bar(u,x='unemployment_rate',y='Automobile_Sales',color='Vehicle_Type',labels={'unemployment_rate':'Unemployment Rate','Automobile_Sales':'Average Automobile Sales'},title='Effect of Unemployment Rate on Vehicle Type and Sales')
        ]
    elif statistics == 'Yearly Statistics' and year not in (None,'Select-year',''):
        year = int(year)
        d = data[data['Year']==year].copy()
        a = data.groupby('Year',as_index=False)['Automobile_Sales'].mean()
        b = d.groupby('Month',as_index=False,observed=True)['Automobile_Sales'].sum().sort_values('Month')
        c = d.groupby('Vehicle_Type',as_index=False)['Automobile_Sales'].mean()
        e = d.groupby('Vehicle_Type',as_index=False)['Advertising_Expenditure'].sum()
        figs = [
            px.line(a,x='Year',y='Automobile_Sales',title='Yearly Automobile Sales Using Line Chart for the Whole Period'),
            px.line(b,x='Month',y='Automobile_Sales',title=f'Total Monthly Automobile Sales in {year}'),
            px.bar(c,x='Vehicle_Type',y='Automobile_Sales',title=f'Average Vehicles Sold by Vehicle Type in {year}'),
            px.pie(e,values='Advertising_Expenditure',names='Vehicle_Type',title='Total Advertisement Expenditure for Each Vehicle')
        ]
    else:
        return html.P('Choose a report type and, for yearly statistics, a year.')
    return [
        html.Div([dcc.Graph(figure=figs[0]),dcc.Graph(figure=figs[1])],style={'display':'flex'}),
        html.Div([dcc.Graph(figure=figs[2]),dcc.Graph(figure=figs[3])],style={'display':'flex'})
    ]

if __name__ == '__main__':
    app.run(debug=False)

