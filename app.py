import streamlit as st 
from billboard import ChartData 
import datetime 
from dateutil.rrule import rrule, YEARLY

def get_dates_from_date_till_now(start_date_str): 
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date() 
    today = datetime.date.today() 
    dates = [date.strftime('%Y-%m-%d') for date in rrule(YEARLY, dtstart=start_date, until=today)]
    dates = [date for date in dates if date >= "1958-08-04" ]
    return dates

@st.cache_data 
def get_first_each_year(date_input): 
    dates = get_dates_from_date_till_now(date_input) 
    my_bar = st.progress(0) 
    songs = {} 
    for n, date in enumerate(dates): 
        char = ChartData('hot-100', date=date, year=None, fetch=True, timeout=25)[0] 
        songs[date] = char.title + " by " + char.artist 
        my_bar.progress((n + 1) / len(dates)) 
    return songs

st.set_page_config(page_title="Get your first song of each year on your birthday", page_icon=":notes:", layout="wide")

st.title("Get your first song of each year on your birthday!")

st.markdown("Choose a birth date, and the app will fetch the first song that was at the top of the charts on that date each year.")

date = st.date_input("Select your birth date", datetime.datetime(2000, 1, 1), min_value=datetime.datetime(1900, 1, 1), max_value=datetime.date.today()).strftime('%Y-%m-%d')

if st.button('Get Songs'):
    songs = get_first_each_year(date)
    st.empty()
    st.write("Here are the first songs that were at the top of the charts on your birthday each year:") 
    for date, song in songs.items(): st.write(datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y') + ': ' + song)
