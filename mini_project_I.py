####Imports
import requests
import os
import streamlit as st 
import pandas as pd

####Main Application Function
def main():

	"""
	This is the main body of the T-LAMP (Transport of London API Mini Project) Application
	which is run when the script is called from the terminal. It makes HTTP requests using 
	user defined functions and extracts values from complex lists and nested dictionaries.   
	"""

	####Configure the page
	st.set_page_config(page_title="T-LAMP")
	st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">', unsafe_allow_html=True)


	#####T-LAMP App Layout
	###Main page title: HTML Formatting Implemented
	html_main_page_title = "<div class='shadow p-3 mb-5 bg-white rounded' style='text-align:center'><h2 style='text-align:center font-weight:550;'>Transport of London API Mini Project</h2></div>"
	st.markdown(html_main_page_title,unsafe_allow_html=True)

	####Main Page Content
	text = open("motivation.txt",'r').read()
	st.markdown(text)
	
	#### Task Header
	st.markdown(f"<div class='shadow p-3 mb-5 bg-white rounded'><h4 style='text-align:center;font-weight:600;'>T-LAMP Tasks</h4></div>",unsafe_allow_html=True)
	####Task containers
	task_1 = st.beta_expander("Air Quality Conditions for Tomorrow", expanded=False)
	task_2 = st.beta_expander("Modes of Transport Operated by Transport of London", expanded=False)
	task_3 = st.beta_expander("BikePoints Operated by Transport of London", expanded=False)
	task_4 = st.beta_expander("Tube & Bus Line in London", expanded=False)
	task_5 = st.beta_expander("Stations in Victoria", expanded=False)
	task_6 = st.beta_expander("Journey from Heathrow Airport to Tower Bridge using Bus and Tube", expanded=False)

	####Add Content to containers
	##Task 1
	task_1.write("API GET: https://api.tfl.gov.uk/AirQuality/")
	task_1.write(get_air_quality()[0])
	task_1.code(get_air_quality()[1])
	#task_1.markdown(f"<h3>Weather Forecast:</h3><h4>{get_air_quality()[0]}</h4>", unsafe_allow_html=True)

	##Task 2
	task_2.write("API GET: https://api.tfl.gov.uk/Journey/Meta/Modes")
	task_2.write(modes_of_transport()[2])
	task_2.markdown(f"<h4>Total Modes of Transport: {modes_of_transport()[1]}</h4><br>", unsafe_allow_html=True)
	task_2.dataframe(modes_of_transport()[0])

	##Task 3
	task_3.write("API GET: https://api.tfl.gov.uk/BikePoint")
	task_3.write(get_bikepoints()[3])
	task_3.markdown(f"<h4>Number of BikePoints operated by Transfer for London: {get_bikepoints()[0]}</h4><br>", 
					unsafe_allow_html=True)
	task_3.markdown(f"<h4>Full Docks: {get_bikepoints()[1]}</h4><br>", unsafe_allow_html=True)
	task_3.markdown(f"<h4>Empty Docks: {get_bikepoints()[2]}</h4><br>", unsafe_allow_html=True)
	task_3.markdown(f"<h4>Total Docks: {get_bikepoints()[0] + get_bikepoints()[1]}</h4><br>",unsafe_allow_html=True)

	##Task 4
	task_4.write("API GET: https://api.tfl.gov.uk/Line/Mode/tube,bus")
	task_4.write(get_tube_bus_lines()[3])
	task_4.markdown(f"<h4>Bus Lines: {get_tube_bus_lines()[0]}</h4><br>", 
					unsafe_allow_html=True)
	task_4.markdown(f"<h4>Tube Lines: {get_tube_bus_lines()[1]}</h4><br>", unsafe_allow_html=True)
	task_4.dataframe(get_tube_bus_lines()[2])

	##Task 5
	task_5.write("API GET: https://api.tfl.gov.uk/Line/victoria/StopPoints")
	task_5.write(get_victoria_line_stations()[2])
	task_5.markdown(f"<h4>Stations with Victoria Line: {get_victoria_line_stations()[0]}</h4><br>", 
					unsafe_allow_html=True)
	task_5.dataframe(get_victoria_line_stations()[1])

	##Task 6
	####Input Containers
	bus_duration = get_journey_plan("bus","tube")[0]
	tube_duration = get_journey_plan("bus","tube")[1]
	task_6.write("API GET: https://api.tfl.gov.uk/Journey/JourneyResults/Hillingdon,HeathrowAirportTerminal2/to/CityofLondon,TowerBridge?date=20210107&time=0930&timeIs=Departing&journeyPreference=LeastTime&mode=bus")
	task_6.write(get_journey_plan("bus","tube")[2])
	task_6.markdown(f"<h4>Planned Duration:<h4>", unsafe_allow_html=True)
	task_6.markdown(f"<h4>Bus: {bus_duration}</h4>", unsafe_allow_html=True)
	task_6.markdown(f"<h4>Tube: {tube_duration}</h4>", unsafe_allow_html=True)


####User defined functions

##Cached Functions
# st.cache(allow_output_mutation=True)
# def get_url_appends():
# 	"""
# 	This function gets the APP_ID and APP_KEY from os
# 	"""
# 	####Get keys from os
# 	app_id = os.environ["APP_ID"]
# 	app_key = os.environ["APP_KEY"]
# 	url_append = f'?app_id={app_id}&app_key={app_key}' 

# 	return url_append

