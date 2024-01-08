# Needs to be kept elsewhere 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_provider_data():
    """
    Returns the provider dataframe
    
    Parameters
    ----------
    None

    Returns
    -------
    df : Data frame
    Dataframe shows the provider i.e. NHS trust total number
    of cancer diagnosis referrals, information about the referall (cancer type,
    stage/route, treatment modality) and for each standard (28, 31 and 62 days)
    the number of referrals meeting the standard and the number of breaches.
    Data is recorded for each month from April 2022 to March 2023.
    """
    # link to national data set
    provider_data_link = r'https://www.england.nhs.uk/statistics/wp-content/' \
        + 'uploads/sites/2/2023/12/' \
        + 'CWT-CRS-2022-23-Data-Extract-Provider-Final.xlsx'

    # Dictionary to map old column names to new column names
    rename_cols = {'STANDARD': 'standard',
                   'ORG CODE': 'org_code',
                   'TOTAL': 'total',
                   'CANCER TYPE': 'cancer_type',
                   'STAGE/ROUTE': 'stage_or_route',
                   'TREATMENT MODALITY': 'treatment_modality',
                   'WITHIN STANDARD': 'within_standard',
                   'BREACHES': 'breaches'}

    # Dictionary to rename values
    values_change = {
        'cancer_type': {
            'Exhibited (non-cancer) breast symptoms - cancer'\
            + ' not initially suspected': 'Unsuspected_breast_ca',
            'Missing or Invalid': 'Invalid',
            'Suspected breast cancer': 'Suspected_breast_ca',
            'Suspected gynaecological cancer': 'Suspected_gynecological_ca',
            'Suspected lower gastrointestinal cancer': 'Suspected_lower_GI_ca',
            'Suspected acute leukaemia': 'Suspected_acute_leukaemia',
            'Suspected brain/central nervous system tumours':
            'Suspected_brain_CNS_ca',
            "Suspected children's cancer": 'Suspected_children_ca',
            'Suspected haematological malignancies'
            + '(excluding acute leukaemia)': 'Suspected_hematological_ca',
            'Suspected head & neck cancer': 'Suspected_head_neck_ca',
            'Suspected lung cancer': 'Suspected_lung_ca',
            'Suspected other cancer': 'Suspected_other_ca',
            'Suspected sarcoma': 'Suspected_sarcoma',
            'Suspected skin cancer': 'Suspected_skin_ca',
            'Suspected testicular cancer': 'Suspected_testicular_ca',
            'Suspected upper gastrointestinal cancer': 'Suspected_upper_GI_ca',
            'Suspected urological malignancies'
            + ' (excluding testicular)': 'Suspected_urological_ca',
            'Breast': 'Breast',
            'Gynaecological': 'Gynecological',
            'Haematological': 'Hematological',
            'Head & Neck': 'Head_Neck',
            'Lower Gastrointestinal': 'Lower_GI',
            'Lung': 'Lung',
            'Other (a)': 'Other',
            'Skin': 'Skin',
            'Upper Gastrointestinal': 'Upper_GI',
            'Urological': 'Urological',
            'ALL CANCERS': 'All_Cancers'
        },
        'treatment_modality': {
            'ALL MODALITIES': 'all',
            'Anti-cancer drug regimen': 'anticancer_drug',
            'Other': 'other',
            'Radiotherapy': 'radiotherapy',
            'Surgery': 'surgery'
        },
        'stage_or_route': {
            'BREAST SYMPTOMATIC, CANCER NOT SUSPECTED': 'breast_symptom_non_cancer',
            'NATIONAL SCREENING PROGRAMME': 'screening',
            'URGENT SUSPECTED CANCER': 'urgent_suspected_cancer',
            'First Treatment': 'first_treatment',
            'Subsequent Treatment': 'subsequent_treatment',
            'Breast Symptomatic': 'breast_symptom',
            'Consultant Upgrade': 'consultant_upgrade',
            'Screening': 'screening',
            'Urgent Suspected Cancer': 'urgent_suspected_cancer'
        }
    }

    # explain NaN value in treatment modality
    recode_nan = {'treatment_modality': 'not_applicable_FDS'}
    # read data from excel stating which columns to use, rename columns and
    # assign variable types
    df = (pd.read_excel(provider_data_link,
                        usecols=['PERIOD',
                                 'STANDARD',
                                 'ORG CODE',
                                 'TREATMENT MODALITY',
                                 'CANCER TYPE',
                                 'STAGE/ROUTE',
                                 'TOTAL',
                                 'WITHIN STANDARD',
                                 'BREACHES'],
                        index_col='PERIOD',
                        parse_dates=True)
          .rename(columns=rename_cols)
          .astype({
              'total': np.int32,
              'within_standard': np.int32,
              'breaches': np.int32})
          .fillna(value=recode_nan)
          .assign(standard=lambda x: pd.Categorical(x['standard']),
                  cancer_type=lambda x: pd.Categorical(x['cancer_type']),
                  treatment_modality=lambda x: pd.Categorical(
                      x['treatment_modality']),
                  org_code=lambda x: pd.Categorical(x['org_code']),
                  stage_or_route=lambda x:  pd.Categorical(
                      x['stage_or_route']))
          .replace(values_change)
          )
    # rename the index to month
    df.index.name = 'month'
    return df


