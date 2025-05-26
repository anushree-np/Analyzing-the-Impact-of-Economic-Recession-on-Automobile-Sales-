#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install pandas numpy matplotlib seaborn folium dash')


# In[3]:


# Importing data manipulation and analysis libraries
import pandas as pd
import numpy as np

# Importing visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Importing geographic visualization library
import folium

# Importing libraries for dashboard creation
from dash import Dash, dcc, html, Input, Output


# In[4]:


import pandas as pd
import requests
from io import BytesIO

# URL of the dataset
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"

# Fetch the dataset
response = requests.get(URL)

# Check if the request was successful
if response.status_code == 200:
    text = BytesIO(response.content)
    df = pd.read_csv(text)
    print('Data downloaded and read into a dataframe!')
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")


# In[5]:


df.columns


# In[6]:


df.describe(include = 'all')


# In[7]:


df.head()


# In[8]:


import matplotlib.pyplot as plt

# Grouping the data by Year to calculate the total sales per year
df['Year'] = pd.to_datetime(df['Date']).dt.year  # Extracting the year from the Date column
yearly_sales = df.groupby('Year')['Automobile_Sales'].sum().reset_index()

# Recession years for annotation
recession_years = [1980, 2008]  # Example: Two recession years

# Plotting the line chart
plt.figure(figsize=(12, 6))
plt.plot(yearly_sales['Year'], yearly_sales['Automobile_Sales'], marker='o', linestyle='-', color='b', label='Automobile Sales')
plt.title('Automobile Sales During Recession', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Automobile Sales', fontsize=12)
plt.grid(True)

# Adding x-axis ticks for all years
plt.xticks(yearly_sales['Year'], rotation=45)

# Annotating recession years
for year in recession_years:
    sales_value = yearly_sales[yearly_sales['Year'] == year]['Automobile_Sales'].values[0]
    plt.annotate(f'Recession {year}', 
                 xy=(year, sales_value), 
                 xytext=(year + 2, sales_value + 2000), 
                 arrowprops=dict(facecolor='red', arrowstyle='->'),
                 fontsize=10, color='red')

# Adding a legend
plt.legend()

# Adjust layout and save plot
plt.tight_layout()
plt.savefig("Line_Plot_1_Recession.png")
plt.show()


# In[10]:


import seaborn as sns

# Grouping data by year and vehicle type to calculate total sales
vehicle_sales = df.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].sum().reset_index()

# Creating a line plot with Seaborn
plt.figure(figsize=(14, 8))
sns.lineplot(data=vehicle_sales, x='Year', y='Automobile_Sales', hue='Vehicle_Type', marker='o')

# Highlighting recession periods
recession_periods = [(1980, 1980), (1981, 1982), (1991, 1991), (2000, 2001), (2007, 2009), (2020, 2020)]
for start, end in recession_periods:
    plt.axvspan(start, end, color='gray', alpha=0.2, label='Recession Period' if start == 1980 else "")

# Adding titles and labels
plt.title('Sales Trends by Vehicle Type During Recession Periods', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Automobile Sales', fontsize=12)
plt.legend(title='Vehicle Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig("Line_Plot_Vehicle_Type.png")
plt.show()


# In[11]:


import seaborn as sns
import matplotlib.pyplot as plt

# Filter the data for Recession (e.g., 2007-2009) and Non-Recession periods
recession_data = df[df['Recession'] == 1]
non_recession_data = df[df['Recession'] == 0]

# Group the data by year, vehicle type, and calculate the total sales
recession_sales = recession_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].sum().reset_index()
non_recession_sales = non_recession_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].sum().reset_index()

# Create a plot for comparison
plt.figure(figsize=(14, 8))

# Plot recession data
sns.lineplot(data=recession_sales, x='Year', y='Automobile_Sales', hue='Vehicle_Type', marker='o', label='Recession')

# Plot non-recession data
sns.lineplot(data=non_recession_sales, x='Year', y='Automobile_Sales', hue='Vehicle_Type', marker='o', label='Non-Recession', linestyle='--')

