import pandas as pd
import datetime
from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def query_circle():
    return supabase.table("Circle").select("*").execute()


def query_kpi(circle_id):
    """
    at the moment, it only returns the KPI ids
    maybe nice to have: info about value type/units and periodicity
    """
    return supabase.table("Kpi").select("id", "Name").eq("CircleId", str(circle_id)).execute()


def query_kpi_name(kpi_id):
    """
    return the kpi name given the kpi id
    """
    return supabase.table("Kpi").select("Name").eq("id", str(kpi_id)).execute().data


# def query_kpi_history(kpi_id, all_time=False, timefrom=(2023,1), timeto=(2023,12)):
def query_kpi_history(kpi_id):
    """
    Return a (sorted) history table for the specific Kpi in the specified time window.
    timefrom, timeto: tuple of (year, month)
    """

    return supabase.table("KpiHistory").select("Value", "PeriodYear", "PeriodMonth").eq(
    "KpiId", str(kpi_id)).execute()


def get_pandas_history(kpi_id, ascending=True):
    """
    Returns pandas Dataframe of the requested time window 
    Use cases: Vanilla Excel-style Table, line graph
    """

    return pd.DataFrame(query_kpi_history(kpi_id).
                        data).sort_values(["PeriodYear", "PeriodMonth"], 
                        ascending=ascending, ignore_index=True)


def get_growth_rate(kpi_id, mode="current", current_year=datetime.datetime.now().year):
    """
    Return the annual/current growth rate of the specified KPI
    Utility function

    Growth rate is defined as (current - previous) / previous * 100;

    if mode == current:
        the current value is the most recent entry in the history table, and the
        previous value is the value preceding the current value

    if mode == annual:
        the current and previous values are the annual averages of the current and the preceding years
    """

    history = get_pandas_history(kpi_id, ascending=False).dropna().reset_index(drop=True)

    if mode == "current":
        current_val = history.loc[0]["Value"]
        previous_val = history.loc[1]["Value"]
    
    elif mode == "annual":
        previous_year = history.iloc[history.loc[
            history["PeriodYear"]==current_year].index[-1]+1]["PeriodYear"]
        tmp = history.loc[history["PeriodYear"] == current_year]
        current_val = tmp["Value"].mean()
        tmp = history.loc[history["PeriodYear"] == previous_year]
        previous_val = tmp["Value"].mean()
    
    else:
        raise RuntimeError("Unrecognised mode")

    avg_growth = (current_val - previous_val) / previous_val * 100

    return current_val, avg_growth


def key_stats(kpi_id):
    """
    Return the current value and the growth rate of the specified KPI
    Use case: stats (number) box
    """

    return get_growth_rate(kpi_id)


def annual_average_growth(kpi_id, years=[2021, 2022]):
    ### Not applicable unless we use synthetic data ###
    """
    Return annual (average) growth for all KPIs for the most recent year
    Use case: bar chart

    Parameter: kpis: list of dictionaries returned by user_choice
               years: list of years to compare
    """

    for year in years:
        avg_growth = []
        _, avg = get_growth_rate(kpi_id, mode="annual", current_year=year)
        avg_growth.append(avg)

    return avg_growth
