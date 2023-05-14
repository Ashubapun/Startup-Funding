import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import pyplot.express as px

st.set_page_config(layout = 'wide', page_title = 'StartUp Analysis')

df = pd.read_csv('Startup_cleaned.csv')

df['Date'] = pd.to_datetime(df['Date'], errors="coerce")

df['year'] = df['Date'].dt.year

df['month'] = df['Date'].dt.month

def load_investor(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['Investor'].str.contains(investor)].head()[['Date', 'Startup Name', 'Vertical', 'City', 'Round', 'Amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # top 5 biggest investments
        big_series = df[df['Investor'].str.contains(investor)].groupby('Startup Name')['Amount'].sum().sort_values(ascending = False).head()
        st.subheader('5 Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['Investor'].str.contains(investor)].groupby('Vertical')['Amount'].sum()

        st.subheader('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels = vertical_series.index, autopct = '%0.2f%%')
        st.pyplot(fig1)

    with col3:
        stage_series = df[df['Investor'].str.contains(investor)].groupby('Round')['Amount'].sum()

        st.subheader('Stages Invested On')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_series, labels = stage_series.index, autopct = '%0.2f%%')
        st.pyplot(fig2)

    with col4:
        city_series = df[df['Investor'].str.contains(investor)].groupby('City')['Amount'].sum()

        st.subheader('Sectors Invested In')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels = city_series.index, autopct = '%0.2f%%')
        st.pyplot(fig3)

    year_series = df[df['Investor'].str.contains(investor)].groupby('year')['Amount'].sum()

    st.subheader('Year On Year Investments')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)
    st.pyplot(fig4)


def load_startup(startup):
    st.title(startup)

def load_overall_analysis():
    st.title('Overall Analysis')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # total invested amount
        total = round(df['Amount'].sum())
        st.metric('Total Invested Amount', str(total) + ' Cr')

    with col2:
        # maximum amount infused in a startup
        maximum = round(df.groupby('Startup Name')['Amount'].max().sort_values(ascending = False).head(1).values[0])
        st.metric('Maximum Amount Infused in a StartUp', str(maximum) + ' Cr')

    with col3:
        # average amount invested in startup
        # average ticket size
        avg_funding = round(df.groupby('Startup Name')['Amount'].sum().mean())
        st.metric('Average Amount Invested in StartUp', str(avg_funding) + ' Cr')

    with col4:
        # total funded startup
        num_startup = df['Startup Name'].nunique()
        st.metric('Total Funded StartUps', num_startup)

    st.header("Month on Month Graph")
    selected_option = st.selectbox("Select Type", ['Total', 'Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['Amount'].sum().reset_index()
        temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df['x-axis'], temp_df['Amount'])
        plt.xticks(rotation = 90)
        st.pyplot(fig5)
    else:
        temp_df = df.groupby(['year', 'month'])['Amount'].count().reset_index()
        temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        fig6, ax6 = plt.subplots()
        ax6.plot(temp_df['x-axis'], temp_df['Amount'])
        plt.xticks(rotation=90)
        st.pyplot(fig6)



st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp', df['Startup Name'].unique())
    btn1 = st.sidebar.button("Find StartUp Details")
    if btn1 :
        load_startup(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['Investor'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor(selected_investor)


