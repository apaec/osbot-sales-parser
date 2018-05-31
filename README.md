
# OSBot Sales Parser



## Overview

A Python tool for visualising OSBot sales data. Parses HTML from 'sales summary' and 'sales all' pages with Beautiful Soup to retrieve raw data. This raw data is then processed and subsequently plotted using matplotlib.



## Usage and Installation


1. Install the required libraries with the following pip command: `pip install -r requirements.txt`

2. Save HTML from https://osbot.org/mvc/scripters/salessum as summary.html in the data directory

3. Save HTML from https://osbot.org/mvc/scripters/salesall as salesall.html in the data directory

4. Run the Python script with: `python parse.py`
5. You can configure the output file format with a command line argument: `python parse.py svg` (default is png)
6. Once script has terminated, see output directory for generated plots