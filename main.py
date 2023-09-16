import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dash import Dash, html, dcc, callback, Output, Input, dash_table
from component import get_card_component, get_student_score_list
from utils import get_total_page

PAGE_SIZE = 10

# dash_table set up column 
TABLE_COLUMN = [
    {'name': 'id', 'id': 'id'},
    {'name': 'MathScore', 'id': 'MathScore'},
    {'name': 'ReadingScore', 'id': 'ReadingScore'},
    {'name': 'WritingScore', 'id': 'WritingScore'},
    {'name': 'avg_score', 'id': 'avg_score'},
]

# load and process the data
df = pd.read_csv('data/data.csv')

# set average score and row id
df['avg_score'] = round((df['MathScore'] + df['ReadingScore'] + df['WritingScore'])/3, 2)
df['id'] = df.index
avg_math_score = round(df['MathScore'].mean(), 2)
avg_reading_score = round(df['ReadingScore'].mean(), 2)
avg_writing_score = round(df['WritingScore'].mean(), 2)

top_100_scores = df.sort_values(by='avg_score', ascending=False).head(100).to_dict('records')


#initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# create color palette
color_discrete_sequence = ['#0a9396','#94d2bd','#e9d8a6','#ee9b00', '#ca6702', '#bb3e03', '#ae2012']


app.layout = html.Div([
    html.H1(children='Student Exam Scores', style={'textAlign':'center', 'padding-bottom': '20px'}),
    dbc.Row([
        get_card_component('Total Students', '{:,}'.format(len(df.index))),
        get_card_component('Avg Math Score', str(avg_math_score)),
        get_card_component('Avg Writing Score', str(avg_writing_score)),
        get_card_component('Avg Reading Score', str(avg_reading_score)),
        
    ]),
    dbc.Row(
        dbc.Col([
            html.H4("Score Distribution"),
            html.Div(
                dbc.RadioItems(
                    id="score-distribution-radios",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-dark",
                    labelCheckedClassName="active",
                    options=[
                        {'label': 'Math Score', 'value': 'MathScore'},
                        {'label': 'Writing Score', 'value': 'WritingScore'},
                        {'label': 'Reading Score', 'value': 'ReadingScore'},
                    ],
                    value='MathScore',
                ),
                className ="radio-group",
                style = {'margin-top': '20px'}
            ),
            dcc.Graph(figure={}, id="score-distribution-histogram")
        ])
    ),
    dbc.Row([
        html.H4("Each Score Relationship"),
        dbc.Col(
            dcc.Graph(figure=px.scatter(df, x="MathScore", y="WritingScore", color_discrete_sequence=['#94d2bd'])),
        ),
        dbc.Col(
            dcc.Graph(figure=px.scatter(df, x="MathScore", y="ReadingScore", color_discrete_sequence=['#e9d8a6'])),
        ),
        dbc.Col(
            dcc.Graph(figure=px.scatter(df, x="WritingScore", y="ReadingScore", color_discrete_sequence=['#ee9b00'])),
        )
    ]),
    dbc.Row(
        dbc.Col([
            html.H4("Explore Categorical Data"),
            html.Div(
                dbc.RadioItems(
                    id="student-categorical-radios",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-dark",
                    labelCheckedClassName="active",
                    options=[
                        {'label': 'Gender', 'value': 'Gender'},
                        {'label': 'Ethnic Group', 'value': 'EthnicGroup'},
                        {'label': 'Parent Education', 'value': 'ParentEduc'},
                        {'label': 'Parent Marital Status', 'value': 'ParentMaritalStatus'},
                        {'label': 'Test Preparation', 'value': 'TestPrep'},
                        {'label': 'Weekly Study Hours', 'value': 'WklyStudyHours'},
                    ],
                    value='Gender',
                ),
                className ="radio-group",
                style = {'margin-top': '20px'}
            ),
            dcc.Graph(figure={}, id="student-categorical-summary"),
            dbc.Row([
                dbc.Col(dcc.Graph(figure={}, id="student-categorical-math-score-distribution")),
                dbc.Col(dcc.Graph(figure={}, id="student-categorical-writing-score-distribution")),
                dbc.Col(dcc.Graph(figure={}, id="student-categorical-reading-score-distribution")),
            ]),
            dbc.Row(
                [
                    html.H4('Top 100 Scores'),

                    # dash bootstrap table and pagination
                    dbc.Table(id="score-list"),
                    dbc.Pagination(id="pagination", max_value=get_total_page(PAGE_SIZE, 100), fully_expanded=False),
                ]
            )
        ])
    ),
    
], style= {"margin": "50px 50px 50px 50px"})

@callback(
    Output("score-distribution-histogram", "figure"), 
    Input("score-distribution-radios", "value")
)
def update_histogram(value):
    figure=px.histogram(df, x=value, color_discrete_sequence=['#0a9396'])

    return figure

@callback(
    Output("student-categorical-summary", "figure"), 
    Output("student-categorical-math-score-distribution", "figure"), 
    Output("student-categorical-writing-score-distribution", "figure"), 
    Output("student-categorical-reading-score-distribution", "figure"), 
    [Input("student-categorical-radios", "value")]
)
def update_categorical_component(value):
    
    grouped_df = pd.DataFrame({'count' : df.groupby( [value] ).size()}).reset_index()
    
    figure = px.bar(grouped_df, x=value, y='count', color=value, color_discrete_sequence=color_discrete_sequence, title = 'Summary')

    math_score_figure = px.box(df, x=value, y="MathScore", color_discrete_sequence=['#0a9396'], title = 'Math Score Distribution')
    writing_score_figure = px.box(df, x=value, y="WritingScore", color_discrete_sequence=['#ee9b00'], title = 'Writing Score Distribution')
    reading_score_figure = px.box(df, x=value, y="ReadingScore", color_discrete_sequence=['#bb3e03'], title = 'Reading Score Distribution')

    return figure, math_score_figure, writing_score_figure, reading_score_figure

@callback(
    Output('score-list', 'children'),
    Input('pagination', 'active_page'),
)
def update_list_scores(page):

    # convert active_page data to integer and set default value to 1
    int_page = 1 if not page else int(page)
    
    # define filter index range based on active page
    filter_index_1 = (int_page-1) * PAGE_SIZE
    filter_index_2 = (int_page) * PAGE_SIZE

    # get data by filter range based on active page number 
    fitler_scores = top_100_scores[filter_index_1:filter_index_2]

    # load data to dash bootstrap table component
    table = get_student_score_list(fitler_scores, (filter_index_1 + 1))

    return table


if __name__ == '__main__':
    app.run(debug=True)