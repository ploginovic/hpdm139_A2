import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


colname_org_code = "ORG_CODE"
cancer_col_name = "CANCER_TYPE"

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
#### NEED TO MAKE PEP8 COMPLIANT
def rename_and_replace(df):
    """
    Rename specified columns and replace values in the 'CANCER_TYPE' column based on a predefined mapping.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: DataFrame with specified column names renamed and values in the 'CANCER_TYPE' column replaced.
    """

    # Dictionary to map old column names to new column names
    cols_to_rename = {'CANCER TYPE': 'CANCER_TYPE', 'ORG CODE': 'ORG_CODE'}

    # Dictionary to map old values to new values in the 'CANCER_TYPE' column
    values_to_change = {
        "CANCER_TYPE": {
            'Exhibited (non-cancer) breast symptoms - cancer not initially suspected': 'unsuspected_breast_ca',
            'Missing or Invalid': 'invalid',
            'Suspected breast cancer': 'suspected_breast_ca',
            'Suspected gynaecological cancer': 'suspected_gynecological_ca',
            'Suspected lower gastrointestinal cancer': 'suspected_lower_GI_ca',
            'Suspected acute leukaemia': 'suspected_acute_leukaemia',
            'Suspected brain/central nervous system tumours': 'suspected_brain_CNS_tumors',
            "Suspected children's cancer": 'suspected_children_cancer',
            'Suspected haematological malignancies (excluding acute leukaemia)': 'suspected_hematological_malignancies',
            'Suspected head & neck cancer': 'suspected_head_neck_ca',
            'Suspected lung cancer': 'suspected_lung_ca',
            'Suspected other cancer': 'suspected_other_ca',
            'Suspected sarcoma': 'suspected_sarcoma',
            'Suspected skin cancer': 'suspected_skin_ca',
            'Suspected testicular cancer': 'suspected_testicular_ca',
            'Suspected upper gastrointestinal cancer': 'suspected_upper_GI_ca',
            'Suspected urological malignancies (excluding testicular)': 'suspected_urological_ca',
            'Breast': 'breast',
            'Gynaecological': 'gynecological',
            'Haematological': 'hematological',
            'Head & Neck': 'head_Neck',
            'Lower Gastrointestinal': 'lower_GI',
            'Lung': 'lung',
            'Other (a)': 'other',
            'Skin': 'skin',
            'Upper Gastrointestinal': 'upper_GI',
            'Urological': 'urological',
            'ALL CANCERS': 'all_Cancers'
        }
    }

    # Rename specified columns
    df.rename(columns=cols_to_rename, inplace=True)

    # Replace values in the 'CANCER_TYPE' column
    df['CANCER_TYPE'] = df['CANCER_TYPE'].map(values_to_change['CANCER_TYPE'])

    return df

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


#Unfinished DOCSTRING
def select_org(df, org_str):
    """
    Pretty much the same as select_month()
    """
    # List of valid organisation codes from the 
    link_data = nhs_code_link()
    valid_org = list(set(df['ORG_CODE']) & set(link_data['ORG_CODE']))

    # Convert input month string to uppercase and use the first three characters
    org_code = org_str[:3].upper()

    # Check if the specified month is valid
    if org_code in valid_org:
        # Select rows corresponding to the specified month
        df_org = df.loc[df['ORG_CODE'] == org_code]
        return df_org
    else:
        # Raise an error for invalid month abbreviation
        raise ValueError("Organisation not found. Suggest exploring organisation table.")
        
def select_cancer(df, cancer_type):
    
    cancer_col_name ='CANCER_TYPE'
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
        

def nhs_code_link():
    
    """This function reads a link file between the 'ORG_CODE' and NHS Trust name
    Based on NHS Digital data provided here: https://odsdatapoint.digital.nhs.uk/predefined
    """
    
    link_data = (pd
                 .read_csv("data/ods_data/geographic_etr.csv")
                 .loc[:,
                      ['Organisation Code', 'Name','National Grouping',
                       'Higher Level Health Geography', 'Postcode']]
                 .rename({'Organisation Code': 'ORG_CODE'}, axis=1, ))
    
    return link_data


