#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 09:59:13 2019

@author: vincientarnold

MOVIE DATA EXPLORATION 

For this project, we want to know a little bit about movie ratings by genre and over time. Since this unstructured data is a text file and genres are not listed as variables, 
we'll have to do some data wrangling with string methods in order to clean our data and get it in a form we can work with. First we'll clean, structure and process the data. 
Then we'll get some basic statistics; finally, we'll create some graphics to visualize 
trends in our data.  
"""
#%% Packages 
import numpy as np                         # NumPy for numeric things 
import pandas as pd                        # Pandas for data structuring
import matplotlib.pyplot as mp             # MatplotLib for data visualization 
import seaborn as sns; sns.set()           # seaborn for alternative visualization

#%% Creating a DataFrame --> tidy data 
movies = pd.Series(open('movies.txt').read().splitlines())              # reading in text file and splitting along lines 

names = pd.Series(movies.str.split("::").str[1])                        # splitting along double colon, turning to Series 
years = pd.Series(names.str[-6:])                                       # subsetting to the years, turning to Series  
years = years.str.strip("(")                                            # taking away the parentheses 
years = years.str.strip(")")                                            # taking away the parentheses 
years = pd.to_numeric(years)                                            # making numeric for future purpose 
indices = pd.to_numeric(pd.Series(movies.str.split("::").str[0]) )      # maintaining the original indices, making Series      
names = names.str[:-6]                                                  # taking the 'names' portion from the names and years 
genre = pd.Series(movies.str.split("::").str[2])                        # subsettting the genre out, making Series  
 
movie = pd.DataFrame({'MovieID': indices,                               # initiating dataframe for movie data 
                      'Names':names,
                      'Orig Names': pd.Series(movies.str.split("::").str[1]),
                      'Genres':genre,
                      'Year':years})

genre_list = ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
               "Film-Noir","Horror", "Musical","Mystery", "Romance", "Sci-Fi", "Thriller", "War","Western"]
# above making a list of all the genre names 
   
# here we encounter an issue: the genres are all listed in one column, so we'll need to make columns for each genre, filled with 0 or 1  
for i in genre_list:     # making columns for each genre, will be a 0 or a 1 (1* portion turns boolean numeric)
    word = i 
    movie[i] = 1*movie['Genres'].str.contains(i)
    
movie

### Rating Scores 
ratings = pd.DataFrame(pd.read_csv('ratings.dat', sep="::", header=None, names=("UserID","MovieID","Rating", "TimeStamp" ))) 
# above reading in ratings by movie 

movie = pd.merge(movie, ratings, on='MovieID')   # merging movie and rating  
#%%  Some Basic Statistics -- getting to know our data 
n = len(movie)                            # this gives us the sample size, n, which is the number of entries in the data set 
avg_rating = np.mean(movie['Rating'])     # this gives us the average rating for the movies 

Hist1 = sns.distplot(movie['Rating'], kde=False, rug=True)                     # histogram of all ratings, (named Hist1)

#%%
## Let's find average rating for each genre, over all the years ## 

def avg_rate(x):                                                               # defining a function to get average rating by genre
    genre_subset = movie[movie[x] == 1]                                        # subsetting to that specific genre via boolean 
    avg_rating = np.mean(genre_subset['Rating'])                               # taking the average of the rating for the subset
    return avg_rating 


rating = []
genre = []   
for i in genre_list:                                                           # initiating for loop to get averages 
    avg_rating = avg_rate(i)
    rating.append(avg_rating)
    genre.append(i) 
    
rating_by_genre = pd.DataFrame({'Genre':genre, 'Average Rating':rating})  
ratings = rating_by_genre.sort_values(by='Average Rating', ascending=False)

"""
          Genre  Average Rating
9     Film-Noir        4.075188
6   Documentary        3.933123
16          War        3.893327
7         Drama        3.766332
5         Crime        3.708679
2     Animation        3.684868
12      Mystery        3.668102
11      Musical        3.665519
17      Western        3.637770
13      Romance        3.607465
15     Thriller        3.570466
4        Comedy        3.522099
0        Action        3.491185
1     Adventure        3.477257
14       Sci-Fi        3.466521
8       Fantasy        3.447371
3    Children's        3.422035
10       Horror        3.215013

