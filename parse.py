import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

rel_summary_path = 'data/summary.html'
abs_summary_path = open(os.path.join(os.path.dirname(__file__), rel_summary_path), 'r')

soup = BeautifulSoup(abs_summary_path, 'html.parser')
table = soup.find("table");

summary_data = {}

# Iterate through all rows, omitting header row
for row in table.find_all('tr')[1:]:
    script_name = row.find_all('td')[1].string
    script_total_profit = float(row.find_all('td')[2].string)

    # Filter out the totals row
    if ":" not in script_name:
        summary_data[script_name] = script_total_profit

plt.style.use('seaborn')
plt.bar(range(len(summary_data)), summary_data.values(), align='center')
plt.xticks(range(len(summary_data)), summary_data.keys())

# Prevent labels overlapping
plt.gcf().autofmt_xdate()
plt.show()

patches, texts, atexts = plt.pie(summary_data.values(), labels=summary_data.keys(), autopct='%1.1f%%')
plt.legend(patches, summary_data.keys())
plt.tight_layout()
plt.axis('equal')
plt.show()
print plt.style.available