def read_icb_sicb_coding():
    """
    Reads the Integrated Care Board (ICB) codes lookup file for Sub-ICB locations
    in England from a CSV file and returns the DataFrame.

    The CSV file contains information mapping Sub-ICB locations to Integrated Care Boards
    in England as of July 2022.

    Returns:
    pd.DataFrame: A DataFrame containing the mapping of Sub-ICB locations to
    Integrated Care Boards in England.
    """
    icb_path = ('data/ons_shapefile/Sub_ICB_Locations_to'
                + '_Integrated_Care_Boards_to_NHS_England'
                + '_(Region)_(July_2022)_Lookup_in_England.csv')
    icb_codes = pd.read_csv(icb_path)
    
    return icb_codes


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

def select_data(df, filters):
    """
    Returns a subset of a DataFrame based on the specified filters.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the data.
    - filters (list of tuples): List of tuples where each tuple contains a filter type and value.

    Returns:
    - pandas.DataFrame: A subset of the input DataFrame containing only
        rows corresponding to the specified filters.

    Raises:
    - ValueError: If any specified filter type or value is not valid.

    Example:
    >>> data = pd.DataFrame({'MONTH': ['JAN', 'FEB', 'MAR', 'APR', 'MAY'],
    ...                      'ORG_CODE': ['R1K', 'R1K', 'R2K', 'R2K', 'R3K'],
    ...                      'CANCER_TYPE': ['Breast', 'Lung', 'Breast', 'Lung', 'Breast'],
    ...                      'STANDARD': ['28-day FDS', '31-day Combined', '62-day Combined', '28-day FDS', '31-day Combined'],
    ...                      'Value': [10, 15, 20, 25, 30]})
    >>> selected_data = select_data(data, [('month', 'mar'), ('org', 'r1k')])
    >>> print(selected_data)
      MONTH ORG_CODE CANCER_TYPE      STANDARD  Value
    0   JAN      R1K      Breast      28-day FDS     10
    1   FEB      R1K        Lung  31-day Combined     15
    """
    for filter_type, filter_value in filters:
        if filter_type == 'month':
            month_list = ['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR']
            filter_value = filter_value[:3].upper()

            if filter_value not in month_list:
                raise ValueError("Invalid month abbreviation. Please enter a valid three-letter month abbreviation.")

            df = df.loc[df['MONTH'] == filter_value]

        elif filter_type == 'org':
            link_data = nhs_code_link()
            valid_org = list(set(df['ORG_CODE']) & set(link_data['ORG_CODE']))
            filter_value = filter_value[:3].upper()

            if filter_value not in valid_org:
                raise ValueError("Organisation not found. Suggest exploring organisation table.")

            df = df.loc[df['ORG_CODE'] == filter_value]

        elif filter_type == 'cancer':
            cancer_col_name = "CANCER_TYPE"
            cancer_type_dict = {i + 1: cancer_type for i, cancer_type in enumerate(df[cancer_col_name].unique())}

            if filter_value not in cancer_type_dict.keys():
                raise ValueError("Incorrect 'cancer type' entered")

            print(f"Selected {cancer_type_dict[filter_value]}")
            df = df.loc[df[cancer_col_name] == cancer_type_dict[filter_value]]

        elif filter_type == 'standard':
            standards_dict = {'FDS': '28-day FDS', 'DTT': '31-day Combined', "RTT": '62-day Combined'}

            if filter_value not in standards_dict.keys():
                raise ValueError("See help_with(standards) or help(select_standard)")

            df = df.loc[df['STANDARD'] == standards_dict[filter_value]]

        else:
            raise ValueError("Invalid filter type. Please choose 'month', 'org', 'cancer', or 'standard'.")

    return df

def proportion_breaches(df, window_size=3):
    # Calculate the proportion of breaches
    df['PROPORTION_BREACHES'] = df['BREACHES'] / df['TOTAL']

# Create a sliding window to calculate the moving average of the proportion of breaches
    df['MOVING_AVERAGE'] = df['PROPORTION_BREACHES'].rolling(window=window_size).mean()
    
    return df

################################## NATIONAL DATA #################################

# Link for national data file perhaps should be stored elsewhere 
national_data_link = r'https://www.england.nhs.uk/statistics/wp-content/' \
    + 'uploads/sites/2/2023/12/' \
    + 'CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-Revisions.xlsx'


def get_national(national_data_link=national_data_link):
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