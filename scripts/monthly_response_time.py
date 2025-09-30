import pandas as pd 

df = pd.read_csv("/Users/antoninberanger/Documents/COMP370/HW5/data/311_records_full.csv")
df = df[df["Borough"] != "Unspecified"]

print("Preprocessing data...")

df["Created Date"] = pd.to_datetime(df["Created Date"])
df["Closed Date"] = pd.to_datetime(df["Closed Date"])   

df["Month"] = df["Created Date"].dt.strftime("%b")

response_time = (df["Closed Date"] - df["Created Date"]).dt.total_seconds() / 3600.0
df["Response Time"] = round(response_time, 2)
df = df[df["Response Time"] >= 0]

df["Month"] = df["Created Date"].dt.strftime("%b")

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

avg_response_time = (
    df.groupby(["Incident Zip", "Month"])["Response Time"]
    .mean()
    .reset_index()
)

avg_response_time['Month Order'] = avg_response_time['Month'].apply(lambda x: month_order.index(x))
avg_response_time = avg_response_time.sort_values(['Incident Zip', 'Month Order']).drop(columns=['Month Order'])

avg_response_time.to_csv(
    "/Users/antoninberanger/Documents/COMP370/HW5/nyc_311_monthly_avg_per_zip.csv",
    index=False,
)

avg_response_time_all = (
    df.groupby("Month")["Response Time"]
    .mean()
    .reset_index()
)
avg_response_time_all["Incident Zip"] = "ALL" 
avg_response_time_all['Month Order'] = avg_response_time_all['Month'].apply(lambda x: month_order.index(x))
avg_response_time_all = avg_response_time_all.sort_values(['Incident Zip', 'Month Order']).drop(columns=['Month Order'])

avg_response_time_all = avg_response_time_all[["Incident Zip", "Month", "Response Time"]] 
avg_response_time_all.to_csv(
    "/Users/antoninberanger/Documents/COMP370/HW5/nyc_311_monthly_avg_all.csv",
    index=False,
)

print("Saved to nyc_311_monthly_avg_per_zip.csv and nyc_311_monthly_avg_all.csv")