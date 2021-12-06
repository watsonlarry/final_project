# Probing the Relationship Between Education and Homelessness in the USA
Authors: Kim Horany, Roy Mojica, Lawrence Watson

## Summary

- Topic: Predicting the severity of homelessness in the United states and how it correlates with education by examining the relationship between the two. 

- Why topic was selected: The swift and unexpected onset of a global health crisis in 2020 led many states to issue stay-at-home orders to curtail the rate of infection.  Without homes to retreat to, our homeless population was most vulnerable during the pandemic. We may not be able to predict or control the next devastating public health crisis, but is there an aspect to homelessness that we might govern to reduce the size of those affected? That is what we hope to discover.  With the focus on education, an area in which there is plenty of data, we hope to discove a method to make accurate projections on the number of homeless

## Data Source

We are using two CSVs which we pulled from Kaggle.com. The first dataset, 2007-2016_Homelessness_USA.csv, contains counts of homeless by state, Continuum of Care (CoC), and severity of homelessness. The second dataset, state_all.csv, contains education data such as, counts of individuals by state, year, grade level, and math/reading scores. Both raw datasets are stored here: Machine Learning > Resources > Raw

## Questions to Answer

- Will homelessness counts increase or decrease in future years?

- How does education level affect homelessness?

## Presentation & Visualizations

