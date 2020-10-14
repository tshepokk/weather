from django.shortcuts import render
import requests
import statistics

from .forms import WeatherForm
from .config.conf import getUrl


def home(request):
	context = {}
	form = WeatherForm()
	context['form'] = form
	# initialize content to be displayed on the view
	display_content = dict()
	display_content1 = []
	results = []

	# ensure correct method is used
	if request.POST:
		form = WeatherForm(request.POST)

		if form.is_valid():
			city = request.POST['city_name']
			period = request.POST['period']
			print(city)
			print(period)

			# initialize url
			mydict = {'q': city, 'cnt': period}
			url = getUrl()

			# query weather app api
			response = requests.get(url, params=mydict)
			data = response.json()
			print(data)

			# get the counter from output data
			my_count = data['count']
			print(my_count)

			# check if the request to the weather API was successful
			if response.status_code == 200:
				print("Request was successful")

				# check if city was found
				if len(data['list']) != 0:
					print("Data found", data['list'][0]['name'])

					if 0 < my_count <= 7:
						print("start computing")
						for i in range(0, my_count):
							temp_min = data['list'][i]['main']['temp_min']
							temp_max = data['list'][i]['main']['temp_max']
							temp_avg = data['list'][i]['main']['temp']
							humid = data['list'][i]['main']['humidity']

							# calculating the median
							temp_list = (temp_min, temp_max, temp_avg, humid)
							sorted_temp_list = sorted(temp_list)
							temp_median = statistics.median(sorted_temp_list)

							# store data to be displayed in the view
							display_content = {
								"min temp": temp_min,
								"max temp": temp_max,
								"avg temp": temp_avg,
								"median temp": temp_median,
								"humidity": humid,
							}
							print(display_content)
							
					else:
						print("Invalid count")
				else:
					print("No data found")

			elif response.status_code == 400:
				print("Bad Request")
			elif response.status_code == 401:
				print("Invalid API key")
			else:
				print("Something went wrong")

	else:
		print("Incorrect Method used")
	# display_content['form'] = WeatherForm()

	return render(request, 'weatherapi/home.html', {'display_content': display_content})
