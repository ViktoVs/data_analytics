import matplotlib.pyplot as plt
import seaborn as sns

#lineplot

#lineplot from dataFrame
def df_lineplot(df, index, columns):
    """
    Create a Linplot from a dataframe. Sets a specific Column as Index and draws all lines in the columns list
    """
    df = df.set_index(index)[columns]
    fig = plt.figure(figsize=(16,10))
    plt.xticks(rotation=90)
    plt.grid(axis="y", linestyle="--")
    display(sns.lineplot(df))

#histogramm
def df_histogram(df, column):
    """
    Create a Histogram with a KDE curve
    """
    fig = plt.figure(figsize=(16,10))
    plt.grid(axis="y", linestyle="--")
    display(sns.histplot(df[column], kde=True))
#histogram from dataFrame

# boxplot
def sns_boxplot(df, x, y, hue=None, figsize=(12, 8), y_limit=None):
    fig, ax = plt.subplots(figsize)
    if y_limit is not None:
        ax.set(ylim=(0, y_limit))
    display((sns.boxplot(data=df, x=x, y=y, hue=hue, ax=ax)).figure)

#boxplot from dataFrame

#barplot
def sns_barplot(df, x, y, hue=None, figsize=(12, 8), fmt="d"):
    fig, ax = plt.subplots(figsize=figsize)
    display((sns.barplot(data=df, x=x, y=y, ci=95, hue=hue, ax=ax)).figure)

#barplot rom dataFrame

#heatmap
def sns_heatmap(df, hue=None, figsize=(12, 8), fmt="d"):
    fig, ax = plt.subplots(figsize)
    display((sns.heatmap(data=df, ax=ax, annot=True, fmt=fmt, cbar=False)).figure)


def draw_sankey(
    sources
    , targets
    , values
    , node_labels
    , node_colors
    , link_colors
    ):
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = node_labels,
        color = node_colors
        ),
        link = dict(
        source = sources, 
        target = targets,
        value = values,
        color = link_colors
    ))])

    return fig