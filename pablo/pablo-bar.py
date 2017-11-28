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
    
    print(dw._samples.columns[0])
    
    data=[go.Bar(
            x=dw._x_axis.tolist(),
            y=dw._samples.values.tolist()[i]
        ) for i in dw._samples.index
    ]
    
    layout=go.Layout(xaxis=dict(
                        title='Compound',
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        mirror='ticks',
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
                        mirror='ticks',
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
    
    
    
