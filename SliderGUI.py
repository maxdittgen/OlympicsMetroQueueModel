import streamlit as st
from StationCode import trains_needed_on_line, station_time

# Default parameter values
CAR_CAPACITY = 166
CARS_PER_TRAIN = 3
FARE = 2.25
OPERATING_COST = 10000
MIN_TRAIN_PER_HOUR = 10
BOARDING_RATE = 0.87 * 1.65 * 9
ALIGHT_RATE = 0.65 * 1.65 * 9
DEPART_RATE = 0.2

def main():
    st.title("Smart Queueing Model")

    col1, col2 = st.columns([4,3], gap="large")

    with col1:
        # Get demands from the user
        demands = st.text_area("Enter hourly demand at each station (comma-separated values):", "9000, 7500, 8000, 5000, 9000")

        # Convert demands to a list of integers
        demands_list = [int(x.strip()) for x in demands.split(',')]

        # Button to update values based on demands textbox
        if st.button("Update Demands"):
            demands_list = [int(x.strip()) for x in demands.split(',')]

        # Sliders for input parameters
        selected_day_index = st.select_slider('Day of the Week', options=list(range(7)), format_func=lambda x: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][x], value=3)
        car_capacity = st.slider("Car Capacity", 50, 300, CAR_CAPACITY, 1, key="car_capacity")
        cars_per_train = st.slider("Cars per Train", 1, 10, CARS_PER_TRAIN, 1, key="cars_per_train")
        # fare = st.slider("Fare", 1.0, 5.0, FARE, 0.25, key="fare")
        # operating_cost = st.slider("Operating Cost", 5000, 20000, OPERATING_COST, 500, key="operating_cost")
        min_train_per_hour = st.slider("Minimum Trains per Hour", 1, 20, MIN_TRAIN_PER_HOUR, 1, key="min_train_per_hour")
        boarding_rate = st.slider("Boarding Rate (People/Second)", 0.1, 2.0, BOARDING_RATE, 0.1, key="boarding_rate")
        alight_rate = st.slider("Alight Rate (People/Sec)", 0.1, 2.0, ALIGHT_RATE, 0.1, key="alight_rate")
        depart_rate = st.slider("Passenger Departure Rate", 0.05, 1.0, DEPART_RATE, 0.05, key="depart_rate")

        # get day of week
        selected_day = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][selected_day_index]

        # Calculate number of trains needed and fill rate
        trains_needed, fill_rate = trains_needed_on_line(
            demands_list, depart_rate, car_capacity, cars_per_train, min_train_per_hour
        )

        # Calculate station time
        station_time_value = station_time(
            demands_list, trains_needed, boarding_rate, alight_rate, depart_rate
        )

    with col2:
        # Display results
        st.header("Results:")
        st.write(f"Number of Trains Needed: {trains_needed}")
        st.write(f"Fill Rate: {fill_rate:.2%}")
        st.write(f"Average Station Time: {station_time_value:.2f} seconds")

if __name__ == "__main__":
    main()
