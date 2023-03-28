import pandas
from pandas_datareader import DataReader
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
from datetime import datetime



dataframe =  pandas.read_csv("Nasdaq.csv")

external_stylesheets = ["style.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

options = []

for element in dataframe.index:

	options.append({"label": dataframe["Name"][element],
			"value": dataframe["Symbol"][element]
			})

app.layout = html.Div([
	html.H1("Stock Ticker Web App"),
	html.Div([
		html.H2("Select a stock:"),
		dcc.Dropdown(
			id="dropdown",
			options = options,
			value = "GOOG",
			multi = True
		)
	]),
	html.Div([
		html.H2(["Select Date"]),
		dcc.DatePickerRange(
			id = "datepicker",
			min_date_allowed = datetime(2017, 1, 1),
			max_date_allowed = datetime.today(),
			start_date = datetime(2020, 1, 1),
			end_date = datetime.today()
		)
	]),
	html.Div([
		html.Button(
			id = "submit-button",
			n_clicks = 0,
			children = "Submit"
			)
	]),
	dcc.Graph(
		id = "stock-graph"
		)
])


@app.callback(Output("stock-graph", "figure"),
		[Input("submit-button", "n_clicks")],
		[State("dropdown", "value"),
		State("datepicker", "start_date"),
		State("datepicker", "end_date")]
		)
def update_graph(number_of_clicks, stocks, start_date, end_date):

	start = datetime.strptime(start_date[:10], "%Y-%m-%d")

	end = datetime.strptime(end_date[:10], "%Y-%m-%d")

	data = []

	for stock in stocks:

		dataframe  = DataReader(stock, "yahoo", start, end)

		dates = []

		for row in range(len(dateframe)):
			new_date = str(dataframe.index[row])

			new_date = new_date[0:10]

			dates.append(new_date)

		dataframe["Date"] = dates

		data.append({
			"x": dataframe["Date"],
			"y": dataframe["Adj Close"],
			"name": stock
		})

	figure = {
		"data": data,
		"layout": {
			"title": "Stock Data",
			"xaxis": {"title": "Date"},
			"yaxis": {"title": "Price"}
		}
	}

	return figure

app.run_server()
