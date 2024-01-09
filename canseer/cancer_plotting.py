import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from data_wrangling import select_data
from data_wrangling import filter_data
from data_wrangling import proportion_breaches

def plot_stacked_referrals(df, subgroups, labels, ncol, graph_title, y_label):
    """

    Parameters
    ----------
    df : dataframe
    subgroups : List
        subgroups of referrals that you would like to plot 
        e.g. subgroups = [df['breaches'], df['within_standard']] will 
        plot number of breached referrals and number within standard for your 
        dataframe over time. 
    labels : list
        List of strings which correspond to the order of the subgroups. 
        e.g. subgroups = [df['breaches'], df['within_standard']] 
        then labels = ['Breaches', 'Within Standard']
    ncol : interger
        The number of subgroups 
    graph_title : string 
        Title of the graph e.g. graph_title = "Cancer referrals in dataframe"
    y_label: string 
       Label of y axis

    Returns
    -------
    fig : Figure
        Stacked plot 
    ax : Axis
        x axis will represent the index of dataframe which is time in months
        y axis will represent the numbers in the subgroups

    """
    # create figure and axis
    fig = plt.figure(figsize=(12, 3))
    ax = fig.add_subplot()
   # set axis titles
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
  # set  x, y ticks
    ax.tick_params(axis='both', labelsize=12)
  # plot and label subgroups 
    stk_plt = ax.stackplot(df.index,
                           subgroups,
                           labels=labels)
    ax.legend(loc='lower center', ncol=ncol)
    plt.title(graph_title)
    return fig, ax

# ToDo for the functions below: display x-axis labels/ticks – currently not working/adding too many 
# Add appropriate titles
# Add national averages to compare with
# Round the proportions displayed

def prop_breaches_graph(df, filters={'start_month':'05-2022',
                                     'end_month':'05-2022',
                                     'standard':'FDS'}, window_size=1):
 # take the dataframe apply the filter function
    df = filter_data(df, filters)
# perform proportion_breaches function on the filtered dataset
    df = proportion_breaches(df, window_size)
# select national comparotor data based on the standard selected in filters
    standard = filters.get('standard')
    if 'FDS' in standard:
        df_nat = get_national_28_day_standard()
    elif 'DTT' in standard:
        df_nat = get_national__31_day_standard()
    elif 'RTT' in standard:
        df_nat = get_national_62_day_standard()
    else:
        print('Standard not recognised')
# apply the timeframe of the dataframe to national data
    df_nat = df_nat.loc[(df_nat.index >= df.index[0])]
    df_nat = df_nat.loc[(df_nat.index <= df.index[-1])]
# run the proportion_breaches function on national data
    df_nat = proportion_breaches(df_nat, window_size)
# A very basic plot would be better to inset your plot from previous function here
# or alternatively I can update my plot to be neater
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
    return fig, ax
    
def breaches_animated_plot(data, filters, window_size=5):
    """
    Create an animated plot with a moving average.

    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the relevant columns.
    - filters (list): A list of tuples specifying the filters to be applied to the data.
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
    fig.add_trace(go.Scatter(x=data['PERIOD'], y=data['PROPORTION_BREACHES'], mode='lines+markers', name='Proportion of Breaches'))

    # Add a line plot for the moving average
    fig.add_trace(go.Scatter(x=data['PERIOD'], y=data['MOVING_AVERAGE'], mode='lines', name=f'Moving Average (Window={window_size})'))

    # Customize the layout
    fig.update_layout(
        title='Proportion of Breaches Over Time',
        xaxis_title='Period',
        yaxis_title='Proportion of Breaches',
        hovermode='x',
        xaxis=dict(tickmode='array',
                   tickvals=data['PERIOD'].astype(int) / 10**9,  # Convert datetime to timestamp in seconds
                   ticktext=data['PERIOD'].dt.strftime('%b %Y'),  # Display months and years as tick labels
                   ),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])
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

    

