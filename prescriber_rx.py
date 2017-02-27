'''
# wongds_prescriber_rx
A Python-based approach for a Tufts Biomedical Data Science Club project to determine whether patterns exist between prescriber demographic information and opioid prescription.

## Datasets
- Prescriber attributes: https://www.kaggle.com/roamresearch/prescriptionbasedprediction
- Opiate prescriptions: https://www.kaggle.com/apryor6/us-opiate-prescriptions
'''
# prescriber_rx.py
# Daniel Wong 26 Feb 2017

# Load some useful libraries
import csv
import jsonlines
import copy
from pprint import pprint
import pandas as pd
import numpy as np

# Load data
# Opiate dataset
opiate_class_data = 'dataset_rx/opioids.csv'
opiate_prescriber_data = 'dataset_rx/prescriber-info.csv'
opiate_overdose_data = 'dataset_rx/overdoses.csv'

# List of opiates
opioids = pd.read_csv(opiate_class_data)

# Opiate prescriber info
opiate_prescribers = pd.read_csv(opiate_prescriber_data)

# Opiate overdoses, by US State
opiate_overdoses = pd.read_csv(opiate_overdose_data)

# Prescriber attribute dataset
prescriber_attr_dataset = 'dataset_prescriber/roam_prescription_based_prediction.jsonl'

# Build a list of dictionaries containing prescriber data
prescriber_attr_data = []
with jsonlines.open(prescriber_attr_dataset) as reader:
    for obj in reader:
        prescriber_attr_data.append(obj)

# Look for prescription of opiates in prescriber_data
opioid_prescribers = {'Drug Name': [],
                      'npi': [],
                     }

# Cycle through each prescriber record
for prescriber in prescriber_attr_data:
    # Look for opioids by Drug Name, and make a record of prescriber by npi.
    # Generic names also appear in 'Drug Name' list.
    for drug in opioids['Drug Name']:
        if drug in prescriber['cms_prescription_counts'].keys():
            opioid_prescribers['Drug Name'].append(drug)
            opioid_prescribers['npi'].append(prescriber['npi'])

# Convert the dictionary to a dataframe and save to csv.
# Use this dataframe to unify prescriber attributes and opioid prescription.
opioid_prescriber_df = pd.DataFrame(opioid_prescribers)
opioid_prescriber_df.to_csv('opioid_prescribers.csv')
