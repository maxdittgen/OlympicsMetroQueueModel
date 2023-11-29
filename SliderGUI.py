import streamlit as st
from streamlit_modal import Modal
from StationCode import trains_needed_on_line, station_time
from SmartPredictor import get_demands, get_percentage_increase

# Default parameter values
CAR_CAPACITY = 166
CARS_PER_TRAIN = 3
FARE = 2.25
OPERATING_COST = 10000
MIN_TRAIN_PER_DAY = 120
BOARDING_RATE = 0.87 * 1.65 * 9
ALIGHT_RATE = 0.65 * 1.65 * 9
DEPART_RATE = 0.2

def main():
    st.title("Paris Metro Line 10 Olympics Queuing Model")

    col1, col2 = st.columns([4,3], gap="large")

    with col1:
        # Get demands from the user
        demands = st.text_area("Enter yesterday's passenger demand for each station on Line 10 (comma-separated values), or \"n/a\" if this is the first day : \
                               Please include 16 demand figures--one for each station on line 10.", "22671, 11854, 4051, 4524, 12508, 4080, 12424, 2792, 9241, 4121, 17618, 3877, 10126, 6267, 430, 5670")

        # Convert demands to a list of integers
        if demands == "n/a":
            demands_list = []
        else:
            demands_list = [int(x.strip()) for x in demands.split(',')]

        # Button to update values based on demands textbox
        if st.button("Update Demands"):
            demands_list = [int(x.strip()) for x in demands.split(',')]

        # Sliders for input parameters
        selected_day_index = st.select_slider('Day of the Week', options=list(range(7)), format_func=lambda x: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][x], value=3)
        car_capacity = st.slider("Car Capacity  \n:gray[ Passenger capacity of each subway car]", 50, 300, CAR_CAPACITY, 1, key="car_capacity")
        cars_per_train = st.slider("Cars per Train  \n:gray[ Number of subway cars on each train]", 1, 10, CARS_PER_TRAIN, 1, key="cars_per_train")
        # fare = st.slider("Fare", 1.0, 5.0, FARE, 0.25, key="fare")
        # operating_cost = st.slider("Operating Cost", 5000, 20000, OPERATING_COST, 500, key="operating_cost")
        min_train_per_hour = st.slider("Minimum Trains per Day  \n:gray[ The minimum operating frequency of trains per day]", 1, 200, MIN_TRAIN_PER_DAY, 1, key="min_train_per_hour")
        boarding_rate = st.slider("Boarding Rate (People/Second)   \n:gray[ Rate at which people can board each subway car]", 0.1, 20.0, BOARDING_RATE, 0.1, key="boarding_rate")
        alight_rate = st.slider("Alight Rate (People/Sec)   \n:gray[ Rate at which people can leave each subway car]", 0.1, 20.0, ALIGHT_RATE, 0.1, key="alight_rate")
        depart_rate = st.slider("Passenger Departure Rate  \n:gray[ Proportion of passengers who depart at each station]", 0.05, 1.0, DEPART_RATE, 0.05, key="depart_rate")

        # give option to reset defaults
        if st.button("Reset Defaults"):
            car_capacity = CAR_CAPACITY
            del st.session_state.car_capacity
            st.session_state.car_capacity = CAR_CAPACITY
            cars_per_train = CARS_PER_TRAIN
            del st.session_state.cars_per_train
            st.session_state.cars_per_train = CARS_PER_TRAIN
            # fare = FARE
            # del st.session_state.fare
            # st.session_state.fare = FARE
            # operating_cost = OPERATING_COST
            # del st.session_state.operating_cost
            # st.session_state.operating_cost = OPERATING_COST
            min_train_per_hour = MIN_TRAIN_PER_DAY
            del st.session_state.min_train_per_hour
            st.session_state.min_train_per_hour = MIN_TRAIN_PER_DAY
            boarding_rate = BOARDING_RATE
            del st.session_state.boarding_rate
            st.session_state.boarding_rate = BOARDING_RATE
            alight_rate = ALIGHT_RATE
            del st.session_state.alight_rate
            st.session_state.alight_rate = ALIGHT_RATE
            depart_rate = DEPART_RATE
            del st.session_state.depart_rate
            st.session_state.depart_rate = DEPART_RATE
            st.rerun()

        # get day of week
        selected_day = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][selected_day_index]

        # Calculate demand for day based on predicted demands on day of week and yesterday's demand
        demands = get_demands(selected_day, demands_list)

        # Calculate change in demand versus a normal day
        percent_change = get_percentage_increase(selected_day, demands)

        # Calculate number of trains needed and fill rate
        trains_needed, fill_rate = trains_needed_on_line(
            demands, depart_rate, car_capacity, cars_per_train, min_train_per_hour
        )

        # Calculate station time
        station_time_value = station_time(
            demands, trains_needed, boarding_rate, alight_rate, depart_rate
        )

    with col2:
        # Display results
        st.header("Today's Metro Forecast:")
        st.write(f"Demand Increase: {percent_change}%")
        st.write(f"Number of Trains Needed: {trains_needed}")
        st.write(f"Fill Rate: {fill_rate:.2%}")
        st.write(f"Average Station Time: {station_time_value:.2f} seconds")
        

if __name__ == "__main__":
    main()
