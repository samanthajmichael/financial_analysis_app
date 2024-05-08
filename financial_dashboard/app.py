import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import time
import millify as my
import calendar

pd.set_option('display.max_columns', None)

st.set_page_config(
    page_title= 'Financial Analysis Dashboard',
    layout='wide',
    initial_sidebar_state="expanded"
)

def hold_please():
    msg = st.toast(f"Hi, {name}!")
    time.sleep(1)
    msg.toast('Welcome to my interactive', icon="🔮")
    time.sleep(1)
    msg.toast('Financial Dashboard!', icon="💸",)
    time.sleep(1)
    msg.toast('Done!', icon = "✅")

#containers
header = st.container()
st.divider()
title = st.container()
select = st.container()
    
#enter name and date
with select:   
    column1, column2 = st.columns(2)

    with column1:
        name = st.text_input("Be sure to click enter!", on_change=hold_please)

    with column2:
        date_input = st.date_input(
            label="What is the date you are interested in analyzing?", 
            value=datetime.date(2022,12,31), min_value=datetime.date(2021,1,1), 
            max_value=datetime.date(2022,12,31), format="YYYY-MM-DD")

year_input = date_input.year
month_input = date_input.month
#date_input = datetime.date.today() # using this later

with title: 
    st.subheader('Please Enter Your Name.')
with select: 
    if st.button('Enter'):
        hold_please()
        time.sleep(2)

    with header: 
        st.title("Samantha's Financial Analysis")
        st.subheader('A Data-Driven Exploration of Spending Trends from 2021-2022') 

@st.cache_data
def load_data(csv):
    df=pd.read_csv(csv)
    return df

finance = load_data('data/finance.csv')
finance['Date'] = pd.to_datetime(finance['Date'], format='%Y-%m-%d')
finance_sorted = finance.sort_values('Category')

income = load_data('data/income.csv')
income['Date'] = pd.to_datetime(income['Date'], format='%Y-%m-%d')

slider = st.container()
with slider: 
    budget_mon = st.slider(
        "Set the date above and use the slider to update the Month and YTD Spend.", 
        min_value=0, max_value=15000, value=50, step=50)
    annual_budget = budget_mon*month_input
    spent_yr = finance.loc[finance['Year']==year_input]
    spent_mon = spent_yr.loc[spent_yr['Month']==month_input]

#spent per month/year variables
spent_total_mon = spent_yr.loc[spent_yr['Month']==month_input]['Debit'].sum().round(2)
spent_mon_var = ((spent_total_mon-budget_mon)*(-1)).round(2)
spent_total_yr = spent_yr['Debit'].sum().round(2)
yr_var = ((spent_total_yr-annual_budget)*(-1)).round(2)

#income variables
monthly_income = income.loc[income['Month'] == month_input, 'Income'].sum().round(2)
monthly_income_var = ((monthly_income - spent_total_mon) * (1)).round(2)

yearly_income = income.loc[income['Year'] == year_input, 'Income'].sum().round(2)
yearly_income_var = ((yearly_income - spent_total_yr) * (-1)).round(2)


st.sidebar.title('Filters:')
st.sidebar.subheader('For use with interactive charts')

expense_type = st.sidebar.multiselect(
    "Category:",
    options=finance_sorted["Category"].unique(),
    default=finance_sorted["Category"].unique()
)
month = st.sidebar.multiselect(
    "Month:",
    options=finance["Month"].unique(),
    default=finance["Month"].unique()
)
year = st.sidebar.multiselect(
    "Year:",
    options=finance["Year"].unique(),
    default=finance["Year"].unique()
)

if len(month) == 0 or len(year) == 0 or len(expense_type) == 0:
    st.error("Please select at least one month, one year, and one category to analyze.")
