from dash import Dash, html, dcc, Input, Output, callback, ctx, State, no_update
import dash
import dash_mantine_components as dmc
import os
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import urllib.parse
import plotly.express as px 
import pandas as pd

app = Dash(__name__, suppress_callback_exceptions=True)


data = {
    'Category': ['Cat', 'Cat', 'Cat', 'Dog', 'Dog', 'Dog', 'Fish', 'Fish', 'Fish'],
    'Status': ['Positive', 'Negative', 'Uncategorized', 'Positive', 'Negative', 'Uncategorized', 'Positive', 'Negative', 'Uncategorized'],
    'Count': [7, 1, 2, 3, 5, 6, 10, 11, 12]
}

df = pd.DataFrame(data)

def get_graph():
    cat_data = [7, 1, 2]
    dog_data = [3, 5, 6]
    fish_data = [10, 11, 12]
    categories = ['cat', 'dog', 'fish']
    fig = px.bar(df, x="Category", y="Count", color="Status", title="Long-Form Input")

    fig.update_layout(barmode='stack')

    return fig

def reset_graph():
    return go.Figure()

graph_figure = get_graph()

home_layout = html.Div([
    html.H1('Page 1'),
    dcc.Link('Go to Page 2', href='/page2'),
    html.Br(),
    dcc.Graph(
        id='graph',
        figure=graph_figure,
        clickData=None 
        )
])

@app.callback(
    Output('url', 'pathname'),
    [Input('graph', 'clickData')],
    prevent_initial_call=True
)
def update_url(clickData):
    if clickData:
        info = clickData['points'][0]['label']
        new_url = f"/page2?info={urllib.parse.quote_plus(info)}"
        return new_url
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'), Input('url', 'search')]
)
def display_page(pathname, search):
    if pathname == '/page2':
        if search:
            info = urllib.parse.unquote_plus(search.lstrip('?info='))
            new_layout = html.Div([
                html.H1('Page 2'),
                dcc.Link('Go back to Page 1', href='/page1'),
                html.Br(),
                html.P(f'You clicked on: {info}')
            ])
            return new_layout
        else:
            return html.P('No information provided.')
    else:
        return home_layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
