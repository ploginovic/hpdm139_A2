import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

commissioning_data_link = 'https://www.england.nhs.uk/statistics/wp-content/' \
    + 'uploads/sites/2/2023/11/' \
    + 'CWT-CRS-Commissioner-Time-Series-Jul-2022-Oct-2023-with-Revisions'


def get_commissioning_data(commissioning_data_link):
    """Parameters
    ----------
    commissioning_data_link : str of URL link to commissioning dataframe

    Returns
    -------
    df: Dataframe of national 28, 31 and 62 day standards
    """

#Data Cleaning, column names and recoding of NaN values to 0
    column_names = {'Monthly': 'Month',
                    'Total': 'Total_28',
                    'Within Standard': 'Within Standard_28',
                    'Outside Standard': 'Outside Standard_28',
                    'Total.1': 'Total_31',
                    'Within Standard.1': 'Within Standard_31',
                    'Outside Standard.1': 'Outside Standard_31',
                    'Total.2': 'Total_62',
                    'Within Standard.2': 'Within Standard_62',
                    'Outside Standard.2': 'Outside Standard_62'
                }
#second dictionary to recode NaN values as 0
    recoding = {'Total_31': 0,
                'Within Standard_31': 0,
                'Outside Standard_31': 0,
                'Total_62': 0,
                'Within Standard_62': 0,
                'Outside Standard_62': 0}

#reading the excel file into a dataframe
    df = (pd.read_excel(commissioning_data_link,
                        sheet_name="Monthly Performance",
                        skiprows=range(0, 3),
                        usecols=['Monthly',
                                 'Total',
                                 'Within Standard',
                                 'Outside Standard',
                                 'Total.1',
                                 'Within Standard.1',
                                 'Outside Standard.1',
                                 'Total.2',
                                 'Within Standard.2',
                                 'Outside Standard.2'])
        #renaming columns
        .rename(columns=column_names)

        #replace NaN values with 0
        .fillna(value=recoding)
    
        #assigning integer values to the 28,31 and 62 day columns
        .astype({'Total_28':np.int32,
               'Within_Standard_28': np.int32,
               'Outside_Standard_28': np.int32,
               'Total_31': np.int32,
               'Within_Standard_31': np.int32,
               'Outside_Standard_31':np.int32,
               'Total_62':np.int32,
               'Within_Standard_62':np.int32,
               'Outside_Standard_62':np.int32})
        #making month a datetime object
        .assign(Month = lambda x:pd.to_datetime(x['Month']))
        )
    return df

#function in main
commissioner = get_commissioning_data(commissioning_data_link)