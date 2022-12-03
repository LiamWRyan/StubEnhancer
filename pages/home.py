import dash
from dash import Dash, Input, Output, dcc, html, callback
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from .shared import generate_navbar

derived_df = pd.read_csv('./derived_data.csv')

dash.register_page(__name__, path='/')

# -------------------------------------------------------------------------------------------------------------


def jobs_happiness_scatterplot():
    layout = go.Layout(
        margin=go.layout.Margin(
            l=100,   # left margin
            r=50,   # right margin
            b=100,   # bottom margin
            t=100    # top margin
        ),
        height=700,
        title_x=0.5,
        title='Average Job Salaries (CAD) Above the Happiness Threshold<br>(at 10th Year Salary) (2005-2014)',
        xaxis_title="Job Order as a Function of Salary (Ascending)",
        yaxis_title="Average Income Ten Years After Graduation (CAD)",
        bargap=0,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
    )

    display_df = derived_df.loc[derived_df['Credential']
                                == 'Overall (All Graduates)']
    display_df = display_df.dropna(axis=0)
    display_df = display_df.sort_values(
        'Average Income Ten Years After Graduation', ascending=True).reset_index()

    fig = px.scatter(
        display_df,
        x=display_df.index,
        y='Average Income Ten Years After Graduation',
    )

    fig.layout = layout

    fig.add_hrect(
        78000, 97000,
        annotation_text='Emotional Well-being', annotation_position='top left',
        annotation=dict(
            font_size=20, font_family='Times New Roman', font_color='white'),
        fillcolor="green", opacity=0.25, line_width=0
    )

    fig.add_hline(
        123000,
        annotation_text='Ideal Income',
        annotation_position='top left',
        annotation=dict(
            font_size=20, font_family='Times New Roman', font_color='white'),
    )

    fig.add_vline(
        int(len(display_df.index) / 2),
        line_width=1,
        line_dash='dash',
        annotation_text='50th Percentile',
        annotation_position='bottom right',
        annotation=dict(
            font_size=20, font_family='Times New Roman', font_color='white'),
    )

    fig.add_vline(
        int(len(display_df.index) * 0.80),
        line_width=1,
        line_dash='dash',
        annotation_text='80th Percentile',
        annotation_position='bottom right',
        annotation=dict(
            font_size=20, font_family='Times New Roman', font_color='white'),
    )

    fig.update_traces(
        hovertemplate='Average Income Ten Years After Graduation: %{y}'
    )

    return dcc.Graph(
        figure=fig
    )

# -------------------------------------------------------------------------------------------------------------


def certification_salaries_barchart():
    layout = go.Layout(
        margin=go.layout.Margin(
            l=150,   # left margin
            r=150,   # right margin
            b=100,   # bottom margin
            t=50    # top margin
        ),
        height=700,
        title_x=0.5,
        title='Mean Incomes by Certification Type',
        xaxis_title="Credential",
        yaxis_title="Mean Income (CAD)",
        bargap=0,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
    )

    figure = go.Figure(
        layout=layout
    )

    dataframe = derived_df.loc[derived_df['Field of Study (CIP code)'].str.contains(
        '00. Total')]
    dataframe = dataframe.loc[dataframe['Credential']
                              != 'Overall (All Graduates)']
    dataframe = dataframe.reset_index()

    # The map of colors for each type of credential
    # NOTE: The credential types will be pulled in the order specified within the list.
    color_map = {
        'Certificate': 'red',
        'Diploma ': 'green',
        'Bachelor\'s degree': 'blue',
        'Professional bachelor\'s degree': 'yellow',
        'Bachelor\'s degree + certificate/diploma': 'grey',
        'Master\'s degree': 'orange',
        'Doctoral Degree': 'teal',
    }

    # Add each bar by certification type
    for certificate_name in color_map:
        # Get the new dataframe for this specific bar (by its credential name)
        bar_df = dataframe[dataframe["Credential"] == certificate_name]

        # Construct the new bar trace
        new_trace = go.Bar(
            x=bar_df["Credential"],
            y=bar_df['Average Income Ten Years After Graduation'],
            text=bar_df['Average Income Ten Years After Graduation'],
            textposition="inside",
            marker=dict(color='#024B7A'),
            marker_line=dict(width=1, color='black'),
            marker_color=color_map[certificate_name],
            width=0.5,
            hovertemplate='<extra></extra><br>Credential: %{x} <br>Average Median Income: %{y}',
            name=certificate_name,
        )

        # Add the new bar trace into the overall figure
        figure.add_traces(new_trace)

    barChart = dcc.Graph(
        figure=figure
    )

    return barChart

# -------------------------------------------------------------------------------------------------------------