def get_national_28_day_standard():
    """
   Creates a national dataframe for the 28 day standard.

   Parameters
    ----------
    None

    Returns
    -------
    df - Dataframe
    Data frame with national data for the 28 day standard which
    reports the total referals, number of breaches and number within standard
    per month from April 2021 to October 2023. Organisation code for the
    national data set is recorded as NAT. Suitable to be appended to provider
    data.

    """
# link to national data set
    national_data_link = r'https://www.england.nhs.uk/statistics/wp-content/' \
        + 'uploads/sites/2/2023/12/' \
        + 'CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-'\
                         + 'Revisions.xlsx'
    # Dictionary of columns to rename
    column_names = {'Outside Standard': 'breaches',
                    'Within Standard': 'within_standard',
                    'Total': 'total'}
# read the excel file, including specific sheet number and columns required,
# assigns variable types and renames columns.
    df = (pd.read_excel(national_data_link,
                        sheet_name="Monthly Performance",
                        skiprows=range(0, 3),
                        usecols=['Monthly',
                                 'Total',
                                 'Within Standard',
                                 'Outside Standard'],
                        index_col='Monthly',
                        parse_dates=True)
          .astype({'Total': np.int32,
                   'Within Standard': np.int32,
                   'Outside Standard': np.int32})
          .rename(columns=column_names)
          )
    # Add extra columns, Org code, Standard and Cancer_Type so details clear
    # if appended to provider data frame.
    df['org_code'] = 'NAT'
    df['standard'] = '28-day FDS'
    df['cancer_type'] = 'all_national_data'
    df['treatment_modality'] = 'not_applicable_FDS'
    df['stage_or_route'] = 'not_applicable_national_data'
    df = df.assign(org_code=lambda x: pd.Categorical(x['org_code']),
                   standard=lambda x: pd.Categorical(x['standard']),
                   cancer_type=lambda x: pd.Categorical(x['cancer_type']),
                   treatment_modality=lambda x: pd.Categorical(
        x['treatment_modality']),
        stage_or_route=lambda x: pd.Categorical(x['stage_or_route'])
    )
    df.index.name = 'month'
    return df


def get_national_31_day_standard():
    """
    Creates a national dataframe for the 31 day standard

   Parameters
    ----------
    None

    Returns
    -------
    Df- Dataframe
    A data frame with national data for the 31 day standard which
    reports the total referals, number of breaches and number within standard
    per month from April 2022 to October 2023. Organisation code for the
    national data set is recorded as NAT. Suitable to be appended to provider
    data.

    """
    # URL for national data
    national_data_link = r'https://www.england.nhs.uk/statistics/wp-content/'\
                         + 'uploads/sites/2/2023/12/' \
                         + 'CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-'\
                         + 'Revisions.xlsx'
    # Dictionary of columns to rename
    column_names = {'Outside Standard.1': 'breaches',
                    'Within Standard.1': 'within_standard',
                    'Total.1': 'total'}
    # dictionary to recode NaN values as 0
    recoding = {'Total.1': 0,
                'Within Standard.1': 0,
                'Outside Standard.1': 0}
