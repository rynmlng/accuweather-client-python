# accuweather-client-python

## Problem

Build a client library in a language of your choice to access AccuWeather's Forecast API. The client library should be able to get the 1 day forecast when provided a zip code.

## Background

This is a client library to access the AccuWeather API written in `Python 3`. In order to use this library you must have `Python 3` installed on your system.

## Setup

1. Ensure you have `Python 3` installed on your system.
2. Install required package dependencies: `pip install requirements.txt`

## Usage

In order to use this application, follow the steps below. Directions may vary because these are customized for OS X:

1. Obtain your `Accuweather` API key as an environment variable. You can find your API key on [this page.](https://developer.accuweather.com/user/me/apps)
2. Open a `Python` shell that can access this client library's folder.
3. Run the following commands to access the 1-day forecast for a location:
```
>>> from client import AccuweatherForecastAPI
>>> AccuweatherForecastAPI("<your api key>").get_forecast(13478)

'Expect showers this afternoon.'
```