def top_vs_bottom_5_barchart():
    layout = go.Layout(
        margin=go.layout.Margin(
            l=150,   # left margin
            r=150,   # right margin
            b=50,   # bottom margin
            t=50    # top margin
        ),
        height=700,
        title_x=0.5,
        title='Top 5 vs Bottom 5 Jobs by 10th Year Salary (CAD)',
        xaxis_title="Top 5 / Bottom 5 Jobs",
        yaxis_title="Mean Income 10 Years After Graduation (CAD)",
        bargap=0,
        uniformtext_minsize=10,
        uniformtext_mode='show',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
    )

    dataframe = derived_df.loc[derived_df['Credential']
                               == 'Overall (All Graduates)']
    dataframe = dataframe.dropna(axis=0)
    dataframe = dataframe.sort_values(
        'Average Income Ten Years After Graduation', ascending=False)

    # Remove the 4 digit code from the start of the FoS string
    dataframe['Field of Study (CIP code)'] = dataframe['Field of Study (CIP code)'].str.replace(
        '[0-9]{2}.[0-9]{2} ', '', regex=True)

    top = dataframe.head(5)
    bottom = dataframe.tail(5)
    dataframe = pd.concat([top, bottom])

    figure = px.bar(
        data_frame=dataframe,
        x='Field of Study (CIP code)',
        y='Average Income Ten Years After Graduation',
        text='Average Income Ten Years After Graduation',
        #color=['Top 5', 'Top 5', 'Top 5', 'Top 5', 'Top 5', 'Bottom 5', 'Bottom 5', 'Bottom 5', 'Bottom 5', 'Bottom 5'],
        # color_discrete_map={
        #    'Top 5': 'pink',
        #    'Bottom 5': 'purple'
        # }
    )

    figure.data[0].marker.color = (
        'pink', 'pink', 'pink', 'pink', 'pink', 'purple', 'purple', 'purple', 'purple', 'purple')

    # Apply the layout described at the top
    figure.layout = layout

    # Manually add a legend to the graph
    figure.update_traces(showlegend=False).add_traces(
        [
            go.Bar(name=m[0], x=[figure.data[0].x[0]],
                   marker_color=m[1], showlegend=True)
            for m in [('Top 5', 'pink'), ('Bottom 5', 'purple')]
        ]
    )

    # Display the text and value as a string inside the bar, with vertical orientation
    figure.update_traces(
        texttemplate='%{x} %{y}',
        textposition=['inside', 'inside', 'inside', 'inside', 'inside',
                      'outside', 'outside', 'outside', 'outside', 'outside'],
        orientation='v',
        textangle=-90,
        hovertemplate='Field of Study: %{x}<br>Average Income Ten Years After Graduation: %{y}',
    )

    # Remove x-axis labels below the graph
    figure.update_xaxes(visible=False, showticklabels=False)

    barChart = dcc.Graph(
        figure=figure
    )

    return barChart

# -------------------------------------------------------------------------------------------------------------


layout = html.Div(className="body", children=[
    generate_navbar(__name__),
    html.Div(className="home-wrapper", children=[
        html.Div(className="home-one", children=[
            html.Div(children="Welcome to Stub Enhancer! We aim to help you enhance your pay "
                     "stub by providing data abstractions based on data from ALIS. "
                     "Our goal is to aid Albertans in their career and education "
                     "decisions.", style={"color": "white", "fontSize":"20px", "padding":"20px"}),
            html.Br(),
            html.Div(children=[
                dcc.Link(html.Button("Get Started!", className="button-start"),
                 href="/salary", refresh=False),
            ], style={"paddingLeft":"20px", "paddingRight":"20px"}),
            html.Br(),
            html.Div(children=[
                "The ideal income, according to a ",
                html.A("study by Purdue University",
                       href='https://www.purdue.edu/newsroom/releases/2018/Q1/money-only-buys-happiness-for-a-certain-amount.html'),
                " is $127K. They also note the emotional wellbeing threshold is 78K-$97K."
            ], style={"color": "white", "fontSize":"20px", "padding":"20px"}
            ),
        ]),
        html.Div(className="home-two", children=[
            dbc.Tabs([
                dbc.Tab(jobs_happiness_scatterplot(),
                        label="Happiness Threshold",
                        active_label_style={"backgroundcolor": "#885fc9"}),
                dbc.Tab(certification_salaries_barchart(),
                        label="Certification",
                        active_label_style={"color": "#885fc9"}),
                dbc.Tab(top_vs_bottom_5_barchart(),
                        label="Top 5 vs Bottom 5",
                        active_label_style={"color": "#885fc9"}),
            ], )
        ]),
    ],),
])
