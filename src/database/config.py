import streamlit as st
from supabase import create_client, Client
from urllib.parse import urlparse

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

parsed = urlparse(url)

st.write("Supabase scheme:", parsed.scheme)
st.write("Supabase hostname:", parsed.hostname)
st.write("Supabase key present:", bool(key))

supabase: Client = create_client(url, key)
