# add to enviroment file and delete from here 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Link for national data file perhaps should be stored elsewhere 
national_data_link = r'https://www.england.nhs.uk/statistics/wp-content/' \
    + 'uploads/sites/2/2023/12/' \
    + 'CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-Revisions.xlsx'


def get_national(national_data_link):
    """
    Parameters
    ----------
    national_data_link : string of URL link to national cancer data frame

    Returns
    -------
    df : Data frame of national 28 day and 31 day standards
    """
    # dictionary of column names
    column_names = {'Monthly': 'Month',
                    'Total': 'Total_28',
                    'Within Standard': 'Within Standard_28',
                    'Outside Standard': 'Outside Standard_28',
                    'Total.1': 'Total_31',
                    'Within Standard.1': 'Within Standard_31',
                    'Outside Standard.1': 'Outside Standard_31'}
    # dictionary to recode NaN values as 0
    recoding = {'Total_31': 0,
                'Within Standard_31': 0,
                'Outside Standard_31': 0}
    # read the excel file, including specific columns required
    df = (pd.read_excel(national_data_link,
                        sheet_name="Monthly Performance",
                        skiprows=range(0, 3),
                        usecols=['Monthly',
                                 'Total',
                                 'Within Standard',
                                 'Outside Standard',
                                 'Total.1',
                                 'Within Standard.1',
                                 'Outside Standard.1'])
          # rename columns
          .rename(columns=column_names)
          # fill in NaN values as 0
          .fillna(value=recoding)
          # asign interger values to the columns
          .astype({
              'Total_28': np.int32,
              'Within Standard_28': np.int32,
              'Outside Standard_28': np.int32,
              'Total_31': np.int32,
              'Within Standard_31': np.int32,
              'Outside Standard_31': np.int32})
          # make month a time value
          .assign(Month=lambda x: pd.to_datetime(x['Month']))
          )
    return df

# function in main will be 
national = get_national(national_data_link)
