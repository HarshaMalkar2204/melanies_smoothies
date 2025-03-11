# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: customize your smoothie :cup_with_straw:")
st.write("choose the fruit you like")

from snowflake.snowpark.functions import col


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)



indgredient_list= st.multiselect(
    'choose upto 5 indgredients:', my_dataframe)

if indgredient_list:
    indgredient_string = ''

    for fruit_chosen in indgredient_list:
        indgredient_string += fruit_chosen + ''

    st.write(indgredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + indgredient_string + """')"""

    st.write(my_insert_stmt)

    if indgredient_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
