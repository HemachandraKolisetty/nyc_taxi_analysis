from flask import Flask, request, jsonify
import numpy as np
from inference import run_login  # Do not change inference.py

# --------------------------
# Helper Function for Prediction
# --------------------------
def predict_internal(input_data):
    """
    Calls the ML inference function (run_login) with input_data.
    Converts any numpy.float32/64 to regular floats if necessary.
    Returns the result.
    """
    try:
        result = run_login(input_data)
        # Convert result if needed:
        if isinstance(result, list):
            result = [float(x) if isinstance(x, (np.float32, np.float64)) else x for x in result]
        elif isinstance(result, dict) and "prediction" in result:
            result["prediction"] = float(result["prediction"])
        elif isinstance(result, (np.float32, np.float64)):
            result = float(result)
        return result
    except Exception as e:
        raise e

# --------------------------
# Flask App Setup
# --------------------------
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        result = predict_internal(input_data)
        return jsonify({
            "status": "success",
            "prediction": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# --------------------------
# Taxi Forecast Function using predict_internal
# --------------------------
def get_forecast(pu, do, date_str, is_amount):
    """
    Constructs an input JSON based on your sample input and calls predict_internal()
    to get a 24-hour forecast.
    
    Expected input JSON:
    {
        "date": "2024-08-15",
        "is_amount": <is_amount>,   // true for fare, false for duration
        "model_number": 1,
        "PULocationID": <pu>,
        "DOLocationID": <do>,
        "trip_distance": <default_value>
    }
    
    Expects run_login to return a list of 24 numeric predictions.
    Converts that list into 24 dictionaries with keys "hour", "fare", and "duration".
    If is_amount is True, predictions are treated as fare;
    if False, they are treated as duration (converted from seconds to minutes).
    """
    default_trip_distance = 5.0  # Adjust as needed

    input_data = {
        "date": date_str,
        "is_amount": is_amount,
        "model_number": 1,
        "PULocationID": pu,
        "DOLocationID": do,
        "trip_distance": default_trip_distance
    }
    print(f"Input data for predict_internal: {input_data}")
    try:
        result = predict_internal(input_data)
        if isinstance(result, dict) and "forecast" in result:
            forecast_values = result["forecast"]
        else:
            forecast_values = result
    except Exception as e:
        print(f"Error calling predict_internal: {e}")
        forecast_values = None

    if not forecast_values or len(forecast_values) != 24:
        print("Warning: Forecast list is missing or not 24 items. Returning 24 empty forecasts.")
        forecast_list = [{"hour": h, "fare": None, "duration": None} for h in range(24)]
    else:
        forecast_list = []
        for hour, val in enumerate(forecast_values):
            if is_amount:
                forecast_list.append({
                    "hour": hour,
                    "fare": float(val),
                    "duration": None
                })
            else:
                # Convert duration from seconds to minutes
                forecast_list.append({
                    "hour": hour,
                    "fare": None,
                    "duration": round(float(val) / 60, 2)
                })
    print("Final forecast data:", forecast_list)
    return forecast_list

# Optional: API endpoint for forecast (if needed)
@app.route('/api/forecast', methods=['GET'])
def forecast_api():
    pu = int(request.args.get('PULocationID', 1))
    do = int(request.args.get('DOLocationID', 1))
    date_str = request.args.get('date', 'default')
    data = get_forecast(pu, do, date_str, is_amount=True)
    return jsonify(data)

# --------------------------
# Dash Dashboard Setup
# --------------------------
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

# Create dropdown options for pickup and dropoff (1 to 265)
dropdown_options = [{'label': str(i), 'value': i} for i in range(1, 266)]

# Initialize the Dash app using the same Flask server.
dash_app = dash.Dash(__name__, server=app, external_stylesheets=external_stylesheets, url_base_pathname='/dashboard/')

dash_app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("NYC Taxi 24-Hour Forecast"), width=12)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Div([
            dbc.Label("Pickup Location (1-265):"),
            dcc.Dropdown(
                id='pickup-dropdown',
                options=dropdown_options,
                value=132,
                searchable=True,
                clearable=False
            )
        ], className="mb-3"), width=6),
        dbc.Col(html.Div([
            dbc.Label("Dropoff Location (1-265):"),
            dcc.Dropdown(
                id='dropoff-dropdown',
                options=dropdown_options,
                value=250,
                searchable=True,
                clearable=False
            )
        ], className="mb-3"), width=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Div([
            dbc.Label("Enter Date (YYYY-MM-DD):"),
            dcc.Input(id='date-input', type='text', value='2024-08-15', className="form-control")
        ], className="mb-3"), width=4),
        dbc.Col(html.Div([
            dbc.Label("Graph Type:"),
            dcc.RadioItems(
                id='graph-type',
                options=[
                    {'label': 'Fare Only', 'value': 'fare'},
                    {'label': 'Duration Only', 'value': 'duration'},
                    {'label': 'Both', 'value': 'both'}
                ],
                value='both',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            )
        ], className="mb-3"), width=8)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(html.Button('Get Forecast', id='submit-button', n_clicks=0, className="btn btn-primary"), width=12)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='forecast-chart'), width=12)
    ])
], fluid=True)

