import sys
import time
import datetime
import calendar
import pandas as pd
import numpy as np
print('python version: ', sys.version)
print('pandas version: ', pd.__version__)
print('numpy version: ', np.__version__)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = ''
    month = ''
    day = ''
    is_city_available = False
    while (city not in CITY_DATA.keys()):
        available_cities = ['Chicago', 'New York City', 'Washington']

        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Which city's data would you like to see - {}: ".format(available_cities)).lower()
        print()

        if city in CITY_DATA.keys():
            is_city_available = True
        else:
            print("The city name {} is not inclued in the bike share analysis. The available cities are {} ".format(city,available_cities))   
            answer = input("Would you like to try another city (Y/N)?\n")

            if answer.upper() == 'N':
                quit()
            elif answer.upper() == 'Y':
                continue
            else:
                while answer not in ["Y", "N"]:
                    print('{} is NOT an available option. Please, select from: {}'.format(answer, ["Y", "N"]))
                    answer = input('\nWould you like to try another city (Y/N)?\n')
            if answer.upper() == 'N':
                quit()
            elif answer.upper() == 'Y':
                continue
                
    if (is_city_available) :
        
        # Get user input for month ('All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun')
        available_month = ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        
        while (month.title() not in available_month):
            month = input("Which month's data would you like to see?\nAvailable month input: {}: \n".format(available_month))
            print()
            if month.title() in available_month:
                break
            else:
                print("{} is NOT a valid month. Please provide valid month input".format(month))
        
        # Get user input for day of week (all, monday, tuesday, ... sunday)
        available_day = ['All', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        while (day.title() not in available_day):
            day = input("Which day's data would you like to see?\nAvailable day input: {}: \n".format(available_day))
            print()
            if day.title() in available_day:
                break
            else:
                print("{} is NOT a valid day of the week. Please provide valid day input".format(day))

        
            
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    #loading the specific city's raw data 
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    #print(df)

    # filter by month if applicable
    if month.title() != 'All':
        # Create dictionaly months calendar to get the corresponding 3 character input
        months = {}
        months = {month: index for index, month in enumerate(calendar.month_abbr) if month}
        month = months[month.title()]
        #print('the chosen month is {}'.format(month))

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        #print(df['month'])

    # filter by day of week if applicable
    if day.title() != 'All':
        days = {}
        days = {day: index for index, day in enumerate(calendar.day_abbr) if day}
        day = days[day.title()]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
        #print(df['day_of_week'])

    return df

def display_data(df):
    """
    Display 5 rows of the indivial trip data until the user input is "no"
    The input value must be either yes or no
    """
    # get  5 rows of the indivial trip data until the user says "no"
    view_raw_data = input("Would you like to see the first 5 rows of the individual trip data? Enter yes or no\n").lower()
    start_loc = 0
    while (view_raw_data=='yes'):
        if view_raw_data=='yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_raw_data = input("Do you wish to see 5 more rows?").lower()
            if view_raw_data=='no':
                break
            else:
                while (view_raw_data not in ('yes','no')):
                    print('Please enter yes or no')
                    view_raw_data = input("Do you wish to see 5 more rows?").lower()


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...in month, day and hour\n')
    start_time = time.time()

    # the following stat will only be displayed when month == all. it doesn't make sense to display the analysis when the specific day is passed
    # display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Popular month :\n', calendar.month_name[popular_month])
    else:
        print('Most Popular month data analysis will be only provided when you choose all')

    # the following stat will only be displayed when day == all. it doesn't make sense to display the analysis when the specific day is passed
    # display the most common day of week
    #df['week'] = df['Start Time'].dt.weekday
    if day == 'all':
        popular_day_of_week = df['day_of_week'].mode()[0]
        print('Most Popular day of week:\n', calendar.day_name[popular_day_of_week])
    else:
        print('Most Popular day of week data analysis will be only provided when you choose all')


    # Display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # Find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:\n {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station_counts = df['Start Station'].value_counts().head(1)
    print("Most Commonly Used Start Station & Counts")
    print("-----------------------------------------")
    print(start_station_counts.to_string())
    print()


    # Display most commonly used end station
    end_station_counts = df['End Station'].value_counts().head(1)
    print("Most Commonly Used End Wtation & Counts")
    print("---------------------------------------")
    print(end_station_counts.to_string())
    print()


    # Display most frequent combination of start station and end station trip
    frequent_combination_station_counts = df[['Start Station','End Station']].value_counts().head(1)
    print("Most Commonly Used Start & End Stations  &  Counts")
    print("--------------------------------------------------")
    print(frequent_combination_station_counts.to_string())
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration ...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = int(df['Trip Duration'].sum())
    print("Total trip duration is:\n{}\n".format(convert_duration_readable(total_trip_duration)))

    # display mean travel time
    average_trip_duration = df['Trip Duration'].mean()
    print("Average trip duration is:\n{}\n".format(convert_duration_readable(average_trip_duration)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_duration_readable(duration):
    """Converting duration values - seconds - to days, hours, minutes and seconds."""
    timedelta_duration = datetime.timedelta(seconds=duration)
    days = timedelta_duration.days
    hours = timedelta_duration.seconds/3600
    minutes = (timedelta_duration.seconds/60)%60
    seconds = timedelta_duration.seconds%60
    
    return '{} days, {} hours, {} minutes, {} seconds'.format(int(days), int(hours), int(minutes), seconds)
    
  
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats on User Type, Gender and Birth Year\n')
    start_time = time.time()

    try:
    # Display counts of user types
        user_types = df['User Type'].value_counts()
        print("Each user type & Counts")
        print("-----------------------")
        print(user_types.to_string())
    except(ValueError, KeyError):
        print("There is no User Type data")

    print()

    try:
        # Display counts of gender
        user_types = df['Gender'].value_counts()
        print("Each gender & Counts")
        print("--------------------")
        print(user_types.to_string())
    except(ValueError, KeyError):
        print("There is no Gender data")
        
    print()
    
    try:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        print("The earliest birth year among users: {}".format(earliest_birth_year))
        recent_birth_year = int(df['Birth Year'].max())
        print("The most recent birth year among users: {}".format(recent_birth_year))
        common_birth_year = int(df['Birth Year'].mode())
        print("The most common birth year among users: {}".format(common_birth_year))
    except(ValueError, KeyError):
        print("There is no Birth Year data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    
    while True:
        try:
            city, month, day = get_filters()
            print( "You have requested the data analsis for {} using month: {} and day: {} ".format(city.title(), month.title(), day.title()))
            answer = input('Would you like to proceed? Enter yes or no. \n').lower()
            if answer == 'yes':
                df = load_data(city, month, day)
                time_stats(df,month,day)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                display_data(df)
                restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
                if restart == 'yes':
                    continue
                elif restart == 'no':
                    break
                else:
                    while restart not in ["yes", "no"]:
                        print('{} is NOT an available option. Please, select from: {}'.format(restart, ["yes", "no"]))
                        restart = input('\nWould you like to restart? Enter "yes" or "no".\n').lower()
                
                if restart == 'yes':
                    continue
                elif restart == 'no':
                    break

        except (ValueError, KeyboardInterrupt) :
            print("the operation has been interrupted - {} ".format(KeyboardInterrupt))
            break


if __name__ == "__main__":
	main()
