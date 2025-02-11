import openpyxl
import pandas as pd
from datetime import datetime

# Load Excel file with automatic date parsing
df = pd.read_excel(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/data-science-in-health-care-basic-statistical-analysis/COVID_19.xlsx',
    sheet_name='Sheet1',  # Specify sheet name
    na_values="NaN",       # Treat "NaN" as missing values
    parse_dates=['Date time'],  # Automatically parse date columns
    index_col=0            # Set first column as index (if needed)
)

# Drop rows with missing values in the 'Gender' column
df = df.dropna(subset=['Gender'])

# Map 'Yes'/'No' to boolean values for 'Do you vaccinated influenza?'
d = {'No': False, 'Yes': True}
c = 'Do you vaccinated influenza?'
df.loc[:, c] = df[c].map(d).fillna(False)  # Use fillna to handle NaN values

# Display data types and missing values
df.info()

# Convert 'Age' column to categorical type
c = 'Age'
df.loc[:, c] = df[c].astype(str).apply(lambda x: x.split('(')[0]).astype('category')

# Apply a similar conversion for other columns, handling any nested text
for c in df.columns[1:-1]:
    df.loc[:, c] = df[c].astype(str).apply(lambda x: x.split('(')[0]).astype('category')

# Display updated DataFrame information
df.info()

# Display summary statistics for categorical columns
df.describe(include=['category'])

# Display the relative frequencies of 'Age' values
print(df['Age'].value_counts(normalize=True))

# Sort DataFrame by 'Age' and 'Gender'
df = df.sort_values(by=['Age', 'Gender'], ascending=[True, False])

# Display the unique values of 'Gender'
print(df['Gender'].value_counts().keys())

# Calculate the mean temperature for females
female_temp_mean = df[df['Gender'].str.strip() == 'Female']['Maximum body temperature'].mean()
print(f"Mean temperature for females: {female_temp_mean}")

# Calculate the maximum temperature for males who smoke and had Covid-19
max_temp_male = df[(df['Gender'].str.strip() == 'Male') &
                   (df['Do you smoke?'].str.strip() == 'Yes') &
                   (df['Have you had Covid`19 this year?'].str.strip() == 'Yes')]['Maximum body temperature'].max()
print(f"Maximum temperature for males who smoke and had Covid-19: {max_temp_male}")

# Create a cross-tabulation between 'Age' and 'Gender'
cross_tab = pd.crosstab(df['Age'], df['Gender'])
print(cross_tab)

# Create a pivot table with the mean temperature for each
pivot_table = pd.pivot_table(
    df, values= 'Maximum body temperature', 
    index= ['Age'], 
    columns=['Gender'], 
    aggfunc='mean', 
    margins=True)
print(pivot_table)

# Display the first few rows of the DataFrame
print(df.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Visualize the number of surveyed men and women in terms of age groups
visual = sns.countplot(x='Age', hue='Gender', data=df)


# Display the plot Men and Women by Age Group
plt.title('Number of Surveyed Men and Women by Age Group')  # Title
plt.xlabel('Age Group')  # Label for the x-axis
plt.ylabel('Count')  # Label for the y-axis
plt.xticks(rotation=45)  # Rotate labels if needed for better readability
plt.show()

# Visualizing the distribution of 'Maximum body temperature' for those who had COVID-19 this year vs maybe
_, axes = plt.subplots(1, 2, sharey=True, figsize=(16, 6))

df_t = df[df['Have you had Covid`19 this year?'] == 'Yes'].dropna(subset=['Maximum body temperature'])
sns.distplot(df_t['Maximum body temperature'], ax=axes[0])
axes[0].set_title('Distribution of Maximum Body Temperature (COVID-19: Yes)')

df_t = df[df['Have you had Covid`19 this year?'] == 'Maybe'].dropna(subset=['Maximum body temperature'])
sns.distplot(df_t['Maximum body temperature'], ax=axes[1])
axes[1].set_title('Distribution of Maximum Body Temperature (COVID-19: Maybe)')

plt.tight_layout()
plt.show()

# Boxplot and violin plot of 'Maximum body temperature' vs 'Age'
cols = ['Maximum body temperature', 'Maximum body temperature']
_, axes = plt.subplots(1, 2, sharey=True, figsize=(16, 6))

# Reset index to avoid duplicate labels issue
df_reset = df.reset_index()

sns.boxplot(y=df_reset["Age"], x=df_reset["Maximum body temperature"], ax=axes[0])
sns.violinplot(y=df_reset["Age"], x=df_reset["Maximum body temperature"], ax=axes[1])

axes[0].set_title('Boxplot: Age vs Maximum Body Temperature')
axes[1].set_title('Violin plot: Age vs Maximum Body Temperature')

plt.tight_layout()
plt.show()