# read the excel file, including specific sheet number and columns required,
# assigns variable types and renames columns, fills in NAN values.
    df = (pd.read_excel(national_data_link,
                        sheet_name="Monthly Performance",
                        skiprows=range(0, 3),
                        usecols=['Monthly',
                                 'Total.1',
                                 'Within Standard.1',
                                 'Outside Standard.1',],
                        index_col='Monthly', parse_dates=True)
          .fillna(value=recoding)
          .astype({'Total.1': np.int32,
                   'Within Standard.1': np.int32,
                   'Outside Standard.1': np.int32})
          .rename(columns=column_names)
          )
    # drop the rows where there is month recorded but no data on referrals
    df = df.drop(df[df['total'] == 0].index)
    # Add extra columns, Org code, Standard and Cancer_Type so details clear
    # if appended to provider data frame.
    df['org_code'] = 'NAT'
    df['standard'] = '31-day Combined'
    df['cancer_type'] = 'all_national_data'
    df['treatment_modality'] = 'not_applicable_national_data'
    df['stage_or_route'] = 'not_applicable_national_data'
    df = df.assign(org_code=lambda x: pd.Categorical(x['org_code']),
                   standard=lambda x: pd.Categorical(x['standard']),
                   cancer_type=lambda x: pd.Categorical(x['cancer_type']),
                   treatment_modality=lambda x: pd.Categorical(
                       x['treatment_modality']),
                   stage_or_route=lambda x: pd.Categorical(x['stage_or_route'])
                   )
    df.index.name = 'month'
    return df


def get_national_62_day_standard():
    """
    Creates a national dataframe for the 62 day standard
    
   Parameters
    ----------
    None

    Returns
    -------
    Df - Dataframe
    A data frame with national data for the 62 day standard which
    reports the total referals, number of breaches and number within standard
    per month from April 2022 to March 2023. Organisation code for the
    national data set is recorded as NAT. Suitable to be appended to provider
    data.

    """
    # URL for national data
    national_data_link = r'https://www.england.nhs.uk/statistics/wp-content/'\
                         + 'uploads/sites/2/2023/12/' \
                         + 'CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-'\
                         + 'Revisions.xlsx'
    # Dictionary of columns to rename
    column_names = {'Outside Standard.2': 'breaches',
                    'Within Standard.2': 'within_standard',
                    'Total.2': 'total'}
    # dictionary to recode NaN values as 0
    recoding = {'Total.2': 0,
                'Within Standard.2': 0,
                'Outside Standard.2': 0}
# read the excel file, including specific sheet number and columns required,
# assigns variable types and renames columns.
    df = (pd.read_excel(national_data_link,
                        sheet_name="Monthly Performance",
                        skiprows=range(0, 3),
                        usecols=['Monthly',
                                 'Total.2',
                                 'Within Standard.2',
                                 'Outside Standard.2'],
                        index_col='Monthly',
                        parse_dates=True)
          .fillna(value=recoding)
          .astype({'Total.2': np.int32,
                   'Within Standard.2': np.int32,
                   'Outside Standard.2': np.int32})
          .rename(columns=column_names)
          .assign(month=lambda x: pd.to_datetime(x['month']))
          )
    # drop the rows where there is month recorded but no data on referrals
    df = df.drop(df[df['total'] == 0].index)
    # Add extra columns, Org code, Standard and Cancer_Type so details clear
    # if appended to provider data frame.
    df['org_code'] = 'NAT'
    df['standard'] = '62-day Combined'
    df['cancer_type'] = 'all_national_data'
    df['treatment_modality'] = 'not_applicable_national_data'
    df['stage_or_route'] = 'not_applicable_national_data'
    df = df.assign(org_code=lambda x: pd.Categorical(x['org_code']),
                   standard=lambda x: pd.Categorical(x['standard']),
                   cancer_type=lambda x: pd.Categorical(x['cancer_type']),
                   treatment_modality=lambda x: pd.Categorical(
                       x['treatment_modality']),
                   stage_or_route=lambda x: pd.Categorical(x['stage_or_route'])
                   )
    df.index.name = 'month'
    return df

