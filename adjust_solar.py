#!/usr/bin/python3

import csv, math, os, glob
from collections import defaultdict
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError



def adjust_solar(address):
	"""
	Function to adjust solar generation
	:param address: the address provided in string format
	:param dates: the dates provided in list format
	:param generation: the generation data provided in list format
	:return adj_gen: the adjusted generation for the given dates
	"""


def get_lat_long(address):
	"""
	Function to get the coordinates of a given address using Geopy
	:param address: the address of interest
	:return coordinates: list of [latitude, longitude]
	"""
	try:
		geolocator = Nominatim(user_agent="Solai", timeout=2)
		try:
			location = geolocator.geocode(address, timeout = 6)
			if location is not None:
				latitude = round_to(location.latitude, .05)
				longitude = round_to(location.longitude, .05)
				if (-43.95 < latitude < -10) and (112.05 < longitude < 154):
					return [latitude, longitude]
				else:
					return [None, None]
		except GeocoderTimedOut as e:
			return [None, None]
	except GeocoderServiceError as e:
		return [None, None]

	
def round_to(n, precision):
	"""
	Function to round a number to a given precision
	:param n: the number to be rounded
	:param precision: the number of significant figures
	:return result: the result of the rounding process
	"""
	result = round(round(n / precision) * precision, 
			-int(math.floor(math.log10(precision))))
	return result



def get_row_num(latitude):
	"""
	Function to get the row number of the BOM file corresponding to given lat
	:param latitude: the given latitude
	:return row_num: return the corresponding row number of the file
	"""
	start_lat = -10
	row_num = round_to((abs(latitude) + start_lat)/.05,.05)
	# this line is necessary to skip the header metadata
	row_num += 6
	return int(row_num)


def get_col_num(longitude):
	"""
	Function to get the column number of the BOM file corresponding to given long
	:param latitude: the given longitude
	:return row_num: return the corresponding column number of the file
	"""
	start_long = 112.05
	col_num = round_to((longitude - start_long)/.05,.05)
	return int(col_num)


def read_csv(csv_file):
	"""
	Read the CSV file and store it's data into python variables
	:param csv_file: the .csv file to be read
	:return generation_data: the csv data stored into a Python dictionary
	:return dates: the dates over which the data covers
	"""

	generation_data = {}
	columns = defaultdict(list)

	with open(csv_file,'r', encoding='utf-8') as enc_in:
		reader = csv.reader(enc_in)
		for row in reader:
			for (i,v) in enumerate(row):
				columns[i].append(v)


	for col in columns:
		address = columns[col][0]
		dataset = columns[col][1:]
		dates = columns[0][1:]

		if (address):
			generation_data[address] = dataset

	return generation_data, dates



def get_weather_perf(date, row_num, col_num):
	"""
	Function to get the weather performance at specific location from BOM files
	:param date:
	:param row_num:
	:param col_num:
	:return weather_perf:
	"""
	bom_folder = 'files/bom_datasets'
	bom_files = os.path.join(bom_folder,"*")
	bom_averages = 'files/bom_averages'
	bom_average_files = os.path.join(bom_averages,"*")

	day, month, year = [int(x) for x in date.split('/')]
	if day < 10:
		day = "0" + str(day)
	if month < 10:
		month = "0" + str(month)
	date_of_interest = str(month)+"."+str(day)+"."+str(year)+".txt"


	for file in glob.glob(bom_files):

		file_date = file[-12:]
		if (file_date == date_of_interest):
			with open(file,'r') as enc_in:
				reader = csv.reader(enc_in)
				i = 1
				for row in reader:
					if i==row_num:
						col_vals = row[0].strip().split(" ")
						radiation = col_vals[col_num]


						for file2 in glob.glob(bom_average_files):
							month_date = file2[-6:]
							if (month_date == (str(month)+".txt")):
								with open(file2,'r') as ave_in:
									reader = csv.reader(ave_in)
									j = 1
									for row in reader:
										if j==row_num:
											col_vals = row[0].strip().split(" ")
											ave_radiation = col_vals[col_num]
										j += 1

						weather_perf = float(radiation) / float(ave_radiation)
						return weather_perf
					i += 1

	return None










if __name__ == '__main__':
	"""
	Function that reads in a specifically defined dataset
	The dataset should have two columns:
	Column 1: Date in format DD/MM/YYYY
	Column 2: Solar generation in a number format
	The header row should have the address of the column's data
	From this location it grabs the local weather data for the date range
	Performs an adjustment on the generation
	Returns a structured table of date, generation and adjusted generation
	Plots the results
	"""



	csv_file = 'files/final_set.csv'
	generation_data, dates = read_csv(csv_file)

	weather_perf_dict = {}
	generation_perf_dict = {}


	for key in generation_data.keys():
		address = key
		latitude, longitude = get_lat_long(address)

		if (latitude and longitude):

			row_num = get_row_num(latitude)
			col_num = get_col_num(longitude)

			weather_perfs = []

			for date in dates:
				weather_perf = get_weather_perf(date, row_num, col_num)
				weather_perfs.append(round_to(weather_perf, .001))

			weather_perf_dict[address] = weather_perfs

		total_gen = 0
		for gen_value in generation_data[key]:
			total_gen += float(gen_value)
		average_gen = (total_gen / len(dates))
		generation_perfs = []
		for gen_value in generation_data[key]:
			generation_perf = (float(gen_value) / average_gen)
			generation_perfs.append(round_to(generation_perf, .001))
		generation_perf_dict[address] = generation_perfs


	





				


