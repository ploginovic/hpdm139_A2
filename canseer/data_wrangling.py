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


#Unfinished DOCSTRING
def select_org(df, org_str):
    """
    Pretty much the same as select_month()
    """
    # List of valid organisation codes from the 
    link_data = nhs_code_link()
    valid_org = list(set(df['ORG CODE']) & set(link_data['ORG CODE']))

    # Convert input month string to uppercase and use the first three characters
    org_code = org_str[:3].upper()

    # Check if the specified month is valid
    if org_code in valid_org:
        # Select rows corresponding to the specified month
        df_org = df.loc[df['ORG CODE'] == org_code]
        return df_org
    else:
        # Raise an error for invalid month abbreviation
        raise ValueError("Organisation not found. Suggest exploring organisation table.")
        
        
def help_with(topic=None):
    """
    Provide information and help related to cancer data.

    Parameters:
    - topic (str): The topic you need help with. Options are 'standards', 'cancers', 'orgs', 'stage'.
      If not provided, the function will prompt the user to select a topic.

    Returns:
    None

    Example:
    >>> help_with('cancers')
    """

    fds_description = ("1. The 28-day Faster Diagnosis Standard (FDS).\n"
                       + "The standard: People should have cancer "
                       + "ruled out or receive a diagnosis within 28 days\n"
                       + "NHS target: 75% of people should meet this standard\n\n")

    dtt_description = ("2. 31-day decision to treat to treatment standard (DTT).\n"
                       + "The standard: Treatment should begin within a month (31 days)"
                       + "of deciding to treat their cancer.\n"
                       + "NHS target: 96% of people should meet this standard\n\n")

    rtt_description = ("3.62-day referral to treatment standard\n"
                       + "The standard: Treatment should begin within"
                       + "two months (62 days) of an urgent referral.\n"
                       + "NHS target: 85% of people should meet this standard\n\n")

    cancer_uk_standards = ('https://news.cancerresearchuk.org/'
                          + '2023/08/17/breaking-down-nhs-englands-'
                          + 'changes-in-standards-for-cancer-care/')

    cancer_types_info = ("Cancer Types Information:\n"
                         + "1. Exhibited (non-cancer) breast symptoms - cancer not initially suspected\n"
                         + "2. Missing or Invalid\n"
                         + "3. Suspected breast cancer\n"
                         + "4. Suspected gynaecological cancer\n"
                         + "5. ... (and so on)\n")

    selection_dict = {1: "standards", 2: 'cancers', 3: 'orgs', 4: 'stage'}

    if topic is None:
        print("Please select which aspect of the data you need help with:" + "\n"
              + "1.) NHS Cancer standards" + "\n"
              + "2.) Types of cancer" + "\n"
              + "3.) NHS Organisation Codes" + "\n"
              + "4.) Stage/Route")
        select_topic = int(input("Select the number of a topic from above: \n\n"))
        topic = selection_dict[select_topic]

    if topic.lower() == 'standards':
        print("There are three standards present in this dataset:\n",
              fds_description,
              dtt_description,
              rtt_description,
              '\n', 'Further info at: ', cancer_uk_standards)

    elif topic.lower() == 'cancers':
        print(cancer_types_info)

    # Add additional conditions for other topics (orgs, stage) as needed

def select_cancer(df, cancer_type):
    
    cancer_col_name ='CANCER TYPE'
    cancer_type_dict = ({i + 1: cancer_type for i, cancer_type
                         in enumerate(df[cancer_col_name].unique())})
    
    if cancer_type in cancer_type_dict.keys():
        print(f"Selected {cancer_type_dict[cancer_type]}")
        df = df.loc[df[cancer_col_name]==cancer_type_dict[cancer_type]]
    else:
        raise ValueError("Incorrect cancer type entered")
    return df
    
def select_standard(df, standard='RTT'):
    
    standards_dict = {'FDS':'28-day FDS', 'DTT':'31-day Combined', "RTT":'62-day Combined'}
    
    if standard in standards_dict.keys():
        df = df.loc[df['STANDARD']==standards_dict[standard]]
    else:
        raise ValueError("See help_with(standards) or help(select_standard)")
    return df
    