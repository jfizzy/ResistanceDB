import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import plotly.figure_factory as ff

import pandas as pd
        
class DataWrapper:
    def __init__(self):
        self._df = pd.read_csv('test.csv')
        self._x_axis = self._df['compound']
        self._samples = self._df.iloc[:,6:]
        
def main():
    dw = DataWrapper()
    app = dash.Dash()
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),
    
        html.Div(children='''
            Dash: A web application framework for Python.'''
        ),
    
        dcc.Graph(
            id='line-plot',
            figure={
                'data': [
                    go.Scatter(
                        x=dw._x_axis.tolist(),
                        y=dw._samples.values.tolist()[i],
                        text=dw._df[dw._df['rt_diff'] == i]['rt_diff'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=dw._samples.values.tolist()[i][0]
                    ) for i in dw._samples.index
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Compound', 'autorange': True},
                    yaxis={'title': 'Intensity', 'autorange': True},
                    margin={'l': 5, 'b': 10, 't': 10, 'r': 5},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest',
                    width=1600  
                )
            }
        ),
        
        html.Div(children=[
            html.H4(children='Table with the Data'),
            generate_table(dw._samples)
        ])
    ])
        
    app.run_server(debug=True)
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    
def generate_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +

        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(len(df))]
    )
    
if __name__ == '__main__':
    main()
    
    
    
