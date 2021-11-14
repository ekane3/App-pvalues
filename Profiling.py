from pandas_profiling import ProfileReport
import pandas as pd

#  Load the data
train_2020 = pd.read_csv('full_2020.csv')

#  Create a profile report
profile = ProfileReport(train_2016, title='Analyse des transactions immobilières en France en 2016', html={'style':{'full_width':True}},minimal=True)

#  Save the profile report
profile.to_notebook_iframe()


