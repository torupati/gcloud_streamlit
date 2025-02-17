import streamlit as st
import numpy as np

st.write("Here's our first attempt at using data to create a table:")

#st.write("Hello world")
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(df)
st.write('st.dataframe')
st.dataframe(df.style.highlight_max(axis=0))
st.write('st.table')
st.table(df)


chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.write('------------------------------------------------')
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

from PIL import Image

file_path = st.file_uploader('', type=['png', 'jpg', 'jpeg'])

img = np.random.randint(255, size=(100, 200, 3))
#img = Image.open(file_path)
st.image(img)

