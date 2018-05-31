import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import parse
from bs4 import BeautifulSoup

summary_file = "summary.html"
salesall_file = "salesall.html"

def parse_summary():

    summary_data = {}

    rel_summary_path  = "data/" + summary_file
    abs_summary_path  = open(os.path.join(os.path.dirname(__file__), rel_summary_path), 'r')

    soup_summary  = BeautifulSoup(abs_summary_path , 'html.parser')
    summary_table = soup_summary.find("table");

    # Iterate through all summary rows, omitting header row
    for row in summary_table.find_all('tr')[1:]:
        row_data = row.find_all('td')
        script_name = row_data[1].string
        script_total_profit = float(row_data[2].string)

        # Filter out the totals row
        if ":" not in script_name:
            summary_data[script_name] = script_total_profit

    print("Successfully parsed " + summary_file)
    return summary_data

def parse_salesall():

    salesall_data = {}

    rel_salesall_path = "data/" + salesall_file
    abs_salesall_path = open(os.path.join(os.path.dirname(__file__), rel_salesall_path), 'r')

    soup_salesall = BeautifulSoup(abs_salesall_path, 'html.parser')

    for table in soup_salesall.find_all("table"):
        for row in table.find_all('tr')[1:]:
            row_data = row.find_all('td')

            # Filter out the totals row
            if ":" not in row_data[0].string:

                # Retrieve data from table
                script_name = row_data[2].string.replace('Renewal: ', '')
                est_profit  = float(row_data[3].string)
                sale_date   = parse(row_data[4].string)

                # Initialise dictionary entry if needed
                if script_name not in salesall_data:
                    salesall_data[script_name] = []

                # Add row sales data to dictionary
                salesall_data[script_name].append((sale_date, est_profit))
    print("Successfully parsed " + salesall_file)
    return salesall_data

def plot_summary_pie_chart(summary_data, width=8, height=6):
    colours = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'slategrey', 'lightgreen', 'lightsalmon', 'burlywood', 'plum', 'cadetblue', 'blanchedalmond']
    plt.figure(figsize=(width, height))
    plt.pie(summary_data.values(), labels=summary_data.keys(), autopct='%1.1f%%', colors=colours)
    plt.tight_layout()
    plt.axis('equal')
    plt.savefig('output/salessum_pie.svg')
    print("Saved sale summary pie chart")

def plot_summary_bar_chart(summary_data, width=12, height=10):
    plt.figure(figsize=(width, height))
    plt.bar(range(len(summary_data)), summary_data.values(), align='center', color='c')
    plt.xticks(range(len(summary_data)), summary_data.keys())
    plt.gcf().autofmt_xdate()
    plt.minorticks_on()
    plt.xlabel("Script")
    plt.ylabel("Net profit ($)")
    plt.grid(which='major', linestyle='-',linewidth=1.25)
    plt.grid(which='minor', linestyle='--')
    plt.savefig('output/salessum_bar.svg')
    print("Saved sale summary bar chart")

def plot_salesall(salesall_data, width=12, height=10):
    plt.figure(figsize=(width, height))

    for script in salesall_data:
        vals = salesall_data[script]
        raw_dates   = [i[0] for i in vals]
        raw_profits = [i[1] for i in vals]
        cumulative_profits = np.cumsum(raw_profits)
        plt.plot(raw_dates, cumulative_profits, '-o', ms=3, label=script)
        plt.gcf().autofmt_xdate()

    plt.minorticks_on()
    plt.grid(which='major', linestyle='-',linewidth=1.25)
    plt.grid(which='minor', linestyle='--')
    plt.xlabel("Date")
    plt.ylabel("Cumulative profit ($)")
    plt.legend(loc='upper left');
    plt.savefig('output/salesall.svg')
    print("Saved all sales individual plot")

def plot_salestotal(salesall_data, width=12, height=10):
    plt.figure(figsize=(width,height))

    combined_data = []

    for script in salesall_data:
        combined_data.extend(salesall_data[script])

    combined_data_sorted = sorted(combined_data, key=lambda s: s[0])
    raw_dates   = [i[0] for i in combined_data_sorted]
    raw_profits = [i[1] for i in combined_data_sorted]
    cumulative_profits = np.cumsum(raw_profits)
    plt.plot(raw_dates, cumulative_profits, '-oc', ms=3)
    plt.gcf().autofmt_xdate()
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-',linewidth=1.25)
    plt.grid(which='minor', linestyle='--')
    plt.xlabel("Date")
    plt.ylabel("Cumulative net profit ($)")
    plt.savefig('output/salestotal.svg')
    print("Saved all sales combined plot")

summary_data = parse_summary()

plot_summary_bar_chart(summary_data)
plot_summary_pie_chart(summary_data)

salesall_data = parse_salesall()

plot_salesall(salesall_data)
plot_salestotal(salesall_data)
