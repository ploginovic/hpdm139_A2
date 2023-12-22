import pandas as pd
import numpy as np


def read_cancer_data(file='main'):
    """
    Reads cancer data from an Excel file or a CSV file based on the specified keyword.

    Parameters:
    - file (str): Keyword specifying the type of cancer data to be read.
      Available options:
        - 'main': Reads data from the NHS England Excel file.
        - 'gdo': Reads data from the Get Data Out (GDO) CSV file.
      Default is 'main'.

    Returns:
    - pandas.DataFrame: A DataFrame containing the cancer data.

    Raises:
    - ValueError: If the specified file keyword is not recognized.

    Examples:
    >>> main_data = read_cancer_data('main')
    >>> gdo_data = read_cancer_data('gdo')
    """
    
    # URLs for the data sources
    full_data_link = ('https://www.england.nhs.uk/'
                      + 'statistics/wp-content/uploads/'
                      + 'sites/2/2023/12/'
                      + 'CWT-CRS-2022-23-Data-Extract-Provider-Final.xlsx')
    
    GDO_all = ("https://www.cancerdata.nhs.uk/"
               + "getdataout/GDO_data_wide.csv")
    
    # Dictionary mapping keywords to data source URLs
    link_keyword_dict = {'main': full_data_link,
                         'gdo': GDO_all}
    
    # Read data based on the specified file keyword
    if file in link_keyword_dict:
        data = pd.read_excel(link_keyword_dict[file]) if file == 'main' else pd.read_csv(link_keyword_dict[file])
    else:
        raise ValueError(f"Unsupported file keyword: {file}")
        
    return data


def select_month(df, month_str):
    """
    Returns a subset of a DataFrame based on the specified month.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the data.
    - month_str (str): A string representing the month
    Returns:
    - pandas.DataFrame: A subset of the input DataFrame containing only
        rows corresponding to the specified month.

    Raises:
    - ValueError: If the specified month abbreviation is not valid.

    Example:
    >>> data = pd.DataFrame({'MONTH': ['JAN', 'FEB', 'MAR', 'APR', 'MAY'],
    ...                      'Value': [10, 15, 20, 25, 30]})
    >>> selected_data = select_month(data, 'mar')
    >>> print(selected_data)
      MONTH  Value
    2   MAR     20
    """
    # List of valid month abbreviations
    month_list = ['APR', 'MAY', 'JUN', 'JUL',
                  'AUG', 'SEP', 'OCT', 'NOV',
                  'DEC', 'JAN', 'FEB', 'MAR']

    # Convert input month string to uppercase and use the first three characters
    month_str = month_str[:3].upper()

    # Check if the specified month is valid
    if month_str in month_list:
        # Select rows corresponding to the specified month
        df_month = df.loc[df.MONTH == month_str]
        return df_month
    else:
        # Raise an error for invalid month abbreviation
        raise ValueError("Invalid month abbreviation. Please enter a valid three-letter month abbreviation.")

def nhs_code_link():
    
    """This function reads a link file between the 'ORG CODE' and NHS Trust name
    Based on NHS Digital data provided here: https://odsdatapoint.digital.nhs.uk/predefined
    """
    
    link_data = (pd
                 .read_csv("data/ods_data/geographic_etr.csv")
                 .loc[:,
                      ['Organisation Code', 'Name','National Grouping',
                       'Higher Level Health Geography', 'Postcode']]
                 .rename({'Organisation Code': 'ORG CODE'}, axis=1, ))
    
    return link_data