else:

    spent_mon_table = spent_mon.copy()
    spent_mon_query=spent_mon.query('Category == @expense_type')

    finance_query = finance.query("Year == @year & Month == @month & Category == @expense_type")

    stats = st.container()
    month = st.container()
    year = st.container()
    time_series = st.container()
    area = st.container()

    with stats: 
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader('Monthly Income')
            st.write('Based on the collected income data')
            monthly_income_format = my.prettify(monthly_income)
            monthly_income_var_format= my.prettify(monthly_income_var)
            st.metric(label=':heavy_dollar_sign:', 
            value=monthly_income_format, 
            delta=monthly_income_var_format, 
            label_visibility='hidden')
        with col2:
            st.subheader('YTD Income')
            st.write('Based on the collected income data')
            yearly_income_format = my.prettify(yearly_income)
            yearly_income_var_format= my.prettify(yearly_income_var)
            st.metric(label=':heavy_dollar_sign:', 
            value=yearly_income_format, 
            delta=yearly_income_var_format, 
            label_visibility='hidden')    
        with col3:
            st.subheader('Month Spend')
            st.write('Adjust your budget above to update')
            spent_total_mon_format = my.prettify(spent_total_mon)
            spent_mon_var_format= my.prettify(spent_mon_var)
            st.metric(label=':heavy_dollar_sign:', 
            value=spent_total_mon_format, 
            delta=spent_mon_var_format, 
            label_visibility='hidden')   
        with col4:    
            st.subheader('YTD Spend')
            st.write('Adjust your budget above to update')
            spent_total_yr_format = my.prettify(spent_total_yr)
            yr_var_format= my.prettify(yr_var)
            st.metric(label=':heavy_dollar_sign:', 
            value=spent_total_yr_format, 
            delta=yr_var_format, 
            label_visibility='hidden')
        st.divider()

    spent_mon_query_group = spent_mon_query.groupby(['Month','Year','Category'])['Debit'].sum().reset_index()
    spent_mon_query_group.columns = ['Month','Year','Category','Total Debits']
    spent_mon_query_sort = spent_mon_query_group.sort_values('Total Debits', ascending=False).head(10).reset_index(drop=True)

    with month:
        col_mon1, col_mon2 = st.columns(2)
        with col_mon1:
            st.subheader('Current Monthly Spending')
            st.write('Top 10 categories with the highest spend: to filter by category, use the sidebar.')
            spent_mon_fig = px.bar(spent_mon_query_sort, x='Category', y='Total Debits', color_discrete_sequence=px.colors.qualitative.Prism)
            spent_mon_fig.update_traces(hovertemplate="<b>Category: </b> %{x}<br><b>Total: $</b> %{y}<br>")
            spent_mon_fig.update_layout(margin= dict(t=0,l=0,r=0,b=0))
            st.plotly_chart(spent_mon_fig, use_container_width=True)

        with col_mon2:
            st.subheader('Ledger')
            st.write('Scroll to see transactions for the current month.')
            fig = go.Figure(data=go.Table(
                header=dict(
                    values=list(spent_mon_table[['Date', 'Account', 'Debit', 'Credit', 'Category']].columns),
                    align='center',
                    fill_color='#5F4690',
                    font=dict(color='#FFFFFF')
                ),
                cells=dict(
                    values=[
                        spent_mon_table.Date.dt.strftime('%m-%d-%Y'), 
                        spent_mon_table.Account, spent_mon_table.Debit, 
                        spent_mon_table.Credit, spent_mon_table.Category
                        ],
                    align='left'
                )
            ))
            fig.update_layout(margin= dict(t=0,l=0,r=0,b=0))
            st.plotly_chart(fig, use_container_width=True)


    spent_past_query=finance.copy()
    spent_past_query_group = spent_past_query.groupby(['Date', 'Account', 'Category'])[['Debit', 'Credit']].sum().round(2).reset_index()
    spent_past_query_group = spent_past_query_group.rename(columns={'Debit': 'Total Debits', 'Credit': 'Total Credits'})
    spent_past_query_ordered = spent_past_query_group.sort_values('Date', ascending=False)
    spent_past_query_ordered.columns = ['Date', 'Account', 'Category', 'Debit', 'Credit']
    spent_past_query_sort = spent_past_query_ordered.sort_values('Date', ascending=False).reset_index(drop=True)

    with year:
        st.subheader('Historical Ledger')
        st.write('Use the sidebar to filter by Month and Year')
        fig = go.Figure(data=go.Table(
            header=dict(
                values=list(spent_past_query_sort[['Date', 'Account', 'Debit', 'Credit', 'Category']].columns),
                fill_color='#6b4ea7',
                font=dict(color='#FFFFFF'),
                align='center'
            ),
            cells=dict(
                values=[
                    spent_past_query_sort.Date.dt.strftime('%m-%d-%Y'), 
                    spent_past_query_sort.Account, 
                    spent_past_query_sort.Debit, 
                    spent_past_query_sort.Credit, 
                    spent_past_query_sort.Category
                    ],
            align='left'
            )
        ))
        fig.update_layout(margin= dict(t=0,l=0,r=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with time_series:
        st.subheader('Spending Over Time')
        st.write("Use the filters in the sidebar to explore.")
        spend_by_year = finance_query.groupby(by=["Year"])[["Debit"]].sum().round(2).reset_index()
        credit_by_year = finance_query.groupby(by=["Year"])[["Credit"]].sum().round(2).reset_index()
        credit_by_year = credit_by_year.rename(columns={'Credit': 'Income'})
        income_table = income.groupby(by=["Year"])[["Income"]].sum().round(2).reset_index()

        combined = pd.merge(credit_by_year,income_table, how='inner', on='Year')
        combined['Income'] = combined['Income_x'] + combined['Income_y']
        combined.drop(['Income_x', 'Income_y'], axis=1, inplace=True)
        combined = combined.merge(spend_by_year, how='left', on='Year')
        combined = combined.rename(columns = {'Debit':'Debits'})
        combined_melted = combined.melt(id_vars='Year', var_name='Type', value_name='Amount')

        fig = px.bar(
            combined_melted, 
            x='Year', 
            y='Amount', 
            color='Type', 
            barmode='group', 
            color_discrete_sequence=['darkcyan', 'orange'])
        fig.update_layout(
                        title= 'Total Income and Debits by Year',
                        xaxis_title='Year',
                        yaxis_title='Amount',
                        title_x=0.35,
                        legend_title='Type')
        fig.update_traces(
            hovertemplate="<b>Year: </b> %{x}<br><b>Amount: $</b> %{y}<br>"
            )

        st.plotly_chart(fig, use_container_width=True)

    spend_by_year = finance_query.groupby(by=['Date'])[["Debit"]].sum().round(2).reset_index()
    spend_by_year = spend_by_year.rename(columns={'Debit': 'Debits'})
    credit_by_year = finance_query.groupby(by=['Date'])[["Credit"]].sum().round(2).reset_index()
    credit_by_year = credit_by_year.rename(columns={'Credit': 'Income'})
    income_table = income.groupby(by=['Date'])[["Income"]].sum().round(2).reset_index()

    dual = pd.merge(credit_by_year,income_table, how='left', on='Date')
    dual['Income'] = dual['Income_x'] + dual['Income_y']
    dual.drop(['Income_x', 'Income_y'], axis=1, inplace=True)
    dual = dual.merge(spend_by_year, how='left', on='Date')
    dual['Income'] = dual['Income'].fillna(0.00).astype(float)

    with area: 
        dual_cumulative = dual[['Debits', 'Income']].cumsum()
        fig1 = px.area(
            dual_cumulative, x=dual['Date'], 
            y=dual_cumulative.columns,
            color_discrete_map={'Income': 'darkcyan', 'Debits': 'orange'}
            )

        custom_text = ['Type: {}'.format(col) for col in dual_cumulative.columns]

        hover_template = (
            '<b>Type:</b>'
            '<b>Date:</b> %{x}<br>'
            '<b>Cumulative Amount:</b> $%{y:,.0f}'
        )

        fig1.update_traces(
            mode='lines+markers',
            hovertemplate=hover_template,
            customdata=dual_cumulative.columns
        )

        fig1.update_layout(
            title='Cumulative Income and Debits Over Time',
            legend_title='Transaction Type',
            xaxis_title="Date",
            yaxis_title="Cumulative Amount",
            title_x=0.35
        )

        fig1.update_xaxes(title_text="Date")
        fig1.update_yaxes(title_text="Cumulative Amount")

        st.plotly_chart(fig1, use_container_width=True)
