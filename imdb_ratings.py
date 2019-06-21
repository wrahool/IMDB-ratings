#!/usr/bin/env python
# coding: utf-8

import imdb as imdb
import pandas as pd
import plotly as py
from plotly import tools
import plotly.graph_objs as go
import math


# if using Jupyter Notebook uncomment the following two lines
# from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
# init_notebook_mode(connected=True)


def get_episodes_ratings(title):
    i1 = imdb.IMDb()
    curr_title = i1.get_movie(title)
    print('Fetching IMDB ratings of every episode of ' + str(curr_title) + '...')

    title_name = curr_title.get('title')
    i1.update(curr_title, 'episodes')

    title_seasons = sorted(curr_title['episodes'].keys())
    season_lengths = [len(curr_title['episodes'][s]) for s in title_seasons]

    ratings_list = []

    episode_no = 1
    for s in title_seasons:
        for e in range(1, season_lengths[s - 1] + 1):
            curr_episode = curr_title['episodes'][s][e]
            d = {
                'title': title_name,
                'episode_no': episode_no,
                'season': s,
                'episode': e,
                'episode_name': curr_episode['title'],
                'episode_rating': curr_episode.get('rating')
            }
            ratings_list.append(d)
            episode_no = episode_no + 1

    rating_df = pd.DataFrame(ratings_list,
                             columns=['title', 'episode_no', 'season', 'episode', 'episode_name', 'episode_rating'])
    rating_df['episode_no'] = [i + 1 for i in rating_df.index]

    return rating_df


show_ids = ['1759761',  # Veep
            '0386676',  # The Office
            '0407362',  # Battlestar Galactica
            '0944947',  # Game of Thrones
            '0903747',  # Breaking Bad
            '1266020',  # Parks and Recreation
            '0108778',  # Friends
            '0367279',  # Arrested Development
            '2467372',  # Brooklyn 99
            '1439629'    # Community
            ]

shows_list = []
for i, show_id in zip(range(len(show_ids)), show_ids):
    shows_list.append(get_episodes_ratings(show_id))

shows_df = pd.DataFrame()
for i in range(len(shows_list)):
    shows_df = shows_df.append(shows_list[i])

shows = [i for i in shows_df.title.unique()]
traces = []
for show in shows:
    show_trace_df = shows_df[shows_df['title'] == show]
    show_trace = go.Scatter(
        x=[i for i in show_trace_df['episode_no']],
        y=[i for i in show_trace_df['episode_rating']],
        name=show,
        text=list(round(show_trace_df["episode_rating"], 1).map(str) +
                  ' (' +
                  'S' + show_trace_df["season"].map(str) +
                  ', E' + show_trace_df["episode"].map(str) +
                  ': ' + show_trace_df["episode_name"].map(str) +
                  ')'),
        hoverinfo='text'
    )
    traces.append(show_trace)

data = [trace for trace in traces]

cols = 2
rows = math.ceil(len(shows) / cols)

fig = tools.make_subplots(rows=rows, cols=cols, subplot_titles=shows)
i = 0
for r in range(rows):
    for c in range(cols):
        if i == len(traces):
            break

        fig.append_trace(traces[i], r + 1, c + 1)
        i = i + 1

for i in range(len(shows)):
    # change the y range for all the subplots to a fixed range
    fig['layout']['yaxis' + str(i + 1)].update(range=[0, 10])

    # change the axes names for all the subplots
    fig['layout']['xaxis' + str(i + 1)].update(title="episode #")
    fig['layout']['yaxis' + str(i + 1)].update(title='IMDB rating')

fig['layout'].update(height=400 * len(shows) / 2,
                     width=900,
                     title='episode ratings for TV show',
                     showlegend=False)

py.offline.plot(fig, filename='IMDB-ratings.html')

# if using Jupyter Notebook use this command instead.
# py.offline.iplot(fig, filename='IMDB-ratings.html')