[Google Slides Presentation](https://docs.google.com/presentation/d/1qcjNdUe6113w7axp-y-amXODMnWzwdU2P95df5-UpWs/edit?usp=sharing)


[Tableau Dashboard Link](https://public.tableau.com/profile/lawrence.watson#!/vizhome/FinalProject-HomlessnessEducationintheUSA/DataExplorationThroughVisualization)


## Process

### Step 1: Data Exploration & Cleaning

Before diving into describing the Machine Learning model and the database, lets go over how we got the data ready for consumption. The code to do this is stored in the Machine Learning folder: clean_data.ipynb, preprocess_data.ipynb. 

Description of preliminary data preprocessing:

   - Homeless Dataset

     - Read raw data from CSV

     - Drop unneeded columns – we decided that the shelter name (CoC) and the Measures column was not relevant to the data

     - Create a key column that will allow us to join to the education dataset

       - Extract year from Year column

       - Concatenate year with state, ex: 2007_AK

     - Group the data by State_Year, Year, State to aggregate the counts

     - Replace Nan values with 0

   - Education dataset

     - Read raw data from CSV 

     - Drop unneeded columns - by checking null counts on the columns, we discovered these columns contained too many nulls: ENROLL, OTHER_EXPENDITURE, AVG_MATH_4_SCORE, AVG_MATH_8_SCORE, AVG_READING_4_SCORE, AVG_READING_8_SCORE. In addition, we decided to drop STATE_REVENUE, LOCAL_REVENUE, INSTRUCTION_EXPENDITURE, SUPPORT_SERVICES_EXPENDITURE, and CAPITAL_OUTLAY_EXPENDITURE to simplify the model and focus just on columns related to counts of students enrolled at school. 

     - Create a key column that will allow us to join to homeless dataset

       - Convert long state name to abbreviated state: ALASKA --> AK

       - Concatenate year with state, ex: 2007_AK

     - Replace remaining NaN values with zeros

     - Convert floats to int

Cleaned Homeless Data:

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/cleaned_homeless.png"/>

Cleaned Education Data:

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/cleaned_education.png"/>

### Step 2: Build Database & Integrate 

To house our data, we built a database in Postgres. We created two tables: one to house the cleaned homeless data and the other to house the cleaned education data.

ERD:

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/ERD.png"/>

After we created our two tables, we knew that we wanted to join the data before feeding it to the machine learning model. For the join, we performed an inner join on the primary key column, State_Year, which is available in both tables. We stored this data in a table: homeless_edu.

Join & Table Creation Statement (found in Database folder, querey.txt):

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/merge_join.png"/>

To integrate the data from our Postgres database, we imported psycopg2 then used the following code, which can also be found in the Machine Learning folder at the top of the machine_learning_final.ipynb file:

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/connect_postgres.png"/>

### Step 3: Data Exploration

In order to get a better idea of which features to include in our model, we first did a quick data exploration exercise. 

The processed data was connected to Tableau to make a few visualizations to familiarize ourselves with the data and search for any useful trends. The visualizations are sourced from the processed_education.csv and processed_homeless.csv files (located at Machine Learning > Resources). The two data sources are then joined via an inner join on State_Year. 

   - Bubble Chart Viz
      - Values: States, Total Homeless, Total Educational Expenditure
      - Description: Data occurs over 10 year period. Total homeless value as a percentage of State population is represented w/ dimensions of bubble labeled by State. Red gradient applied to bubble represents the total educational expenditure of the state ($25million-$1billion). Primary observation is that the states that spend the most on education have the largest homeless populations--however these states are also the most populous.

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/bubble_chart.png"/>

   - Decade Heat Map Viz
         - Values: Years, States, Total Homeless
         - Description: A heat map to display the homeless population in each state for every year 2007-2016. Essentially we're running the same information form the last visualization but with each year of the decade represented by its own color value. The purpose is to see if there any state made progress over time w/ diminishing its homelessness numbers. There were no states that made an obvious trend downward with its numbers. Most maintained steady, unwavering numbers. 
        
<img src="https://github.com/kimcheese33/final_project/blob/main/Images/state_heat_over_time.png"/>

- Enrolled v. Sheltered Line Viz 
         - Values: Years, Total Homeless, Enrolled Grade School Students, States
         - Description: Testing another educational value from our data set, we mapped sheltered homeless numbers against k-12 student enrollment numbers from each state over the ten year period. Again, little was gleaned. As the number of students rose so did the homeless population. No state had a trend that performed differently. 

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/competing_%20line_graphs.png"/>

Though, that our data was stable across all states over time, boded well for our machine learning model's predictive potential. 

- Interactive Comprehensive Data Map
         - Values: Total Homeless, Enrolled Students, Educational Expenditure, States, Years
         - Description: An overview map of the United States that allows us to compare the values of multiple fields against each other. One or many states and/or years can be selected to view the total homeless, enrolled student, and educational expenditure values in the chosen range. Using the map is a quick way to check the data on any of our identified patterns.

<img src="https://github.com/kimcheese33/final_project/blob/watson/segment_4/Images/data_map.png">

Due to the nature of our data and what we are hoping to achieve, we knew that we would be doing a linear regression. This means that we need to take a look at each variable and the relationship it has with Homeless_Count, our dependent variable. To do this, we used the Seaborn's pairplot to visualize the relationship. After looking at each variable, we can see that they all have a fairly weak relationship with Homeless_Count. However, it looks like TOTAL_EXPENDITURE and TOTAL_REVENUE have the best relationship. In Step 5, we will discuss how we came to our final model.


<img src="https://github.com/kimcheese33/final_project/blob/main/Images/seaborn1.png"/>

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/seaborn2.png"/>

This code can be viewed in machine_learning_final.ipynb file in the Machine Learning folder.

### Step 4: Feature Engineering & Splitting the Data

Preliminary feature engineering included scaling the features using Standard Scaler. We also chose to drop State as this is a categorical variable that should not be included in the model. We chose the features for the final model to be the Year, TOTAL_REVENUE, TOTAL_EXPENDITURE, GRADES_PK_G,GRADES_KG_G,GRADES_4_G,GRADES_8_G,GRADES_12_G,GRADES_1_8_G,GRADES_9_12_G,GRADES_ALL_G columns to be the features. We wanted to see if this combination of columns could be used to accurately predict homeless counts for subsequent years. We also split the data into training and testing sets using sklearn's train_test_split. Then we split the Year and State data manually: first 75% of rows is the training set and the remaining 25% is the testing set. The code for this can be found in the Machine Learning folder in the machine_learning_final.ipynb file.

### Step 5: Machine Learning Model

Now that we have our data ready, it's finally time to put together the model. The model we chose to use is a Multiple Linear Regression Model. We chose this model, because we are wanting to predict the count of homeless people, a dependent variable, by looking at multiple independent variables. The advantages of using a linear regression is that it gives information about the relevance of features and is simple to implement and interpret. The disadvantages are that linear regression can be susceptible to overfitting. However, this can be fixed by reducing dimensions, which we attempt below. It's worth mentioning that we intially wanted to break down the homeless count by sheletered homeless, unsheltered homeless, and other homeless situations and perform a Multivariate Regression. However, we decided we would be able to interpret the results better if we simplify, so we used a Multiple regression instead.

To determine how well the model is doing, we used four statistical measures: R Squared, Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RSME). The R Squared value tells us goodness of fit; it measures the strength of the relationship between the model and the dependent variable. MAE tells us the absolute difference of the data and the model's predictions. The MSE is like the MAE except we are squaring the difference; this means that outliers will cause the error to grow quadratically instead of proportionally. Finally, the RMSE is the square root of MSE; taking the square root converts the metric back to similar units as the inputs. Outliers are still a big contributing factor to this error value.

 We iterated through the machine learning model several times to try and get the best outcome by adding/removing features to see what the effect would be. For each attempt, the X features changed but the model code itself was the same:

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/model.png"/>

 #### Attempt 1: All Features

For our first attempt, we decided to include all the features, except State. Our results show an R Squared of 93.22%, an MAE of 20304.48, MSE of 995095019.37, and an RMSE of 31545.13.

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/ml_all.png"/>

This code can be viewed in machine_learning_final.ipynb file in the Machine Learning folder.

#### Attempt 2: All Except Pre K

For our second attempt, we decided to include all features, except State and GRADES_PK_G. This is because when looking at our graphs from the exploratory phase (see above), we can see that the GRADES_PK_G graph has values that deviate more from the line. For this attempt our results show an R Squared of 93.05%, an MAE of 20500.56, an MSE of 1019401083.26, and an RMSE of 31928.06.

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/ml_prek.png"/>

This code can be viewed in machine_learning_no_prek.ipynb file in the Machine Learning folder.

#### Attempt 3: Only Total Expenditure and Total Revenue

For our last attempt, we decided to only include TOTAL_REVENUE and TOTAL_EXPENDITURE as the features. This is because from our exploratory graphs we saw that these two variables had the best looking relationship with Homeless_Count. For this attempt we got an R Squared of 78.97%, an MAE of 30281.50, and MSE of 3085178327.84, and an RMSE of 55544.38.

<img src="https://github.com/kimcheese33/final_project/blob/main/Images/ml_noedu.png"/>

This code can be viewed in machine_learning_no_edu.ipynb file in the Machine Learning folder.

#### Model Analysis

Based off the results from our three attempts it looks like the best outcome was our first attempt, including all features in the model. Although this was our best attempt, the outcome is still not very good. The MAE, MSE, and RMSE values are all very high, which indicates bad model performance. This could be due to too many zeroes in the data and/or many outliers. 

## Conclusion

While we were able to build a model that could make predictions on what homeless counts would be, the accuracy of this model definitely  has room for improvement. With our Machine Learning visualizations we were able to see that the more students enrolled at school, the more homeless there are in that state. However, this is more likely due to higher population in that state, rather than education itself. In future attempts we could improve our model by trying to get a larger dataset, get different variables related to education (SAT scores, graduation rates, etc.), and/or prune the data more to reduce missing data (NaN's replaced by zeroes). 
