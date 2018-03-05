# Twitter Sentiment Analysis
This repository shows the instruction on how to collect tweets using Requests library and perform sentiment analysis to generate Trump approval rates by location. Finally, all results are visualized in Tableau.

<br></br>
 **Graph can be acessed using this [link](https://public.tableau.com/views/TrumpApprovalRatingfromTweets/Dashboard1?:embed=y&:display_count=yes)**
<div class='tableauPlaceholder' id='viz1520272334804' style='position: relative'><noscript><a href='#'><img alt='Trump Approval Rating from Tweets ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Tr&#47;TrumpApprovalRatingfromTweets&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TrumpApprovalRatingfromTweets&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Tr&#47;TrumpApprovalRatingfromTweets&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                



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

