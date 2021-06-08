import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

app = dash.Dash(__name__)

server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

app.layout = html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, 
children=[
    html.H1(
        children='Probability of Having Studied Sufficient Topics',
        style={
            'textAlign': 'center'
            
        }
    ),
    
    html.Div([
        
        html.Div([
            html.Div(["Topics: ",
              dcc.Input(
                  id='topics', 
                  value='15', 
                  type='number')]
                  ),
            html.Div(["Questions: ",
              dcc.Input(
                  id='questions', 
                  value='10', 
                  type='number')]
                  ),
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Div(["Questions to answer: ",
              dcc.Input(
                  id='q2a', 
                  value='1', 
                  type='number')]
                  ),
            html.Div(["Risk: ",
              dcc.Input(
                  id='risk', 
                  value='100', 
                  type='number')]
                  ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ],
    ),

    dcc.Graph(id='indicator-graphic'),

    html.Div(id='t2s')

])

@app.callback(
    #Output('indicator-graphic', 'figure'),
    Output('t2s', 'children'),
    Input('topics', 'value'),
    Input('questions', 'value'),
    Input('q2a', 'value'),
    Input('risk', 'value')    
    )
def return_risk(tops, qs, qtwoa, r):
    tops, qs, qtwoa, r = int(tops), int(qs), int(qtwoa), float(r)/100

    for i in range(0, tops):
        temp_studied = i
        none_prob = 1
        for i in range(0, qs):
            proba = (tops-temp_studied-i)/(tops-i)
            none_prob = none_prob*proba
        if (1 - none_prob) >= r:
            break
    return 'Topics Required to study: {}'.format(temp_studied)

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('topics', 'value'),
    Input('questions', 'value'),
    Input('q2a', 'value'),
    Input('risk', 'value')    
    )
def update_graph(tops, qs, qtwoa, r):
    tops, qs, qtwoa, r = int(tops), int(qs), int(qtwoa), float(r)/100
    
    risks = []
    for i in range(0, tops):
        temp_studied = i
        none_prob = 1
        for i in range(0, qs):
            proba = (tops-temp_studied-i)/(tops-i)
            none_prob = none_prob*proba
        risks.append(1-none_prob)
    #risks=risks.reverse()
    r_df = pd.DataFrame({"risk_level": risks})
    #q_list = [range(0,qs)]

    fig = px.scatter(x=r_df.index,
                     y=r_df["risk_level"], 
                     template="plotly_dark")
                     #hover_data=[q_list,risks])

    #fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title="Topics to Study")

    fig.update_yaxes(title="Risk Level")

    fig.add_hline(y=r, line_color="red")

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)