################################################ NY CITIBIKE DASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image
import seaborn as sns

################################################ Initial settings for the dashboard #####################################################

st.set_page_config(page_title = 'New York Citi Bike Strategy Dashboard', layout='wide')
st.title("NY Citi Bike Strategy Dashboard")

# Define sidebar
st.sidebar.title('Dashboard Pages')
page = st.sidebar.selectbox('Aspects of The Analysis:',
                            ['Introduction',
                             'Most Popular Stations',
                             'Weather Component and Bike Usage',
                             'Interactive Map With Aggregated Bike Trips',
                             'Member Vs. Casual Riders',
                             'Recommendations'])

########################## Import data ###########################################################################################

df = pd.read_csv('NY_CitiBike_2022_sampled.csv', index_col = 0)
top20 = pd.read_csv('NY_top20.csv', index_col = 0)
df_temp = pd.read_csv('NY_CitiBike_temp.csv', index_col = 0)

######################################### DEFINE THE PAGES #######################################################################

## Introduction Page ##
if page == 'Introduction':
    st.markdown("The objective of this dashboard is to provide some helpful observations on the expansion problems that New York Citi Bike is facing as of now.")
    st.markdown("Currently, New York Citi Bikes is experiencing high demand which is resulting in fewer bikes being available at certain times and/or certain locations. This analysis will look into potential reasons resulting in this problem and provide some recommendations.")

    st.markdown("#### Overall Approach: ")
    st.markdown("1. Define objective and goals")
    st.markdown("2. Source NY Citi Data and Weather data")
    st.markdown("3. Geospatial plot")
    st.markdown("4. Interactive visualizations")
    st.markdown("5. Creating a dashboard")
    st.markdown("6. Findings and recommendations")
    
    st.markdown("#### Dashboard Sections: ")
    st.markdown("The dropdown menu of the left labeled 'Aspects of The Analysis' will take you to the different aspects of the analysis our team explored")
    st.markdown(" - Most Popular Stations")
    st.markdown(" - Weather Component and Bike Usage")
    st.markdown(" - Interactive Map With Aggregated Bike Trips")
    st.markdown(" - Member Vs. Casual Riders")
    st.markdown(" - Recommendations")

    myImage = Image.open("bike_photo.jpg") #Source: https://unsplash.com/photos/blue-citi-bike-bicycles-parked-on-sidewalk-8ol9rD0BHAU
    st.image(myImage)
  
## Most popular stations page ##
elif page == 'Most Popular Stations':
    st.header("Most Popular Stations")
    
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'RdPu'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Looking at the bar chart, it is clear that some stations are more popular than others. The top three stations are: West 21 St & 6 Ave, West St & Chambers St, and 1 Ave & E 68 St. West 21 & 6 Ave is located in the Flatiron District neighborhood in Manhattan, there are many nearby parks and popular tourist locations which makes it a very popular station among tourists and the locals. West St & Chambers St is located near colleges, high schools, and Washington Park making it another popular destination in New York. 1 Ave & E 68 St is located in the Upper East Side and there are many food destinations and a park near the station, this could be another reason why this station is popular. Furthermore, looking at the chart, there is a significant difference between the most popular station and the least popular station. Even between the top two stations, we can see that West 21 st & 6 Ave is significantly more popular than West St & Chambers St, which shows that West 21 St and 6 Ave is a very popular bike station.")

## Weather component and bike usage page ##
elif page == "Weather Component and Bike Usage": 
    st.header("Daily Bike Rides and Temperatures")
    
    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df_temp['date'], y = df_temp['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df_temp['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df_temp['date'], y = df_temp['avgTemp'], name = 'Daily temperature', marker={'color': df_temp['avgTemp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 600
    )
    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("Looking at the line chart above, there is an obvious correlation between the temperatures and their relationships with the frequency of the bike trips taken daily. As the temperature lowers, the bike rides also lower, as the temperature rises the bike rides also rise. Furthermore, the temperature and bike rides follow closely with each other in the colder seasons, but in the hotter temperatures, the temperature is noticeably higher than the bike rides which makes sense because in hotter weather it can be challenging to be outside for long.")

## Interactive map Page ##
elif page == "Interactive Map With Aggregated Bike Trips":  
    # Add the map
    path_to_html = "NY_Bike_Trips_Aggregated.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    # Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)

    st.markdown("##### By using the filter on the left side, we can filter the map and check some of the most popular trips taken. ")
    st.markdown("Looking at the interactive map, we can see the most popular routes are 12 Ave & 40 St and Vesey St & Church St. If we look at where these stations are located on the map, we can see that these popular destinations are near the Hudson River and the World Trade Center. These results indicate that many tourists and locals may be renting bikes to go to these popular destinations.")

## Member vs Non-Member Page ##
elif page == 'Member Vs. Casual Riders':
    st.header("Member Vs Casual Riders")
    
    member = df[df['member_casual'] == 'member']
    casual = df[df['member_casual'] == 'casual']
    member_data = go.Histogram(x = member['avgTemp'], name = 'Member', marker = dict(color = 'red'))
    casual_data = go.Histogram(x = casual['avgTemp'], name = 'Casual', marker = dict(color = 'purple'))
    layout = go.Layout(
        title = 'Histogram of Member Vs. Casual by Temperature',
        xaxis = dict(title = 'Average Temperature'),
        yaxis = dict(title = 'Frequency'),
        barmode = 'overlay'
    )
    fig3 = go.Figure(data = [member_data, casual_data], layout = layout)
    st.plotly_chart(fig3)

    st.markdown("Looking at the histogram above, we can see that riders who are members use NY CitiBikes more than casual riders. The data also shows that more bikes are being used in warmer temperatures than in cooler temperatures,  however, members use the bike more than casual riders in warmer temperatures compared to the other temperatures")

## Recommendation Page ##
else:
    st.header("Conclusions and Recommendations")

    bikes = Image.open("bike_image.jpg") # source: https://unsplash.com/photos/assorted-commuter-bicycle-park-ahead-near-yellow-car-at-daytime-KEhNcoCldbk
    st.image(bikes)

    st.markdown("### Our analysis shows that NY CitiBikes should focus on the following objectives moving forwards:")
    st.markdown("- Some stations are more popular than other stations, most of these popular stations are located near the central park and popular tourist destinations. I recommend adding more bikes and bike parking to these locations since a lot of customers would go to these stations.")
    st.markdown("- Weather should be another factor the company considers for bike usage. The line chart shows a clear correlation between temperatures and daily bike trips. I recommend that the company ensures that the bikes are fully stocked during warmer seasons such as spring and summer to meet the higher demands. However, the company should also provide a lower supply during the colder seasons such as fall and winter to reduce costs.")
    st.markdown("- Members use the bikes more than the casual riders, especially in warmer temperatures. It would be a good idea for the company to do more marketing for memberships during warmer temperatures, especially during summer and spring.")
    
    
    
