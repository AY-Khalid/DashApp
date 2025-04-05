import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import folium
from folium import plugins
from dash import Dash

data_url = 'https://raw.githubusercontent.com/AY-Khalid/DashApp/refs/heads/main/SampleSuperstore.csv'
            
df_data = pd.read_csv(data_url)

df = df_data.iloc[:, :-3]

latitudes = {
    "Kentucky": 37.6681,
    "California": 36.7783,
    "Florida": 27.9944,
    "North Carolina": 35.6301,
    "Washington": 47.4009,
    "Texas": 31.0545,
    "Wisconsin": 44.2685,
    "Utah": 40.1500,
    "Nebraska": 41.1254,
    "Pennsylvania": 40.5908,
    "Illinois": 40.3495,
    "Minnesota": 45.6945,
    "Michigan": 43.3266,
    "Delaware": 39.3185,
    "Indiana": 39.8494,
    "New York": 42.1657,
    "Arizona": 33.7298,
    "Virginia": 37.7693,
    "Tennessee": 35.7478,
    "Alabama": 32.8067,
    "South Carolina": 33.8569,
    "Oregon": 44.5720,
    "Colorado": 39.0598,
    "Iowa": 42.0115,
    "Ohio": 40.3888,
    "Missouri": 38.4561,
    "Oklahoma": 35.5653,
    "New Mexico": 34.8405,
    "Louisiana": 31.1695,
    "Georgia": 33.0406,
    "Nevada": 38.3135,
    "Mississippi": 32.7416,
    "Arkansas": 34.9697,
    "Montana": 46.9219,
    "Maryland": 39.0639,
    "District of Columbia": 38.8951,
    "Kansas": 38.5266,
    "South Dakota": 44.2998,
    "Idaho": 44.2405,
    "North Dakota": 47.5289,
    "Wyoming": 42.7559,
    "West Virginia": 38.4912
}

longitudes = {
    "Kentucky": -84.6701,
    "California": -119.4179,
    "Florida": -81.7603,
    "North Carolina": -79.8064,
    "Washington": -121.4905,
    "Texas": -97.5635,
    "Wisconsin": -89.6165,
    "Utah": -111.8624,
    "Nebraska": -98.2681,
    "Pennsylvania": -77.2098,
    "Illinois": -88.9861,
    "Minnesota": -93.9002,
    "Michigan": -84.5361,
    "Delaware": -75.5071,
    "Indiana": -86.2583,
    "New York": -74.9481,
    "Arizona": -111.4312,
    "Virginia": -78.1699,
    "Tennessee": -86.6923,
    "Alabama": -86.7911,
    "South Carolina": -80.9450,
    "Oregon": -122.0709,
    "Colorado": -105.3111,
    "Iowa": -93.2105,
    "Ohio": -82.7649,
    "Missouri": -92.2884,
    "Oklahoma": -96.9289,
    "New Mexico": -106.2485,
    "Louisiana": -91.8678,
    "Georgia": -83.6431,
    "Nevada": -117.0554,
    "Mississippi": -89.6787,
    "Arkansas": -92.3731,
    "Montana": -110.4544,
    "Maryland": -76.8021,
    "District of Columbia": -77.0364,
    "Kansas": -96.7265,
    "South Dakota": -99.4388,
    "Idaho": -114.4788,
    "North Dakota": -99.7840,
    "Wyoming": -107.3025,
    "West Virginia": -80.9545
}

df["lat"] = df["State"].map(latitudes)
df["lon"] = df["State"].map(longitudes)

df = df.dropna(subset=["lat", "lon"])

def create_folium_map(df):
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

    for idx, row in df.iterrows():
        state = row['State']
        lat = row['lat']
        lon = row['lon']
        sales = row['Sales']

        radius = (sales / df['Sales'].max()) * 30 + 5  # Normalize the radius based on sales

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            tooltip=f"State: {state}<br>Sales: ${sales}",
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6
        ).add_to(m)

    # Save the map to an HTML file
    map_path = 'interactive_map.html'
    m.save(map_path)
    return map_path

# Generate the folium map and save it as HTML
map_file = create_folium_map(df)

