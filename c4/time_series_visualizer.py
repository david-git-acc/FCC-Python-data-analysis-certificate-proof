import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# NOTE:
## double hashtag means it's one of my comments, # just means a comment included in the boilerplate starting code

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",parse_dates=True, index_col="date")

## Decided to do this in one line since I didn't expect there'd be any specific subdivision based on one condition but not the other
topbottomfilt = ( df["value"] < df["value"].quantile(0.975) ) & (df["value"] > df["value"].quantile(0.025))

# Clean data
df = df[topbottomfilt]

## Entering these manually was faster than searching for a datetime function to convert them into their natural names
## After searching it now (this is after I did the challenge), there's a calendar module but I don't want to have to import another module
## With replit unfortunately I had to install all the modules for each individual challenge which was annoying
months = ["January","February","March","April","May","June","July","August","September","October","November","December"]


## Out of the 3 plots, this was by far the fastest and easiest for me to do, as no data manipulation is required
def draw_line_plot():
    # Draw line plot
    
    fig, ax = plt.subplots()
    
    ## Fairly self-explanatory
    lineplot = ax.plot(df.index, df["value"],color="red" )
    
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

## Made this minifunction because 2016 had 4 months missing, since presumably they didn't start recording until April/May
## Just checks the difference in months and adds the required number of missing numbers
def prepend_list(arr):
    if len(arr) < 4:
        diff = 4-len(arr)
        return diff*[0] + arr
    return arr

## This was slightly irritating because the course told me to group by year, whereas in matplotlib to do multiple bar charts with months
## you actually need to group by month instead. I really tried to make the years groupby work but this was so much faster for me
def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    
    ## A very time-saving feature
    df_bar = df.resample("M").mean()
    
    ## Declare the month column so we can group the values by it
    df_bar["month"] = df_bar.index.month
    
    ## Turn each year for that month (e.g July 2016, July 2017, July 2018, July 2019) into a list and then convert back into a dataframe
    ## This way of doing it lends itself naturally to extracting it into matplotlib and plotting it
    df_bar = pd.DataFrame( df_bar.groupby("month").apply(lambda x : list(x["value"])) )
    
    ## Need to transpose so the months are columns, that way I can call each month by df[month]
    df_bar = df_bar.rename(columns = {0 : "yearlyvalues"}).T
    
    years = np.arange(2016,2019+1)

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(9,6))
    
    ## I initially chose 0.2 but it was too thick for the graph, the bars crashed into each other
    ## This width gives us a reasonably close estimate to the example figure so I chose this
    barwidth = 0.05
    
    ## Now we'll plot each month one-by-one, each month draws one bar for each year 2016-2019
    for month in range(1,12+1):     
        plt.bar(np.arange(4)+month*barwidth , 
                prepend_list(df_bar[month][0]), ## Need [0] to actually get the list itself from the dataframe, here is where prepend_list is useful
                width= barwidth, 
                label=months[month-1]) ## This is where months is useful, easier than importing an entire new module
    
    ## I wanted the ticks to look like in the example - set them at their positions + half the width of each mini-barchart to put in the middle
    ax.set_xticks(np.arange(4) + 12 * barwidth / 2)
    ax.set_xticklabels(years,rotation="vertical") # Again the example has them vertically so I'll also align the labels vertically
    
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")



    # Save image and return fig (don't change this part)
    plt.legend()
    fig.savefig('bar_plot.png')
    return fig

## This part was quick since there was no data manipulation involved, I had to brush up on my seaborn boxplots though
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    ## Rename the columns to match how they looked in the example figure
    df_box = df_box.rename(columns={"year" : "Year" , "value" : "Page Views","month" : "Month"})

    # Draw box plots (using Seaborn)
    fig, (ax1,ax2) = plt.subplots(ncols=2,nrows=1)
    
    ## Just pull from the data, no need for complicated manipulation here
    boxes1 = sns.boxplot(x="Year",y ="Page Views", data=df_box, ax=ax1)

    ax1.set_title("Year-wise Box Plot (Trend)")

    ## Need to define the ordering for this one, I don't know why it didn't start in January, maybe because 2016 had no January-April?
    boxes2 = sns.boxplot(x="Month", y= "Page Views", data=df_box, order=[x[0:3] for x in months],ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't chSange this part)
    fig.savefig('box_plot.png')
    return fig


draw_box_plot()