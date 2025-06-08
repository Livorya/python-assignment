import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import requests
from io import StringIO


@st.cache_data
def load_data():
    """Loads data from a csv-file from a specified GitHub repository and returns it as a dataframe."""
    url = "https://raw.githubusercontent.com/Livorya/python-assignment/refs/heads/main/data/diamonds.csv"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None

def calc_depth(x, y, z):
  """Calculates depth of a diamond using the standard formula and returns the result as procentage with one decimal."""
  return round(2 * (z / (x + y)) * 100, 1)

def clean_data(diamonds_df):
  """Cleans diamond data in the order that has been proven to be most correct."""
  diamonds_clean = diamonds_df[diamonds_df.duplicated(keep="first") == False]

  diamonds_clean = diamonds_clean[(diamonds_clean.y < 30) & (diamonds_clean.z < 30) & (diamonds_clean.x > 0) & (diamonds_clean.y > 0) & (diamonds_clean.z > 0)].copy()

  diamonds_calc_depth = pd.DataFrame(diamonds_clean, columns=["x", "y", "z", "depth"])
  diamonds_calc_depth["depth_calc"] = calc_depth(diamonds_calc_depth.x, diamonds_calc_depth.y, diamonds_calc_depth.z)
  diamonds_clean = diamonds_clean.loc[diamonds_calc_depth["depth"] == diamonds_calc_depth["depth_calc"]]

  diamonds_no_xyz = pd.DataFrame(diamonds_clean, columns=["carat", "cut", "clarity", "color","depth", "table", "price"])
  diamonds_clean = diamonds_clean[diamonds_no_xyz.duplicated(keep="first") == False]

  diamonds_4c = pd.DataFrame(diamonds_clean, columns=["carat", "cut", "clarity", "color", "price"])
  diamonds_clean = diamonds_clean[diamonds_4c.duplicated(keep="first") == False]

  return diamonds_clean
    
def text_color_light_to_dark(df, column, nr):
  """Selects the color of the text in a boxplot for a given column, going from light to dark."""
  even = len(df[column].value_counts().values) % 2 == 0
  middle_nr = len(df[column].value_counts().values) // 2

  if nr < middle_nr:
    return "w"
  elif even:
    if nr >= middle_nr:
      return "k"
  elif nr > middle_nr:
    return "k"
  else:
    return "gray"
  
def boxplot_category_to_price(df, category, palette, text_color="black", use_legend=False):
  """Creates a series of boxplot for the categories using hue looking at the distrubution over price."""
  ax = sns.boxplot(x=category, y="price", data=df, hue=category, legend=use_legend, palette=palette, medianprops={"color":text_color})
  plt.title(f"{category.capitalize()} - price distrubution")
  ax.set_xlabel(f"{category.capitalize()}")
  ax.set_ylabel("Price")

  medians = df.groupby([category], observed=False)["price"].median().values
  nr = df[category].value_counts().values
  nr = [str(x) for x in nr.tolist()]
  nr = ["nr: " + i for i in nr]

  pos = range(len(nr))
  for tick in pos:
    ax.text(pos[tick],
            medians[tick],
            nr[tick],
            horizontalalignment="center",
            verticalalignment="bottom",
            fontsize=6,
            color=text_color,
            weight="semibold")
  return ax

def make_scatterplot(df, category, palette, ax, use_legend=True):
  """Returns a seaborn scatterplot for the dataframe, colored after the category in the palette given."""
  return sns.scatterplot(
    data=df,
    ax=ax,
    x="carat",
    y="price",
    hue=category,
    palette=palette,
    legend=use_legend,
    marker="D",
    edgecolor="dimgray",
    s=60,
    alpha=0.7
  )

def make_carat_bin_plot(category, carat_bin_df, palette, ax):
  """Returns a seaborn scatterplot for the given carat bin colored after the category in the palette given."""
  return sns.scatterplot(
    data=carat_bin_df,
    ax=ax,
    x="carat",
    y="price",
    hue=category,
    palette=palette,
    marker="D",
    edgecolor=None,
    s=60,
    alpha=0.6
  )
