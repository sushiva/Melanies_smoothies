# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col



name_on_order = st.text_input("Name on Smoothie!")
st.write("The name on your Smoothie will be", name_on_order)

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """**Choose the Fruit you want in your Smoothie!**
  """
)


# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe =  session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingradients_list = st.multiselect(
    "Chose upto 5 ingradients",    
     my_dataframe,
     max_selections=5
)

if ingradients_list:
    ingredients_string = '' 
    for fruit_chosen in ingradients_list:
        ingredients_string += fruit_chosen +' '      
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")




