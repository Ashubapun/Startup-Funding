import streamlit as st
import pandas as pd

st.title('First Dashboard')

email = st.text_input('Enter Email')
password  = st.text_input('Enter the Password')
st.selectbox('Select Gender',['Male','Female','Others'])

file = st.file_uploader('Upload a csv file')

if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.head())

btn = st.button('Login')
if btn:
    if email == 'abcd@gmail.com' and password == '1234':
        st.success('Login Successful!')
        st.balloons()
    else:
        st.error('Login Failed!')

