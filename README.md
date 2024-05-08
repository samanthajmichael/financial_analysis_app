# Financial Analysis Streamlit App
## A Data-Driven Exploration of Spending Trends from 2021-2022
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://a-financial-analysis-app.streamlit.app/)

In 2022, I decided to create a budget to track my expenditures and see how I was spending my money. The goal was to identify any trends or hidden patterns that could help improve my financial well-being. 

# Data Sources & Preparation:
The data was collected from my personal financial statements and stored in a google sheet. For this app, I connected to the Google API to access the data. A link has been cited below with a tutorial that you can follow if you want to try this for yourself. 

The data was cleaned in python and google sheets. There is an 'clean_data.ipynb' file in the repo that outlines the data manipulation.

# Dashboard Features
- Monthly and Yearly Financial Statistics
- Analyze 10 categories with the highest spend. This is the default but you can filter for specific categories with the sidebar 
- View the selected month's ledger and view the historical ledger 
- Analyze the Income and Debits and how they change over time
- See the cumulative Income and Debits for the selected years 

# Running the App
[Streamlit App](https://a-financial-analysis-app.streamlit.app/)

## After forking the repo: 
1. Open terminal and use command `pip -r requirements.txt` to install required packages an version numbers. 
2. Run with terminal command `streamlit run app.py`
3. Optional: Use the `import data.ipynb` file to import your data from googlesheets
4. Optional: Run the `clean_data.ipynb` to clean the data and concatenate multiple sheets into a single dataframe

# Future work:
I plan to add more data for years 2023 and 2024. I also hope to add a file uploader so that I can upload data directly into Streamlit when it is current.
I would also like to add a 'Select All' check box to the sidebar to select all categories.

## Resources: 
[Medium Article - Reading Google Sheets into a Pandas Dataframe](https://medium.com/@vince.shields913/reading-google-sheets-into-a-pandas-dataframe-with-gspread-and-oauth2-375b932be7bf)

Connecting to Google Sheets API -- Ensure you give access to google sheets api (not explictly stated in the tutorial)

[Streamlit Documentation](https://docs.streamlit.io/)