#### Filters ####
def select_months(df, start_date='2022-12-01', end_date='2023-01-01'):
    """

    Parameters
    ----------
    df : Dataframe
    start_date : string 
        Format should be month-year 
        e.g start date of April 2022 is start_date = '04-2022'
    end_date :string 
        Format should be month-year 
        e.g end date of May 2022 is end_date = '05-2022'

    Returns
    -------
    df: Dataframe 
    Dataframe with referalls from start to end date.

    """

    df = df.loc[(df.index >= start_date)
                     & (df.index <= end_date)]
    return df

def select_org(df, org_list):
    """

    Parameters
    ----------
    df : Dataframe
       Dataframe that requires filtering
    org_list : List of org_codes that you wish to include
        For example org_list = ["R1K", "NAT"] will include data containing
        only provider "R1K" and "NAT" for the national data.

    Raises
    ------
    ValueError
        If any org in org_list is not in the dataframe

    Returns
    -------
    df: Dataframe
        Dataframe containing only the organisations in the org_code list.

    """
    # Convert org list to uppercase and only use the first three characters
    org_list_format = []
    for org in org_list:
        org_list_format.append(org[:3].upper())
    # check to see if each string in org list is in the dataframe
    for org in org_list_format:
        if not df['org_code'].eq(org).any():
            raise ValueError(
                'Org code in org_list is not in the dataframe')
            break
    # Filter dataframe based on the list of org codes
    df = df[df['org_code'].isin(org_list_format)]
    return df 

def select_standard(df, standards):
    """

    Parameters
    ----------
     df : Dataframe
       Dataframe that requires filtering
       
    standard_list : A string or iterables (list) of standard that you wish to include from
    
    FDS = Four week wait (28 days) from patient told they have cancer to cancer
    diagnosed or excluded.
    DTT = 31 days wait from decision to treat/ earliest clinically appropriate
    date to first or subsequant treatment of cancer.
    RTT = 62 days wait from urgent suspected cancer,
    breast symptomatic referall,urgent screening referall or consultant upgrade
    to first definitive treatment of cancer.
    e.g to include only FDS and DTT standards:
    standard_list = ['FDS', 'DTT']


    Raises
    ------
    ValueError
        If any standard in standard_list is not 'FDS', 'DTT', or 'RTT'

    Returns
    -------
    df : Dataframe
    Containing only standards in standard_list

    """
    # Dictionary of standard in the dataframe
    standard_dict = {'FDS': '28-day FDS',
                     'DTT': '31-day Combined',
                     'RTT': '62-day Combined'}
    standard_format = []
    error_value_message = str('Standards in standard list is not FDS,'
                        + 'DTT, or RTT\n'
                        + 'See help_with("standards")'
                        + 'or help(select_standard)')
    
    # If standard not in dictionary raises error
    if isinstance(standards, str):
        if standards in standard_dict:
            standard_format.append(standard_dict[standards])
        elif standards not in standard:
            raise ValueError(error_value_message)

    elif isinstance(standards, list):
        for stan in standards:
            if stan not in standard_dict:
                raise ValueError(error_value_message)
                break
        # If it is add the row value to the standard_format list 
            else:
                standard_format.append(standard_dict[stan])
                continue
    # Keep the rows which have a standard in the standard_format list
    df = df[df['standard'].isin(standard_format)]
    return df

def select_cancer(df, cancer_type=[]):
    """

    Parameters
    ----------
    df : Dataframe
        Dataframe which requires filtering
    cancer_type_list : List 
        List of cancer types you wish to include in data frame.
        e.g. for all breast:
            cancer_type_list = [Unsuspected_breast_ca', 'Suspected_breast_ca']

    Raises
    ------
    ValueError
        If the cancer type list contains a cancer type not in the dataframe.

    Returns
    -------
    df : Dataframe
        Dataframe containing only cancer types in the cancer_type_list

    """
# check to see if each string in the cancer type list is in the dataframe.
    for can in cancer_type:
        if not df['cancer_type'].eq(can).any():
            raise ValueError(
                'Cancer types in cancer_type_list are not in the dataframe')
            break
        else:
            continue
# filters the dataframe based on the cancer type list
    df = df[df['cancer_type'].isin(cancer_type_list)]
    return df

