import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from canseer.data_wrangling import filter_data
from canseer.data_wrangling import proportion_breaches
from canseer.data_wrangling import get_national_28_day_standard, get_national_31_day_standard, get_national_62_day_standard
from canseer.data_wrangling import read_icb_sicb_coding, nhs_code_link


def plot_stacked_referrals(df, subgroups, labels, ncol, graph_title, y_label):
    """
    Returns stacked plot graph of number of referrals over time.
    Parameters
    ----------
    - df : dataframe
    - subgroups : List
        subgroups of referrals that you would like to plot
        e.g. subgroups = [df['breaches'], df['within_standard']] will
        plot number of breached referrals and number within standard for your
        dataframe over time.
    - labels : list
        List of strings which correspond to the order of the subgroups.
        e.g. subgroups = [df['breaches'], df['within_standard']]
        then labels = ['Breaches', 'Within Standard']
    - ncol : interger
        The number of subgroups
    - graph_title : string
        Title of the graph e.g. graph_title = "Cancer referrals in dataframe"
    - y_label: string
       Label of y axis

    Returns
    -------
    - fig : Figure
        Stacked plot
    - ax : Axis
        x axis will represent the index of dataframe which is time in months
        y axis will represent the numbers in the subgroups

    """
    # create figure and axis
    fig = plt.figure(figsize=(12, 3))
    ax = fig.add_subplot()
    #set axis titles
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    #set  x, y ticks
    ax.tick_params(axis='both', labelsize=12)
    #plot and label subgroups
    stk_plt = ax.stackplot(df.index,
                           subgroups,
                           labels=labels)
    ax.legend(loc='lower center', ncol=ncol)
    # add graph_title
    plt.title(graph_title)
    return fig, ax

def prop_breaches_graph(df, filters={'start_month': '05-2022',
                                     'end_month': '05-2022',
                                     'standard': 'FDS'}, labels=None):
    """
    Graph of proportion of breaches of filtered dataset compared to
    proportion of breaches of national dataset
    Parameters
    ----------
    - df : Dataframe
        Dataframe of provider NHS trust level referall data.
    - filters : Dictionary
       Filters to be applied to provider NHS data.
       As with filter_data function filters,  the following key words
       should be used :
           'start_month',
           'end_month',
            'standard',
            'org',
            'stage_or_route',
            'treatment',
            'cancer_type'.
        Not all the filter keys need to be used.
        If start_month is used the format should be start_month: 'M -YYYY'
        If end_month is used the format should be end_month: 'M -YYYY'
        For the other filters the format should be key: ['string', 'string']
        with 'string' corresponding to the row value or values you would want
        to include.
        Only one standard should be compared.
        The default is {'start_month':'05-2022','end_month':'05-2022',
        'standard':'FDS'
      - labels - list 
        labels of dataset the first corresponds to the filtered dataframe
        the second the National dataframe. 
        for example labels = ['Referrals for DTT for surgery from RDE', 
                              'National DTT standard']

    Returns
    -------
    - Touple (matplotlib.figure.Figure, matplotlib.axes) A graph with
    proportion of breaches for a provider NHS trust(s) dataframe
    compared to the proportion of breaches nationally for the same standard.

    """
# take the dataframe apply the filter function
    df = filter_data(df, filters)
# perform proportion_breaches function on the filtered dataset
    df = proportion_breaches(df, window_size=1)
# select national comparotor data based on the standard selected in filters
    standard = filters.get('standard')
    if 'FDS' in standard:
        df_nat = get_national_28_day_standard()
    elif 'DTT' in standard:
        df_nat = get_national_31_day_standard()
    elif 'RTT' in standard:
        df_nat = get_national_62_day_standard()
    else:
        print('Standard not recognised')
# apply the timeframe of the dataframe to national data
    df_nat = df_nat.loc[(df_nat.index >= df.index[0])]
    df_nat = df_nat.loc[(df_nat.index <= df.index[-1])]
# run the proportion_breaches function on national data
    df_nat = proportion_breaches(df_nat, window_size=1)
# Plots the proportion of breaches for df and national df
    x = df.index
    y = df['proportion_breaches']
    fig, ax = plt.subplots()
    ax.plot(x, y)
    x2 = df_nat.index
    y2 = df_nat['proportion_breaches']
    ax.plot(x2, y2)
    ax.set(xlabel='Month', ylabel='Proportion of breaches',
           title='Proportion of breaches over time')
    ax.grid()
    ax.legend(labels, loc='upper left', fontsize='8')
    return fig, ax


