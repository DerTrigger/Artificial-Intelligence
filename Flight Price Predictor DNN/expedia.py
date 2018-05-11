import json
import requests
from lxml import html
from collections import OrderedDict
import argparse
import time
import os

def parse(source,destination,date):
	for i in range(5):
		try:
			url = ("https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},"
                  "departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&"
                  "options=cabinclass%3Aeconomy&mode=search&origref="
                  "www.expedia.com".format(source,destination,date))
			response = requests.get(url)
			parser = html.fromstring(response.text)
			json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
			raw_json =json.loads(json_data_xpath[0])
			flight_data = json.loads(raw_json["content"])

			flight_info  = OrderedDict() 
			lists=[]

			for i in flight_data['legs'].keys():
				total_distance =  flight_data['legs'][i]["formattedDistance"]
				exact_price = flight_data['legs'][i]['price']['totalPriceAsDecimal']

				departure_location_airport = 'PDX' #flight_data['legs'][i]['departureLocation']['airportLongName']
				departure_location_city = flight_data['legs'][i]['departureLocation']['airportCity']
				departure_location_airport_code = flight_data['legs'][i]['departureLocation']['airportCode']
				
				arrival_location_airport = 'MOW' #flight_data['legs'][i]['arrivalLocation']['airportLongName']
				arrival_location_airport_code = flight_data['legs'][i]['arrivalLocation']['airportCode']
				arrival_location_city = flight_data['legs'][i]['arrivalLocation']['airportCity']
				airline_name = flight_data['legs'][i]['carrierSummary']['airlineName']
				
				no_of_stops = flight_data['legs'][i]["stops"]
				flight_duration = flight_data['legs'][i]['duration']
				flight_hour = flight_duration['hours']
				flight_minutes = flight_duration['minutes']
				flight_days = flight_duration['numOfDays']
				todate = time.strftime("%d/%m/%Y")

				if no_of_stops==0:
					stop = "Nonstop"
				else:
					stop = str(no_of_stops)+' Stop'

				total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days,flight_hour,flight_minutes)
				departure = departure_location_airport+", "+departure_location_city
				arrival = arrival_location_airport+", "+arrival_location_city
				carrier = flight_data['legs'][i]['timeline'][0]['carrier']
				plane = carrier['plane']
				plane_code = carrier['planeCode']
				formatted_price = "{0:.2f}".format(exact_price)

				if not airline_name:
					airline_name = carrier['operatedBy']
				
				flight_info={
					'departure date':date,
					'request date':todate,
					'stops':stop,
					'departure':departure,
					'arrival':arrival,
					'flight duration':total_flight_duration,
					'airline':airline_name,
					'ticket price':formatted_price
					#'plane':plane,
					#'timings':timings,
					#'plane code':plane_code'
				}
				lists.append(flight_info)
			sortedlist = sorted(lists, key=lambda k: k['ticket price'],reverse=False)
			return sortedlist
		
		except ValueError:
			print ("Rerying...")
			
		return -1

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('source',help = 'Source airport code')
	argparser.add_argument('destination',help = 'Destination airport code')
	argparser.add_argument('date',help = 'MM/DD/YYYY')

	args = argparser.parse_args()
	source = args.source
	destination = args.destination
	date = args.date
	print ("Fetching flight details")
	scraped_data = parse(source,destination,date)
	if scraped_data != -1:
		print ("Writing data to output file")
		filename = 'flight-results.json'
		if not os.path.exists(filename):
			with open(filename,'w') as fp:
				json.dump(scraped_data,fp, indent = 4)
		else:
			with open(filename,'r') as f:
				data = json.load(f)
				data.append(scraped_data)
			os.remove(filename)
			with open(filename, 'w') as f:
				json.dump(data, f, indent = 4)
