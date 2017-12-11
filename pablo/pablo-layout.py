# standard library
import os

# flask
import sys
from flask import send_from_directory

# dash libs
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# pydata stack
import pandas as pd
#from sqlalchemy import create_engine

# dash stylesheet
stylesheet = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

###########################
# Data Manipulation / Model
###########################

class DataWrapper:
    def __init__(self, data_file):
        self.df = self.fetch_data(data_file)
        self.compounds = self.get_compounds()
        self.sample_matrix = abs(self.get_sample_matrix())

    def get_compounds_list(self):
        '''returns the compounds attribute contents as a list'''
        return self.compounds.tolist()

    def get_sample_names(self):
        '''returns the sample names as a list'''
        columns = self.df.columns.tolist()
        return columns[6:]

    def get_sample_lists(self):
        '''returns the samples as a list of lists'''
        return self.sample_matrix.values.tolist()

    def fetch_data(self, f):
        df = pd.read_csv(f, sep='\t|,', lineterminator='\n', header=0, error_bad_lines=False, engine='python')
        return df

    def get_compounds(self):
        '''returns the compounds that are listed in the data file'''
        return self.df['compound']

    def get_sample_matrix(self):
        return self.df.ix[:,6:]

class GraphUtil:

    def __init__(self):
        self.num_compounds = None
        self.row_height = 40
        self.num_samples = None
        self.layout = None
        self.data = None

    def draw_sample_graph(self, compounds, sample_names, sample_matrix, index=0):
        title = sample_names[index]
        sample_data = sample_matrix[index]

        figure = go.Figure(
            data=[
                go.Scatter(
                    x=compounds,
                    y=sample_data,
                    mode='markers',
                    opacity=0.7,
                    marker=dict(
                        size=15,
                        line=dict(width=0.5, color='white')
                    ),
                    name=title
                )
            ],
            layout=go.Layout(
                title='Sample Compound Intensities - {}'.format(title),
                showlegend=False
            )
        )

        return figure

    def draw_scatter_plot(self, compounds, sample_names, sample_matrix):
        title = 'Compound Intensities'

        figure = go.Figure(
            data=[
                go.Scatter(x=compounds,
                           y=sample,
                           text=name,
                           mode='markers',
                           opacity=0.7,
                           marker=dict(
                               size=15,
                               line=dict(width=0.5, color='white')
                           ),
                           name=name,
                ) for sample, name in zip(sample_matrix, sample_names)
            ],
            layout=go.Layout(
                title='Sample Compound Intensities',
                showlegend=True,
                margin=dict(
                    l=120,
                    r=120,
                    t=100,
                    b=80,
                    pad=0,
                    autoexpand=True
                ),
                xaxis=dict(
                    type='category',
                    visible=True,
                    autorange=True,
                    range=[compounds[0], compounds[len(compounds)-1]],
                    categoryorder='trace',
                    color='#444',
                    title='Compound',
                    tickvals=compounds,
                    ticktext=compounds,
                    nticks=len(compounds),
                    showticklabels=True,
                    tickfont=dict(
                        family='\"Open Sans\", verdana, arial, sans-serif',
                        size=12,
                        color='#444'
                    ),
                    tickangle=90,
                    gridwidth=1,
                    showgrid=True,
                    anchor='y',
                    side='bottom',
                    layer='above traces',
                    constrain='range',
                    constraintoward='center',
                ),
                yaxis=dict(

                )
            )
        )

        return figure

    def draw_heatmap(self, compounds, sample_names, sample_matrix):
        self.num_compounds = len(compounds.values.tolist())
        self.num_samples = len(sample_names)
        figure = go.Figure([
            go.Heatmap(z=sample_matrix.values.tolist(),
                                x=sample_names,
                                y=compounds.values.tolist(),
                                colorscale='Viridis',
                                ),
            go.Layout(
            title='Sample Intensities',
            autosize=True,
            xaxis=dict(type='category', categoryarray=sample_names, categoryorder='array', showgrid=True),
            yaxis=dict(type='category', categoryorder='index', categoryarray=compounds.values.tolist(), dtick=1),

            shapes=self.draw_heatmap_shapes(),

            height=self.num_compounds * self.row_height,
            )
        ])

        return figure

    def draw_generalized_heatmap(self, compounds, sample_names, sample_matrix):
        self.num_compounds = len(compounds.values.tolist())
        self.num_samples = len(sample_names)

        z = sample_matrix.values.tolist()
        x = sample_names
        y = compounds.values.tolist()
        z2 = []
        for s in z:
            items=[]
            for item in s:
                if item > 0:
                    items.append(1)
                elif item < 0:
                    items.append(-1)
                else:
                    items.append(0)
            z2.append(items)

        figure = go.Figure([
            go.Heatmap(z=z2,
                x=x,
                y=y,
                colorscale='RdBu',
                text=z,
                hoverinfo='x+y+text',
                reversescale=True
            ),
            go.Layout(
                title='Sample Compound Intensities',
                autosize=True,
                xaxis=dict(type='category', categoryarray=sample_names, categoryorder='array', showgrid=True),
                yaxis=dict(type='category', categoryorder='index', categoryarray=compounds.values.tolist(), dtick=1),
                shapes=self.draw_heatmap_shapes(),

                height=self.num_compounds * self.row_height,
            )
        ])

        return figure

    def draw_3D_surface(self, compounds, sample_names, sample_matrix):
        self.num_compounds = len(compounds.values.tolist())
        self.num_samples = len(sample_names)

        min_mz = self.min_value(sample_matrix)
        max_mz = self.max_value(sample_matrix)

        figure = go.Figure([
            go.Surface(
                z=sample_matrix.values.tolist(),
                x=sample_names,
                y=compounds.values.tolist(),
                colorscale='Viridis',
            ),
            go.Layout(
            scene=dict(
                xaxis=dict(type='category', categoryarray=sample_names, categoryorder='array', dtick=1, title='Sample'),
                yaxis=dict(type='category', categoryorder='index', categoryarray=compounds.values.tolist(), dtick=1, title='Compound ({})'.format(self.num_compounds)),
                zaxis=dict(title='MZ')
            ),
            margin=dict(
            r=20, l=10,
            b=10, t=10)
            )
        ])

        return figure


    @staticmethod
    def max_value(inputlist):
        return max([sublist[-1] for sublist in inputlist])

    @staticmethod
    def min_value(inputlist):
        return min([sublist[-1] for sublist in inputlist])

    def draw_heatmap_shapes(self):
        shapes_v = [self.make_vertical_line(x) for x in range(0, self.num_samples+1)[::2]]
        seps_v = [self.make_seperator_line(x) for x in range(1, self.num_samples)[::2]]
        shapes_h = [self.make_horizontal_line(y) for y in range(0, self.num_compounds+1)]
        shapes_v.extend(shapes_h)
        shapes_v.extend(seps_v)
        return shapes_v

    def make_vertical_line(self, x):
        return dict({'type': 'line',
              'x0': x-0.5,
              'y0': -0.5,
              'x1': x-0.5,
              'y1': self.num_compounds-0.5,
              'line': {
                'color': 'black',
                'width': 2,
            }})

    def make_seperator_line(self, x):
        return dict({'type': 'line',
              'x0': x-0.5,
              'y0': -0.5,
              'x1': x-0.5,
              'y1': self.num_compounds-0.5,
              'line': {
                'color': 'dark grey',
                'width': 2,
                'dash': 'dashdot'
            }})

    def make_horizontal_line(self, y):
        return dict({
            'type': 'line',
            'x0': -0.5,
            'y0': y-0.5,
            'x1': self.num_samples-0.5,
            'y1': y-0.5,
            'line': {
                'color': 'black',
                'width': 2,
            },
        })
