import pandas as pd
import numpy as np

# NOTE:
## double hashtag means it's one of my comments, # just means a comment included in the boilerplate starting code

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")


    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df["race"].value_counts() ## By far easiest way to do this

    # What is the average age of men?
    manfilt = df["sex"] == "Male"  
    
    ## This really annoyed me, the tests won't accept your answer unless it's in the perfect number of decimals they want
    ## even if it's correct
    average_age_men =  np.round(  df[manfilt].mean(numeric_only=True)["age"]  , decimals=1)

    # What is the percentage of people who have a Bachelor's degree?
    ## Ditto here and for lots of the other parts of this exercise
    ## Easy way to do this by just using the normalize keyword on valuecounts
    percentage_bachelors = np.round(  df["education"].value_counts(normalize=True)["Bachelors"] * 100 ,decimals=1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    ## Made these separate so it's easier to read and the code makes more intuitive sense
    edufilt = df["education"].isin(["Bachelors","Masters","Doctorate"])
    moneyfilt = df["salary"] == ">50K"

    ## Wasn't sure what these were meant for?
    higher_education =  None
    lower_education = None

    # percentage with salary >50K
    ## Basic percentage calculating here
    higher_education_rich = np.round( 100* ( len( df[edufilt & moneyfilt] ) / len(df[edufilt])) , decimals=1)
    lower_education_rich = np.round( 100 * (len(df[~edufilt & moneyfilt ]) / len(df[~edufilt])) , decimals=1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min() ## I love numpy

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    
    ## In general I prefer to explicitly declare my filter series before using them, makes it easier to read
    minhoursfilt = df["hours-per-week"] == min_work_hours
    
    ## Again not sure why this keyword was needed
    num_min_workers = None

    ## Many of the problems here are just percentage questions really, I should've made a percentage calculating function
    ## Unfortunately this requires 2 decimals of precision, and this was not specified by the challenge, had to find out the hard way
    rich_percentage = np.round(  100 * ( len(df[minhoursfilt & moneyfilt]) / len(df[minhoursfilt]) ) , decimals=2)

    # What country has the highest percentage of people that earn >50K?
    
    ## This took much longer to do than I would've thought, I still (as of writing) need more experience with groupby
    mostrichppl = df.groupby(["native-country"]).apply(
        ## Calculate the percentage for each country, then just select the highest percentage in the next line 
        lambda countrydata : np.round( 100* ( len ( countrydata[countrydata["salary"] == ">50K"]) / len(countrydata) ) , decimals=1) )
    
    ## This will give us the country immediately as the indices are the countries themselves, very useful pandas feature
    highest_earning_country = mostrichppl.idxmax()
    
    ## Now we have the highest earning country, since our groupby has already collected the percentages, just get the percentage value of
    ## the highest earning country, which we've already found
    highest_earning_country_percentage = mostrichppl[highest_earning_country]
    

    # Identify the most popular occupation for those who earn >50K in India.
    
    ## Much nicer than the above, I was expecting another hard groupby question
    indianfilt = df["native-country"] == "India" 
    top_IN_occupation = df[moneyfilt & indianfilt]["occupation"].value_counts().idxmax()
    


    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

for k,v in calculate_demographic_data().items():
    print(k,v)