Takeaway: Horror, unsurprisingly, is the least popular, and surprisingly, we find film-noir to have the highest average rating. 
This may be explainable however by the few number of movies and ratings in that genre. 
"""
#%%   Now let's get some box plots for those ratings ## 

ratings = []
genres = []   
for i in genre_list: 
    ratings.append(movie[movie[i] == 1]['Rating'] )
    genres.append(i) 

ratings_by_genre = pd.DataFrame({'Action'      : ratings[0], 
                                 'Adventure'   : ratings[1],
                                 'Animation'   : ratings[2],
                                 "Children's"  : ratings[3],
                                 'Comedy'      : ratings[4], 
                                 'Crime'       : ratings[5], 
                                 'Documentary' : ratings[6],
                                 'Drama'       : ratings[7], 
                                 'Fantasy'     : ratings[8],
                                 'Film-Noir'   : ratings[9],
                                 'Horror'      : ratings[10],
                                 'Musical'     : ratings[11], 
                                 'Mystery'     : ratings[12], 
                                 'Romance'     : ratings[13], 
                                 'Sci-Fi'      : ratings[14], 
                                 'Thriller'    : ratings[15], 
                                 'War'         : ratings[16],
                                 'Western'     : ratings[17]})    
    
BoxPlot1 = sns.boxplot(data=ratings_by_genre, orient='h', fliersize=3)      # a bunch of boxplots for rating (named BoxPlot1)

#%%
## Let's determine the top 5 most common genres ##

percentages = []              # initiating list to count the percent of movies that are said genre 
for i in genre_list: 
    percent = (np.sum(movie[i] == 1) / n ) * 100   # summing (since boolean, sum is the same as the count of those that are true), dividing by length of dataset, getting percentage 
    percentages.append(percent)                    # appending to percentages list 

percents_by_genre = pd.DataFrame({'Genre':genre, 'Percent of Total': percentages})  # intiating dataframe with genres and percent total count
top_5 = percents_by_genre.sort_values(by='Percent of Total', ascending=False)[0:5]  # sorting largest to smallest by percentage of total and taking top 5 
genre_list2 = list(top_5['Genre'])                                                  # producing new genre list 

"""
       Genre         Percent of Total
4     Comedy         35.650549
7      Drama         35.445492
0     Action         25.740320
15  Thriller         18.964037
14    Sci-Fi         15.726113
""" 
#%%  Now let's get average rating by year for each of the top five genres 

dfrmlist = []
for i in genre_list2:                                                             # making dfrms from the genrre_list2
    gen_dfrm = movie[movie[i] == 1]
    gen_dfrm = pd.DataFrame(gen_dfrm['Rating'].groupby(gen_dfrm['Year']).mean()) 
    gen_dfrm['year'] = gen_dfrm.index
    dfrmlist.append (gen_dfrm)
    
# as you can see, the issue below is that we have a different number of years for each dfrm, so we'll need to merge carefully
comedy = dfrmlist[0]                    # type = DataFrame, (74, 2)
comedy.columns = ['comedy', 'year']
# note: between comedy and drama, the one row difference is bc comedy has a 1920 record, whereas drama does not; this type of issue will occur again 
drama = dfrmlist[1]                     # type = DataFrame, (75, 2) 
drama.columns = ['drama', 'year']

action = dfrmlist[2]                    # type = DataFrame, (52, 2) 
action.columns = ['action', 'year']

thriller = dfrmlist[3]                  # type = DataFrame, (67, 2)
thriller.columns = ['thriller', 'year']

sci_fi = dfrmlist[4]                    # type = DataFrame, (51, 2)
sci_fi.columns = ['sci-fi', 'year']

# below we'll merge the dataframes for genre, but we'll use the how='outer' argument so that we capture all the years 
# for example, if one dfrm has data for 1921 but another doesn't, we wanna keep 1921 and just put a nan value for the genre
# that doens't have data for that year; in this manner, we should get all years in which records were kept 
merge_1 = pd.merge(action, drama, on = "year", how='outer').sort_values(by='year')     
merge_2 = pd.merge(merge_1, comedy, on = "year", how='outer').sort_values(by='year') 
merge_3 = pd.merge(merge_2, thriller, on = "year", how='outer').sort_values(by='year') 
merged_genres = pd.merge(merge_3, sci_fi, on = "year", how='outer').sort_values(by='year') 

# here we rearrange the columns so that year comes first by 'remaking' the dataframe based on its own columns 
merged_genres = merged_genres[['year', 'action','comedy','drama', 'thriller','sci-fi']]  

#%% Now let's make a line plot to show the changing averages each year since 1950 of the top 3 most popular genres 

merged_genres_sub = merged_genres[['year', 'action','comedy','drama']]     # we only want the top three most popular genres
merged_genres_sub = merged_genres_sub[merged_genres_sub['year'] >= 1950]   # subsetting to years starting at 1950, since there's too much missing data before then
merged_genres_sub = merged_genres_sub.set_index('year')                    # setting the index to year, for plotting purposes 
gen_by_year_plot = sns.lineplot(data=merged_genres_sub)                    # line graph (saved as the variable name)

# Notably, all the average ratings decrease over time, and the volatility is pretty extreme, especially with action movies. 

#%% 