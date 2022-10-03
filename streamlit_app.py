
import streamlit 
import pandas as pd 
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some Fruits", list(my_fruit_list.index))

fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

def get_fruityadvice_data(fruit_choice):
  fruityvice_response = requests.get("http://fruityvice.com/api/fruit/" + fruit_choice)
  # Take the JSON version and normalize it 
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  # Output the JSON Version as a Table 
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please Select a Fruit to Get Information")
  else:
    streamlit.dataframe(get_fruityadvice_data(fruit_choice))
except URLError as e:
  streamlit.error()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+ new_fruit +"');")
    return 'Thanks for adding: ' + new_fruit

  
add_my_fruit = streamlit.text_input('Enter Food')
if streamlit.button("Add a Fruit to the List"):
  
  streamlit.write("Thanks for adding ", insert_row_snowflake(add_my_fruit))

my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.text("The Fruit List Contains: ")
streamlit.dataframe(my_data_rows)



