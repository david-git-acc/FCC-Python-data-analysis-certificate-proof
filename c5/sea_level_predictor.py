import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

# NOTE:
## double hashtag means it's one of my comments, # just means a comment included in the boilerplate starting code
        
def draw_plot():
    # Read data from file
    df = pd.read_csv("epa-sea-level.csv")

    ## Some people may not like this way of defining things but I think it's good for when the variables are associated with each other
    X,Y=( df["Year"].values,
          df["CSIRO Adjusted Sea Level"].values )

    ## Didn't know when the data started, too lazy to find out
    X2050 = np.arange(X.min(), 2050+1)

    # Create scatter plot
    ## Wanted to give them clear and defining colours so they wouldn't get confused and easy to see and read the plots
    ## When I finished this, I went back here and added a label since I'd done this for both regression lines so good to explain things more
    scatter = plt.scatter(X,Y,c="green", label="Data points")

    # Create first line of best fit
    best_fit1 = linregress(X,Y)
    
    ## Again, I like this way of defining things, since these quantities are linked
    m1,b1 = (best_fit1.slope,best_fit1.intercept)
    
    ## The course explicitly said I should put this plot OVER the scatter plot, 
    ## so I set zorder to 10 (even though it was already over it)
    ## Also added a label so the plot makes more sense
    bestfit1plot = plt.plot(X2050,m1*X2050+b1,label="All-data prediction", color="blue",zorder=10)

    # Create second line of best fit
    ## Again I like to manually declare my boolean series for clarity/readability
    from_2000s = df["Year"] >= 2000
    data2000s_onwards = df[from_2000s]
    
    ## Get the new values when only accounting for 2000s data
    ## Wasn't sure if it'd work without specifying .values which makes it into a numpy array, so better to do it and be safe imo
    X2,Y2 = (data2000s_onwards["Year"].values,
             data2000s_onwards["CSIRO Adjusted Sea Level"].values)
    
    ## Same approach, but only 2 lines so not going to make a function for it
    best_fit2 = linregress(X2,Y2)
    m2,b2 = (best_fit2.slope,best_fit2.intercept)
    
    ## Figured since it's data from the 2000s only I should start there, again added a label for clarity
    newX=np.arange(2000,2050+1)
    bestfit2plot = plt.plot(newX,m2*newX+b2, label="Prediction from 2000s+ data", color="red")

    # Add labels and title
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.title("Rise in Sea Level")

    plt.legend()
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
    
    
    
draw_plot()