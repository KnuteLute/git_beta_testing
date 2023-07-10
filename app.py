from dash import Dash, html, dcc, Input, Output, callback, ctx, State, no_update
import dash
import dash_mantine_components as dmc
import os
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


app = Dash(__name__, suppress_callback_exceptions=True)


@callback(
    Output('url', 'pathname'),
    Input('draw', 'n_clicks'),
    Input('reset', 'n_clicks'),
    prevent_initial_call=True
)
def update_graph(button1, button2):
    

    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    # print(triggered_id)
    if triggered_id == 'reset':
         return '/'
    elif triggered_id == 'draw':
         return '/page1'

def get_link():
    return dcc.Link('Home', href='/dedef')


def get_graph():
    
    x_data = [7, 1, 2]
    y_data = [0, 1, 2]
    z_data = [10, 11, 12]
    categories = ['Positive', 'Negative', 'Uncategorized']
    fig = go.Figure(data=[
        go.Bar(name='Positive', x=x_data, y=categories, orientation='h', marker_color='green'),
        go.Bar(name='Negative', x=y_data, y=categories, orientation='h', marker_color='red'),
        go.Bar(name='Uncategorized', x=z_data, y=categories, orientation='h', marker_color='blue')
    ])

    fig.update_layout(barmode='stack')

    return fig


def reset_graph():
    return go.Figure()

graph_figure = get_graph()


home_layout = html.Div([
    html.H1('Page 1'),
    dcc.Link('Home', href='/'),
    html.Br(),
    html.Button('Draw Graph', id='draw'),
    html.Button('Reset Graph', id='reset'),
    dcc.Graph(
        id='graph',
        figure=graph_figure,
        clickData=None 
        ),
   
])



new_layout = html.Div([
    html.H1('Page 1'),
    dcc.Link('Home', href='/'),
    html.Br(),
    
    html.Div(id='link-to-home')
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return new_layout
    else:
        return home_layout
    

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)





