# from dotenv import load_dotenv
# load_dotenv()
# import os
# from supabase import create_client, Client

from utils import *

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(url, key)


def generate_xlabel(years, months):
    month_dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mai", 6: "Jun", 
                  7: "Jul", 8: "Aug", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Dez"}
    
    return [str(month_dict[month]) + str(year)[-2:] for month, year in zip(months, years)]


def invert_xlabel(label):
    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Mai": 5, "Jun": 6, 
                  "Jul": 7, "Aug": 8, "Sep": 9, "Okt": 10, "Nov": 11, "Dez": 12}
    
    month = label[:3]
    year = label[-2:]

    return (int("20"+year), month_dict[month])
    


def generate_linechart(kpi_id, timefrom, timeto, alltime=False):
    history = get_pandas_history(kpi_id)
    xs = generate_xlabel(history["PeriodYear"], history["PeriodMonth"])
    history["Time"] = xs

    if alltime:
        return history

    ind_st = history.index[(history["PeriodYear"] == timefrom[0])
                        & (history["PeriodMonth"] == timefrom[1])][0]
    ind_end = history.index[(history["PeriodYear"] == timeto[0])
                        & (history["PeriodMonth"] == timeto[1])][0]

    df = history[(history.index >= ind_st) & (history.index <= ind_end)]

    xs = generate_xlabel(df["PeriodYear"], df["PeriodMonth"])
    df["Time"] = xs

    return df


def generate_barchart(kpis):
    """
    Return current growth of all KPIs in the circle
    Use case: bar chart

    Parameter: kpis: list of dictionaries returned by user_choice
    """

    curr_growth, names = [], []

    for kpi in kpis:
        names.append(kpi["Name"])
        _, curr_gr = get_growth_rate(kpi["id"], mode="current")
        curr_growth.append(curr_gr)
    
    return pd.DataFrame({"KPI": names, "growth rate": curr_growth})
    

def generate_multibarchart(kpis, years):
    
    names = []
    for kpi in kpis:
        names.append(kpi["Name"])

    vals = annual_average_growth(kpis, years=years)

    return pd.DataFrame({"KPI": names, "annual growth": vals, "years": years})
    
