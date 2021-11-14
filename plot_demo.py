import streamlit as st
import time
import numpy as np
import seaborn as sns
import pandas as pd


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1,1)
chart = st.line_chart(last_rows)

for i in range(1,101):
    new_rows = last_rows[-1:] + np.random.randn(5,1).cumsum(axis=0)
    
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    status_text.text('The latest random value is %.3f' % i)
    last_rows = new_rows
    time.sleep(0.1)

progress_bar.empty()


df = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 30, 70]})
sns.lineplot(x='x', y='y', data=df)
st.pyplot()
#Streamlit widgets automatically run the script from top to bottom.
#So, we can use the progress bar to show the progress of the script.

st.button('Re-run')

# do a function of streamlit chart