st.cache(allow_output_mutation=True)
def get_air_quality():
	"""
	This function returns the air aquality for tommorrow
	"""
	url_base = "https://api.tfl.gov.uk/AirQuality"
	# url_params = get_url_appends()

	###send request to API
	res = requests.get(url_base)

	if res.status_code != 200:
		tmrw_air_quality =  f"{res.status_code} Error"
	else:
		json_file = res.json() 
		tmrw_air_quality = json_file['currentForecast'][0]['forecastSummary']

	result = json_file['currentForecast'][0]['forecastSummary']

	return (json_file,result)


st.cache(allow_output_mutation=True)
def modes_of_transport():
	"""
	This function returns the different modes of transport operated by Transport of London
	"""

	url_base = "https://api.tfl.gov.uk/Journey/Meta/Modes"
	# url_params = get_url_appends()

	###send request to API
	res = requests.get(url_base)

	if res.status_code != 200:
		task_2.write(f"{res.status_code} Error")
	else:
		modes_of_transport = []
		json_file = res.json()
		for mode in json_file:
		    modes_of_transport.append(mode['modeName'])

	df_modes_of_transport = pd.DataFrame(columns = ["Modes of Transport"], data= modes_of_transport)
	number_of_modes = len(df_modes_of_transport.index)
	return (df_modes_of_transport, number_of_modes, json_file)


st.cache(allow_output_mutation=True)
def get_bikepoints():
	"""
	This function returns the number of BikePoints operated by Transport of London
	and for each BikePoint, the corresponding full and empty docks
	"""

	url_base = "https://api.tfl.gov.uk/BikePoint"
	# url_params = get_url_appends()

	###send request to API
	res = requests.get(url_base)

	if res.status_code != 200:
		task_3.write(f"{res.status_code} Error")
	else:
		bikepoints = []
		empty_docks = 0
		full_docks = 0
		json_file = res.json()
		for bikepoint in json_file:
		    bikepoints.append(int(bikepoint['id'].split('_')[1]))

		    for property_desc in bikepoint['additionalProperties']:
		        if property_desc['key'] == 'NbDocks':
		            full_docks +=1
		        elif property_desc['key'] == 'NbEmptyDocks':
		        	empty_docks += 1 
		        else:
		            pass

	return (len(bikepoints),full_docks,empty_docks,json_file)

st.cache(allow_output_mutation=True)
def get_tube_bus_lines():
	"""
	This function returns the number of tubes and bus lines operated by Transport of London
	"""

	url_base = "https://api.tfl.gov.uk/Line/Mode/tube,bus"
	# url_params = get_url_appends()

	###send request to API
	res = requests.get(url_base)

	if res.status_code != 200:
		 task_4.write(f"{res.status_code} Error")
	else:
		bus_lines = []
		tube_lines = []
		json_file = res.json()
		for modelines in json_file:
		    if modelines['modeName'] == 'bus':
		        bus_lines.append(modelines['name'])
		    elif modelines['modeName'] == 'tube':
		        tube_lines.append(modelines['name'])
		    else:
		        pass

	df_tube_lines = pd.DataFrame(columns=["Tube Lines"], data=tube_lines)

	return (len(bus_lines),len(tube_lines),df_tube_lines,json_file)

st.cache(allow_output_mutation=True)
def get_victoria_line_stations():
	"""
	This function returns the number of stations with a victoria line operated by Transport of London
	"""

	url_base = "https://api.tfl.gov.uk/Line/victoria/StopPoints"
	# url_params = get_url_appends()

	###send request to API
	res = requests.get(url_base)

	if res.status_code != 200:
		 task_5.write(f"{res.status_code} Error")
	else:
		stations = []
		json_file = res.json()
		for station in json_file:
		    stations.append(station['stationNaptan'])

	df_stations = pd.DataFrame(columns=["Stations"], data=stations)

	return (len(stations),df_stations,json_file)

st.cache(allow_output_mutation=True)
def get_journey_plan(mode_1,mode_2):
	"""
	This function returns the duration by bus and tube from Hillingdon, Heathrow Airport Terminal 2
	to City of London, Tower Bridge
	"""

	url_base_mode_1 = f"https://api.tfl.gov.uk/Journey/JourneyResults/Hillingdon, Heathrow Airport Terminal 2/to/City of London, Tower Bridge?date=20210107&time=0930&timeIs=Departing&journeyPreference=LeastTime&mode={mode_1}"
	url_base_mode_2 = f"https://api.tfl.gov.uk/Journey/JourneyResults/Hillingdon, Heathrow Airport Terminal 2/to/City of London, Tower Bridge?date=20210107&time=0930&timeIs=Departing&journeyPreference=LeastTime&mode={mode_2}"
	# url_params = get_url_appends()

	###send request to API
	res_mode_1 = requests.get(url_base_mode_1)
	res_mode_2 = requests.get(url_base_mode_2)

	if res_mode_1.status_code != 200 or res_mode_2.status_code != 200:
		 task_6.write(f"{res.status_code} Error")
	else:
		journey_plan_bus = res_mode_1.json()
		journey_bus_duration = []

		for journey_bus in journey_plan_bus['journeys']:
			journey_bus_duration.append(int(journey_bus['duration']))
		bus_duration = min(journey_bus_duration)

		journey_plan_tube = res_mode_2.json()
		journey_tube_duration = []
		for journey_bus in journey_plan_tube['journeys']:
			journey_tube_duration.append(int(journey_bus['duration']))
		tube_duration = min(journey_tube_duration)

	return (bus_duration, tube_duration,journey_plan_bus)


if __name__ == "__main__":
	main()