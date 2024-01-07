import pandas as pd
import numpy as np


commissioning_data_link = r'https://www.england.nhs.uk/statistics/wp-content/' \
    + 'uploads/sites/2/2023/11/' \
    + 'CWT-CRS-Commissioner-Time-Series-Jul-2022-Oct-2023-with-Revisions.xlsx'

#Defining where to read data from as ICB/ODS code and Month columns are mismatched (indexes 4 and 3)
ICB_row = 4
Total_index = 3

#Storing the duration of collected data (July 2022-November 2023) as a 'month' variable
commissioning_months = pd.date_range(start= "2022-07", end="2023-11",freq = 'M')


#Function to read 28 day sheet
def read_commissioning_data(commissioning_data_link, sheet_name, commissioning_months, Total_index, ICB_row):
    """
    Parameters
    ----------
    commissioning_data_link : str
        URL link to commissioning dataframe
    sheet_name : str
        Name of the sheet in the Excel file
    commissioning_months : iterable
        Iterable containing months to process
    Total_index : int
        Column index where 'Total' data starts
    ICB_row : int
        Row index where header is located

    Returns
    -------
    DataFrame
        Dataframe of commissioning standards sheet
    """
    df = pd.read_excel(commissioning_data_link, sheet_name=sheet_name, header=ICB_row)

    #Loop organises data by list and month, 
    #returning the number of 'within standard' and performance for each area and month.
    processed_data = []

    for i, month in enumerate(commissioning_months):
        month_str = month.strftime('%Y-%m')
        column_index = Total_index + i * 3

        for _, row in df.iterrows():
            area = row['Integrated Care Board (ICB) Commissioning Hub']
            total = row[df.columns[column_index]]
            within_standard = row[df.columns[column_index + 1]]
            performance = row[df.columns[column_index + 2]]
            processed_data.append({
                'area': area,
                'month': month_str,
                'total': total,
                'within_standard': within_standard,
                'performance': performance
            })
    #processed_data list is converted to a dataframe
    processed_df = pd.DataFrame(processed_data)
    
    # Replaces NaN values with 0
    processed_df= processed_df.fillna(0,inplace=True)

    # Assigns integer values to the columns
    processed_df = processed_df.astype({
        'total': np.int32, 
        'within_standard': np.int32, 
        'performance': np.int32
    })
    
    # Converts 'month' to a datetime object
    processed_df['month'] = pd.to_datetime(processed_df['month'], format='%Y-%m')

    return processed_df

#Creates a dataframe for each standard
df_28_day = read_commissioning_data(
    commissioning_data_link, '28-DAY FDS', commissioning_months, 'Total Told', 'Within Standard','Performance', ICB_row
    )
df_31_day = read_commissioning_data(
    commissioning_data_link, '31-Day', commissioning_months, 'Total Treated', 'Within Standard', 'Performance', ICB_row
    )
df_62_day = read_commissioning_data(
    commissioning_data_link, '62-Day', commissioning_months, 'Total Treated', 'Within Standard', 'Performance', ICB_row
    )


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

commissioning_data_link = 'https://www.england.nhs.uk/statistics/wp-content/' \
    + 'uploads/sites/2/2023/11/' \
    + 'CWT-CRS-Commissioner-Time-Series-Jul-2022-Oct-2023-with-Revisions'

def read_in_comminsioning():
    
# link to provider data set
    com_data_link = r'https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2023/12/CWT-CRS-Commissioner-Time-Series-Jul-2022-Oct-2023-with-Revisions.xlsx'
# assigns variable types and renames columns.
    df = (pd.read_excel(com_data_link,
                        sheet_name='28-DAY FDS',
                       skiprows=range(0,4)))
    return df
    
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
