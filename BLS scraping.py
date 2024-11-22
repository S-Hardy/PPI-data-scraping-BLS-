#PPI commodity indexes available at: https://www.bls.gov/ppi/data-retrieval-guide/

#pip install requests pandas
import requests
import pandas as pd
from datetime import datetime
import json

def chunk(data,length):                 #Split list into chunks of equal size. For dealing with API max requests.
    chunk_list=[]                          #def list of chunks
    for i in range(0,len(data), length):    #iterate in steps.
        chunk_list.append(data[i:i+length]) #add each step as a separate list.
    return chunk_list


url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
series_id_list=list(df_cleaned2["identity"])
API_KEY = 'a54f3f2fc04f4c548e347be4e76f528f'
start_year = 2013
end_year = 2024

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": series_id_list,"startyear":str(start_year), "endyear":str(end_year),"registrationkey":API_KEY})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)

all_data=pd.DataFrame()

# Loop through each series in the returned data
for series in json_data['Results']['series']:
    series_id = series['seriesID']
    series_points = series['data']

    # Extracting data and creating a DataFrame
    dates = [datetime.strptime(f"{point['year']}-{point['period'][1:]}", "%Y-%m") for point in series_points]
    values = [float(point['value']) for point in series_points]

    temp_df = pd.DataFrame({
        "Date": dates,
        series_id: values  # Use series_id as the column name
    })

    # Merge the data into the all_data DataFrame
    if all_data.empty:
        all_data = temp_df
    else:
        all_data = pd.merge(all_data, temp_df, on="Date", how="outer")

# Sorting the DataFrame by date
all_data.sort_values("Date", inplace=True)
all_data.reset_index(drop=True, inplace=True)

# Displaying the DataFrame
print(all_data.head())


for i in range(1,20,5):
    print(i)