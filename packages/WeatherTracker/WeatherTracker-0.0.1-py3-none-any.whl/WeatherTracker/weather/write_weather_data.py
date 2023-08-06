import os
import csv
import shutil
from datetime import datetime
from WeatherTracker import ROOT_PATH


class WriteWeatherData:
    def __init__(self, data):
        self.data = data
        self.dir_path = None
        self.write()

    def write(self):
        dt = datetime.now()
        date_str = f'{str(dt.year)}{str(dt.month).zfill(2)}{str(dt.day).zfill(2)}'
        self.dir_path = os.path.join(ROOT_PATH, 'data', f'{self.data.city}')
        self.make_dir()  # create new directory if necessary
        data_path = os.path.join(self.dir_path, f'{date_str}_{self.data.city}.csv')
        row = [self.data.dt, self.data.lat, self.data.lon, self.data.t_now, self.data.t_feel, self.data.humid,
               self.data.p_now, self.data.wind_vel, self.data.wind_dir, self.data.clouds, self.data.params,
               self.data.descript, str(dt)]
        if not os.path.exists(data_path):
            with open(data_path, 'w') as f:
                col_labels = ['datetime', 'latitude', 'longitude', 'temperature (K)', 'feels like temperature (K)',
                              'humidity (%)', 'pressure (kPa)', 'wind speed (m/s)', 'wind direction (deg)',
                              'cloudiness (%)', 'parameters', 'description', 'retrieval datetime']
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(col_labels)
                writer.writerow(row)
        else:
            with open(data_path, 'a') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(row)

    def make_dir(self):
        if not os.path.isdir(self.dir_path):  # Check if directory exists already
            os.mkdir(self.dir_path)  # Create new empty directory