def select_treatment_modality(df, treatment_modality):
    """

    Parameters
    ----------
    df : Dataframe
       Dataframe that requires filtering
     treatment_modality: A string or list of treatments that you wish to include
        For example treatment_modality_list = ["surgery", "radiotherapy"]
        will includedata containing only surgery and radiotherapy.

    Raises
    ------
    ValueError
        If any treatment modality is not in the dataframe

    Returns
    -------
    df  : Dataframe
        Dataframe containing the treatments in treatment_modality_list.

    """
    error_value_message='One of the specified treatment_modality is not in the dataframe'
    
    if isinstance(treatment_modality, str):
        
        if treatment_modality not in df['treatment_modality'].unique():
            raise ValueError(error_value_message)
        
        else:
            df = df.loc[df.treatment_modality==treatment_modality]
            return df
            

    elif isinstance(treatment_modality, list):
        # check to see if each treatment is not in the dataframe.
        for treat in treatment_modality:
            if not df['treatment_modality'].eq(treat).any():
                print(f"Error occured with value '{treat}'")
                raise ValueError(error_value_message)
                break
    # Filter dataframe based on the list of treatment modalitys
    df = df[df['treatment_modality'].isin(treatment_modality)]
    return df


def select_stage_or_route(df, stage_or_route_list):
    """

    Parameters
    ----------
    df : Dataframe
       Dataframe that requires filtering
     stage_or_route_list: List of stage/route that you wish to include
        For example stage_or_route = ["screening", "urgent_suspected_cancer"]
        will include data containing screening and urgent_suspected_cancer
        referrals.

    Raises
    ------
    ValueError
        If any route/stage is not in the dataframe

    Returns
    -------
    df : Dataframe
        Dataframe containing the routes or stage in stage_or_route_list

    """

    # check to see if each treatment is not in the dataframe.
    for stage in stage_or_route_list:
        if not df['stage_or_route'].eq(stage).any():
            raise ValueError(
                'stage or route in stage_or_route_list is not in the dataframe')
            break
    # Filter dataframe based on the list of stage_or_route
    df = df[df['stage_or_route'].isin(stage_or_route_list)]
    return df

def filter_data(df, filters={}):
    """

    Parameters
    ----------
    df : dataframe
        dataframe to be filters
    filters : Dictionary 
        Filters to be applied to data.
        The following key words should be used 'start_month', 'end_month',
        'standard', 'org', 'stage_or_route', 'treatment', 'cancer_type'.
        Not all the filter keys need to be used.
        If start_month is used the format should be start_month: 'M -YYYY'
        If end_month is used the format should be end_month: 'M -YYYY'
        For the other filters the format should be key: ['string', 'string']
        with 'string' corresponding to the row value or values you would want to include.
        
        For example 
        filters = {'start_month': '08-2022',
           'end_month' : '09-2022',
          'standard': ['FDS', 'DTT'],
          'org': ['RWP', 'RXQ'],
          'stage_or_route': ['subsequent_treatment'],
          'treatment': ['radiotherapy'] }
          
    Returns
    -------
    df : Dataframe
       Dataframe with filers applied

    """

    if 'start_month' in filters:
        df = df.loc[(df.index >= filters.get('start_month'))]

    if 'end_month' in filters:
        df = df.loc[(df.index <= filters.get('end_month'))]

    if 'standard' in filters:
        standard_list = filters.get('standard')
        df = select_standard(df, standard_list)

    if 'org' in filters:
        df = select_org(df, filters.get('org'))

    if 'stage_or_route' in filters:
        df = select_stage_or_route(df, filters.get('stage_or_route'))

    if 'treatment' in filters:
        df = select_treatment_modality(df, filters.get('treatment'))

    if 'cancer_type' in filters:
        df = select_cancer(df, filters.get('cancer_type'))
    return df

