import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


#################################################
# Database Setup

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/Beatport.sqlite"
db = SQLAlchemy(app)

# created a base class reflected from the existing model
Base = automap_base()

# reflect the tables
Base.prepare(db.engine, reflect=True)

# create a reference for the table 
songs_table = Base.classes.tab
#################################################
# Route Setup

@app.route("/")
def index():
  """Return the homepage."""
  return render_template("index.html")

@app.route("/songs")
def songs():
  """Return a list of sample names."""
  unique_songs = db.engine.execute("SELECT DISTINCT(track_title) FROM tab").fetchall()
  # print(unique_songs, "is my unique songs")
  unique_songs = sorted([ song[0] for song in unique_songs])
  return jsonify(unique_songs)
  
  
  # go to the database, select the cols you want
  # where the track_title = song_name
  # return a JSON dataset that plotlyJS can consume for the chart
  # this route, will be called when the dropdown value changes

@app.route('/songs/<track_title>')
def get_song_stats(track_title):

  # create a result object from the track_title specified
  songs_info  = db.engine.execute("""
    SELECT artists, date_pulled, track_title, max(chart_rank) as chart_rank FROM tab
    WHERE track_title = '{}'
    GROUP BY 1,2
    """.format(track_title))

  # songs_info  = db.engine.execute(""" 
  #   SELECT * FROM tab
  #   WHERE track_title = '{}'
  #   """.format(track_title))
  
  # create a 'columns' variable containing the column names
  columns = songs_info.keys()
  
  # retrieved all info for the track specified by 'songs_info'
  song_rows = songs_info.fetchall()
  
  # empty list holding each song object found in database
  days_on_top100 = []

  for row in song_rows:
    days_on_top100.append(
      dict(zip(columns, row))
    )
  
  return jsonify(days_on_top100)
  
  
@app.route("/songs/<track_title>")
def sample_metadata(track_title):
    """Return the MetaData or a given sample."""
    sel = [
        songs_table.artists,
        songs_table.track_title,
        songs_table.release,
        songs_table.date_pulled,
        songs_table.chart_rank,
    ]

    results = db.session.query(*sel).filter(songs_table.track_title == track_title).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["artists"] = result[0]
        sample_metadata["track_title"] = result[1]
        sample_metadata["release"] = result[2]
        sample_metadata["date_pulled"] = result[3]
        sample_metadata["chart_rank"] = result[4]

    print(sample_metadata)
    return jsonify(sample_metadata)


# @app.route("/samples/<sample>")
# # probally going to bu used for piechart data
# # the <sample> here is the same ID as the <sample> at the medadata
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(tab).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)