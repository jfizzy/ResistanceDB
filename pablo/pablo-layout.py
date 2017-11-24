# standard library
import os

# flask
import flask
from flask import send_from_directory

# dash libs
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import plotly.graph_objs as go

# pydata stack
import pandas as pd
#from sqlalchemy import create_engine

# set params
data_file = 'test.csv'

# dash stylesheet
stylesheet = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

###########################
# Data Manipulation / Model
###########################

class DataWrapper:
    def __init__(self):
        self.df = self.fetch_data(data_file)
        self.compounds = self.get_compounds(self.df)
        self.sample_matrix = self.get_sample_matrix(self.df)

    def get_compounds_list(self):
        '''returns the compounds attribute contents as a list'''
        return self.compounds.tolist()

    def get_sample_names(self):
        '''returns the sample names as a list'''
        return self.df.columns.get_values().tolist()[6:]

    def get_sample_lists(self):
        '''returns the samples as a list of lists'''
        return self.sample_matrix.values.tolist()

    def fetch_data(self, f):
        df = pd.read_csv(f)
        return df

    def get_compounds(self, df):
        '''returns the compounds that are listed in the data file'''
        return df['compound']

    def get_sample_matrix(self, df):
        return df.ix[:,6:]

def draw_sample_graph(sample):
    pass

#########################
# Dashboard Layout / View
#########################

def generate_table(df, max_rows=10):
    '''Given dataframe, return template generated using Dash components
    '''

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +

        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for  i in range(min(len(df), max_rows))]
    )

def onLoad_sample_options(dw):
    '''Actions to perform upon initial page load'''
    sample_options = (
        [{'label': sample, 'value': index}
         for index,sample in enumerate(dw.get_sample_names())]
    )
    return sample_options

# Set up Dashboard and create layout
app = dash.Dash()

# allow stylesheet serving
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# parse the data file
dw = DataWrapper()

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
            dcc.Graph(id='comparison-graph'),
        ])
    ], className='twelve columns'),

    # Dropdown Grid
    html.Div([
        html.Div([
            # Select Sample Dropdown
            html.Div([
                html.Div('Sample', className='three columns'),
                html.Div(dcc.Dropdown(
                    id='sample-selector',
                    options=onLoad_sample_options(dw)),
                    className='nine columns')
            ]),
        ], className='six columns'),

        # Sample Summary
        html.Div([

            # Sample Graph
            dcc.Graph(id='sample-graph')
        ], className='six columns'),

    # Table Grid
    html.Div([
        # Sample Table
        html.Table(

        )
    ], className='tewlve columns')

    ], className='twelve columns'),
])

# serve custom stylesheets
@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


#############################################
# Interaction Between Components / Controller
#############################################

# Template
#@app.callback(
    #Output(component_id='selector-id', component_property='figure'),
    #[
    #    Input(component_id='input-selector-id', component_property='value')
    #]
#)
def ctrl_func(input_selection):
    return None


# start Flask server
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='0.0.0.0',
        port=8050
)
