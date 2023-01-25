#lineplot

#lineplot from dataFrame
def dfLineplot(index, columns, *args, **kwargs):
    return **kwargs

#histogramm

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
