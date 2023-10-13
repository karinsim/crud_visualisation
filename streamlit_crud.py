import streamlit as st
from supabase import create_client, Client


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 20 min.
@st.cache_data(ttl=1200)
def run_query():
    return supabase.table("circle").select("*").execute()

rows = run_query()


for row in rows.data:
    st.write(f"{row['name']}")
