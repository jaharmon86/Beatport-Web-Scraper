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
  unique_songs = [ song[0] for song in unique_songs]
  return jsonify(unique_songs)
  
  
  # go to the database, select the cols you want
  # where the track_title = song_name
  # return a JSON dataset that plotlyJS can consume for the chart
  # this route, will be called when the dropdown value changes

@app.route('/songs/<track_title>')
def get_song_stats(track_title):

  # create a result object from the track_title specified
  songs_info  = db.engine.execute("""
    SELECT * FROM tab
    WHERE track_title = '{}'
    """.format(track_title))  
  
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
  # songs_data = {}
  
  # for song in songs_info:
  #   songs_data['artist'] = song[0]
  #   songs_data['track_title'] = song[2]
  #   songs_data['release'] = song[3]
  #   songs_data['date pulled'] = song[4]
  #   songs_data['chart rank'] = song[5]
  
  
  
  # print(songs_data)
  
  # return jsonify(songs_data)
  


# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData or a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
#         Samples_Metadata.WFREQ,
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # # Create a dictionary entry for each row of metadata information
    # sample_metadata = {}
    # for result in results:
    #     sample_metadata["sample"] = result[0]
    #     sample_metadata["ETHNICITY"] = result[1]
    #     sample_metadata["GENDER"] = result[2]
    #     sample_metadata["AGE"] = result[3]
    #     sample_metadata["LOCATION"] = result[4]
    #     sample_metadata["BBTYPE"] = result[5]
    #     sample_metadata["WFREQ"] = result[6]

    # print(sample_metadata)
    # return jsonify(sample_metadata)


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