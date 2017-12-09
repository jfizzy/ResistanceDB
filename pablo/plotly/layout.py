import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

data_file = '../condensed.csv'

class DataWrapper:
    def __init__(self):
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

    def fetch_data(self, f=data_file):
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
        self.num_samples = None
        self.layout = None
        self.data = None

    def generate_trace(self, compounds, sample_names, sample_matrix):
        self.num_compounds = len(compounds.values.tolist())
        self.num_samples = len(sample_names)

        self.data = [go.Heatmap(z=sample_matrix.T.values.tolist(),
                                x=compounds.values.tolist(),
                            y=sample_names,
                            colorscale='Viridis',
                            )
                    ]

    def generate_layout(self):
        self.layout = go.Layout(
            title='Sample Intensities',
            xaxis=dict(ticks='', nticks=self.num_compounds, ticklen=10),
            yaxis=dict(ticks=''),
            autosize=True,
        )

    def generate_graph(self):
        fig = go.Figure(data=self.data, layout=self.layout)
        py.plot(fig, filename='heatmap.html')

def tbone_main():
    dw = DataWrapper()
    gu = GraphUtil()
    gu.generate_trace(dw.compounds, dw.get_sample_names(), dw.get_sample_matrix())
    gu.generate_layout()
    gu.generate_graph()

if __name__ == '__main__':
    tbone_main()