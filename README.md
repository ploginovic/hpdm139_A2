# hpdm139_Assesment_2
# CANSEER 

## Installation [![PyPI version](https://badge.fury.io/py/canseer.svg)](https://badge.fury.io/py/canseer)
### Canseer 0.1.3 is available on PyPI: https://pypi.org/project/canseer/
pip install canseer

## Binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ploginovic/hpdm139_A2/HEAD?labpath=user_guide.ipynb)
### Alternatively, the user_guide.ipynb notebook can be run on the Jupyter server through Binder. To access this, click on the logo above.
Depending on how you want to use the Notebook, 'Run All' can be selected for a complete demonstration of the package, or selected cells can be run.

<img width="513" alt="Screenshot 2024-01-13 at 10 22 52" src="https://github.com/ploginovic/hpdm139_A2/assets/90516111/958372a8-60b0-4468-a5fb-78216893c6c9">






# Description 
Canseer is a toolkit which allows the user to analyse data from NHS statistics on adherence to cancer diagnosis standards. The data can be downloaded, presented in dataframe and filtered through our data wrangling functions. There are different tools which can be employed to visualise the data, displaying both trends over time and geographical variation.
The 'Canseer'package leverages multiple sources of NHS data, and allows seamless and flexible visualisation of NHS cancer targets on a map.

# Motivation 

Improving cancer diagnosis is a key pillar of the NHS Long Term Plan. The UK has lower cancer survival rates than other comparator countries (Arnold et al. Lancet Oncology 2019 DOI:https://doi.org/10.1016/S1470-2045(19)30456-5) and waiting times for cancer diagnostics is thought to contribute to the poor outcomes seen in the UK. From the 1st October 2023 new cancer diagnosis standards have been announced; Faster Diagnosis Standard: a diagnosis or ruling out of cancer within 28 days of referral (set at 75%), 31-day treatment standard: that treatment should be commenced within 31 days of a decision to treat (set at 96%), 62-day treatment standard: that treatment should be commenced within 62 days of being referred (set at 85%). In order to support and improve cancer diagnosis, there is a need to understand trends in the adherence to these standards at both national and regional levels. Comparing the adherence to these standards across different patient groups (e.g. those awaiting particular treatment types, or with certain cancers) can allow better targeting of diagnostic resources.


NHS statistics collects data nationally, on a provider NHS trust level and on a commissioning level on the cancer diagnosis standards. Our toolkit allows the user the ability to analyse the different datasets provided by NHS statistics in one place. The visualisation tools can help display trends, highlight geographical discrepancies and compare across different patient groups.


#Data

This toolkit uses data provided by NHS statistics website for cancer diagnosis and treatment referrals.

National data - https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2023/12/CWT-CRS-National-Time-Series-Oct-2009-Oct-2023-with-Revisions.xlsx

Provider (NHS Trust) data - https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2023/12/CWT-CRS-2022-23-Data-Extract-Provider-Final.xlsx'

This toolkit also uses data provided by the ONS to link NHS trust regions to geographical areas and a map (shapefile format) of Integrated Care Boards (ICBs); to supply organatisation codes for each NHS trust.

Office for National Statistics Data - https://www.ons.gov.uk/methodology/geography/ukgeographies/healthgeography
 

# User guide 

This is provided in the Juptyer Notebook entitled User guide.


 
