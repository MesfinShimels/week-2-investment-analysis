Week-2-Investment-Analysis
Overview
This repository contains the work for Week 2 of the 10 Academy's Artificial Intelligence Mastery program. The project focuses on analyzing TellCo, a mobile service provider in the Republic of Pefkakia, to evaluate its potential as an acquisition target. The goal is to provide insights into customer behavior, engagement, and experience to help the investor assess the business's growth potential.
Project Objective
The project aims to analyze TellCo’s customer data and explore opportunities for business growth. The analysis is divided into two main tasks for this week:
1.Task 1: User Overview Analysis: Understand user behavior, including top handset usage, data session metrics, and user engagement with applications like social media, YouTube, and gaming.
2.Task 2: User Engagement Analysis: Evaluate user engagement metrics such as session frequency, duration, and traffic, and classify users into engagement clusters using k-means clustering.
Data
The analysis uses xDR records from TellCo, which track user activities on various applications and network metrics like TCP retransmission, RTT, and throughput. The data is extracted from a PostgreSQL database, and the schema is provided.
Key Tasks
Task 1: User Overview Analysis
Objective: Identify insights into user behavior and handset usage.
Identify the top 10 handsets and top 3 manufacturers.
Aggregate session metrics: number of sessions, duration, and total data (DL + UL).
Perform univariate, bivariate, and correlation analysis on user data and application behavior.
Segment users into decile classes based on session duration.
Calculate total data usage across applications.
Task 2: User Engagement Analysis
Objective: Measure user engagement and segment users based on activity.
Aggregate session metrics (frequency, duration, total traffic) per user.
Normalize engagement metrics and apply k-means clustering to segment users into 3 engagement groups.
Identify the top engaged users and visualize engagement per application.
Use the elbow method to optimize the number of clusters for engagement.
Tools and Technologies
Python: For data analysis, machine learning, and dashboard development.
pandas, numpy: For data manipulation.
matplotlib, seaborn: For data visualization.
scikit-learn: For clustering and machine learning.
Streamlit: For building the dashboard.
PostgreSQL: For database management and data extraction.
Data Processing and Functions
Task 1: User Overview Analysis

Aggregation of User Behavior: Data is aggregated to understand session counts, total session duration, and total data usage (DL + UL) for each user, segmented by different application categories.

oFunction: aggregate_user_behavior(df)
oIt groups data by IMSI (user identifier) and aggregates key metrics like session counts and data usage per application.

Variable Transformation: Users are segmented into deciles based on session duration to analyze user behavior patterns and data consumption.

oFunction: perform_variable_transformations(df)
oSegments users into 10 deciles based on session duration and calculates total data usage across all applications.
Task 2: User Engagement Analysis
K-means Clustering: Engagement is measured using session frequency, duration, and data usage, and users are grouped using the k-means clustering algorithm. 
oFunction: perform_kmeans_clustering(df)
oK-means clustering is applied to segment users based on engagement metrics, and the elbow method is used to find the optimal number of clusters.
Next Steps
Continue to build on the findings from Tasks 3, 4, and 5.
Analyze user experience and satisfaction in subsequent tasks.
Develop an interactive Streamlit dashboard to visualize the analysis and communicate insights.