#########################
# Dashboard Layout / View
#########################

# Set up Dashboard and create layout
app = dash.Dash()

# allow stylesheet serving
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# serve custom stylesheets
@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


#############################################
# Interaction Between Components / Controller
#############################################

def dash_main(output_file, condensed_file=None):
    o_dw = DataWrapper(output_file)

    gu = GraphUtil()
    gu.draw_heatmap(o_dw.compounds, o_dw.get_sample_names(), o_dw.get_sample_matrix())

    if condensed_file is not None:
        c_dw = DataWrapper(condensed_file)
        gu = GraphUtil()
        gu.draw_3D_surface(c_dw.compounds, c_dw.get_sample_names(), c_dw.get_sample_matrix())

        gu.draw_generalized_heatmap(c_dw.compounds, c_dw.get_sample_names(), c_dw.get_sample_matrix())

    # set up the page layout
    app.layout = html.Div([

        # Default Styles
        html.Link(
            rel='stylesheet',
            href=stylesheet
        ),

        # Custom Styles
        html.Link(
            rel='stylesheet',
            href='/static/style.css'
        ),

        # Page Header
        html.Div([
            html.H1(children='Mass Spec Sample Viewer',
                    style={
                        'textAlign': 'center'
                    })
        ]),

        # Comparison Grid
        html.Div([
            html.Div([
                dcc.Graph(id='comparison-graph',
                          figure=gu.draw_scatter_plot(o_dw.get_compounds(), o_dw.get_sample_names(), o_dw.get_sample_matrix())
                          ),
            ])
        ], className='twelve columns'),
    ])

    app.run_server(
        debug=True,
        host='0.0.0.0',
        port=8050
    )

# start Flask server
if __name__ == '__main__':
    if len(sys.argv) == 3:
        dash_main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        dash_main(sys.argv[1])
    else:
        exit(0)
