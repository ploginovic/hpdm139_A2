import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

