import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from data_wrangling import select_data

def plot_stacked(data, labels, y_label, leg_loc='best', n_cols=1):
    """
    Plots a stack plot over time 
    ----------
    data : dataframe 
    labels : String 
        Labels of different subgroups plotted 
    y_label : String 
        y label axis
    leg_loc : TYPE, optional
        DESCRIPTION. The default is 'best', where the graph is located
    n_cols : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    fig : Time series figure
    ax : axis on the figure

    """
    
    # selects figure size
    fig = plt.figure(figsize=(12,3))
    # select axis label 
    ax = fig.add_subplot()
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    # include x, y grid
    ax.grid(ls='--')

    # set size of x, y ticks
    ax.tick_params(axis='both', labelsize=12)

    # create stacked plot
    stk_plt = ax.stackplot(data['Month'],
                           data.drop('Month',
                           axis=1).T, labels=labels
                           )
    # add legend - matplotlib decides placement
    ax.legend(loc=leg_loc, ncol=n_cols)
            
    return fig, ax


# ToDo for the functions below: display x-axis labels/ticks – currently not working/adding too many 
# Add appropriate titles
# Add national averages to compare with
# Round the proportions displayed
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
    for filter_key, filter_value in filters:
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


