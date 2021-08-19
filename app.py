import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import globals
from dash.dependencies import Input, Output, State, MATCH, ALL

items_dict = globals.get_items_dict()
items_stack = [[], []]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.DataFrame({
    "Item": ["Armor-Piercing Rounds"],
    "Amount": [0]
})

fig = px.bar(df, x="Item", y="Amount")

divs = []


def get_data(item_stack, item, value):
    relevant = 0
    for i in range(len(items_stack[0])):
        if items_stack[0][i] == item:
            relevant = i
    # relevant = [i for i in items_stack[0] if i == item]
    # for item_type in items_dict:
    #     item_stack[0][item_type] = item_type
    #     item_stack[1][item_type] = value
    item_stack[1][relevant] = value
    return item_stack


for item_type in items_dict:
    divs.append(html.Div([
        html.Label(items_dict[item_type].name),
        dcc.Input(
            id={'type': 'input', 'index': 'input_{}'.format(items_dict[item_type].name)},
            type="number",
            placeholder=0,
            min=0)
    ]))
    items_stack[0].append(items_dict[item_type].name)
    items_stack[1].append(0)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Survivor'),
            dcc.Dropdown(
                options=[
                    {'label': 'Commando', 'value': 'Commando'},
                    {'label': 'Huntress', 'value': 'Huntress'},
                    {'label': 'Bandit', 'value': 'Bandit'},
                    {'label': 'Mul-T', 'value': 'Mult'},
                    {'label': 'Artificer', 'value': 'Artificer'},
                    {'label': 'REX', 'value': 'Rex'},
                    {'label': 'Mercenary', 'value': 'Mercenary'},
                    {'label': 'Engineer', 'value': 'Engineer'},
                    {'label': 'Acrid', 'value': 'Acrid'},
                    {'label': 'Loader', 'value': 'Loader'},
                    {'label': 'Captain', 'value': 'Captain'}
                ],
                value='Commando',
                clearable=False
            ),
            html.H3('Loadout'),
            html.Div(children=divs,
                     style={"maxHeight": "700px", "overflow": "scroll"})
        ], className="two columns"),
        html.Div([
            html.H1('Properties'),
            html.Div('Luck, Base Damage, Crit Chance, Attack Speed, Armor, Regen, Speed, Jumps, Health'),
            dcc.Graph(
                id='item-graph',
                figure={
                    'layout': {
                        'height': 800
                    }
                }
            ),
            html.Div(children=[],
                     id='id_output')
        ], className="ten columns")
    ])
])


@app.callback(
    Output('item-graph', 'figure'),
    Input({'type': 'input', 'index': ALL}, 'value'),
)
def update_graph(values):
    ctx = dash.callback_context

    if not ctx.triggered:
        id = 'No clicks yet'
        value = 0
    else:
        id = ctx.triggered[0]['prop_id'].split('.')[0].split(',')[0].split('_')[1].replace('"', '')
        value = ctx.triggered[0]['value']

    global items_stack
    items_stack = get_data(items_stack, id, value)
    [item, stack_size] = items_stack
    df = pd.DataFrame({
        "Item": item,
        "Amount": stack_size
    })
    fig = px.bar(df, x=item, y=stack_size)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