def breaches_animated_plot(data, filters, window_size=5):
    """
    Create an animated plot with a moving average.

    Parameters:
    - data (pd.DataFrame): Input DataFrame containing relevant columns.
    - filters (list): A list of tuples specifying filters to be applied.
    - window_size (int): The size of the moving average window.

    Returns:
    - None: The plot is displayed interactively.
    """

    # Apply filters to the data
    data = select_data(data, filters)

    # Sort data by the 'PERIOD' column
    data.sort_values(by='PERIOD', inplace=True)

    # Create the interactive graph
    fig = go.Figure()

    # Add a scatter plot for the proportion of breaches
    fig.add_trace(go.Scatter(x=data['PERIOD'],
                             y=data['PROPORTION_BREACHES'],
                             mode='lines+markers',
                             name='Proportion of Breaches'))

    # Add a line plot for the moving average
    fig.add_trace(go.Scatter(x=data['PERIOD'],
                             y=data['MOVING_AVERAGE'],
                             mode='lines',
                             name=f'Moving Average (Window={window_size})'))

    # Customize the layout
    fig.update_layout(
        title='Proportion of Breaches Over Time',
        xaxis_title='Period',
        yaxis_title='Proportion of Breaches',
        hovermode='x',
        xaxis=dict(tickmode='array',
                   # Convert datetime to timestamp in seconds
                   tickvals=data['PERIOD'].astype(int) / 10**9,
                   # Display months and years as tick labels
                   ticktext=data['PERIOD'].dt.strftime('%b %Y'),
                   ),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None,
                      dict(frame=dict(duration=500, redraw=True),
                           fromcurrent=True)])
                     ])
                     ])

    # Create animation frames
    frames = [go.Frame(data=[go.Scatter(x=data['PERIOD'].iloc[:i + 1],
                                        y=data['MOVING_AVERAGE'].iloc[:i + 1],
                                        mode='lines',
                                        marker=dict(color='red'),
                                        name=f'Moving Average (Window={window_size})')]) for i in range(len(data))]

    # Add frames to the figure
    fig.frames = frames

    # Show the interactive plot
    fig.show()

def create_cmap(threshold=0.25):
    """
    Create a custom colormap with an inflection point.

    Parameters
    ----------
    - threshold : float, optional
        The threshold value at which the color transitions from green to red.
        Should be between 0 and 1. Default is 0.25.

    Returns
    -------
    - custom_cmap : matplotlib.colors.LinearSegmentedColormap
        A custom colormap with an inflection point at the specified threshold.
        The colormap transitions from green to red below the threshold and
        includes additional colors above the threshold.

    Notes
    -----
    The colors below the inflection point are defined by the range of colors
    from bright green to yellow, while the colors above the inflection point
    include shades of red, purple, and transparent red.

    Examples
    --------
    >>> create_cmap()  # Default threshold of 0.25
    <matplotlib.colors.LinearSegmentedColormap object at 0x...>

    >>> create_cmap(threshold=0.5)
    <matplotlib.colors.LinearSegmentedColormap object at 0x...>
    """
    # Define colors for the colormap
    colors_below_inflection = [(0.0, 0.7, 0.0, 1),
                               (1.0, 0.85, 0.0, 1)]
    colors_above_inflection = [(1.0, 0, 0, 0.5),
                               (0.75, 0, 0, 1),
                               (0.7, 0, 0.7, 1)]

    # Define where to change from green to red. This will change by standard
    inflection = threshold

    # Calculate the number of colors for each segment
    num_colors_below_inflection = int(256 * inflection)
    num_colors_above_inflection = 256 - num_colors_below_inflection

    # Create the colormap using LinearSegmentedColormap
    cmap_below_inflection = LinearSegmentedColormap.from_list(
        'below_inflection', colors_below_inflection, N=num_colors_below_inflection
     )
    
    cmap_above_inflection = LinearSegmentedColormap.from_list(
        'above_inflection', colors_above_inflection, N=num_colors_above_inflection
    )

    # Combine the colormaps above and below the inflection point
    cmap_custom = np.vstack(
        (cmap_below_inflection(np.linspace(0, 1, num_colors_below_inflection)),
         cmap_above_inflection(np.linspace(0, 1, num_colors_above_inflection)))
    )

    # Create a custom colormap with an inflection point at the specified threshold
    custom_cmap = LinearSegmentedColormap.from_list(
        'custom_colormap', cmap_custom, N=256
    )

    return custom_cmap

def read_shapefile():
    """
    Read and return a GeoDataFrame from an ONS shapefile for
        Integrated Care Boards (ICBs).

    Returns
    -------
    - gdf : GeoDataFrame
        A GeoDataFrame containing geographical information for ICBs.

    """
    path_to_shapefile = ('canseer/data/ons_shapefile/'
                         + 'Integrated_Care_Boards_'
                         + 'April_2023_EN_BFC_1659257819249669363/')
    gdf = gpd.read_file(path_to_shapefile)
    return gdf

