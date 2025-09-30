import pandas as pd
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import Select, ColumnDataSource, Legend
from bokeh.layouts import column

monthly_avg_per_zip = pd.read_csv("/Users/antoninberanger/Documents/COMP370/HW5/data/nyc_311_monthly_avg_per_zip.csv")
monthly_avg_all = pd.read_csv("/Users/antoninberanger/Documents/COMP370/HW5/data/nyc_311_monthly_avg_all.csv")

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def sort_by_month(df):
    return df.assign(month_order=df['Month'].apply(lambda x: month_order.index(x))).sort_values(by='month_order').drop(columns=['month_order'])

monthly_avg_per_zip = sort_by_month(monthly_avg_per_zip)
monthly_avg_all = sort_by_month(monthly_avg_all)

zipcodes = sorted(monthly_avg_per_zip['Incident Zip'].unique())
zipcodes = [str(int(z)) for z in zipcodes]

dropdown_zip1 = Select(title="Zipcode 1", options=zipcodes, value=zipcodes[0] if len(zipcodes) > 0 else None)
dropdown_zip2 = Select(title="Zipcode 2", options=zipcodes, value=zipcodes[1] if len(zipcodes) > 1 else zipcodes[0])

p = figure(
    title="Monthly Average Response Time",
    x_axis_label="Month",
    y_axis_label="Average Response Time (hours)",
    x_range=month_order,
    height=400,
    width=800
)

source_all = ColumnDataSource(monthly_avg_all)
line_all = p.line(
    x="Month",
    y="Response Time",
    source=source_all,
    color="blue",
    legend_label="All Zipcodes",
    line_width=2
)

source_zip1 = ColumnDataSource(monthly_avg_per_zip[monthly_avg_per_zip['Incident Zip'] == int(dropdown_zip1.value)])
source_zip2 = ColumnDataSource(monthly_avg_per_zip[monthly_avg_per_zip['Incident Zip'] == int(dropdown_zip2.value)])

line_zip1 = p.line(
    x="month",
    y="response_time",
    source=source_zip1,
    color="red",
    legend_label=f"Zipcode {dropdown_zip1.value}",
)

line_zip2 = p.line(
    x="month",
    y="response_time",
    source=source_zip2,
    color="green",
    legend_label=f"Zipcode {dropdown_zip2.value}",
)

def update_plot(attr, old, new):
    zip1 = dropdown_zip1.value
    zip2 = dropdown_zip2.value

    df_zip1 = sort_by_month(monthly_avg_per_zip[monthly_avg_per_zip["Incident Zip"] == int(zip1)])
    df_zip2 = sort_by_month(monthly_avg_per_zip[monthly_avg_per_zip["Incident Zip"] == int(zip2)])

    source_zip1.data = dict(month=df_zip1["Month"], response_time=df_zip1["Response Time"])
    source_zip2.data = dict(month=df_zip2["Month"], response_time=df_zip2["Response Time"])

    p.legend.items = [
        ("All Zipcodes", [line_all]),
        (f"Zipcode {zip1}", [line_zip1]),
        (f"Zipcode {zip2}", [line_zip2])
    ]

dropdown_zip1.on_change('value', update_plot)
dropdown_zip2.on_change('value', update_plot)

update_plot(None, None, None)

layout = column(dropdown_zip1, dropdown_zip2, p)

curdoc().add_root(layout)
curdoc().title = "311 Response Time Dashboard"