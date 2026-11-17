import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mtick
import numpy as np
from matplotlib.colors import to_rgb, to_hex
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

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

CAT_COLORS   = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                '#8c564b', '#e377c2', '#bcbd22', '#17becf']
UNSURE_COLOR = '#a6a6a6'   # bars / lines / nodes
UNSURE_TEXT  = '#7a7a7a'   # tick labels

# Same funding source = same colour in every chart
FUNDING_COLORS = {
    'University/academic institution (cash)':    CAT_COLORS[0],
    'University/academic institution (in-kind)': CAT_COLORS[1],
    'Article Processing Charges (APCs)':         CAT_COLORS[2],
    'APCs':                                      CAT_COLORS[2],
    'Government grants':                         CAT_COLORS[3],
    'Non-government grants':                     CAT_COLORS[4],
    'Membership fees':                           CAT_COLORS[5],
    'Subscriptions':                             CAT_COLORS[6],
    'Advertising':                               CAT_COLORS[7],
    'Other':                                     CAT_COLORS[8],
}
APC_COLORS = {'Charges APC': CAT_COLORS[1], 'No APC': CAT_COLORS[0]}

DATA_FS = 11     # numbers drawn on / next to bars (kept smaller than axis text)
BAR_H   = 0.6    # horizontal bar thickness (fraction of row height)


def esc(s):
    """Escape $ so matplotlib doesn't read '$500-$1000' as math text."""
    return str(s).replace('\\$', '$').replace('$', '\\$')


def is_unsure(label):
    s = str(label).lower()
    return 'unsure' in s or 'prefer not' in s


def sequential_colors(labels, lo=0.28, hi=0.95):
    """labels must be listed smallest -> largest value.
    Smallest = lightest blue, largest = darkest. 'Unsure' labels get grey."""
    real   = [l for l in labels if not is_unsure(l)]
    shades = plt.cm.Blues(np.linspace(lo, hi, len(real)))
    out = {l: to_hex(c) for l, c in zip(real, shades)}
    for l in labels:
        if is_unsure(l):
            out[l] = UNSURE_COLOR
    return out


def text_on(color):
    """Dark text on light fills, white text on dark fills."""
    r, g, b = to_rgb(color)
    return '#2d2d2d' if (0.299 * r + 0.587 * g + 0.114 * b) > 0.6 else 'white'


def hex_to_rgba(color, alpha):
    r, g, b = to_rgb(color)
    return f'rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, {alpha})'


def barh_figsize(n_bars, width=12):
    """Figure size that keeps horizontal bars ~0.45in thick however many rows there are."""
    return (width, n_bars * 0.78 + 2.6)


def grey_unsure_ticklabels(ax, axis='y'):
    labels = ax.get_yticklabels() if axis == 'y' else ax.get_xticklabels()
    for t in labels:
        if is_unsure(t.get_text()):
            t.set_color(UNSURE_TEXT)


def desc_order(labels):
    """Largest value first (labels given smallest -> largest); 'Unsure' always last."""
    real = [l for l in labels if not is_unsure(l)]
    return real[::-1] + [l for l in labels if is_unsure(l)]


def strip_legend(fig, color_map, order, caption=None, title=None, ncols=None, lines=False):
    """One legend strip along the bottom of the figure, entries left->right in `order`.
    Replaces plt.tight_layout(): it lays the figure out and reserves room for the strip."""
    fig_h  = fig.get_figheight()
    cap_in = 0.35 if caption else 0
    if lines:
        handles = [Line2D([0], [0], color=color_map[l], lw=2.5, marker='o', label=esc(l)) for l in order]
    else:
        handles = [Patch(facecolor=color_map[l], label=esc(l)) for l in order]
    fig.legend(handles=handles, loc='lower center',
               bbox_to_anchor=(0.5, cap_in / fig_h),
               ncols=ncols or len(order), frameon=False,
               title=title, columnspacing=1.8, handlelength=1.3)
    if caption:
        fig.text(0.01, 0.1 / fig_h, caption, ha='left', va='bottom',
                 fontsize=10, color='#555555')
    reserve = 0.75 + cap_in + (0.3 if title else 0)
    fig.tight_layout(rect=(0, reserve / fig_h, 1, 1))


