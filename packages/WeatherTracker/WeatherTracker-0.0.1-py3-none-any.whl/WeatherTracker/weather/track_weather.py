import os
import sys
import time
import schedule
from WeatherTracker import ROOT_PATH
from WeatherTracker.weather.get_weather_data import GetWeatherData
from WeatherTracker.weather.write_weather_data import WriteWeatherData


class TrackWeather:
    def __init__(self, lat, lon, interval):
        print('Running...')
        self.lat = lat
        self.lon = lon
        self.interval = interval
        self.data = None
        self.last_dt = None
        self.run()

    def run(self):
        self.data = GetWeatherData(self.lat, self.lon)
        schedule.every(self.interval).minutes.do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self):
        try:
            self.data.now()
            print()
            self.data.print_data()
            if self.last_dt is None or self.last_dt != self.data.dt:
                print('writing new data')
                WriteWeatherData(self.data)
            else:
                print('repeat data detected')
            self.last_dt = self.data.dt
        except Exception as e:  # If an exception occurs during model application
            print(f"Exception when retrieving data: {e}")  # Print exception
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Exception type:", exc_type, "\nFile:", f"{fname},", "Line", exc_tb.tb_lineno)


if __name__ == '__main__':
    # # Urbana
    # job = TrackWeather(lat=40.1106, lon=-88.2073, interval=3)

    # # Pekin
    # job = TrackWeather(lat=40.5675, lon=-89.6407, interval=3)

    # Denver
    # job = TrackWeather(lat=39.7392, lon=-104.9903, interval=3)

    # # Memphis TN
    # job = TrackWeather(lat=35.1495, lon=-90.0490, interval=3)

    # Ogrlthorpe
    job = TrackWeather(lat=40.103180704025185, lon=-88.17479134286376, interval=3)