@dash_app.callback(
    Output('forecast-chart', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('pickup-dropdown', 'value'),
     State('dropoff-dropdown', 'value'),
     State('date-input', 'value'),
     State('graph-type', 'value')]
)
def update_forecast(n_clicks, pickup, dropoff, date_str, graph_type):
    if n_clicks > 0:
        if graph_type == 'both':
            # Get fare forecast and duration forecast separately.
            fare_data = get_forecast(pickup, dropoff, date_str, is_amount=True)
            duration_data = get_forecast(pickup, dropoff, date_str, is_amount=False)
            hours = [item['hour'] for item in fare_data]  # Both lists should have same hours.
            fare_values = [item['fare'] for item in fare_data]
            duration_values = [item['duration'] for item in duration_data]
            trace1 = go.Scatter(
                x=hours, y=fare_values, mode='lines+markers',
                name='Forecasted Fare ($)',
                line=dict(color='blue'),
                marker=dict(color='blue')
            )
            trace2 = go.Scatter(
                x=hours, y=duration_values, mode='lines+markers',
                name='Forecasted Duration (min)',
                yaxis='y2',
                line=dict(color='red'),
                marker=dict(color='red')
            )
            yaxis1_title = "Fare ($)"
            yaxis2_title = "Duration (min)"
            data_traces = [trace1, trace2]
            layout = go.Layout(
                title=f"24-Hour Forecast for Pickup {pickup} and Dropoff {dropoff} on {date_str}",
                xaxis=dict(title='Hour of Day', dtick=1),
                yaxis=dict(
                    title={'text': yaxis1_title, 'font': {'color': 'blue'}},
                    tickfont={'color': 'blue'}
                ),
                yaxis2=dict(
                    title={'text': yaxis2_title, 'font': {'color': 'red'}},
                    tickfont={'color': 'red'},
                    overlaying='y',
                    side='right'
                ),
                legend=dict(x=0, y=1),
                margin=dict(l=50, r=50, t=50, b=50)
            )
        else:
            # Only one type is selected.
            is_amount = True if graph_type == 'fare' else False
            data_single = get_forecast(pickup, dropoff, date_str, is_amount)
            hours = [item['hour'] for item in data_single]
            values = [item['fare'] if is_amount else item['duration'] for item in data_single]
            y_title = "Fare ($)" if is_amount else "Duration (min)"
            color = 'blue' if is_amount else 'red'
            trace = go.Scatter(
                x=hours, y=values, mode='lines+markers',
                name=f'Forecasted {y_title}',
                line=dict(color=color),
                marker=dict(color=color)
            )
            data_traces = [trace]
            layout = go.Layout(
                title=f"24-Hour Forecast for Pickup {pickup} and Dropoff {dropoff} on {date_str}",
                xaxis=dict(title='Hour of Day', dtick=1),
                yaxis=dict(
                    title={'text': y_title, 'font': {'color': color}},
                    tickfont={'color': color}
                ),
                legend=dict(x=0, y=1),
                margin=dict(l=50, r=50, t=50, b=50)
            )
        figure = {'data': data_traces, 'layout': layout}
        return figure

    return {
        'data': [],
        'layout': go.Layout(title='Enter pickup, dropoff, a date, choose graph type, then click "Get Forecast"')
    }

# --------------------------
# Run the App, open http://127.0.0.1:5001/dashboard/
# --------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
