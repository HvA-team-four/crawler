#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utilities.models import *
from honeycomb import *


@db_session
def load_statistics(statistic):
    """This function takes a string as parameter and returns a certain value, which is then displayed in the statistics
    bar on the keyword settings page.
    """
    if statistic == 'total':
        return select(p for p in Keyword).count()

    elif statistic == 'active':
        total = select(p for p in Keyword).count()
        if total != 0:
            active = select(p for p in Keyword if p.active).count()
            percentage = int(active/total*100)
        else:
            percentage = 0
        return '{}%'.format(percentage)

    elif statistic == 'matches':
        count_query = db.select('select count(*) from content_keyword')
        for number in count_query:
            return number


# Creating a dataframe and filling it with one row: No data loaded.
df = pd.DataFrame(columns=['Keyword',
                           'Status'])

df = df.append({'Keyword': 'No data loaded'}, ignore_index=True)

# Defining the lay-out of this page.
layout = html.Div([
    html.H3('Keyword Settings',
            style={'text-align': 'center'}),

    html.P('''On this page, you are able to add Keywords to the database and enable/disable certain keywords.
           The statistics are refreshed every 30 seconds.''',
           style={'width': 380,
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  'textAlign': 'center',
                  'marginBottom': 10}),

    html.Div([
        html.Div([
            html.Div(children=load_statistics('total'),
                     id='KeywordStatisticsBox1',
                     className='statisticsBox'),
            html.Div(children='Total',
                     className='title'),
            html.Div(children='Amount of keywords in the database',
                     className='description')
        ], className='statisticsWrapper'),

        html.Div([
            html.Div(children=load_statistics('active'),
                     className='statisticsBox',
                     id='KeywordStatisticsBox2'),
            html.Div(children='Active',
                     className='title'),
            html.Div(children='Percentage of active keywords',
                     className='description')
        ], className='statisticsWrapper'),

        html.Div([
            html.Div(children=load_statistics('matches'),
                     className='statisticsBox',
                     id='KeywordStatisticsBox3'),
            html.Div(children='Matches',
                     className='title'),
            html.Div(children='Amount of keyword matches in the database',
                     className='description')
        ], className='statisticsWrapper'),

        html.Button('Refresh statistics',
                    id='refresh-keyword-statistics',
                    className='refresh_button')
    ], className='statisticsRow'),

    html.Button('Load table',
                id='reload-button',
                style={'marginLeft': 20,
                       'float': 'right'}),

    html.Div([
        dcc.Input(id='keyword-input-box',
                  type='text',
                  style={'width': 480},
                  placeholder='Keyword which need to be added to the database.'),

        html.Button('Submit',
                    id='keywordsubmit',
                    style={'marginLeft': 20}),

        html.Br(),
        html.Br(),

        html.Div(id='output-container-keyword')
    ]),

    html.Br(),

    html.Div(
        dt.DataTable(
            rows=df.to_dict('records'),
            sortable=True,
            row_selectable=True,
            filterable=True,
            selected_row_indices=[],
            id='keyword-table')
    ),

    html.Button('Set active',
                id='keyword_set_active',
                style={'marginTop': 20,
                       'float': 'left'}),

    html.Div(id='activate_warning'),

    html.Button('Set inactive',
                id='keyword_set_inactive',
                style={'marginTop': 20,
                       'marginLeft': 20,
                       'float': 'left'}),

    html.Div(id='inactivate_warning')
], style={'paddingBottom': 55})
