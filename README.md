Week-2-Investment-Analysis
Overview
This repository contains the work for Week 2 of the 10 Academy's Artificial Intelligence Mastery program. The project focuses on analyzing TellCo, a mobile service provider in the Republic of Pefkakia, to evaluate its potential as an acquisition target. The goal is to provide insights into customer behavior, engagement, and experience to help the investor assess the business's growth potential.
Project Objective
The project aims to analyze TellCo’s customer data and explore opportunities for business growth. The analysis is divided into four main tasks for this week:
1.	Task 1: User Overview Analysis: Understand user behavior, including top handset usage, data session metrics, and user engagement with applications like social media, YouTube, and gaming.
2.	Task 2: User Engagement Analysis: Evaluate user engagement metrics such as session frequency, duration, and traffic, and classify users into engagement clusters using k-means clustering.
3.	Task 3: Experience Analytics: Analyze user experience metrics, including network parameters and handset characteristics.
4.	Task 4: Satisfaction Analysis: Evaluate user satisfaction using engagement and experience metrics.
Data
The analysis uses xDR records from TellCo, which track user activities on various applications and network metrics like TCP retransmission, RTT, and throughput. The data is extracted from a PostgreSQL database.
Key Tasks
Task 1: User Overview Analysis
Objective: Identify insights into user behavior and handset usage.
•	Identify the top 10 handsets and top 3 manufacturers.
•	Aggregate session metrics: number of sessions, duration, and total data (DL + UL).
•	Perform univariate, bivariate, and correlation analysis on user data and application behavior.
•	Segment users into decile classes based on session duration.
•	Calculate total data usage across applications.
Task 2: User Engagement Analysis
Objective: Measure user engagement and segment users based on activity.
•	Aggregate session metrics (frequency, duration, total traffic) per user.
•	Normalize engagement metrics and apply k-means clustering to segment users into 3 engagement groups.
•	Identify the top engaged users and visualize engagement per application.
•	Use the elbow method to optimize the number of clusters for engagement.
Task 3: Experience Analytics
Objective: Analyze user experience metrics, including network parameters and handset characteristics.
•	Aggregate average TCP retransmission, RTT, throughput, and handset type per user.
•	Compute the top, bottom, and most frequent values for TCP, RTT, and throughput.
•	Perform k-means clustering to group users based on experience metrics.
Task 4: Satisfaction Analysis
Objective: Evaluate user satisfaction using engagement and experience metrics.
•	Assign engagement and experience scores to each user based on clustering results.
•	Calculate satisfaction scores as the average of engagement and experience scores.
•	Build a regression model to predict satisfaction scores.
•	Perform k-means clustering on engagement and experience scores and analyze satisfaction per cluster.
•	Export results to a local MySQL database.
Tools and Technologies
•	Python: For data analysis, machine learning, 
•	pandas, numpy: For data manipulation.
•	matplotlib, seaborn: For data visualization.
•	scikit-learn: For clustering and machine learning.
•	Streamlit: For building the dashboard.
•	PostgreSQL: For database management and data extraction.
Data Processing and Functions
Task 1: User Overview Analysis
•	Aggregation of User Behavior: Data is aggregated to understand session counts, total session duration, and total data usage (DL + UL) for each user, segmented by different application categories.
o	Function: aggregate_user_behavior(df)
o	Groups data by IMSI (user identifier) and aggregates key metrics like session counts and data usage per application.
•	Variable Transformation: Users are segmented into deciles based on session duration to analyze user behavior patterns and data consumption.
o	Function: perform_variable_transformations(df)
o	Segments users into 10 deciles based on session duration and calculates total data usage across all applications.
Task 2: User Engagement Analysis
•	K-means Clustering: Engagement is measured using session frequency, duration, and data usage, and users are grouped using the k-means clustering algorithm. 
o	Function: perform_kmeans_clustering(df)
o	K-means clustering is applied to segment users based on engagement metrics, and the elbow method is used to find the optimal number of clusters.
Task 3: Experience Analytics
•	Network Metrics Aggregation: User experience is assessed based on TCP retransmission, RTT, and throughput.
o	Function: aggregate_experience_metrics(df)
o	Aggregates network performance metrics to evaluate user experience.
•	K-means Clustering: Clusters users based on network performance metrics for segmentation.
o	Function: perform_experience_clustering(df)
Task 4: Satisfaction Analysis
•	Satisfaction Scoring: Combines engagement and experience scores to calculate overall satisfaction.
o	Function: calculate_satisfaction_scores(df)
o	Computes user satisfaction based on the average of engagement and experience scores.
•	Regression Model: Predicts satisfaction scores using regression analysis.
o	Function: build_satisfaction_model(df)
Folder Structure
Week-2-Investment-Analysis/
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows
│       ├── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
├── notebooks/
│   ├── data_load.ipynb
│   ├── task_1_and_2.ipynb
│   ├── task_3_and_4.ipynb
│   └── __init__.py
├── tests/
│   ├── __init__.py
├── scripts/
│   ├── data_analysis.py
│   ├── data_clearing.py
│   ├── data_exploration.py
│   ├── data_formatting.py
│   ├── Experience_analysis.py
│   ├── load_data.py
│   ├── Satisfaction_Analysis.py
│   ├── sql_queries.py
│   ├── user_overview_analysis.py
│   ├── __init__.py
│   └── README.md
├── screenshots/
│   └── [Contains all screenshots of the results when the code is run.]

