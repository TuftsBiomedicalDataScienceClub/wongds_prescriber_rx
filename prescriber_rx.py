# prescriber_rx.py
# Daniel Wong 26 Feb 2017

import csv
import jsonlines
import copy
from pprint import pprint
import pandas as pd
import numpy as np

# Process the prescriber information dataset first, to convert from JSON to dataframe
## Location of dataset
prescriber_dataset = 'dataset_prescriber/roam_prescription_based_prediction.jsonl'

## Build a list of dictionaries containing prescriber data
prescriber_data = []
with jsonlines.open(prescriber_dataset) as reader:
    for obj in reader:
        prescriber_data.append(obj)
        
## Set up column names for Pandas DataFrame
column_names = ['drug_name', 'count', 'npi']
column_names.extend(list(prescriber_data[0]['provider_variables'].keys()))

## Set up the dataframe
prescriptions = pd.DataFrame(np.nan, index=[], columns=column_names)

## Migrate data into the dataframe
### Re-format JSONL data to Pandas dataframe for CSV, one line for each prescriber/drug prescrbed combination
for entry in prescriber_data:
    # Prescriber information
    prescriber_info = {'npi': entry['npi']}
    prescriber_info.update(entry['provider_variables'])
    
    for drug_name, count in entry['cms_prescription_counts'].items():
        data_row = {column_names[0]: drug_name,
                    column_names[1]: count,
                    column_names[2]: prescriber_info['npi'],
                    column_names[3]: prescriber_info['settlement_type'],
                    column_names[4]: prescriber_info['region'],
                    column_names[5]: prescriber_info['specialty'],
                    column_names[6]: prescriber_info['gender'],
                    column_names[7]: prescriber_info['generic_rx_count'],
                    column_names[8]: prescriber_info['brand_name_rx_count'],
                    column_names[9]: prescriber_info['years_practicing'],
                   }
        #print(data_row, column_names)
        dataframe_row = pd.DataFrame(data_row,
                                     index=[1],
                                     columns=column_names)
        #print(dataframe_row)
        prescriptions = pd.concat([prescriptions, dataframe_row], ignore_index=True)
prescriptions.to_csv('prescriptions.csv')        
#print(prescriptions)
