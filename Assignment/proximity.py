import pandas as pd
import math
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
	
	# distance between latitudes and longitudes in radians
	dlat = math.radians(lat2 - lat1) 
	dlon = math.radians(lon2 - lon1) 

	lat1 = math.radians(lat1) 
	lat2 = math.radians(lat2) 

	# apply formulae
	a = math.sin(dlat / 2) ** 2 + (math.sin(dlon / 2) ** 2 * math.cos(lat1) * math.cos(lat2))
	rad = 6371
	c = 2 * math.asin(math.sqrt(a))
	return rad * c


def detect_proximity(df,threshold ):
    df_out = []

    # for each unique timestamp, we find the mmsis present at that time
    for timestamp in df['timestamp'].unique():
        unique_ts = df[df['timestamp'] == timestamp]
        mmsis = unique_ts['mmsi'].values
        lat_lon = unique_ts[['lat', 'lon']].values
        
        #creating numpy array containing the haversine distances
        no_of_mmsis = len(mmsis)
        distance = np.zeros((no_of_mmsis, no_of_mmsis))
        for i in range(no_of_mmsis):
            for j in range(i + 1, no_of_mmsis):
                distance[i][j] = distance[j][i] = haversine(lat_lon[i][0], lat_lon[i][1], lat_lon[j][0], lat_lon[j][1])
                
         #finding the vessels crossing threshold value       
        for i in range(no_of_mmsis):
            vessel_proximity = []
            for j in range(no_of_mmsis):
                 if distance[i][j] <= threshold and mmsis[j] != mmsis[i]:
                      vessel_proximity.append(mmsis[j])
            if vessel_proximity:
                df_out.append({'mmsi': mmsis[i], 'vessel_proximity': vessel_proximity, 'timestamp': timestamp})
    
    return pd.DataFrame(df_out)


   

csv_file=".\sample_data.csv"

df= pd.read_csv(csv_file)

threshold = float(input('Enter threshold value: '))

print(detect_proximity(df, threshold))


