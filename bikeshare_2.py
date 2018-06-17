import time
import pandas as pd
#import numpy as np

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
    #Create the list of cities, months and days to store the valid values 
    months = ['all','january','february','march','april','may','june']
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please specify the city you want to analyze (Chicago,New York City, Washington):")
    while city.lower() not in CITY_DATA:
        print("You have entered a city which is not in my datastore.")
        city = input("Please specify the city you want to analyze (Chicago,New York City, Washington):")
    
    # get user input for month (all, january, february, ... , june)
    month = input("Please specify the month (all, january, february, ... , june):")
    while month.lower() not in months:
        print("You have entered an incorrect month")
        month = input("Please specify the month (all, january, february, ... , june):")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please specify the day of the week (all, monday, tuesday, ... sunday):")
    while day.lower() not in days:
        print("You have entered an incorrect day of week")
        day = input("Please specify the day of the week (all, monday, tuesday, ... sunday):")
    print('-'*40)
    return city.lower(), month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df["month"]==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"]==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = months[pd.to_datetime(df["Start Time"]).dt.month.mode()[0]-1]
    print("Most common month is {}.".format(common_month))

    # display the most common day of week
    common_day_of_week = pd.to_datetime(df["Start Time"]).dt.weekday_name.mode()[0]
    print("\nMost common day of week is {}.".format(common_day_of_week))

    # display the most common start hour
    common_start_hour = pd.to_datetime(df["Start Time"]).dt.hour.mode()[0]
    print("\nMost common start hour is {}.".format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print("Most commonly used Start station is \"{}\".".format(common_start_station))

    # display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print("\nMost commonly used End station is \"{}\".".format(common_end_station))

    # display most frequent combination of start station and end station trip
    df["Station Combination"] = df["Start Station"] + " - "+ df["End Station"]
    common_combination_station = df["Station Combination"].mode()[0]
    print("\nMost frequent combination of Start and End station trip is \"{}\".".format(common_combination_station))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    total_travel_time = df["Trip Duration"].sum()
    travel_time_hours = total_travel_time // (60*60)
    travel_time_minutes = (total_travel_time // 60)-(travel_time_hours * 60)
    travel_time_seconds = total_travel_time % 60
    
    # display total travel time
    print("Total travel time is {} hours {} minutes and {} seconds.".format(travel_time_hours,travel_time_minutes,travel_time_seconds))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    mean_travel_minutes = mean_travel_time // 60
    mean_travel_seconds = mean_travel_time % 60
    print("\nMean travel time is {} minutes and {} seconds.".format(mean_travel_minutes,mean_travel_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here are the counts of user types:\n")
    print(df["User Type"].value_counts())

    # Display counts of gender
    if("Gender" in df):
        print("\nHere are the counts of gender:")
        print(df["Gender"].value_counts())
    else:
        print("\nNo Gender information in file to analyze")

    # Display earliest, most recent, and most common year of birth
    if("Birth Year" in df):
        earliest_birth_year = df["Birth Year"].min()
        print("\nEarliest year of birth is {}.".format(str(int(earliest_birth_year))))
        recent_birth_year = df["Birth Year"].max()
        print("\nMost recent year of birth is {}.".format(str(int(recent_birth_year))))
        common_birth_year = df["Birth Year"].mode()[0]
        print("\nMost common year of birth is {}.".format(str(int(common_birth_year))))
    else:
        print("\nNo Birth Year information in file to analyze")
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
