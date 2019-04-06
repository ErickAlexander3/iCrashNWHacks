#from oauth2client.client import GoogleCredentials
import googleapiclient
import googleapiclient.discovery
from datetime import datetime, timedelta
from pyowm import OWM
import pdb

'''
    Normalization values obtained from data points used to train model
    Note: If retraining with different data, PLEASE update these values
'''
NORMALIZATION = {
    "MONTH": {"mean": 6.730589, "std": 3.425069},
    "DAY": {"mean": 3.953694, "std": 1.925329},
    "HOUR": {"mean": 13.719150, "std": 4.958253},
    "WEATHER": {"mean": 1.560086, "std": 1.098658},
}

WEATHER_CONDITIONS = {
    "default": 1,
    "clear": 1,
    "clouds": 2,
    "overcast": 2,
    "rain": 3,
    "drizzle": 3,
    "snow": 4,
    "freezing": 5,
    "sleet": 5,
    "mist": 6,
    "sand": 6,
    "dust": 6,
    "thunderstorm": 7
}

WEATHER_KEY = "b06f80f842209659a5af60b2bf16d736"


def generate_predicted_points():
    instances = []
    today = datetime.today()
    weather = WEATHER_CONDITIONS["default"]

    owm = OWM(WEATHER_KEY)
    obs = owm.three_hours_forecast('Vancouver,CA')
    forecasts = obs.get_forecast()

    for i in range(0, 8):
        current_instance = []
        current_time = today + timedelta(hours=i*3)
        month = current_time.month
        weekday = current_time.weekday()
        hour = current_time.hour
        forecast = forecasts.get(i).get_detailed_status()
        #check if any keyword in the weather description matches, or else use previous weather
        for word in forecast.split():
            if word in WEATHER_CONDITIONS:
                weather = WEATHER_CONDITIONS[word]
                break

        current_instance.append((month - NORMALIZATION["MONTH"]["mean"]) / NORMALIZATION["MONTH"]["std"])
        current_instance.append((weekday - NORMALIZATION["DAY"]["mean"]) / NORMALIZATION["DAY"]["std"])
        current_instance.append((hour - NORMALIZATION["HOUR"]["mean"]) / NORMALIZATION["HOUR"]["std"])
        current_instance.append((weather - NORMALIZATION["WEATHER"]["mean"]) / NORMALIZATION["WEATHER"]["std"])

        instances.append(current_instance)

    result = predict_json(instances)
    result_as_json = []
    for entry in result:
        as_json = {"latitude": entry["dense_14/BiasAdd:0"][0], "longitude": entry["dense_14/BiasAdd:0"][1]}
        result_as_json.append(as_json)

    #pdb.set_trace()
    return result_as_json


def predict_json(instances=None, project='icrash', model='iCrashModel', version='test_model'):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    if instances is None:
        instances = [[-1.673131, -1.534124,  0.460011,  0.400410], ]
    service = googleapiclient.discovery.build('ml', 'v1')
    name = 'projects/{}/models/{}'.format(project, model)
    name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']