# Initialize the Dash app
app = Dash(__name__)
server = app.server
# Layout of the app
app.layout = html.Div([
    html.H1("Sample SuperStore Sales Analysis Dashboard"),
    html.P("This is a python dashboard application by AY Khalid", style={"font-style": "italic", "font-size":"14px", "color":"grey"}),
    html.Div([

    html.H3(id="total-sales", children="Total Sales: $0.00", style={"flex":1, "alignContent":"center", "color":"grey", "backgroundColor":"white", "padding":"5px", "fontSize":"20px"}),
    html.Div([
        html.P("Select Ship Mode", style={"font-size":"20px","font-style": "italic", "color":"grey", "textAlign": "right"}),
        dcc.Dropdown(
            id="ship-mode-dropdown",
            options=[{"label": mode, "value": mode} for mode in df["Ship Mode"].unique()],
            value=df["Ship Mode"].unique()[0]
            , style={"fontSize":"20px"}
        ),
    ], style={"flex":1, "alignContent":"center", "display":"inline-block"})

    ], style={"display":"flex", "gap":"60px"}),



    html.Div([

        html.Div([
            html.H3("Sales by Product Sub-Categories", style={"opacity":0.5, "textAlign": "left"}),
            html.P("Technological products consistently outperform other categories in sales, with furniture products following closely behind.", style={"opacity":0.5, "textAlign": "left"}),
        dcc.Graph(id="bar-chart")
        ], style="display":"inline-block"),

        html.Div([
                    
        html.Div([
            html.H3("Sales by Segment", style={"opacity":0.5, "textAlign": "left"}),
            html.P("Sales appear to be consistently proportional across all segments, regardless of the ship mode.", style={"opacity":0.5, "textAlign": "left"}),
        dcc.Graph(id="bar-chart2", style={"flex":1, "justifyContent":"center", "alignContent":"center"})
        ], style="display":"inline-block"),

        # Embed the map using Iframe
        html.Div([
            html.H3("Sales by State", style={"opacity":0.5, "textAlign": "left"}),
            html.P("The size of the circles are in proportion to sales value, i.e states with highest sales have a bigger circle.", style={"opacity":0.5, "textAlign": "left"}),
            html.Iframe(
                srcDoc=open(map_file, 'r').read(),
                width="100%",
                height="600px"
            ), ], style={"flex":2, "backgroundColor":"white", "justifyContent":"center", "alignContent":"center"}),


        ], style={"display":"flex", "marginTop":"20px", "marginBottom":"20px", "gap":"20px"}),



    ]),
], style={"textAlign": "center", "padding": "20px", "backgroundColor": "#f1f3f7", "width": "90vw", "margin": "0 auto", "display": "block"})

# Callback for updating graphs based on dropdown selection
@app.callback(
    [Output("bar-chart", "figure"), Output("bar-chart2", "figure"), Output("total-sales", "children")],
    Input("ship-mode-dropdown", "value")
)
def update_charts(selected_ship_mode):
    df_group1 = df.groupby(["Ship Mode", "Sub-Category"])["Sales"].sum().sort_values(ascending=False).reset_index()
    df_group2 = df.groupby(["Ship Mode", "Segment"])["Sales"].sum().reset_index()

    filtered_df3 = df[df["Ship Mode"] == selected_ship_mode]

    filtered_df1 = df_group1[df_group1["Ship Mode"] == selected_ship_mode]
    filtered_df2 = df_group2[df_group2["Ship Mode"] == selected_ship_mode]

    total_sales = filtered_df3["Sales"].sum()

    # Bar chart for Sub-Category sales
    bar_chart = px.bar(filtered_df1, x="Sub-Category", y="Sales")
    bar_chart.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white'
)

    # Bar chart for Segment sales
    bar_chart2 = px.bar(filtered_df2, x="Segment", y="Sales")
    bar_chart2.update_layout(
    paper_bgcolor='white' ,
    plot_bgcolor='white'
)

    return bar_chart, bar_chart2, f"Total Sales: ${total_sales:,.2f}"

if __name__ == "__main__":
    app.run(debug=True)
