import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the dataset
data_path = '/mnt/data/numberofinternetusers new.csv'
data = pd.read_csv(data_path)

# Dashboard setup
app = dash.Dash(__name__)

# Prepare the visualizations
# 1. World Map
latest_year = data['Year'].max()
map_data = data[data['Year'] == latest_year]
map_fig = px.choropleth(map_data,
                        locations="Code",
                        color="Number of Internet users",
                        hover_name="Entity",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title=f"Number of Internet Users in {latest_year}")

# 2. Histogram
hist_fig = px.histogram(data, x="Number of Internet users", title="Distribution of Internet Users Worldwide")

# 3. Time Series
selected_country = 'United States'
time_series_data = data[data['Entity'] == selected_country]
line_fig = px.line(time_series_data, x='Year', y='Number of Internet users', title=f'Internet Users Over Time in {selected_country}')

# 4. Scatterplot
scatter_data = data[data['Year'].isin([1990, latest_year])]
scatter_fig = px.scatter(scatter_data, x='Year', y='Number of Internet users', color='Entity', title='Change in Internet Users from 1990 to Latest Year')

# 5. Barplot
top_countries_data = map_data.nlargest(5, 'Number of Internet users')
bar_fig = px.bar(top_countries_data, x='Entity', y='Number of Internet users', title='Top 5 Countries with the Most Internet Users')

# App layout
app.layout = html.Div(children=[
    html.H1(children='Internet Users Dashboard'),
    html.Div(children='''Geospatial and statistical analysis of internet users.'''),
    dcc.Graph(id='map-graph', figure=map_fig),
    dcc.Graph(id='histogram-graph', figure=hist_fig),
    dcc.Graph(id='line-graph', figure=line_fig),
    dcc.Graph(id='scatter-graph', figure=scatter_fig),
    dcc.Graph(id='bar-graph', figure=bar_fig)
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
