import pandas as pd
import glob
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import holidays
from datetime import time
import requests


class calendarSetup:
    def __init__(self, lat, lon ):
        self.lat = round(float(lat),6)
        self.lon = round(float(lon), 6)
        self.raw_data_path=r"C:\Users\esian\Desktop\Kafe\src\data\raw_data"
        self.processed_data=r"C:\Users\esian\Desktop\Kafe\src\data\processed_data"
        # final merging data csv
        self.merged_df = None
        

        # merge files
    def mergingFiles(self):
        # Get all CSV and Excel files in that folder
        files = glob.glob(os.path.join(self.raw_data_path, "*"))
        all_dfs = []
        categories_df = ['item','sales','time']

        for file in files:
            try:
                if file.endswith(".csv"):
                    df = pd.read_csv(file)
                elif file.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(file)
                
                df.columns = [col.lower() for col in df.columns]
                # Remove the first row if it's just repeated header/info
                df = df.iloc[1:]
                df = df[categories_df]

                all_dfs.append(df)

            except Exception as e:
                print(f"Error loading {file}: {e}")

        # Merge all into one DataFrame
        if all_dfs:
            self.merged_df = pd.concat(all_dfs, ignore_index=True)

            # set the dates
            self.merged_df['time'] = pd.to_datetime(self.merged_df['time'], errors='coerce')
            self.merged_df= self.merged_df.sort_values(by='time', ascending=True)
            self.merged_df['day_of_week'] = self.merged_df['time'].dt.dayofweek
            self.merged_df['year'] = self.merged_df['time'].dt.year
            self.merged_df['month'] = self.merged_df['time'].dt.month
            self.merged_df['day'] = self.merged_df['time'].dt.day

            # print(f"Merged file saved as: {output_file}")
            print(f"Total rows: {self.merged_df.shape[0]}")
        else:
            print("No files found to merge.")

        
        
        return self.merged_df
    
    def setLagVal(self, target_col="sales", lags=[1,2,3,7]):
       
        if self.merged_df is None:
            print("Merged data not found.")
            return None
        
        df = self.merged_df.copy()
        
        # Sort by item and time
        df = df.sort_values(by=["item", "time"])
        
        # For each lag, shift sales within each item group
        for lag in lags:
            df[f"{target_col}_lag_{lag}"] = df.groupby("item")[target_col].shift(lag)
            self.merged_df[f"{target_col}_lag_{lag}"]= df[f"{target_col}_lag_{lag}"]
        
        # Drop rows with NaNs created by lagging (optional)
        df = df.dropna().reset_index(drop=True)
        
        print(f"Lag features {['{}_lag_{}'.format(target_col, l) for l in lags]} added for each item.")
        return self.merged_df

    def cleanLocation(self):
        if self.lat is None or self.lon is None:
            return None
        return round(float(self.lat), 6), round(float(self.lon), 6)
    
    # find country/city
    def countryFinder(self):
        # set up user agent
        geolocator = Nominatim(user_agent="my_coffee_app", timeout=10)
        # reverse coord for address, city and country
        location = geolocator.reverse(f"{self.lat},{self.lon}", exactly_one=True)

        if location:
            address = location.raw['address']
            city = address.get('city', address.get('town', address.get('village', 'N/A')))
            country_code = address.get('country_code', 'N/A')
        else:
            print('Error')
        
        return city, country_code
    
    def setCalendar(self):

        city, country_code = self.countryFinder()
        df = self.merged_df

        if country_code == 'N/A':
            print("Could not determine country.")
            return None
        
        my_country_code = country_code.upper()
            

        # Setup holidays for the country
        try:
            years = self.merged_df['time'].dt.year.dropna().astype(int).unique().tolist()  # extract all years in your data
            country_holidays = holidays.CountryHoliday(my_country_code, years=years)

            # Add is_holiday column
            df['is_holiday'] = df['time'].isin(country_holidays).astype(int)

            print(f"Holiday calendar applied for {city}, {country_code}")
            return df
        
        except NotImplementedError:
            print(f"Holiday calendar not available for {country_code}")
            return None
    
        # Add weather columns and save final CSV
    def setWeather(self):
        if self.merged_df is None:
            print("No merged DataFrame.")
            return None

        start_date = self.merged_df['time'].min().date()
        end_date = self.merged_df['time'].max().date()

        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={self.lat}&longitude={self.lon}"
            f"&start_date={start_date}&end_date={end_date}"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            "&timezone=auto"
        )

        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to fetch weather data")
            return None

        data = response.json()
        weather_df = pd.DataFrame(data['daily'])
        weather_df['time'] = pd.to_datetime(weather_df['time'])
        self.merged_df['time'] = pd.to_datetime(self.merged_df['time'])

        self.merged_df = self.merged_df.merge(weather_df, on="time", how="left")

        print(f"Weather added")

        return self.merged_df
  


    
    def savedCSV(self):
        # Save final enriched CSV
        self.merged_df.drop(['time','month','year','day'], axis=1, inplace=True)
        output_file = os.path.join(self.processed_data, "merged_data.csv")
        self.merged_df.to_csv(output_file, index=False)
    

    # Full pipeline: merge, holidays, weather
    def run_full_pipeline(self):
        self.mergingFiles()
        self.setLagVal()
        self.setCalendar()
        self.setWeather()
        self.savedCSV()

if __name__=='__main__':
    cal = calendarSetup(40.7128, -74.0060)
    cal.run_full_pipeline()




