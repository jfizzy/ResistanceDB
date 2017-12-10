import sys
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

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

    def generate_trace(self, compounds, sample_names, sample_matrix):
        self.num_compounds = len(compounds.values.tolist())
        self.num_samples = len(sample_names)

        self.data = [go.Heatmap(z=sample_matrix.values.tolist(),
                                x=sample_names,
                            y=compounds.values.tolist(),
                            colorscale='RdBu',
                            )
                    ]

        self.layout = go.Layout(
            title='Sample Intensities',
            autosize=True,
            xaxis=dict(type='category', categoryarray=sample_names, categoryorder='array', showgrid=True),
            yaxis=dict(type='category', categoryorder='index', categoryarray=compounds.values.tolist(), dtick=1),

            shapes=self.draw_grid_shapes(),

            height=self.num_compounds * self.row_height,
        )

    def generate_graph(self):
        fig = go.Figure(data=self.data, layout=self.layout)
        py.plot(fig, filename='heatmap.html')

    def draw_grid_shapes(self):
        shapes_v = [self.make_vertical_line(x) for x in range(0, self.num_samples+1)[::2]]
        shapes_h = [self.make_horizontal_line(y) for y in range(0, self.num_compounds+1)]
        shapes_v.extend(shapes_h)
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

def tbone_main(output_file, condensed_file=None):
    o_dw = DataWrapper(output_file)

    gu = GraphUtil()
    gu.generate_trace(o_dw.compounds, o_dw.get_sample_names(), o_dw.get_sample_matrix())
    gu.generate_graph()

    if condensed_file is not None:
        c_dw = DataWrapper(condensed_file)
        gu = GraphUtil()
        gu.generate_trace(c_dw.compounds, c_dw.get_sample_names(), c_dw.get_sample_matrix())
        gu.generate_graph()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        tbone_main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        tbone_main(sys.argv[1])
    else:
        exit(0)
