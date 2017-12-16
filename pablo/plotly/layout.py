import sys
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import os

import numpy as np

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
        sample = self.df.ix[:,6:]
        sample = (sample - sample.mean()) / (sample.max() - sample.min())
        return sample

class GraphUtil:
    def __init__(self):
        self.num_compounds = None
        self.row_height = 40
        self.num_samples = None
        self.layout = None
        self.data = None

    def generate_heatmap_trace(self, compounds, sample_names, sample_matrix):
        self.num_compounds = len(compounds.values.tolist())
        self.num_samples = len(sample_names)

        self.data = [go.Heatmap(z=sample_matrix.values.tolist(),
                                x=sample_names,
                            y=compounds.values.tolist(),
                            colorscale='Viridis',
                            )
                    ]

        self.layout = go.Layout(
            title='Sample Heatmap Comparisons',
            autosize=True,
            xaxis=dict(type='category', categoryarray=sample_names, categoryorder='array', showgrid=True),
            yaxis=dict(type='category', categoryorder='index', categoryarray=compounds.values.tolist(), dtick=1),

            shapes=self.draw_heatmap_shapes(),

            height=self.num_compounds * self.row_height,
        )

    def generate_annotated_heatmap_trace(self, compounds, sample_names, sample_matrix):
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
        self.data = [go.Heatmap(z=z2,
                                x=x,
                                y=y,
                                colorscale='RdBu',
                                text=z,
                                hoverinfo='x+y+text',
                                reversescale=True
                            )
                    ]

        self.layout = go.Layout(
            title='Sample Production/Consumption Comparisons',
            autosize=True,
            xaxis=dict(type='category', categoryarray=sample_names, categoryorder='array', showgrid=True),
            yaxis=dict(type='category', categoryorder='index', categoryarray=compounds.values.tolist(), dtick=1),
            shapes=self.draw_heatmap_shapes(),

            height=self.num_compounds * self.row_height,
        )

    def generate_3dsurface_trace(self, compounds, sample_names, sample_matrix):
        self.num_compounds = len(compounds.values.tolist())
        self.num_samples = len(sample_names)

        min_mz = self.min_value(sample_matrix)
        max_mz = self.max_value(sample_matrix)

        self.data = [
            go.Surface(
                z=sample_matrix.values.tolist(),
                x=sample_names,
                y=compounds.values.tolist(),
                colorscale='Viridis',
            )
        ]

        self.layout = go.Layout(
            scene=dict(
                xaxis=dict(type='category', categoryarray=sample_names, categoryorder='array', dtick=1, title='Sample'),
                yaxis=dict(type='category', categoryorder='index', categoryarray=compounds.values.tolist(), dtick=4, title='Compound ({})'.format(self.num_compounds)),
                zaxis=dict(title='MZ')
            ),
            margin=dict(
            r=20, l=10,
            b=10, t=10
            ),
        )


    @staticmethod
    def max_value(inputlist):
        return max([sublist[-1] for sublist in inputlist])

    @staticmethod
    def min_value(inputlist):
        return min([sublist[-1] for sublist in inputlist])

    def generate_graph(self, filename):
        fig = go.Figure(data=self.data, layout=self.layout)
        py.plot(fig, filename=filename)

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

    def generate_scatter_plot(self, compounds, sample_names, sample_matrix):

        self.data = []
        index = 0
        for sample in sample_matrix.T.values.tolist():
            name = sample_names[index]
            for value in sample:
                self.data.append(
                    go.Scatter(x=compounds.values.tolist(),
                               y=value,
                               mode='markers+lines',
                               opacity=0.7,
                               marker=dict(
                                   size=15,
                                   line=dict(width=0.5, color='white')
                               ),
                               name=name,
                               )
                )
            index = index + 1

        self.data = [
            go.Scatter(x=compounds.values.tolist(),
                       y=sample,
                       mode='markers',
                       opacity=0.7,
                       marker=dict(
                           size=15,
                           line=dict(width=0.5, color='white')
                       ),
                       name=name,
                       ) for sample, name in zip(sample_matrix.T.values.tolist(), sample_names)
            ]

        self.layout=go.Layout(
            title='Sample Compound Intensities',
            showlegend=True,
            xaxis=dict(type='category', categoryarray=compounds.values.tolist(), categoryorder='array', dtick=1, title='Sample'),
            yaxis=dict(type='range', title='MZ'),
        )

def tbone_main(output_file, output_dir, condensed_file=None, condensed_dir=None):
    o_dw = DataWrapper(output_file)

    gu = GraphUtil()
    gu.generate_heatmap_trace(o_dw.compounds, o_dw.get_sample_names(), o_dw.get_sample_matrix())
    gu.generate_graph(os.path.join(output_dir, 'output_heatmap.html'))

    gu.generate_scatter_plot(o_dw.compounds, o_dw.get_sample_names(), o_dw.get_sample_matrix())
    gu.generate_graph(os.path.join(output_dir, 'output_scatterplot.html'))

    gu.generate_3dsurface_trace(o_dw.compounds, o_dw.get_sample_names(), o_dw.get_sample_matrix())
    gu.generate_graph(os.path.join(output_dir, 'output_3dsurface.html'))

    if condensed_file is not None and condensed_dir is not None:
        c_dw = DataWrapper(condensed_file)
        gu = GraphUtil()

        gu.generate_annotated_heatmap_trace(c_dw.compounds, c_dw.get_sample_names(), c_dw.get_sample_matrix())
        gu.generate_graph(os.path.join(condensed_dir, 'condensed_heatmap.html'))

        gu.generate_scatter_plot(c_dw.compounds, c_dw.get_sample_names(), c_dw.get_sample_matrix())
        gu.generate_graph(os.path.join(condensed_dir, 'condensed_scatterplot.html'))

        gu.generate_3dsurface_trace(c_dw.compounds, c_dw.get_sample_names(), c_dw.get_sample_matrix())
        gu.generate_graph(os.path.join(condensed_dir, 'condensed_3dsurface.html'))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        tbone_main(sys.argv[1], os.path.dirname(sys.argv[1]), sys.argv[2], os.path.dirname(sys.argv[2]))
    elif len(sys.argv) == 2:
        tbone_main(sys.argv[1], os.path.dirname(sys.argv[1]))
    else:
        exit(0)
