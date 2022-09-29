
import streamlit 
import pandas as pd 

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.multiselect("Pick some Fruits", list(my_fruit_list.index), ['Apple', 'Avocado'])
streamlit.dataframe(my_fruit_list)
