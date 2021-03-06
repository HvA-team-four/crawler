#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utilities.models import *
from honeycomb import *


@db_session
def load_statistics(statistic):
    """This function takes a string as parameter and returns a certain value, which is then displayed in the statistics
    bar on the url-settings page.
    """
    if statistic == 'total':
        return select(p for p in Url).count()

    elif statistic == 'scanned':
        total = select(p for p in Url).count()
        if total != 0:
            scanned = select(p for p in Url if p.date_scanned is not None).count()
            percentage = int(scanned/total*100)
        else:
            percentage = 0

        return '{}%'.format(percentage)

    elif statistic == 'scraped':
        total = select(p for p in Url).count()
        if total != 0:
            scraped = select(p for p in Url if p.date_scraped is not None).count()
            percentage = int(scraped/total*100)
        else:
            percentage = 0
        return '{}%'.format(percentage)


# Creating a dataframe and filling it with one row: No data loaded.
df = pd.DataFrame(columns=['URL',
                           'Date Added',
                           'Date Scan',
                           'Date Scrape',
                           'Priority Scrape',
                           'Priority Scan'])

df = df.append({'URL': 'No data loaded'}, ignore_index=True)

# Defining the lay-out of this page.
layout = html.Div([
    html.H3('URL Settings',
            style={'text-align': 'center'}),

    html.P('''On this page, you are able to add URLs to the database which will automatically receive 
    a priority flag. The statistics are refreshed every 30 seconds.''',
           style={'width': 380,
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  'textAlign': 'center',
                  'marginBottom': 10}),

    html.Div([
        html.Div([
            html.Div(children=load_statistics('total'),
                     id='UrlStatisticsBox1',
                     className='statisticsBox'),
            html.Div(children='Total',
                     className='title'),
            html.Div(children='Amount of URLs in the database',
                     className='description')
        ], className='statisticsWrapper'),

        html.Div([
            html.Div(children=load_statistics('scanned'),
                     className='statisticsBox',
                     id='UrlStatisticsBox2'),
            html.Div(children='Scanned',
                     className='title'),
            html.Div(children='Percentage of scanned URLs',
                     className='description')
        ], className='statisticsWrapper'),

        html.Div([
            html.Div(children=load_statistics('scraped'),
                     className='statisticsBox',
                     id='UrlStatisticsBox3'),
            html.Div(children='Scraped',
                     className='title'),
            html.Div(children='Percentage of scraped URLs',
                     className='description')
        ], className='statisticsWrapper'),

        html.Button('Refresh statistics',
                    id='refresh-url-statistics',
                    className='refresh_button')
    ], className='statisticsRow'),

    html.Button('Load table',
                id='reload-button',
                style={'marginLeft': 20,
                       'float': 'right'}),

    html.Div([
        dcc.Input(id='input-box',
                  type='text',
                  style={'width': 480},
                  placeholder='URL which need to be added to the database.'),
        
        html.Button('Submit',
                    id='urlsubmit',
                    style={'marginLeft': 20}),

        html.Br(),
        html.Br(),

        html.Div(id='output-container-button')
    ]),

    html.Br(),

    html.Div(
        dt.DataTable(
            rows=df.to_dict('records'),
            sortable=True,
            id='url-table')
    ),
])
