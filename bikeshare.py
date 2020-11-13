import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months=['january', 'february','march','april','may', 'june']
days=['mo','tu','wed','thu','fri','sa','su']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input('\nWould You like to see data for chicago , new york city or washington :  \n')
    while (city.lower() not in CITY_DATA) :
        city=input('Invalid input Please Enter city as seen here :chicago , new york city or washington \n')
    city=city.lower()
    # get user input for month (all, january, february, ... , june)
    msg_1=input('Great!, it seems You select {} , Would You like to filter by month ?: \'yes\' or \'No\'\n'.format(city))
    while (msg_1.lower()!='no' and msg_1.lower()!='yes') :
        msg_1=input('Invalid input Please Type : \'yes\' or \'No\' to select Filter or not \n')
    if (msg_1.lower()=='no') :
        month='all'
    if (msg_1.lower()=='yes') :
        month=input('Which month ?: january, february, .. , june \n' )
        while (month.lower() not in months) :
            month=input('Invalid Input Please Select Month : january, february, .. , june \n' )
    month=month.lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    msg_2=input('Would You like to filter by day ?: \'yes\' or \'No\'\n')
    while (msg_2.lower()!='no' and msg_2.lower()!='yes') :
        msg_2=input('Invalid input Please Type : \'yes\' or \'No\' to select Filter or not \n')
    if (msg_2.lower()=='no') :
        day='all'
    if (msg_2.lower()=='yes') :
        day=input('Which day ?: su, mo, tu, wed, thu, fri, sa \n' )
        while (day.lower() not in days) :
            day=input('Invalid Input Please Select day : su, mo, tu, wed, thu, fri, sa \n' )
    day=day.lower()
    print(city)
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
    df=pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    
    # filter by month to create the new dataframe	
    if(month !='all') :
        # use the index of the months list to get the corresponding int
        month=months.index(month)+1
        df=df[df['month']==month]
    # filter by day of week if applicable
    if (day != 'all'):
        # filter by day of week to create the new dataframe
        day=days.index(day)
        df = df[df['day_of_week']== day]
    
    return df

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()

    # display mean travel time
    avg_travel_time=df['Trip Duration'].mean()
    
    print("Total Trip Duration is : {} seconds \n".format(total_travel_time))
    print("Average Trip Duration is : {} seconds \n".format(avg_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
   
    # Display counts of user types
    user_type_count=df['User Type'].value_counts()

    # Display counts of gender
    if city=='washington' :
        print("OOPs! No Data For Gender & Year of birth available \n")
    else:
        gender_count=df['Gender'].value_counts()
        # Display earliest, most recent, and most common year of birth
        earliest=df['Birth Year'].min()
        most_recent=df['Birth Year'].max()
        common=df['Birth Year'].mode()[0]
        print("Counts of user types is \n{}\n".format(user_type_count))
        print('*'*20)
        print("Counts of Gender is \n{}\n".format(gender_count))
        print('*'*20)
        print("Earliest Year Of Birth is {} \n".format(earliest))
        print("Most Recent Year Of Birth is {} \n".format(most_recent))
        print("Common Year Of Birth is {} \n\n".format(common))
        
    print("Counts of user types is \n{}\n".format(user_type_count))
    print('*'*20)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def time_stats(df): 
    """Displays statistics on the most frequent times of travel."""
    weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # extract month , day of week and hour from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday
    df['hour']=df['Start Time'].dt.hour
    # display the most common month
    common_month=df['month'].mode()[0]
    mon=months[common_month-1]
    # display the most common day of week
    common_day=df['day_of_week'].mode()[0]
    da=weekdays[common_day]
    # display the most common start hour
    common_hour=df['hour'].mode()[0]
   
    print("Most Common Month : {} \n".format(mon))
    print("Most Common Day Of Week : {} \n".format(da))
    print("Most Common hour : {} \n".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df['Start Station'].mode()[0]

    # display most commonly used end station
    common_end_station=df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+df['End Station']
    combin=df['combination'].mode()[0]
    
    print("Most Common Used Start Station is : {} \n".format(common_start_station))
    print("Most Common Used end Station is : {} \n".format(common_end_station))
    print("most frequent combination of start station and end station trip : {} \n".format(combin))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
