# Streamlit App
### Author: Emile EKANE
### Date: 2021-11-14
### Link : https://share.streamlit.io/ekane3/app-pvalues/App.py
<br><br>

# Description

Why this project ? So in this project, we will be using the [Streamlit](https://streamlit.io/) framework to create a web application that will allow us to explore the data of the property values requests /annual files of refunds of transfers for valuable consideration from France from 2016 to 2020. You can see the open data through this [link](https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres/)  
To do a good data exploration we had to pass by several steps such as : the loading of our data,preprocessing and cleaning then finally exploration step and decision making.
<br><br>

# 1 - Data loading
Normally to load the data we use the method read_csv of [pandas](https://pandas.pydata.org/) library by passing the path of the file.
Our file normally is in our folder called full_data.csv.But to the huge size of the file , we couldnt upload it on github so we had to download it from  [jtellier](https://jtellier.fr/DataViz/full_2020.csv) website.  
We loaded up to 1 million rows of data in our dataframe.

<br>

# 2 - Data preprocessing
Like every other dataset, some preprocessing is always a good idea.  
So with our dataframe, we jad to drop the columns that we dont need and to change the type of the columns that we need.  
Replace some Nan by 0.  
Create some columns that we will use later from others.  
To know in advance varibles that we will use later, we can use the method describe of pandas library to get the description of our dataframe or simply use panda profiling.

<br>

# 3 - Data exploration
Streamlit is a powerful tool to create interactive web applications.
It has a lot of features, such as charts, tables, and widgets.In our project we used the following features : bar chart, line chart, histogram, pie chart, and map.
2 pages : one for description and one for the data exploration.
<br>

# 4 - To run the app
(0) Clone the repository  
(1) Install Streamlit : pip install streamlit  
(2) Run the app : streamlit run App.py  
(3) Open the app : http://localhost:8501/  
(4) Explore the data & make a decision  
(5) Enjoy the app








