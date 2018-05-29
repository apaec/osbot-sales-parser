import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import parse
from bs4 import BeautifulSoup

rel_summary_path  = 'data/summary.html'
abs_summary_path  = open(os.path.join(os.path.dirname(__file__), rel_summary_path), 'r')

rel_salesall_path = 'data/salesall.html'
abs_salesall_path = open(os.path.join(os.path.dirname(__file__), rel_salesall_path), 'r')

soup_summary  = BeautifulSoup(abs_summary_path , 'html.parser')
soup_salesall = BeautifulSoup(abs_salesall_path, 'html.parser')

summary_data  = {}
salesall_data = {}

# Parse summary #
summary_table = soup_summary.find("table");

# Iterate through all summary rows, omitting header row
for row in summary_table.find_all('tr')[1:]:
    row_data = row.find_all('td')
    script_name = row_data[1].string
    script_total_profit = float(row_data[2].string)

    # Filter out the totals row
    if ":" not in script_name:
        summary_data[script_name] = script_total_profit

# Parse salesall #
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

def plot_summary_pie_chart():
    plt.figure(figsize=(8, 6))
    patches, texts, atexts = plt.pie(summary_data.values(), labels=summary_data.keys(), autopct='%1.1f%%')
    plt.legend(patches, summary_data.keys())
    plt.tight_layout()
    plt.axis('equal')
    plt.savefig('output/salessum_pie.svg')

def plot_summary_bar_chart():
    plt.figure(figsize=(12, 10))
    plt.bar(range(len(summary_data)), summary_data.values(), align='center', color='c')
    plt.xticks(range(len(summary_data)), summary_data.keys())
    plt.gcf().autofmt_xdate()
    plt.savefig('output/salessum_bar.svg')

def plot_salesall():
    plt.figure(figsize=(12, 10))

    for script in salesall_data:
        vals = salesall_data[script]
        raw_dates   = [i[0] for i in vals]
        raw_profits = [i[1] for i in vals]
        cumulative_profits = np.cumsum(raw_profits)
        plt.plot(raw_dates, cumulative_profits, '-o', ms=3, label=script)
        plt.gcf().autofmt_xdate()

    plt.xlabel("Date")
    plt.ylabel("Cumulative profit ($)")
    plt.legend(loc='upper left');
    plt.savefig('output/salesall.svg')

plot_summary_bar_chart()
plot_summary_pie_chart()
plot_salesall()
