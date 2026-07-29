import matplotlib.pyplot as plt
import matplotlib as mpl

"""
# --- Colour palette ---
COLORS = {
    'primary':    '#1f77b4',
    'secondary':  '#ff7f0e',
    'highlight':  '#2ca02c',
    'neutral':    '#7f7f7f',
    'palette':    ['#1f77b4', '#ff7f0e', 
                   '#2ca02c', '#d62728', 
                   '#9467bd', '#8c564b',
                   '#e377c2', '#7f7f7f', 
                   '#bcbd22', '#17becf']
}
"""

# --- Colour palette ---
COLORS = {
    'primary':    '#6aaed6',   
    'secondary':  '#2171b5',   
    'highlight':  '#c6dbef',   
    'neutral':    '#8c8c8c',   
    'palette':    [
        '#084594',  
        '#2171b5',  
        '#4292c6',  
        '#6aaed6',  
        '#9ecae1',  
        '#c6dbef',  
        '#deebf7',  
        '#f7fbff',  
        '#3a8fc1',  
        '#84c4dd',  
    ]
}

# --- Typography & layout ---
FONT = 'Arial'   

mpl.rcParams.update({
    'figure.figsize':       (10, 6),
    'figure.dpi':           150,
    'axes.spines.top':      False,
    'axes.spines.right':    False,
    'axes.titlesize':       14,
    'axes.titleweight':     'bold',
    'axes.titlepad':        12,
    'axes.labelsize':       11,
    'xtick.labelsize':      10,
    'ytick.labelsize':      10,
    'legend.frameon':       False,
    'legend.fontsize':      10,
    'font.family':          FONT,
    'text.color':           '#2d2d2d',
    'axes.labelcolor':      '#2d2d2d',
    'xtick.color':          '#2d2d2d',
    'ytick.color':          '#2d2d2d',
})