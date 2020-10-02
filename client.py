from math import floor, log
import requests


API_METHOD_GET = "get"
LOCATION_POSTAL_CODE_RESOURCE = "http://dataservice.accuweather.com/locations/v1/postalcodes/search"
FORECAST_ONE_DAY_RESOURCE = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"


class AccuweatherAPIException(Exception):
    """ Custom exception for any errors encountered accessing the Accuweather API. """
    pass


class AccuweatherForecastAPI:
    ACCEPTED_API_METHODS = (API_METHOD_GET,)

    API_KEY_LENGTH = 32
    API_MAX_TIMEOUT = 5 # seconds

    def __init__(self, api_key):
        if not isinstance(api_key, str) or len(api_key) != self.API_KEY_LENGTH:
            raise ValueError("Provided API key must be a 32-character string.")

        self.api_key = api_key


    def _get_location_key(self, zip_code):
        """ Get the Accuweather location key for a location from the zip code. """

        params = {"apikey": self.api_key, "q": zip_code}
        response = self._make_request(API_METHOD_GET, LOCATION_POSTAL_CODE_RESOURCE, params=params)
        return response[0]["Key"]


    def _make_request(self, method, resource, params):
        """ Make a request to the given resource and return the response. """

        if method not in self.ACCEPTED_API_METHODS:
            raise ValueError(f"{method} is not an acceptable method for a request.")

        try:
            response = getattr(requests, method)(resource, params=params, timeout=self.API_MAX_TIMEOUT)
        except Exception as e:
            error_message = f"The following error was encountered when making the following request:"
            error_message += f"\n  {method}: {resource}"
            error_message += f"\n    params={params}"
            error_message += f"\n  ERROR: {e}"

            raise AccuweatherAPIException(error_message)

        if response.status_code == 401:
            raise AccuweatherAPIException("API returned a 401 status code, did you provide the correct API key?")
        elif response.status_code != 200:
            raise AccuweatherAPIException(f"API returned with status code {response.status_code}")

        return response.json()


    def get_forecast(self, zip_code):
        """ Get the headline forecast for a location by zip code. """

        self.validate_zip_code(zip_code)
        location_key = self._get_location_key(zip_code)

        resource_url = FORECAST_ONE_DAY_RESOURCE.format(location_key=location_key)

        params = {"apikey": self.api_key, "details": "false", "metric": "false"}
        response = self._make_request(API_METHOD_GET, resource_url, params=params)

        return response["Headline"]["Text"]


    def validate_zip_code(self, zip_code):
        """ Validate that the zip code provided is a valid US 5-digit zip code. """
        if not isinstance(zip_code, int) or floor(log(zip_code, 10)+1) != 5:
            raise ValueError("Only 5-digit zip codes are permitted")
