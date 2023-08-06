# import required modules
import json
import requests
import schedule
import numpy as np
from datetime import datetime


class GetWeatherData:
	def __init__(self, lat, lon):
		self.api_key = "10d274e4344f8f19dab6bbceb9e5232f"
		self.lat = lat
		self.lon = lon

		self.response = None
		self.data = None
		self.dt = None
		self.t_now = None
		self.t_feel = None
		self.t_max = None
		self.t_min = None
		self.p_now = None
		self.humid = None
		self.clouds = None
		self.params = None
		self.descript = None
		self.wind_vel = None
		self.wind_dir = None
		self.wind_gust = None
		self.city = None

	def now(self):
		url = f"http://api.openweathermap.org/data/2.5/weather?" \
			f"appid={self.api_key}&lat={str(self.lat)}&lon={str(self.lon)}"
		self.response = requests.get(url)
		self.data = self.response.json()

		if self.data["cod"] != "404":  # check that city is found
			self.dt = datetime.fromtimestamp(self.data['dt'])		# Time of call converted to datetime object
			self.t_now = self.data["main"]["temp"]  	   			# Current temperature [K]
			self.t_feel = self.data["main"]["feels_like"]  			# Current feels like temperature [K]
			self.t_max = self.data["main"]["temp_max"]	   			# High temperature for the day [K]
			self.t_min = self.data["main"]["temp_min"]	   			# Low temperature for the day [K]
			self.p_now = self.data["main"]["pressure"]/10  			# Current pressure [kPa]
			self.humid = self.data["main"]["humidity"]	   			# Current humidity [%]
			self.lon = self.data["coord"]["lon"]  					# Longitude location [deg]
			self.lat = self.data["coord"]["lat"]  					# Latitude location [deg]
			self.clouds = self.data['clouds']['all']				# Cloudiness [%]
			self.params = self.data["weather"][0]["main"]  			# Qualitative description 1
			self.descript = self.data["weather"][0]["description"]  # Qualitative description 2
			self.wind_vel = self.data['wind']['speed']  			# Wind speed [m/s]
			self.wind_dir = self.data['wind']['deg']  				# Wind direction [deg]
			self.city = self.data['name']  							# City name

	# def forecast(self, cnt: int = 8):
	# 	self.cnt = cnt  # number of days to return [1 to 5]
	# 	url = f"http://api.openweathermap.org/data/2.5/forecast?" \
	# 		f"lat={str(self.lat)}&lon={str(self.lon)}&appid={self.api_key}&cnt={str(cnt)}"
	# 	self.response = requests.get(url)
	# 	self.data = self.response.json()
	#
	# 	self.t_arr = np.array([])
	# 	self.t_feel_arr = np.array([])
	# 	self.p_arr = np.array([])
	# 	self.humid_arr = np.array([])
	# 	self.main_arr = np.array([])
	#
	# 	for x in self.data['list']:
	# 		self.t_arr = np.append(self.t_arr, x['main']['temp'])
	# 		self.main_arr = np.append(self.main_arr, x['weather'][0]['main'])

	def print_data(self):
		t = self.datetime_to_str(self.dt, military=False)
		print(f'Weather in {self.city} at {t["hour"]}:{t["min"]}{t["meridian"]}, {t["month"]}/{t["day"]}/{t["year"]} (called {datetime.now()})')
		print(f'Temperature: {round(self.convert_temp(self.t_now, "f"), 3)}' + u'\N{DEGREE SIGN}F')
		print(f'Feels like:  {round(self.convert_temp(self.t_feel, "f"), 3)}' + u'\N{DEGREE SIGN}F')
		print(f'Wind speed:  {round(self.wind_vel * 2.237, 2)} mph')
		print(f'Humidity:    {self.humid}%')
		print(f'Pressure:    {self.p_now} kPa')
		print(f'Cloudiness:  {self.clouds}%')

	@staticmethod
	def convert_temp(T_in, units='C'):
		"""
		Converts temperature in K to deg F or deg C.
		:param T_in: Input temperature in K
		:type T_in: float
		:param units: Units to convert to ('C' or 'F')
		:return units: str
		"""
		if units.lower() == 'c':
			return T_in - 273.15
		elif units.lower() == 'f':
			return (T_in - 273.15)*9/5 + 32
		else:
			raise ValueError("'Unit' invalid.")

	@staticmethod
	def datetime_to_str(dt, military=True):
		hour = dt.hour
		if not military:
			if hour >= 12:
				meridian = 'pm'
				hour = hour - 12 if hour > 12 else hour
			else:
				meridian = 'am'
				hour = 12 if hour < 1 else hour
		else:
			meridian = ''

		dictionary = {
			'year': str(dt.year),
			'month': str(dt.month),
			'day': str(dt.day).zfill(2),
			'hour': str(hour) if not military else str(hour).zfill(2),
			'min': str(dt.minute).zfill(2),
			'sec': str(dt.second).zfill(2),
			'meridian': meridian,
					}
		return dictionary


if __name__ == '__main__':
	# Urbana weather
	lat = 40.103180704025185
	lon = -88.17479134286376
	data = GetWeatherData(lat=lat, lon=lon)
	data.now()
	data.print_data()
	# data.forecast()
