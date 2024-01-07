import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


#URL link to commissioner data
commissioner_data_link = 'https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2023/11/CWT-CRS-Commissioner-Time-Series-Jul-2022-Oct-2023-with-Revisions.xlsx'


#Loads data from the excel file and initialises an empty dataframe for analysis 

df_28_day = pd.read_excel(commissioner_data_link, sheet_name='28-DAY FDS', skiprows=3)
df_28_day_analysis = pd.DataFrame()


# This funciton uses a loop to iterate through each of the 3 columns, to get 'month', and then calculates stats such as ICB performance for the 28 day referral
def get_28_day_analysis(df_28_day):
    """ 
    Parameters
    ----------
    df_28_day : dataframe of 28 day standards
    
    Returns
    -------
    Dataframe of the total 28 day cancer standard (Time waiting from urgent referral to patient told they have cancer, or whether this is definitely excluded.
    This is done for each time period (Month) for the Integrated Care Board (ICB) and corresponding ODS code.

    The number of patients who have been told they do or don't have cancer within 28 days is reported, alongside the number of referrals within the standard. 
    Performance is returned as a percentage.

    """
    global df_28_day_analysis
    for i in range(3, len(df_28_day.columns), 3):
         # Extracts the month from the column header
        month = df_28_day.columns[i]
        month_formatted = pd.to_datetime(month, errors='coerce').strftime('%Y-%m') if pd.notna(month) else None

        # Extracts the required data
        if month_formatted:
            total_told = df_28_day.iloc[1:, i]
            within_standard = df_28_day.iloc[1:, i + 1]

        # Calculates the percentage of referrals within the standard
        performance = within_standard.astype(float) / total_told.astype(float) * 100

        # Creates a temporary dataframe for the current month's data
        temp_df = pd.DataFrame({
            'area': df_28_day['Unnamed: 0'] + ' - ' + df_28_day['Unnamed: 1'],
            'time': month_formatted,
            'total_told': total_told,
            'within_standard': within_standard,
            'performance': performance
        })

        # Appends the temporary dataframe to the main dataframe
        df_28_day_analysis = pd.concat([df_28_day_analysis, temp_df], ignore_index=True)

        # Drops rows with NaN values for the 28 day analysis
        df_28_day_analysis = df_28_day_analysis.dropna().reset_index(drop=True)

    return df_28_day_analysis

    #Assigns the result to the global variable and prints the dataframe
df_28_day_analysis = get_28_day_analysis(df_28_day)
print(df_28_day_analysis)


def analyse_day_sheet_with_missing_values(commissioner_data_link, sheet_name= '28-DAY FDS'):
    """
    Parameters
    ----------
    commissioner_data_link : dataframe of commissioner data
    
    Returns
    -------
    A cleaned dataframe of the 28 day commissioner data, accounting for missing values."""
    df_day_sheet = pd.read_excel(commissioner_data_link, sheet_name= '28-DAY FDS', skiprows=3)

    # Initialises an empty dataframe for analysis
    df_day_analysis = pd.DataFrame()

    # Iterates through each group of three columns to extract the data
    for i in range(3, len(df_day_sheet.columns), 3):
        # Extracts the month from the column header
        month = df_day_sheet.columns[i]
        month_formatted = pd.to_datetime(month, errors='coerce').strftime('%Y-%m') if pd.notna(month) else None

        if month_formatted:
            total_treated = df_day_sheet.iloc[1:, i].fillna(0)
            within_standard = df_day_sheet.iloc[1:, i + 1].fillna(0)

            # Calculates the percentage of treatments within the standard, and also replaces NaN with 0 (if applicable)
            performance = within_standard / total_treated * 100
            performance = performance.fillna(0)  

            # Creates a temporary dataframe for this month's data
            temp_df = pd.DataFrame({
                'area': df_day_sheet['Unnamed: 0'] + ' - ' + df_day_sheet['Unnamed: 1'],
                'time': month_formatted,
                'total_treated': total_treated,
                'within_standard': within_standard,
                'performance': performance
            })

            # Appending the temporary dataframe to the main dataframe
            df_day_analysis = pd.concat([df_day_analysis, temp_df], ignore_index=True)

    return df_day_analysis


#need to repeat same functions for 31 day and 62 day dataframes, and cleaning 