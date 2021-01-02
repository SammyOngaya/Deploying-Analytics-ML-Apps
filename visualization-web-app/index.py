from flask import Flask, jsonify,request, Response, render_template
import json
import pandas as pd


import plotly.graph_objs as go
import plotly
# import plotly.offline as plt


app = Flask(__name__)




@app.route("/")
def index():
	return render_template('index.html')

@app.route("/titanic")
def titanic():
	df = pd.read_csv("titanic.csv")
	# Gender Fare group
	df_gender_fare=pd.DataFrame(df.groupby(['Sex'],as_index=False)['Fare'].sum())
	gender_fare_trace = go.Bar(x=df_gender_fare["Sex"], y=df_gender_fare["Fare"])
	gender_fare_layout = go.Layout(title="Gender and Fare", xaxis=dict(title="Sex"),
                       yaxis=dict(title="Fare"), )
	gender_fare_data = [gender_fare_trace]
	gender_fare_fig = go.Figure(data=gender_fare_data, layout=gender_fare_layout)
	gender_fare_fig_json = json.dumps(gender_fare_fig, cls=plotly.utils.PlotlyJSONEncoder)

	# Gender Passenger Count
	df_gender_count=pd.DataFrame(df.groupby(['Sex'],as_index=False)['Fare'].count())
	gender_count_trace = go.Bar(x=df_gender_count["Sex"], y=df_gender_count["Fare"])
	gender_count_layout = go.Layout(title="Gender Count", xaxis=dict(title="Gender"),
                       yaxis=dict(title="No."), )
	gender_count_data = [gender_count_trace]
	gender_count_fig = go.Figure(data=gender_count_data, layout=gender_count_layout)
	gender_count_fig_json = json.dumps(gender_count_fig, cls=plotly.utils.PlotlyJSONEncoder)
	


	return render_template('titanic.html', gender_fare_plot=gender_fare_fig_json, gender_count_plot=gender_count_fig_json)


if __name__ == "__main__":
	app.run(debug=True, port=5001)