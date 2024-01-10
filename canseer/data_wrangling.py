import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_provider_data():
    """
    Returns the provider dataframe
    
    Parameters
    ----------
    - None
    
    Returns
    -------
    - df : Data frame
        Dataframe shows the provider i.e. NHS trust total number
        of cancer diagnosis referrals, information about the referral (cancer type,
        stage/route, treatment modality) and for each standard (28, 31, and 62 days)
        the number of referrals meeting the standard and the number of breaches.
        Data is recorded for each month from April 2022 to March 2023.
    """
    # link to provider data set
    provider_data_link = (
        r'https://www.england.nhs.uk/statistics/wp-content/'
        'uploads/sites/2/2023/12/'
        'CWT-CRS-2022-23-Data-Extract-Provider-Final.xlsx'
    )

    # Dictionary to map old column names to new column names
    rename_cols = {
        'STANDARD': 'standard',
        'ORG CODE': 'org_code',
        'TOTAL': 'total',
        'CANCER TYPE': 'cancer_type',
        'STAGE/ROUTE': 'stage_or_route',
        'TREATMENT MODALITY': 'treatment_modality',
        'WITHIN STANDARD': 'within_standard',
        'BREACHES': 'breaches'
    }

    # Dictionary to rename values
    values_change = {
        'cancer_type': {
            'Exhibited (non-cancer) breast symptoms - cancer not initially suspected': 'Unsuspected_breast_ca',
            'Missing or Invalid': 'Invalid',
            'Suspected breast cancer': 'Suspected_breast_ca',
            'Suspected gynaecological cancer': 'Suspected_gynecological_ca',
            'Suspected lower gastrointestinal cancer': 'Suspected_lower_GI_ca',
            'Suspected acute leukaemia': 'Suspected_acute_leukaemia',
            'Suspected brain/central nervous system tumours': 'Suspected_brain_CNS_ca',
            "Suspected children's cancer": 'Suspected_children_ca',
            'Suspected haematological malignancies (excluding acute leukaemia)': 'Suspected_hematological_ca',
            'Suspected head & neck cancer': 'Suspected_head_neck_ca',
            'Suspected lung cancer': 'Suspected_lung_ca',
            'Suspected other cancer': 'Suspected_other_ca',
            'Suspected sarcoma': 'Suspected_sarcoma',
            'Suspected skin cancer': 'Suspected_skin_ca',
            'Suspected testicular cancer': 'Suspected_testicular_ca',
            'Suspected upper gastrointestinal cancer': 'Suspected_upper_GI_ca',
            'Suspected urological malignancies (excluding testicular)': 'Suspected_urological_ca',
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
            ('BREAST SYMPTOMATIC, CANCER NOT SUSPECTED'): 'breast_symptom_non_cancer',
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

    # Explain NaN value in treatment modality
    recode_nan = {'treatment_modality': 'not_applicable_FDS'}

    # Read data from Excel stating which columns to use, rename columns and
    # assign variable types
    df = (
        pd.read_excel(
            provider_data_link,
            usecols=['PERIOD', 'STANDARD', 'ORG CODE',
                     'TREATMENT MODALITY', 'CANCER TYPE',
                     'STAGE/ROUTE', 'TOTAL', 'WITHIN STANDARD', 'BREACHES'
                    ],
            index_col='PERIOD',
            parse_dates=True
        )
        .rename(columns=rename_cols)
        .astype({
            'total': np.int32,
            'within_standard': np.int32,
            'breaches': np.int32
        })
        .fillna(value=recode_nan)
        .assign(
            standard=lambda x: pd.Categorical(x['standard']),
            cancer_type=lambda x: pd.Categorical(x['cancer_type']),
            treatment_modality=lambda x: pd.Categorical(x['treatment_modality']),
            org_code=lambda x: pd.Categorical(x['org_code']),
            stage_or_route=lambda x: pd.Categorical(x['stage_or_route'])
        )
        .replace(values_change)
    )

    # Rename the index to month
    df.index.name = 'month'

    return df
    

def get_national_28_day_standard():
    """
    Creates a national dataframe for the 28 day standard.

    Parameters
    ----------
    - None

    Returns
    -------
    - df - Dataframe
    Data frame with national data for the 28 day standard which
    reports the total referrals, number of breaches, and number within standard
    per month from April 2021 to October 2023. Organisation code for the
    national data set is recorded as NAT. Suitable to be appended to provider
    data.

    """
    # link to national data set
    national_data_link = (
        r'https://www.england.nhs.uk/statistics/wp-content/'
        'uploads/sites/2/2023/12/'
        'CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-'
        'Revisions.xlsx'
    )
    
    # Dictionary of columns to rename
    column_names = {
        'Outside Standard': 'breaches',
        'Within Standard': 'within_standard',
        'Total': 'total'
    }
    
    # read the excel file, including a specific sheet number and columns required,
    # assigns types, and renames columns.
    df = (
        pd.read_excel(
            national_data_link,
            sheet_name="Monthly Performance",
            skiprows=range(0, 3),
            usecols=['Monthly', 'Total', 'Within Standard', 'Outside Standard'],
            index_col='Monthly',
            parse_dates=True
        )
        .astype({'Total': np.int32, 'Within Standard': np.int32, 'Outside Standard': np.int32})
        .rename(columns=column_names)
    )

    # Add extra columns, Org code so its clear if appended to the provider data frame.
    df['org_code'] = 'NAT'
    df['standard'] = '28-day FDS'
    df['cancer_type'] = 'all_national_data'
    df['treatment_modality'] = 'not_applicable_FDS'
    df['stage_or_route'] = 'not_applicable_national_data'
    # columns are categories 
    df = df.assign(
        org_code=lambda x: pd.Categorical(x['org_code']),
        standard=lambda x: pd.Categorical(x['standard']),
        cancer_type=lambda x: pd.Categorical(x['cancer_type']),
        treatment_modality=lambda x: pd.Categorical(x['treatment_modality']),
        stage_or_route=lambda x: pd.Categorical(x['stage_or_route'])
    )
    # names index of df as month
    df.index.name = 'month'
    return df


def get_national_31_day_standard():
    """
    Creates a national dataframe for the 31 day standard

    Parameters
    ----------
    - None

    Returns
    -------
    - df - Dataframe
    A data frame with national data for the 31 day standard which
    reports the total referrals, number of breaches, and number within standard
    per month from April 2022 to October 2023. Organisation code for the
    national data set is recorded as NAT. Suitable to be appended to provider
    data.

    """
    # URL for national data
    national_data_link = (
        r'https://www.england.nhs.uk/statistics/wp-content/'
        'uploads/sites/2/2023/12/'
        'CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-'
        'Revisions.xlsx'
    )
    
    # Dictionary of columns to rename
    column_names = {'Outside Standard.1': 'breaches',
                    'Within Standard.1': 'within_standard',
                    'Total.1': 'total'}
    
    # Dictionary to recode NaN values as 0
    recoding = {'Total.1': 0,
                'Within Standard.1': 0,
                'Outside Standard.1': 0}
    
    # Read the excel file, including specific sheet number and columns required,
    # assigns variable types, and renames columns, fills in NAN values.
    df = (
        pd.read_excel(
            national_data_link,
            sheet_name="Monthly Performance",
            skiprows=range(0, 3),
            usecols=['Monthly', 'Total.1', 'Within Standard.1', 'Outside Standard.1'],
            index_col='Monthly',
            parse_dates=True
        )
        .fillna(value=recoding)
        .astype({'Total.1': np.int32, 'Within Standard.1': np.int32, 'Outside Standard.1': np.int32})
        .rename(columns=column_names)
    )

    # Drop the rows where there is month recorded but no data on referrals
    df = df.drop(df[df['total'] == 0].index)
    
    # Add extra columns so its clear if appended to the provider data frame.
    df['org_code'] = 'NAT'
    df['standard'] = '31-day Combined'
    df['cancer_type'] = 'all_national_data'
    df['treatment_modality'] = 'not_applicable_national_data'
    df['stage_or_route'] = 'not_applicable_national_data'
    # columns are catergories 
    df = df.assign(
        org_code=lambda x: pd.Categorical(x['org_code']),
        standard=lambda x: pd.Categorical(x['standard']),
        cancer_type=lambda x: pd.Categorical(x['cancer_type']),
        treatment_modality=lambda x: pd.Categorical(x['treatment_modality']),
        stage_or_route=lambda x: pd.Categorical(x['stage_or_route'])
    )
    # names index of df as month 
    df.index.name = 'month'
    
    return df

def get_national_62_day_standard():
    """
    Creates a national dataframe for the 62 day standard
    
    Parameters
    ----------
    - None

    Returns
    -------
    - df - Dataframe
        A data frame with national data for the 62 day standard which
        reports the total referrals, number of breaches, and number within standard
        per month from April 2022 to March 2023. Organisation code for the
        national data set is recorded as NAT. Suitable to be appended to provider
        data.

    """
    
    # URL for national data
    national_data_link = (
        r'https://www.england.nhs.uk/statistics/wp-content/'
        'uploads/sites/2/2023/12/'
        'CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-'
        'Revisions.xlsx'
    )
    
    # Dictionary of columns to rename
    column_names = {'Outside Standard.2': 'breaches',
                    'Within Standard.2': 'within_standard',
                    'Total.2': 'total'}
    
    # Dictionary to recode NaN values as 0
    recoding = {'Total.2': 0,
                'Within Standard.2': 0,
                'Outside Standard.2': 0}
    
    # Read the excel file, including specific sheet number and columns required,
    # assigns variable types and renames columns.
    df = (
        pd.read_excel(
            national_data_link,
            sheet_name="Monthly Performance",
            skiprows=range(0, 3),
            usecols=['Monthly', 'Total.2', 'Within Standard.2', 'Outside Standard.2'],
            index_col='Monthly',
            parse_dates=True
        )
        .fillna(value=recoding)
        .astype({'Total.2': np.int32, 'Within Standard.2': np.int32, 'Outside Standard.2': np.int32})
        .rename(columns=column_names)
    )

    # Drop the rows where there is month recorded but no data on referrals
    df = df.drop(df[df['total'] == 0].index)
    
    # Add extra columns so details clear if appended to the provider data frame.
    df['org_code'] = 'NAT'
    df['standard'] = '62-day Combined'
    df['cancer_type'] = 'all_national_data'
    df['treatment_modality'] = 'not_applicable_national_data'
    df['stage_or_route'] = 'not_applicable_national_data'
    # columns are categories 
    df = df.assign(
        org_code=lambda x: pd.Categorical(x['org_code']),
        standard=lambda x: pd.Categorical(x['standard']),
        cancer_type=lambda x: pd.Categorical(x['cancer_type']),
        treatment_modality=lambda x: pd.Categorical(x['treatment_modality']),
        stage_or_route=lambda x: pd.Categorical(x['stage_or_route'])
    )
    # names index of df as month
    df.index.name = 'month'
    return df

#### Filters ####
def select_months(df, start_date='2022-04-01', end_date='2023-03-01'):
    """
    Filter data based on a time frame. 
    Parameters
    ----------
    - df : Dataframe
    - start_date : string 
        Format should be month-year 
        e.g start date of April 2022 is start_date = '04-2022'
    - end_date : string 
        Format should be month-year 
        e.g end date of May 2022 is end_date = '05-2022'

    Returns
    -------
    - df : Dataframe 
        Dataframe with referrals from start to end date.
    """

    df = df.loc[(df.index >= start_date) & (df.index <= end_date)]
    return df


def select_org(df, orgs, strict=False):
    """
    Filters data based on org codes. 
    Parameters
    ----------
    - df : Dataframe
       Dataframe that requires filtering
    - org : String or list of org_codes that you wish to include
        For example org_list = ["R1K", "NAT"] will include data containing
        only provider "R1K" and "NAT" for the national data.

    Raises
    ------
    ValueError
        If any org in org_list is not in the dataframe

    Returns
    -------
    - df: Dataframe
        Dataframe containing only the organisations in the org_code list.

    """
    # list of org codes 
    
    org_list_format=[]
    
    # if one org code supplied check to see if in dataframe 
    if isinstance(orgs, str):
        if not df['org_code'].eq(orgs[:3].upper()).any():
            raise ValueError(
                'Org code in org_list is not in the dataframe')
        # if in df append it to org_list_format
        elif df['org_code'].eq(orgs).any():
            org_list_format.append(orgs[:3].upper())
            
    elif isinstance(orgs, list):

        # check to see if each string in org list is in the dataframe
        for org in orgs:
            if not df['org_code'].eq(org[:3].upper()).any():
                if strict:
                    raise ValueError(
                        'Org code in org_list is not in the dataframe')
                    break
                elif not strict:
                    print(f'Value {org} was not in the list, continuing')
                    continue
            elif df['org_code'].eq(org[:3].upper()).any():
                org_list_format.append(org[:3].upper())      
                
    # Filter dataframe based on the list of org codes
    df = df[df['org_code'].isin(org_list_format)]
    return df 


def select_standard(df, standards, strict=False):
    """
    Filters dataframe based on the standard. 
    
    Parameters
    ----------
     - df : Dataframe
       Dataframe that requires filtering
       
    - standard_list : A string or list of standard that you wish to include from
    
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
                if strict:
                    raise ValueError(error_value_message)
                    break
                elif not strict:
                    print(f'Value "{stan}" not found, continuing filtering for other')
                    continue
                    
        # If it is add the row value to the standard_format list 
            elif stan in standard_dict:
                standard_format.append(standard_dict[stan])
                continue
    # Keep the rows which have a standard in the standard_format list
    df = df[df['standard'].isin(standard_format)]
    return df

def select_cancer(df, cancer_type, strict=False):
    """
    Filters dataframe based on cancer type. 
    Parameters
    ----------
    - df : Dataframe
        Dataframe which requires filtering
    - cancer_typet : List or Str 
        List or string of cancer types you wish to include in data frame.
        e.g. for all breast:
            cancer_type = [Unsuspected_breast_ca', 'Suspected_breast_ca']
    - strict: Bool (default = False)
        If False, ignore incorrect/unexisting value types in the list

    Raises
    ------
    - ValueError
        If the cancer type list contains a cancer type not in the dataframe.

    Returns
    -------
    - df : Dataframe
        Dataframe containing only cancer types in the cancer_type_list

    """
    # Raised error if cancer type not in df 
    if isinstance(cancer_type, str):
        if not df['cancer_type'].eq(cancer_type).any():
            raise ValueError(
                 f'Cancer type "{cancer_type}" are not in the dataframe')
    # returns df filtered based on cancer type 
        else:
            df = df.loc[df.cancer_type ==cancer_type]
            return df
        
   # If a list of cancer type raised error 
    elif isinstance(cancer_type, list):
        # check to see if each string in the cancer type list is in the dataframe.
        for can in cancer_type:
            if not df['cancer_type'].eq(can).any():
        # if strict is False continue to next cancer type in list otherwise break.
                if strict:
                    raise ValueError(
                        f'Cancer type "{cancer_type}" are not in the dataframe')
                    break
                if not strict:
                    print(f'Error ocurred with value "{can}", removing it and continuing')
                    cancer_type.remove(can)
                    continue
            else:
                continue
                
            # filters the dataframe based on the cancer type list
        df = df[df['cancer_type'].isin(cancer_type)]
        return df

def select_treatment_modality(df, treatment_modality, strict=False):
    """
    Filters dataframe based on treatment modality. 
    Parameters
    ----------
    - df : Dataframe
       Dataframe that requires filtering
     treatment_modality: A string or list of treatments that you wish to include
        For example treatment_modality_list = ["surgery", "radiotherapy"]
        will include data containing only surgery and radiotherapy.

    Raises
    ------
    - ValueError
        If any treatment modality is not in the dataframe

    Returns
    -------
    - df  : Dataframe
        Dataframe containing the treatments in treatment_modality_list.

    """
    error_value_message='One of the specified treatment_modality is not in the dataframe'

    # if treatment modality not in df raise error otherwise filter 
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
                if strict:
                    print(f"Error occured with value '{treat}'")
                    raise ValueError(error_value_message)
                    break
                elif not strict:
                    print((f"Value '{treat}' not in df, "
                           + "continuing without it"))
                    treatment_modality.remove(treat)
                    continue
                        
    # Filter dataframe based on the list of treatment modalitys
    df = df[df['treatment_modality'].isin(treatment_modality)]
    return df


def select_stage_or_route(df, stage_or_route):
    """
    Filters data based on stage or route of referral. 
    Parameters
    ----------
    - df : Dataframe
       Dataframe that requires filtering
     - stage_or_route_list: List or str 
     Stage/route that you wish to include
     For example stage_or_route = ["screening", "urgent_suspected_cancer"]
     will include data containing screening and urgent_suspected_cancer
     referrals.

    Raises
    ------
    - ValueError
        If any route/stage is not in the dataframe

    Returns
    -------
    - df : Dataframe
        Dataframe containing the routes or stage in stage_or_route_list

    """
    error_value_message='One of the specified stage_or_route is not in the dataframe'
    
    # if one stage/route given, check to see if it is in the df  filter df based on that stage/route 
    if isinstance(stage_or_route, str):
        
        if stage_or_route not in df['stage_or_route'].unique():
            raise ValueError(error_value_message)
     # filter df based on that stage/route   
        else:
            df = df.loc[df.stage_or_route==stage_or_route]
            return df
        
     # If a list of stage/route is given    
    elif isinstance(stage_or_route, list):
        # check to see if each stage/route is not in the dataframe, raised error messages.
        for stag in stage_or_route:
            if not df['stage_or_route'].eq(stag).any():
        # if criteria is strict stop function 
                if strict:
                    print(f"Error occured with value '{stag}'")
                    raise ValueError(error_value_message)
                    break
        # if criteria is not strict continue with the function 
                elif not strict:
                    print((f"Value '{stag}' not in df, "
                           + "continuing without it"))
                    stage_or_route.remove(stag)
                    continue
                        
    # Filter dataframe based on the list of stage/routes 
    df = df[df['stage_or_route'].isin(stage_or_route)]
    return df


def filter_data(df, filters={}):
    """
    Filters data based on filter dictionary. 
    
    Parameters
    ----------
    - df : dataframe
        dataframe to be filters
    - filters : Dictionary 
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
    - df : Dataframe
       Dataframe with filers applied

    """

    if 'start_month' in filters:
        df = df.loc[(df.index >= filters.get('start_month'))]

    if 'end_month' in filters:
        df = df.loc[(df.index <= filters.get('end_month'))]

    if 'standard' in filters:
        df = select_standard(df, filters.get('standard') )

    if 'org' in filters:
        df = select_org(df, filters.get('org'))

    if 'stage_or_route' in filters:
        df = select_stage_or_route(df, filters.get('stage_or_route'))

    if 'treatment' in filters:
        df = select_treatment_modality(df, filters.get('treatment'))

    if 'cancer_type' in filters:
        df = select_cancer(df, filters.get('cancer_type'))
    return df

#### Help ####


def name_org_code(trust_name=None, print_dict=False):
    """
    Provides the organization code for each trust name.

    Parameters
    ----------
    trust_name : str, optional
        The full name of the NHS Trust. Defaults to None.
    print_dict : bool, optional
        If True, prints the dictionary of names to organization codes. Defaults to False.

    Returns
    -------
    str or dict or None
        If trust_name is specified, returns the organization code for that trust.
        If trust_name is None, prints a dictionary of all names to organization codes
        and returns the dictionary. If trust_name is not found, returns None.

    Notes
    -----
    - Trust names are case-insensitive.
    - Trust names should match exactly for accurate organization code retrieval.

    Examples
    --------
    >>> name_org_code('Manchester University Nhs Foundation Trust')
    'R0A'
    >>> name_org_code(print_dict=True)
    South Tyneside And Sunderland Nhs Foundation Trust: R0B
    University Hospitals Dorset Nhs Foundation Trust: R0D
    ...
    {'Manchester University Nhs Foundation Trust': 'R0A', ...}

    """
    # Read in file with Name and organization code from the data folder
    use_cols = ['Name', 'Organisation Code']
    df = pd.read_csv("canseer/data/ods_data/geographic_etr.csv", usecols=use_cols)

    # Make the 'Name' column into camel case
    df['Name'] = df['Name'].apply(lambda x: x.title())

    # Create a dictionary of names to organization codes
    name_org_code_dict = df.set_index('Name')['Organisation Code'].to_dict()

    if trust_name is not None:
        # Trust_name is case-insensitive
        trust_name = trust_name.title()
        if trust_name not in name_org_code_dict:
            print("Trust name not in dictionary")
            return None
        return name_org_code_dict[trust_name]
    elif trust_name is None:
        # If None input, print the dictionary line by line if print_dict is True
        if print_dict:
            for name, org_code in name_org_code_dict.items():
                print(f"{name}: {org_code}")
        return name_org_code_dict


def nhs_code_link():
    
    """This function reads a link file between the 'ORG_CODE' and NHS Trust name
    Based on NHS Digital data provided here: https://odsdatapoint.digital.nhs.uk/predefined
    """
    
    link_data = (pd
                 .read_csv("canseer/data/ods_data/geographic_etr.csv")
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
    icb_path = ('canseer/data/ons_shapefile/Sub_ICB_Locations_to'
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

##### Proportion of breaches ##### 

def proportion_breaches(df, window_size=1):
    """
    Creates a proportion_breaches column in dataframe and a moving average

    Parameters
    ----------
    - df : dataframe
        Dataframe of cancer referrals 
    - window_size : interger , optional
        Window size over which moving avergae is taken
        For example if window size is 3 moving average taken every 3 months.
        The default is 1.

    Returns
    -------
    - Df dataframe 
    Datafrane with proportion of breaches and moving average. 

    """
    # Calculate the proportion of breaches
    df['proportion_breaches'] = df['breaches'] / df['total']

# Create a sliding window to calculate the moving average of the proportion of breaches
    df['moving_average'] = df['proportion_breaches'].rolling(window=window_size).mean()
    
    return df
