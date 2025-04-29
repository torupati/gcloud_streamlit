import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Folium Map in Streamlit")

# Initial settings
default_latitude = 35.6895
default_longitude = 139.6917
default_zoom = 13

# State management for map parameters using session_state
if 'latitude' not in st.session_state:
    st.session_state['latitude'] = default_latitude
if 'longitude' not in st.session_state:
    st.session_state['longitude'] = default_longitude
if 'zoom' not in st.session_state:
    st.session_state['zoom'] = default_zoom

def create_map(lat, lon, zoom):
    """Creates a new Folium Map object."""
    m = folium.Map(location=[lat, lon], zoom_start=zoom)
    folium.Marker([lat, lon], popup="Selected Location").add_to(m)
    return m

st.sidebar.header("Map Settings")
new_latitude = st.sidebar.number_input("Latitude", value=st.session_state['latitude'])
new_longitude = st.sidebar.number_input("Longitude", value=st.session_state['longitude'])
new_zoom = st.sidebar.slider("Zoom Level", 1, 18, st.session_state['zoom'])

if st.sidebar.button("Update Map"):
    st.session_state['latitude'] = new_latitude
    st.session_state['longitude'] = new_longitude
    st.session_state['zoom'] = new_zoom

# Create and display the map based on the values in session_state
m = create_map(st.session_state['latitude'], st.session_state['longitude'], st.session_state['zoom'])
st_folium(m, width=700, height=500, key="map")