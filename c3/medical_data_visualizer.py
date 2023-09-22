import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# NOTE:
## double hashtag means it's one of my comments, # just means a comment included in the boilerplate starting code

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
## Height is in cm so /100 to turn into metres
bmi = df["weight"] / ( df["height"] / 100) **2 > 25
df['overweight'] = bmi.apply(lambda x : 1 if x else 0)


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

## I found the wording of the above very confusing, since I didn't understand which value they meant by "make the value 0"
## Eventually I figured that they must've just meant the values of cholesterol and gluc since they're the only ones they stated
df["gluc"] = df["gluc"].apply(lambda x : 0 if x == 1 else 1)
df["cholesterol"] = df["cholesterol"].apply(lambda x : 0 if x ==1 else 1)

cardiofilt = df["cardio"] == 1

## This will be used in the wide-to-long conversion
nonidcolnames = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']






# Draw Categorical Plot
def draw_cat_plot():
    
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    
    ## I understand the idea of wide-to-long conversion , but I can't fully wrap my head around making id_vars a different variable
    ## This was the only part of the entire course I had to seek help for, I just couldn't get it at the time
    df_cat = pd.melt(df, id_vars="cardio", value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    ## Got stuck on this too until I discovered the size() function, need reset_index() because there's only 1 index for each "cardio" type otherwise
    df_cat = df_cat.groupby(["cardio","variable","value"]).size().reset_index()
    df_cat = df_cat.rename(columns={0 : "total"})
    
    ## Seaborn won't let you plot based on numerical values
    df_cat["value"] = df_cat["value"].astype(str)

    # Draw the catplot with 'sns.catplot()'
    bars = sns.catplot(data=df_cat, 
                       x="variable",
                       y="total",
                       hue="value",
                       col="cardio",
                       kind="bar")


    # Get the figure for the output
    fig = plt.gcf()


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    
    ## I was very confused on this because the course literally gives you the code by themselves, you just copy-paste it
    ## Decided to make these separate both for clarity and in case another related question came up that needed one of these filts separately
    pressure_filt = df["ap_lo"] <= df["ap_hi"]
    height_filt = (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975))
    weight_filt = (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))
    
    
    # Clean the data
    df_heat = df[pressure_filt & height_filt & weight_filt]
    

    # Calculate the correlation matrix
    ## I wouldn't have known how to do this by myself, so I'm glad this pandas function exists
    corr =  df_heat.corr()
    
    # Generate a mask for the upper triangle
    ## Googled how to do this on stack overflow, you need ones_like or there's errors in the masking
    mask = np.triu(np.ones_like(corr))

    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    ## I added some extra formaatting to make mine look like the example figure
    the_heatmap = sns.heatmap(data=corr,linewidths=0.5, annot=True, mask=mask, fmt="0.1f" )


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

draw_heat_map()