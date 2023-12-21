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