def name_org_code(trust_name=None):
    """

    Parameters
    ----------
    name : String,
    The default is None, Name of trust.

    Returns
    -------
    Organisation Code for that trust or if input is None printed
    dictionary of all the Names to Organisation Codes.

    """
    # read in file with Name and organisation code from the data folder
    use_cols = ['Name', "Organisation Code"]
    df = pd.read_csv(r"data/ods_data/geographic_etr.csv", usecols=use_cols)
    # make the columns into a dictionary
    name_org_code_dict = df.set_index('Name')['Organisation Code'].to_dict()
    # trust_name is upper case 
    trust_name = trust_name.upper()
    # if None input print the dictionary 
    if trust_name is None:
        print(name_org_code_dict)
    # if trust_name not in dictionary print a message 
    elif trust_name not in name_org_code_dict:
        print("Trust name not in dictionary")
    # print org_code corresponding to trust_name 
    else:
        print(name_org_code_dict[trust_name])

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
    - topic (str): The topic you need help with. Options are 'standards',
    'cancers', 'orgs', 'stage'.
      If not provided, the function will prompt the user to select a topic.

    Returns:
    None

    Example:
    >>> help_with('cancers')
    """
# description of column data
    fds_description = ("1. The 28-day Faster Diagnosis Standard (FDS).\n"
                       + "The standard: People should have cancer "
                       + "ruled out or receive a diagnosis within 28 days\n"
                       + "NHS target: 75% of people should meet this standard\n\n"
                       )

    dtt_description = ("2. 31-day decision to treat to treatment standard (DTT).\n"
                       + "The standard: Treatment should begin within a month (31 days)"
                       + "of deciding to treat their cancer.\n"
                       + "NHS target: 96% of people should meet this standard\n\n"
                       )

    rtt_description = ("3.62-day referral to treatment standard\n"
                       + "The standard: Treatment should begin within"
                       + "two months (62 days) of an urgent referral.\n"
                       + "NHS target: 85% of people should meet this standard\n\n"
                       )

    cancer_uk_standards = ('https://news.cancerresearchuk.org/'
                           + '2023/08/17/breaking-down-nhs-englands-'
                           + 'changes-in-standards-for-cancer-care/')

    cancer_types_info = ("Cancer Types Information:\n"
                         + "Column in dataset of cancer referrals from\n"
                         + " individual providers (NHS trusts) "
                         + "1.  Unsuspected_breast_ca \n"
                         + "2.  Invalid\n"
                         + "3.  Suspected_breast_ca\n"
                         + "4.  Suspected_gynecological_ca\n"
                         + " 5.  Suspected_lower_GI_ca\n"
                         + " 6.  Suspected_acute_leukaemia\n"
                         + "7.  Suspected_brain_CNS_ca\n"
                         + "8.  Suspected_children_ca\n"
                         + "9.  Suspected_hematological_ca\n"
                         + "10. Suspected_head_neck_ca\n"
                         + "11. Suspected_lung_ca\n"
                         + "12. Suspected_other_ca\n"
                         + "13. Suspected_sarcoma\n"
                         + "14. Suspected_skin_ca\n"
                         + "15. Suspected_testicular_ca\n"
                         + "16. Suspected_upper_GI_ca\n"
                         + " 17. Suspected_urological_ca\n"
                         + "18. Breast\n"
                         + "19. Gynecological\n"
                         + "20. Hematological\n"
                         + "21. Head_Neck\n"
                         + "22. Lower_GI\n"
                         + "23. Lung\n"
                         + "24  Other\n"
                         + "25. Skin\n"
                         + "26. Upper_GI\n"
                         + "27  Urological\n"
                         + "28. All_Cancers\n"
                         + "29. all_national_data\n\n"
                         )

    org_code_info = ("Org_code Information: \n"
                     + "Column in dataset of cancer referrals from"
                     + " individual providers (NHS trusts).\n "
                     + "Each NHS trust is represented by an org_code.\n"
                     + "To find an org_code for an individual trust the"
                     + "function () can be used\n\n"
                     )

    stage_or_route_info = ("Stage_or_route Information: \n"
                           + "Column in dataset of cancer referrals from"
                           + " individual providers (NHS trusts).\n "
                           + "The route of the referral is shown.\n"
                           + "1. breast_symptom_non_cancer\n"
                           + "2. screening\n"
                           + "3. urgent_suspected_cancer\n"
                           + "4. first_treatment\n"
                           + "5. subsequent_treatment\n"
                           + "6. breast_symptom\n"
                           + "7. consultant_upgrade\n"
                           + "8. urgent_suspected_cancer\n"
                           + "9. not_applicable_national_data\n\n")

    treatment_modality_info = ("Treatment_modality Information: \n"
                               + "Column in dataset of cancer referrals from"
                               + " individual providers (NHS trusts).\n "
                               + "Treatment modality applies to the DTT and RTT"
                               + "standards.\n"
                               + "1. Not_applicable_FDS\n"
                               + "2. all\n"
                               + "3. anticancer_drug\n"
                               + "4. other\n"
                               + "5. radiotherapy\n"
                               + "6. surgery\n"
                               + "7. not_applicable_national_data\n\n")

    breaches_info = (
        "Breaches: The number of referrals not meeting the standard\n\n")

    within_standard_info = (
        "Within_standard: The number of referrals meeting the standard")

# Dictionary of selection option
    selection_dict = {1: "standards",
                      2: "cancer_type",
                      3: "org_code",
                      4: "stage_or_route",
                      5: "treatment_modality",
                      6: "breaches",
                      7: "within_standard"}

# If topic not selected ask user for number input
    if topic is None:
        print("Please select which aspect of the data you need help with:" + "\n"
              + "1.) NHS Cancer standards" + "\n"
              + "2.) Types of cancer" + "\n"
              + "3.) NHS Organisation Codes" + "\n"
              + "4.) Stage/Route" + "\n"
              + "5.) Treatment modality" + "\n"
              + "6.) Breaches" + "\n"
              + "7.) Within Standard" + "\n""\n")

        select_topic = int(
            input("Select the number of a topic from above: \n\n"))
        topic = selection_dict[select_topic]

# If topic is selected then print information
    if topic.lower() == 'standards':
        print("There are three standards present in this dataset:\n",
              fds_description,
              dtt_description,
              rtt_description,
              "\n", "Further info at: ", cancer_uk_standards)

    elif topic.lower() == "cancer_type":
        print(cancer_types_info)

    elif topic.lower() == "org_code":
        print(org_code_info)

    elif topic. lower() == "stage_or_route":
        print(stage_or_route_info)

    elif topic.lower() == "treatment_modality":
        print(treatment_modality_info)

    elif topic.lower() == "breaches":
        print(breaches_info)

    elif topic.lower() == "within_standard":
        print(within_standard_info)


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
    ...                      'cancer_type': ['Breast', 'Lung', 'Breast', 'Lung', 'Breast'],
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

            df = df.loc[df['month'] == filter_value]

        elif filter_type == 'org':
            link_data = nhs_code_link()
            valid_org = list(set(df['org_code']) & set(link_data['org_code']))
            filter_value = filter_value[:3].upper()

            if filter_value not in valid_org:
                raise ValueError("Organisation not found. Suggest exploring organisation table.")

            df = df.loc[df['org_code'] == filter_value]

        elif filter_type == 'cancer':
            cancer_col_name = "cancer_type"
            cancer_type_dict = {i + 1: cancer_type for i, cancer_type in enumerate(df[cancer_col_name].unique())}

            if filter_value not in cancer_type_dict.keys():
                raise ValueError("Incorrect 'cancer type' entered")

            print(f"Selected {cancer_type_dict[filter_value]}")
            df = df.loc[df[cancer_col_name] == cancer_type_dict[filter_value]]

        elif filter_type == 'standard':
            standards_dict = {'FDS': '28-day FDS', 'DTT': '31-day Combined', "RTT": '62-day Combined'}

            if filter_value not in standards_dict.keys():
                raise ValueError("See help_with('standards') or help(select_standard)")

            df = df.loc[df['standard'] == standards_dict[filter_value]]

        else:
            raise ValueError("Invalid filter type. Please choose 'month', 'org', 'cancer', or 'standard'.")

    return df

def proportion_breaches(df, window_size=3):
    # Calculate the proportion of breaches
    df['proportion_breaches'] = df['breaches'] / df['total']

# Create a sliding window to calculate the moving average of the proportion of breaches
    df['moving_average'] = df['proportion_breaches'].rolling(window=window_size).mean()
    
    return df
    
################################## NATIONAL DATA #################################
### I think with the new function likely no longer needed 
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