def create_lookup_dict_icb():
    """
    Create lookup dictionaries for ICB codes and NHS Trust organization codes.

    Returns
    -------
    - icb_code_to_names : dict
        A dictionary mapping ICB 3-digit codes to ICB names.
    - org_to_hlhg : dict
        A dictionary mapping NHS Trust organization codes to 
        Higher Level Health Geography.

    Notes
    -----
    - The function reads ICB and SICB coding from an external source.
    - It also retrieves a link between NHS Trust organization codes 
      and Higher Level Health Geography.
    - The resulting dictionaries provide easy lookup for ICB codes 
       and organizational information.

    Examples
    --------
    >>> create_lookup_dict_icb()
    ({'QF7': 'NHS South Yorkshire ICB','QH8': 'NHS Mid and South Essex ICB',...},
     {'R0A': 'QOP', 'R0B': 'QHM', ...})
    """
    icb_codes = read_icb_sicb_coding()
    nhs_link = nhs_code_link()

    # Creates dictionary of ICB 3-digit code to ICB Name
    icb_code_to_names = dict(zip(icb_codes['ICB22CDH'], icb_codes['ICB22NM']))

    # Creates dictionary of NHS Trust Org code to Higher Level Health Geography
    org_to_hlhg = dict(zip(nhs_link['ORG_CODE'], 
                           nhs_link['Higher Level Health Geography']))

    return icb_code_to_names, org_to_hlhg


def select_to_plot(data, gdf=None, filters=None, start_month='2022-04-01',
                   end_month='2023-03-01', standard='FDS',
                   stage_or_route=None, treatment=None,
                   cancer_type=None, return_filtered=False):
    """
    Select and filter data for plotting on a map.

    Parameters
    ----------
    - data : DataFrame
        The input DataFrame containing the data to be filtered and plotted.
    - gdf : GeoDataFrame, optional
        The GeoDataFrame representing the geographical data
        for mapping. Default is None.
    - filters : dict, optional
        A dictionary of filters to apply.
        If provided, other filtering arguments ignored. Default is None.
    start_month : str, optional
        The start month for filtering data. Default is '2022-04-01'.
    end_month : str, optional
        The end month for filtering data. Default is '2023-03-01'.
    standard : str, optional
        The standard for filtering data. Default is 'FDS'.
    stage_or_route : str, optional
        The stage or route for filtering data. Default is None.
    treatment : str, optional
        The treatment modality for filtering data. Default is None.
    cancer_type : str, optional
        The cancer type for filtering data. Default is None.
    - return_filtered : bool, optional
        If True, return the filtered DataFrame
            in addition to the mapped GeoDataFrame and labels.
            This can be useful for checking/more controls over data
        Default is False.

    Returns
    -------
    - result : tuple
        A tuple containing the mapped GeoDataFrame, labels for plotting,
        and optionally, the filtered DataFrame.

    Notes
    -----
    - If filters is provided, other filtering arguments are ignored
    - The function calculates proportions of breaches for each ICB23NM category
    - The GeoDataFrame is merged with the proportions of breaches based on 
    ICB23NM.

    Examples
    --------
    >>> select_to_plot(data, gdf, start_month='2022-04-01',
    ...                end_month='2023-03-01', standard='FDS'
    ...                )
    (<GeoDataFrame>, {'cancer_type': array([...]), 'period': array([...]), 
                        standard': array([...])})

    >>> select_to_plot(data, filters, return_filtered=True)
    (<GeoDataFrame>, {'cancer_type': array([...])}, <DataFrame>)
    """
    if filters is None:
        # Create a dictionary with all arguments
        args_dict = locals()
        keywords = {'start_month', 'end_month',
                    'standard', 'stage_or_route',
                    'treatment', 'cancer_type'
                   }
        filter_dict = ({key: value for key, value
                        in args_dict.items()
                        if key in keywords and value is not None
                       }
                      )
        
    elif filters is not None:
        filter_dict = filters

    filtered_df = filter_data(data, filter_dict)

    icb_code_to_names, org_to_hlhg = create_lookup_dict_icb()

    # Explicitly create a copy to avoid chained indexing
    filtered_df = filtered_df.copy()

    # Use .loc to modify the original DataFrame
    filtered_df.loc[:, 'hlhg'] = filtered_df.loc[:, 'org_code'].map(org_to_hlhg)
    filtered_df.loc[:, 'ICB23NM'] = filtered_df.loc[:, 'hlhg'].map(icb_code_to_names)

    labels_for_plotting = {'cancer_type': filtered_df.cancer_type.unique(),
                           'period': filtered_df.index.unique(),
                           'standard': filtered_df.standard.unique()}

    icb_breaches = round(filtered_df.groupby('ICB23NM').breaches.sum()
                         / filtered_df.groupby('ICB23NM').total.sum(), 2
                        ).astype(float)

    icb_breaches.rename('proportion_breaches', inplace=True)

    if gdf is None:
        gdf = read_shapefile()

    merged_gdf = pd.merge(gdf, icb_breaches, left_on='ICB23NM', right_index=True)

    if not return_filtered:
        return merged_gdf, labels_for_plotting
    elif return_filtered:
        return merged_gdf, labels_for_plotting, filtered_df
    
    
