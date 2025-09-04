import pandas as pd
import glob
import os
import csv
import holidays
from pandas.tseries.holiday import USFederalHolidayCalendar

#create calendar for US
cal = USFederalHolidayCalendar()

# Folder where your uploaded files are stored
folder_path = r"C:\Users\esian\Desktop\Kafe\data\raw_data"
saved_path = r"C:\Users\esian\Desktop\Kafe\data\merged_data"
opened_folder = 'merged_dataset.csv'
categories_df = ["time", "item", "sales"]

# Get all CSV and Excel files in that folder
files = glob.glob(os.path.join(folder_path, "*"))

all_dfs = []

for file in files:
    try:
        if file.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file) 
        else:
            df = pd.read_csv(file)
        print(f"Loaded: {file}")
        df.columns = [col.lower() for col in df.columns]
        df = df[categories_df]

 # Remove the first row if it's just repeated header/info
        df = df.iloc[1:]

# set the dates
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        df= df.sort_values(by='time', ascending=True)
        df['day_of_week'] = df['time'].dt.dayofweek
        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day
        df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)

# set the holidays on the csv
        uholidays = cal.holidays(start= df["time"].min(), end=df['time'].max())
        df['is_holiday'] = df['time'].isin(holidays).astype(int)

# make the data clean
        df_cleaned = df.dropna(subset=['time'])
        df_cleaned.drop('time', axis=1, inplace=True)
        all_dfs.append(df_cleaned)
    except Exception as e:
        print(f"Error loading {file}: {e}")




# Merge all into one DataFrame
if all_dfs:
    merged_df = pd.concat(all_dfs, ignore_index=True)
    
    # Save to a single CSV file
    output_file = os.path.join(saved_path, "merged_dataset.csv")
    merged_df.to_csv(output_file, index=False)
    print(f"✅ Merged file saved as: {output_file}")
    print(f"Total rows: {merged_df.shape[0]}")
else:
    print("⚠ No files found to merge.")

