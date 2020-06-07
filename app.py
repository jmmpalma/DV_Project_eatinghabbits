import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

# ------------------------------------
path_dataset = 'https://raw.githubusercontent.com/jmmpalma/DV_Project_eatinghabbits/master/eatinghabbits_averagepercountry.csv'

df_eatinghabits = pd.read_csv(path_dataset, sep=';')

df_eatinghabits.head()

# ----------------------------------
df_country_points = pd.read_csv(
    'https://raw.githubusercontent.com/jmmpalma/DV_Project_eatinghabbits/master/country_points.csv')

df_country_points.columns

# -----------------------------------
import urllib.request, json

with urllib.request.urlopen('https://raw.githubusercontent.com/jmmpalma/DV_Project_eatinghabbits/master/europe.geo.json') as url:
    europe_geo = json.loads(url.read().decode())
for feature in europe_geo['features']:
    feature['id'] = feature['properties']['admin']

# ----------------------------------------
data_choroplethmap = dict(type='choroplethmapbox',
                          geojson=europe_geo,
                          locations=df_eatinghabits['Country'],
                          z=df_eatinghabits['avg_GramsPerDay'],
                          colorscale='inferno',
                          colorbar=dict(title='CO2 Emissions (log scaled)')
                          )

layout_choroplethmap = dict(mapbox=dict(style='white-bg',
                                        layers=[dict(source=feature,
                                                     below='traces',
                                                     type='fill',
                                                     fill=dict(outlinecolor='gray')
                                                     ) for feature in europe_geo['features']]
                                        ),
                            title=dict(text='Eating habits',
                                       x=.5  # Title relative position according to the xaxis, range (0,1)
                                       )
                            )
fig_choropleth = go.Figure(data=data_choroplethmap, layout=layout_choroplethmap)

fig_choropleth.show()

# The App itself

app = dash.Dash(__name__)

server = app.server


app.layout = html.Div(children=[
    html.H1(children='Dashboard teste'),

    html.Div(children='''
        Example of html Container
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig_choropleth
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

# ---------------------------------------
# data_choropleth = dict(type='choropleth',
#                      locations=df_eatinghabits['Country'],
# There are three ways to 'merge' your data with the data pre embedded in the map
#                      locationmode='country names',
#                     z=df_eatinghabits['avg_GramsPerDay'],
#                    text=df_eatinghabits['avg_GramsPerDay'],
#                   colorscale='inferno'
#                  )

# layout_choropleth = dict(geo=dict(scope='world',  # default
#                                 projection=dict(type='orthographic'
#                                                ),
#                                  # showland=True,   # default = True
#                                  landcolor='black',
#                                  lakecolor='white',
#                                  showocean=True,  # default = False
#                                  oceancolor='azure'
#                                  ),
#
#                         title=dict(text='World CO2 Emissions Choropleth Map',
#                                    x=.5  # Title relative position according to the xaxis, range (0,1)
#                                    )
#                         )
#
# fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)
#
# fig_choropleth.show()
