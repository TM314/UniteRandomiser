from dash import Dash, html, dcc, callback, Output, Input, dash_table
import random
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.SOLAR])

def load_data():
    mons = np.genfromtxt("mons.txt", delimiter=",", dtype="str", skip_header=1)
    battle_items = np.genfromtxt("battle_items.txt", delimiter=",", dtype="str", skip_header=1)
    held_items = np.genfromtxt("held_items.txt", delimiter=",", dtype="str", skip_header=1)
    return(mons, battle_items, held_items)

def randomise(mons, battle_items, held_items, team_size=1):
    res = []
    counter = 0

    while counter < team_size:
        # print(counter)
        selection = []

        mon_num = random.randint(0,len(mons)-1)
        mon = mons[mon_num]


        # print(selection)

        if mon[0] == "mew":
            selection.append(str(mon[0]))
            # print("MEW")
            moveset1_nums = np.random.permutation(3)
            moveset2_nums = np.random.permutation(3)
            temp = []
            for i in zip(moveset1_nums, moveset2_nums):
                temp.append(str((mon[2].split("/")[i[0]], mon[4].split("/")[i[1]])))
            selection.append(str(temp))

            can_crit = ["no/no/no"]
        elif mon[0] == "Scyther/Scizor":
            # print('SCYTHER/SCIZOR')
            moveset_flip1 = random.randint(0,1)
            moveset_flip2 = random.randint(0,1)

            # print(mon[0].split("/"))
            selection.append(str(mon[0].split("/")[moveset_flip1]))

            move1 = mon[2].split("/")[moveset_flip1]
            move2 = mon[4].split("/")[moveset_flip2]

            selection.append(str(move1))
            selection.append(str(move2))

            can_crit = []
            can_crit.append(str(mon[3].split("/")[moveset_flip1]+"/"+mon[5].split("/")[moveset_flip2]))
        else:
            selection.append(str(str(mon[0])))

            moveset_flip1 = random.randint(0,1)
            moveset_flip2 = random.randint(0,1)

            move1 = mon[2].split("/")[moveset_flip1]
            move2 = mon[4].split("/")[moveset_flip2]

            selection.append(str(move1))
            selection.append(str(move2))

            can_crit = []
            can_crit.append(str(mon[3].split("/")[moveset_flip1]+"/"+mon[5].split("/")[moveset_flip2]))


        if mon[1] == "physical":
            phys_spec = 0
        else:
            phys_spec = 1

        possible_held_items = []

        for row in held_items:
            if row[1].split("/")[phys_spec] == "yes":
                if row[0] == "scope_lens":
                    if "yes" in can_crit[0] or mon[-1] == "yes":
                        possible_held_items.append(str(row[0]))
                    else:
                        None
                else:
                    possible_held_items.append(str(row[0]))

        # print(possible_held_items)

        held_item_nums = [random.randint(0,len(possible_held_items)-1)]
        # print(possible_held_items[held_item_nums[-1]])
        while len(held_item_nums) < 3:
            temp = random.randint(0,len(possible_held_items)-1)
            if temp in held_item_nums:
                None
            else:
                held_item_nums.append(temp)
            # print(possible_held_items[held_item_nums[-1]])


        # print(held_item_nums)

        for i in held_item_nums:
            selection.append(str(possible_held_items[i]))

        # print(selection)

        selection.append(str(battle_items[random.randint(0,len(battle_items)-1)]))

        res.append(selection)
        # print(selection)
        # print(mons[:,0])
        mons = np.delete(mons, mon_num, axis=0)
        # print(mons[:,0])
        counter += 1

    lanes = np.random.permutation(["Jungler","Top","Top","Bot","Bot"])
    if team_size == 5:
        for i in range(len(res)):
            res[i].append(str(lanes[i]))

    return(res)

app.layout = [
    html.H1(
        'Pokemon Unite Randomiser', style={'textAlign': 'center'}
        ),
    html.Div([
    dcc.Slider(1, 5, 1, value=5, id='slider', 
        marks=None,
        # title='Number of Pokemon to randomise',
        tooltip={
        "always_visible": True,
        "style": {"color": "LightSteelBlue", "fontSize": "20px"},
    }),
    html.Button('RANDOMISE', id='button', n_clicks=0),
    ], style={"width": '25%', 'display': 'inline-block', 'margin-left': '20px'}
    ),
    dash_table.DataTable(
        id='random_table',
        # df.to_dict('records'),
        # [{'name': i, 'id': i} for i in df.columns],
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': 'rgb(150, 150, 150)',
            'color': 'black',
            'fontWeight': 'bold'
        },
        style_data_conditional=
        [{
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(220, 220, 220)',
        'color': 'black'
        },
        {
        'if': {'row_index': 'even'},
        # 'backgroundColor': 'rgb(220, 220, 220)',
        'color': 'black'
        }]
        )
]

@callback(
    Output('random_table', 'data'),
    Output('random_table', 'columns'),
    Input('slider', 'value'),
    Input('button', 'n_clicks'),
    prevent_initial_call=True
)
def generate_table(nmons, n_clicks):
# def generate_table(n_clicks):
    if n_clicks > 0:
        mons, battle_items, held_items = load_data()
        team = randomise(mons, battle_items, held_items, nmons)
        if nmons == 5:
            df = pd.DataFrame(team, columns=['Pokemon', 'Move 1', 'Move 2', 'Held Item 1', 'Held Item 2', 'Held Item 3', 'Battle Item', 'Lane'])
        else:
            df = pd.DataFrame(team, columns=['Pokemon', 'Move 1', 'Move 2', 'Held Item 1', 'Held Item 2', 'Held Item 3', 'Battle Item'])
        
        return(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns])
    else:
        return([], [])

if __name__ == '__main__':
    app.run(debug=True)