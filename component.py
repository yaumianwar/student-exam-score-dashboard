import dash_bootstrap_components as dbc

from dash import html

# create reusable card component
def get_card_component(title, data):
    component = dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H4(title),
                            html.H4(data)
                        ]), 
                        color="dark", 
                        outline=True,
                        className = 'text-dark',
                        style={'textAlign': 'center', 'margin-bottom': '20px'}
                    ),
                )
    return component

def get_student_score_list(scores, counter):

    table_header = [
        html.Thead(
            html.Tr([
                html.Th("No."), 
                html.Th("Math Score"), 
                html.Th("Reading Score"), 
                html.Th("Writing Score"), 
                html.Th("Avg Score"), 
            ])
        )
    ]

    table_rows = []
    for score in scores:
        table_row = html.Tr([
            html.Td(counter), 
            html.Td(score['MathScore']),    
            html.Td(score['ReadingScore']),    
            html.Td(score['WritingScore']),    
            html.Td(score['avg_score']),    
        ])
        table_rows.append(table_row)
        counter += 1


    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3')

    return table