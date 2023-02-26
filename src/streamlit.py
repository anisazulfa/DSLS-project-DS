import streamlit as st
import requests
from PIL import Image

# Load and set images in the first place
header_images = Image.open('assets/banner.png')
st.image(header_images)

# Add some information about the service
# st.title("Time prediction to travel traffic jam")
st.subheader("Just enter variabel below then click Predict button :sunglasses:")

# Create form of input
with st.form(key = "air_data_form"):
    jam_level = st.number_input(
        label = "Enter jam level:",
        min_value = 0,
        max_value = 5,
        help = "0=free flow; 1=80-61% of free flow; 2=61-41% of free flow; 3=40-21% of free flow; 4=20-1% of free flow;"
    )
    median_length = st.number_input(
        label = "Enter irregularity length in meter:",
        min_value = 0.00,
        max_value = 20000.00,
        format = "%.2f",
        help = "Continous value range from 0 to 20000"
    )
    median_delay_seconds = st.number_input(
        label = "Enter delay in seconds from regular speed:",
        min_value = 0.00,
        max_value = 4000.00,
        format = "%.2f",
        help = "Continous value range from 0 to 4000"
    )
    median_regular_speed = st.number_input(
        label = "Enter historical regular speed in segment in kmh:",
        min_value = 0.00,
        max_value = 350.00,
        format = "%.2f",
        help = "Continous value range from 0 to 350"
    )
    total_records = st.number_input(
        label = "Enter total data recorded:",
        min_value = 1,
        max_value = 200,
        help = "Continous value range from 1 to 200"
    )
    median_speed = st.number_input(
        label = "Enter traffic speed in irregularity:",
        min_value = 0.00,
        max_value = 60.00,
        format = "%.2f",
        help = "Continous value range from 0 to 60"
    )

     # Create button to submit the form
    submitted = st.form_submit_button("Predict")

    # Condition when form submitted
    if submitted:
        # Create dict of all data in the form
        raw_data = {
            "jam_level" : jam_level,
            "median_length" : median_length,
            "median_delay_seconds" : median_delay_seconds,
            "median_regular_speed" : median_regular_speed,
            "total_records" : total_records,
            "median_speed" : median_speed
        }
        # Create loading animation while predicting
        with st.spinner("Sending data to prediction server ..."):
            res = requests.post("http://localhost:8080/predict", json = raw_data).json()
            
        # Parse the prediction result
        if res["error_msg"] != "":
            st.error("Error Occurs While Predicting: {}".format(res["error_msg"]))
        else:
            st.success(res["res"])