# Adding titles and labels
plt.title('Sales Trend Comparison: Recession vs Non-Recession Period', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Automobile Sales', fontsize=12)
plt.legend(title='Period & Vehicle Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Adjust layout and display the plot
plt.tight_layout()
plt.savefig("Sales_Trend_Recession_vs_NonRecession.png")
plt.show()


# In[ ]:


import matplotlib.pyplot as plt

# Filter data for recession and non-recession periods
recession_data = df[df['Recession'] == 1]
non_recession_data = df[df['Recession'] == 0]

# Group by Year and calculate the average GDP for each year
recession_gdp = recession_data.groupby('Year')['GDP'].mean().reset_index()
non_recession_gdp = non_recession_data.groupby('Year')['GDP'].mean().reset_index()

# Create subplots: one for recession and one for non-recession
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot for Recession Period
axes[0].plot(recession_gdp['Year'], recession_gdp['GDP'], marker='o', color='red')
axes[0].set_title('GDP Variation During Recession Periods')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('GDP (USD)')
axes[0].grid(True)

# Plot for Non-Recession Period
axes[1].plot(non_recession_gdp['Year'], non_recession_gdp['GDP'], marker='o', color='green')
axes[1].set_title('GDP Variation During Non-Recession Periods')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('GDP (USD)')
axes[1].grid(True)

# Adjust layout for better spacing
plt.tight_layout()
plt.savefig("GDP_Variations_Recession_vs_NonRecession.png")
plt.show()


# In[12]:


import seaborn as sns
import matplotlib.pyplot as plt

# Filter data for the recession and non-recession periods
rec_data = df[df['Recession'] == 1]

# Create a bubble plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Seasonality_Weight', y='Automobile_Sales', 
                size='Advertising_Expenditure', sizes=(20, 200), # bubble size range
                data=rec_data, hue='Recession', palette='coolwarm', legend=True)

# Add labels and title
plt.xlabel('Seasonality Weight')
plt.ylabel('Automobile Sales')
plt.title('Impact of Seasonality on Automobile Sales (Recession Period)')

# Show the plot
plt.tight_layout()
plt.show()


# In[13]:


plt.figure(figsize=(10, 6))
sns.scatterplot(x='Price', y='Automobile_Sales', data=rec_data, color='blue')

# Add title and labels
plt.title('Scatter Plot: Vehicle Price vs. Sales Volume during Recession Period')
plt.xlabel('Average Vehicle Price (USD)')
plt.ylabel('Automobile Sales')

# Calculate and display the correlation coefficient
correlation = np.corrcoef(rec_data['Price'], rec_data['Automobile_Sales'])[0, 1]
plt.figtext(0.15, 0.85, f'Correlation: {correlation:.2f}', fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()


# In[14]:


import matplotlib.pyplot as plt

# Filter data for recession and non-recession periods
rec_data = df[df['Recession'] == 1]
non_rec_data = df[df['Recession'] == 0]

# Calculate total advertising expenditure for each period
total_rec_ad_exp = rec_data['Advertising_Expenditure'].sum()
total_non_rec_ad_exp = non_rec_data['Advertising_Expenditure'].sum()

# Data for the pie chart
labels = ['Recession Period', 'Non-Recession Period']
sizes = [total_rec_ad_exp, total_non_rec_ad_exp]
colors = ['#FF9999', '#66B3FF']

# Create the pie chart
plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.1, 0))  # explode the first slice (recession)
plt.title('Advertising Expenditure Distribution: Recession vs Non-Recession Periods')

# Display the chart
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


# In[15]:


import matplotlib.pyplot as plt

# Filter data for the recession period
rec_data = df[df['Recession'] == 1]

# Group data by Vehicle_Type and sum the advertising expenditure
vehicle_ad_exp = rec_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()

# Data for the pie chart
labels = vehicle_ad_exp.index  # Vehicle types as labels
sizes = vehicle_ad_exp.values  # Total advertising expenditure for each vehicle type
colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFD700', '#FF6347']  # Different colors for each slice

# Create the pie chart
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.1, 0, 0, 0, 0))  # Explode the first slice for emphasis
plt.title('Advertising Expenditure Distribution per Vehicle Type (Recession Period)')

# Display the chart
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.show()


# In[19]:


import matplotlib.pyplot as plt
import seaborn as sns

# Filter data for the recession period
rec_data = df[df['Recession'] == 1]

# Group data by Year, Vehicle_Type and calculate the total sales and average unemployment rate
unemployment_sales = rec_data.groupby(['Year', 'Vehicle_Type']).agg({'unemployment_rate': 'mean', 'Automobile_Sales': 'sum'}).reset_index()

# Create a line plot
plt.figure(figsize=(12, 6))

# Use Seaborn to plot the lines for each vehicle type
sns.lineplot(data=unemployment_sales, x='unemployment_rate', y='Automobile_Sales', hue='Vehicle_Type', marker='o')

# Title and labels
plt.title('Effect of Unemployment Rate on Vehicle Sales During Recession Period')
plt.xlabel('Unemployment Rate (%)')
plt.ylabel('Total Automobile Sales')

# Display the plot
plt.legend(title='Vehicle Type')
plt.tight_layout()
plt.show()


# In[20]:


sns.lineplot(data=unemployment_sales, y='unemployment_rate', x='Year')


# In[ ]:




