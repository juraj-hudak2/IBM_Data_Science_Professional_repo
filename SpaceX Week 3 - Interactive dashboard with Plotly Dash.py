# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())
launch_sites = spacex_df['Launch Site'].unique()
dropdown_opt = [{'label': 'All Sites', 'value': 'ALL'}]
for x in launch_sites:
    dropdown_opt.append({'label': x, 'value': x})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options = dropdown_opt,
                                    value = 'ALL',
                                    placeholder = "Select a Launch Site",
                                    searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # step = 1000 would make rangeslider display max value as 10000, not observed 9600 
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=100,
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site].groupby('class', as_index = False)['Launch Site'].count()
        fig = px.pie(filtered_df, values='Launch Site', names='class', title='Total Success Launches for Site ' + entered_site)
        return fig

@app.callback(Output(component_id='payload-slider', component_property='marks'),
              Input(component_id='payload-slider', component_property='value'))
def edit_marks(values):
    return {0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000', values[0]: str(values[0]), values[1]: str(values[1])}

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), 
            Input(component_id="payload-slider", component_property="value")])
def update_scatterplot(entered_site, slider_values):
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(slider_values[0], slider_values[1])], x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        fig = px.scatter(spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)'].between(slider_values[0], slider_values[1]))], x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    print([min_payload,max_payload])
    app.run_server()
