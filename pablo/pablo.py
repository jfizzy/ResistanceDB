import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
    
    data=[go.Scatter(
            x=dw._x_axis.tolist(),
            y=dw._samples.iloc[i].tolist(),
            text=dw._df[dw._df['rt_diff'] == i]['rt_diff'],
            mode='markers',
            opacity=0.7,
            marker=dict(
                size=15,
                line=dict(width=0.5, color='white')
            ),
            name=dw._samples.values.tolist()[i][0]
        ) for i in dw._samples.index
    ]
    
    layout=go.Layout(xaxis=dict(
                        title='Compound',
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        showticklabels=True,
                        gridcolor='#bdbdbd',
                        gridwidth=0.5,
                        zerolinecolor='#969696',
                        zerolinewidth=4,
                        linecolor='#636363',
                        linewidth=6
                    ),
                    yaxis=dict(
                        title='Intensity',
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        gridcolor='#bdbdbd',
                        gridwidth=2,
                        zerolinecolor='#969696',
                        zerolinewidth=4,
                        linecolor='#636363',
                        linewidth=6
                    ),
                    margin=dict(
                        l=5,
                        b=10,
                        t=10,
                        r=5
                    ),
                    legend=dict(
                        x=1,
                        y=0
                    ),
                    hovermode='closest',
                    barmode='group',
                    height=800,
                    width=1600
                    )
    
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),
    
        dcc.Graph(
            id='line-plot',
            figure=go.Figure(data=data, layout=layout)
        ),
        
        html.Div([
            dcc.Input(id='my-id', value='something', type="text"),
            html.Div(id='my-div')
        ]),
        
        html.Div(children=[
            html.H4(children='Table with the Data'),
            generate_table(dw._samples)
        ])
    ])
    
    
        
    app.run_server(debug=True)
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    
    @app.callback(
        Output(component_id='my-div', component_property='children'),[Input(component_id='my-id', component_property='value')]
    )

    def update_output_div(input_value):
        return 'You\'ve entered "{}"'.format(input_value)

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
    
    
    
