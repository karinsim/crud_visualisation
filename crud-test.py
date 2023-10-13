from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

import pandas as pd
import streamlit as st
import numpy as np


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

data = supabase.table("Kpi").select("*").execute()