def format_map_label(label_dict):
    """
    Format a label for an Integrated Care Board (ICB) map based
        on the provided information.

    Parameters
    ----------
    label_dict : dict
        Dictionary containing information for the label.
        Output of the 'select_to_plot()' function

    Returns
    -------
    label : str
        Formatted label for the ICB map.

    Notes
    -----
    - 'period' key should contain a list of Timestamps representing
        the time period.
    - 'cancer_type' key should contain a list of cancer types.
    - 'standard' key should contain a list with the standard information.

    Examples
    --------
    >>> label_dict = {'period': [pd.Timestamp('2022-04-01'),
    ...               pd.Timestamp('2023-03-01')],
    ...               'cancer_type': ['Breast', 'Lung'],
    ...               'standard': ['FDS']}
    >>> format_map_label(label_dict)
    'ICB map for FDS standard.\nCancer types:
        Breast, Lung\nPeriod from April 2022 to March 2023'
    """
    start_date = label_dict['period'][0].strftime('%B %Y')
    end_date = label_dict['period'][-1].strftime('%B %Y')
    date_str = f"From {start_date} to {end_date}"

    cancer_type = str()
    if len(label_dict['cancer_type']) < 4:
        for cancer in label_dict['cancer_type']:
            cancer_type += cancer.replace('_', " ") + ", "
    elif len(label_dict['cancer_type']) >= 4:
        cancer_type = "more than 3 cancer types"

    standard_str = label_dict['standard'][0]

    label = (f"ICB map for {standard_str} standard.\n"
             + f"Cancer types: {cancer_type}\n"
             + f"Period from {start_date} to {end_date}")

    return label


def plot_icb_map(data, filters={'standard':'FDS'},
                 figsize=(7, 7), dpi=300,
                 edgecolor='black', lw=0.2):
    """
    Plot an Integrated Care Board (ICB) map based on specified filters.
    Colourmap is reflects which ICBs meet the NHS target for specific standard.


    Parameters
    ----------
    - data : DataFrame
        DataFrame containing the necessary data for mapping.
    - filters : dict, optional
        Dictionary specifying filters for data selection.
        Defaults to {'standard': 'FDS'}. See filter_data()
    - figsize : tuple, optional
        Tuple specifying the figure size. Defaults to (7, 7).
    - dpi : int, optional
        Dots per inch for the figure resolution. Defaults to 300.
    edgecolor : str, optional
        Colour of the map boundaries. Defaults to 'black'.
    - lw : float, optional
        Line width of the map boundaries. Defaults to 0.2.

    Returns
    -------
    - fig : matplotlib.figure.Figure
        The created matplotlib Figure.
    - ax : matplotlib.axes._subplots.AxesSubplot
        The created matplotlib AxesSubplot.

    Examples
    --------
    >>> plot_icb_map(data, filters={'standard': 'FDS'})
    """
    if filters is None:
        print('Data filtering has been suppressed: '
              '"filters" is an empty dict. '
              'Continuing with default select_data() params')
        geodf, all_labels = select_data(data, filters=None)
    else:
        geodf, all_labels = select_to_plot(data, filters=filters)
        if filters['standard'] == 'FDS':
            threshold = 0.25
        elif filters['standard'] == 'DTT':
            threshold = 0.04
        elif filters['standard'] == 'RTT':
            threshold = 0.15

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Plot the GeoDataFrame with specified colormap subplot 'ax'
    geodf.plot(column='proportion_breaches',
               cmap=create_cmap(threshold=threshold),
               legend=False, edgecolor=edgecolor, linewidth=lw, ax=ax)

    plt.title(label=format_map_label(all_labels), fontdict={'fontsize': 7})

    # Create a colorbar next to the subplot
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    # Adjust the normalization based on the data range
    sm = ScalarMappable(
        cmap=create_cmap(threshold=threshold),
        norm=Normalize(vmin=0, vmax=1)
    )
    sm.set_array([])
    plt.colorbar(sm, cax=cax,
                 label=(("Proportion of Breaches\nNHS target threshold"
                         + f"for {filters['standard']} "
                         + f"(<{int(100*threshold)}% breaches)")
                       )
                )

    ax.tick_params(axis='x', which='both', bottom=False,
                   top=False, labelbottom=False
                   )
    ax.tick_params(axis='y', which='both',
                   bottom=False, top=False, labelbottom=False
                  )

    plt.show()

    return fig, ax
