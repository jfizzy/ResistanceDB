import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df = pd.read_csv('test.csv')

sample_data = df.iloc[:,6:]

app.layout = html.Div(children=[
    html.H1(children='Pablo',
            style={
            'textAlign': 'center'
            }
    ),
    dcc.Graph(
        id='heatmap',
        figure={
            'data': [
                go.Heatmap(z=sample_data.values.tolist(),
                    x=sample_data.columns.values.tolist(),
                    y=df['compound'].tolist()
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Sample'},
                yaxis={'title': 'rt_diff'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
            )
        }
    )]    
)
'''dcc.Graph(
        id='medMz vs rt_diff',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['compound'] == i]['medMz'],
                    y=df[df['compound'] == i]['rt_diff'],
                    text=df[df['compound'] == i]['compound'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df['compound']
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'medMz'},
                yaxis={'title': 'rt_diff'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),'''

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server(debug=True)