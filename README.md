# Twitter Sentiment Analysis
This repository shows the detailed instruction on how to collect tweets using Requests library and perform sentiment analysis to generate Trump approval rates by location. Finally, all results are visualized in Tableau.


## Data
Using Requests library to stream tweets (contain keyword: Trump) periodically. Only text and location fields are keeped. All cleaned and trimmed data are stored in **tweets_processed.txt**.

**AFINN-en-165.txt** is a list of English words rated for valence with an integer between minus five (negative) and plus five (positive). The words have been manually labeled by Finn Årup Nielsen in 2009-2011. The file is used to perform NLP.

**us_cities_states_counties.csv** contains all US cities and states, which is used to filter locations.

**uscity_38148_population.csv** contains longitude and latitude associate with each city. Population is also included. This file is used in Tableau map in order to add extra details for visualization.

**Trump Approval Rating from Tweets.twbx** Tableau Packaged Workbooks

## Algorithm
Please **see tweets_main.py**

## AWS EC2 Instruction
[AWS EC2 with Spark.txt]( https://github.com/sxl5507/Twitter-Sentiment-Analysis/blob/master/instruction/AWS%20EC2%20with%20Spark.txt) shows instruction of how to setup environment and install pyspark with Jupyter Notebook in AWS EC2 Ubuntu.

