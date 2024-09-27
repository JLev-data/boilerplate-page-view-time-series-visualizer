import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates=True,index_col=0)

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20,5))
    plt.plot(df['value'],'r',data=df)
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy().reset_index()
    df_bar['Year'] = [d.year for d in df_bar.date]
    df_bar['Month'] = [d.strftime('%m') for d in df_bar.date]
    df_bar = df_bar.groupby(by=['Year','Month'],sort=True)['value'].mean().unstack()
    df_bar = df_bar.sort_values(by='Month',axis=1)
    df_bar.columns = pd.Series(data=['January','February','March','April','May','June','July','August','September','October','November','December' ],name='Month')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(7,7))
    df_bar.plot(kind='bar',ax=ax,xlabel='Years',ylabel='Average Page Views')
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['Month'] = pd.Categorical(df_box['Month'], categories=month_order, ordered=True)
    df_box.rename(columns={'value': 'Page Views'},inplace=True)

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(ncols=2,figsize=(20,5))
    sns.boxplot(data=df_box,x='Year',y='Page Views',hue='Year',ax=ax[0],legend=False,fliersize=1).set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(data=df_box,x='Month',y='Page Views',hue='Month',ax=ax[1],fliersize=1).set_title('Month-wise Box Plot (Seasonality)')

    plt.tight_layout()
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