def n_labels_pct(ax, totals, x=1.01):
    """'n=..' to the right of 100%-stacked horizontal bars (row i sits at y=i)."""
    for i, n in enumerate(totals):
        ax.text(x, i, f'n={int(n)}', transform=ax.get_yaxis_transform(),
                va='center', ha='left', fontsize=DATA_FS + 1, color='#2d2d2d',
                clip_on=False)


def n_labels_end(ax, bars, values, pad_frac=0.012):
    """'n=..' just past the end of single-series horizontal bars (set xlim first)."""
    xmax = ax.get_xlim()[1]
    for bar, v in zip(bars, values):
        ax.text(v + xmax * pad_frac, bar.get_y() + bar.get_height() / 2,
                f'n={int(v)}', va='center', ha='left',
                fontsize=DATA_FS + 1, color='#2d2d2d')


def stacked_barh_pct(counts, series, colors, title, xlabel='% of journals',
                     legend_order=None, legend_title=None, caption=None,
                     label_min=0.04, label_fn=None, width=12, ytick_labels=None,
                     n_header=None, side_header=None, side_texts=None,
                     savepath=None):
    """100%-stacked horizontal bars. `counts` = DataFrame (rows = bars, top -> bottom;
    columns include `series`, stacked left -> right). `colors` = {series: colour}.
    Optional: n_header (title over the n= column), side_header + side_texts
    (a note column to the right of n=, one string per row)."""
    counts = counts[series]
    totals = counts.sum(axis=1)
    pct    = counts.div(totals, axis=0)
    n_rows = len(counts)
    y      = np.arange(n_rows)
    label_fn = label_fn or (lambda n, p: str(int(n)))

    fig, ax = plt.subplots(figsize=barh_figsize(n_rows, width))
    left = np.zeros(n_rows)
    for col in series:
        ax.barh(y, pct[col], left=left, color=colors[col], height=BAR_H)
        for yi, (l, p, n) in enumerate(zip(left, pct[col], counts[col])):
            if p > label_min:
                ax.text(l + p / 2, yi, label_fn(n, p), ha='center', va='center',
                        color=text_on(colors[col]), fontsize=DATA_FS, fontweight='bold')
        left += pct[col].values

    ax.set_yticks(y)
    ax.set_yticklabels(ytick_labels or [esc(i) for i in counts.index])
    ax.invert_yaxis()                                   # first row on top
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.set_xlim(0, 1)
    ax.set_xlabel(xlabel)
    ax.set_title(title, pad=40 if n_header else None)
    n_labels_pct(ax, totals)
    grey_unsure_ticklabels(ax, 'y')

    tr = ax.get_yaxis_transform()
    if n_header:
        ax.text(1.01, -0.72, n_header, transform=tr, ha='left', va='center',
                fontsize=DATA_FS + 1, fontweight='bold', clip_on=False)
    if side_texts is not None:
        for i, t in enumerate(side_texts):
            ax.text(1.17, i, t, transform=tr, ha='left', va='center',
                    fontsize=DATA_FS + 1, color='#2d2d2d', clip_on=False)
        if side_header:
            ax.text(1.17, -0.72, side_header, transform=tr, ha='left', va='center',
                    fontsize=DATA_FS + 1, fontweight='bold', clip_on=False)

    strip_legend(fig, colors, legend_order or series, caption=caption, title=legend_title)
    if savepath:
        plt.savefig(savepath, bbox_inches='tight')
    plt.show()
    return fig, ax

# --- Typography & layout ---
FONT = 'Arial'   

mpl.rcParams.update({
    'figure.figsize':        (10, 6),
    'figure.dpi':            150,
    'axes.spines.top':       False,
    'axes.spines.right':     False,
    'axes.titlesize':        18,
    'axes.titleweight':      'bold',
    'axes.titlepad':         14,
    'axes.labelsize':        16,
    'axes.labelpad':         14,
    'xtick.labelsize':       13,
    'ytick.labelsize':       13,
    'legend.frameon':        False,
    'legend.fontsize':       13,
    'legend.title_fontsize': 13,
    'font.family':           FONT,
    'text.color':            '#2d2d2d',
    'axes.labelcolor':       '#2d2d2d',
    'xtick.color':           '#2d2d2d',
    'ytick.color':           '#2d2d2d',
})