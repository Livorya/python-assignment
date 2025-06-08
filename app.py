import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import functions as func


st.write("# Analysis of Diamonds")

diamonds = func.load_data()

if not diamonds.empty:
  # setup
  diamonds["cut"] = pd.Categorical(diamonds.cut, ["Fair", "Good", "Very Good", "Premium", "Ideal"], ordered=True)
  diamonds["clarity"] = pd.Categorical(diamonds.clarity, ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"], ordered=True)
  diamonds["color"] = pd.Categorical(diamonds.color, " ".join("JIHGFED").split(), ordered=True)

  diamonds_clean = func.clean_data(diamonds).reset_index()

  # table
  st.write("#### Table of Diamonds after cleaning the data")
  st.write("(cleaning = removing duplicates and incorrect data)")
  st.dataframe(diamonds_clean)
  st.write(f"Number of rows = {len(diamonds_clean)}")

  # carat bins setup
  diamonds_clean["carat_bins"] = pd.cut(diamonds_clean["carat"], 9)
  mean_carat_bins = round(diamonds_clean.groupby("carat_bins", observed=False)["carat"].mean(), 2)

  carat_range = diamonds_clean.copy()
  carat_range = carat_range.groupby("carat_bins", observed=False).first().index.values

  carat_bin_dfs = {}
  for i, interval in enumerate(carat_range):
    df_interval = diamonds_clean[diamonds_clean["carat_bins"] == interval].copy()
    carat_bin_dfs[f"df_bin_{i}"] = df_interval

  # carat-price scatterplot
  st.write("#### The effect on the price by carat")
  fig, ax = plt.subplots(figsize=(9, 5))

  ax.scatter(
      diamonds_clean["carat"], 
      diamonds_clean["price"], 
      marker="D",
      edgecolors="slateblue",
      facecolors="skyblue",
      linewidths=0.5,
      alpha=0.7
  )
  ax.set_xlabel("Carat")
  ax.set_ylabel("Price")
  ax.set_title("Price per Carat")

  plt.tight_layout()
  st.pyplot(fig)
  st.write("You can clearly see the positive correlation between the price and carat. You can see that the lowest price per carat goes up from beginning to end. The highest price per carat seems to be affected by other variabels.")

  # carat-price boxplot
  st.write("##### The distrubution of prices per carat bin")
  fig, ax = plt.subplots()
  ax = func.boxplot_category_to_price(diamonds_clean, "carat_bins", "Set3", "black", True)
  ax.set_xticklabels(mean_carat_bins)
  ax.set_xlabel("Carat bins (mean values)")

  plt.title("Carat - price distrubution")
  st.pyplot(fig)

  st.write("The division of carats shows where the price distrubution is the heaviest per bin.")

  #carat-price scatterplot with bins
  fig, ax = plt.subplots(figsize=(10, 6))

  func.make_scatterplot(diamonds_clean, "carat_bins", "Set3", ax)
  ax.set_title("Price per Carat by Carat Bin")
  ax.set_xlabel("Carat")
  ax.set_ylabel("Price")

  plt.tight_layout()
  st.pyplot(fig)

  st.write("This figure helps show how I will divide the graf in later comparisions.")

  st.write("##### How clarity plays a part on the price of the diamond")
  # clarity-price boxplot
  fig, ax = plt.subplots()
  ax = func.boxplot_category_to_price(diamonds_clean, "clarity", "cubehelix", "gray")

  for i,text in enumerate(ax.texts):
    text.set_color(func.text_color_light_to_dark(diamonds_clean, "clarity", i))

  st.pyplot(fig)

  st.write("You can see a slight upturn per category exept for the last two. Future grafs will show that this is completley size related.")

  # carat-price scatterplot with clarity
  st.write("##### The distrubution of prices per carat when colored by the clarity categories")
  fig, ax = plt.subplots(figsize=(10, 6))
  func.make_scatterplot(diamonds_clean, "clarity", "cubehelix", ax)

  ax.set_title("Price per Carat by Clarity")
  ax.set_xlabel("Carat")
  ax.set_ylabel("Price")

  plt.tight_layout()
  st.pyplot(fig)

  st.write("Here you can see that the last two categories are primarily in the first smaller carat bins.")
  st.write("This graf is hard to properly see how the clarity effects the price. Next graf will have the image divided into the carat bins to see a bit more clearly.")

  # carat bin-price scatterplots with clarity
  st.write("##### The distrubution of prices per carat bin when colored by the clarity categories")
  n_bins = len(carat_bin_dfs)
  n_cols = 2 
  n_rows = (n_bins + n_cols - 1) // n_cols 

  fig, axs = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
  axs = axs.flatten()  

  for i, bin_name in enumerate(carat_bin_dfs):
    ax = axs[i]
    func.make_carat_bin_plot("clarity", carat_bin_dfs[bin_name], "cubehelix", ax)
    ax.set_title(f"Carat bin: {bin_name}")
    ax.set_title(f"Price per Carat {carat_range[i]} by Clarity")
    ax.set_xlabel("Carat")
    ax.set_ylabel("Price")

  for j in range(i + 1, len(axs)):
    axs[j].set_visible(False)

  plt.tight_layout()
  st.pyplot(fig)

  st.write("When slightly enlarged it shows more clearly that there is a gradient from lowest quality up to the highest quality. It shows that the clarity does play a part to the pricing of the diamond.")
  st.write("It also shows that the bigger the diamond the lesser the quality seems to get.")

  st.write("##### How color plays a part on the price of the diamond")
  # color-price boxplot
  fig, ax = plt.subplots()
  ax = func.boxplot_category_to_price(diamonds_clean, "color", "Spectral")

  st.pyplot(fig)

  st.write("The color price distrubution seems almost to be dropping in price the better the color quality.")

  # carat-price scatterplot with color
  st.write("##### The distrubution of prices per carat when colored by the color categories")
  fig, ax = plt.subplots(figsize=(10, 6))
  func.make_scatterplot(diamonds_clean, "color", "Spectral", ax)

  ax.set_title("Price per Carat by Color")
  ax.set_xlabel("Carat")
  ax.set_ylabel("Price")

  plt.tight_layout()
  st.pyplot(fig)
  
  st.write("You can see the gradient of the color quality from lowest to highest. Even if the graf is a little hard to see there seems to be an even larger correlation between lower carat and better color than with clarity.")

  # carat bin-price scatterplots with color
  st.write("##### The distrubution of prices per carat bin when colored by the color categories")
  n_bins = len(carat_bin_dfs)
  n_cols = 2 
  n_rows = (n_bins + n_cols - 1) // n_cols 

  fig, axs = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
  axs = axs.flatten()  

  for i, bin_name in enumerate(carat_bin_dfs):
    ax = axs[i]
    func.make_carat_bin_plot("color", carat_bin_dfs[bin_name], "Spectral", ax)
    ax.set_title(f"Carat bin: {bin_name}")
    ax.set_title(f"Price per Carat {carat_range[i]} by Color")
    ax.set_xlabel("Carat")
    ax.set_ylabel("Price")

  for j in range(i + 1, len(axs)):
    axs[j].set_visible(False)

  plt.tight_layout()
  st.pyplot(fig)

  st.write("There is clearly a correlation between color and carat. It is also very clear that there is an effect on the price of the diamond.")

  st.write("##### How cut plays a part on the price of the diamond")
  # cut-price boxplot
  fig, ax = plt.subplots()
  ax = func.boxplot_category_to_price(diamonds_clean, "cut", "hls")

  st.pyplot(fig)

  st.write("The cut does seem to have some effect on the pricing.")

  # carat-price scatterplot with cut
  st.write("##### The distrubution of prices per carat when colored by the cut categories")
  fig, ax = plt.subplots(figsize=(10, 6))
  func.make_scatterplot(diamonds_clean, "cut", "hls", ax)

  ax.set_title("Price per Carat by Cut")
  ax.set_xlabel("Carat")
  ax.set_ylabel("Price")

  plt.tight_layout()
  st.pyplot(fig)

  st.write("This graf is extremley hard to see how the cut categories works with each other.")

  # carat bin-price scatterplots with cut
  st.write("##### The distrubution of prices per carat bin when colored by the cut categories")
  n_bins = len(carat_bin_dfs)
  n_cols = 2 
  n_rows = (n_bins + n_cols - 1) // n_cols 

  fig, axs = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
  axs = axs.flatten()  

  for i, bin_name in enumerate(carat_bin_dfs):
    ax = axs[i]
    func.make_carat_bin_plot("cut", carat_bin_dfs[bin_name], "hls", ax)
    ax.set_title(f"Carat bin: {bin_name}")
    ax.set_title(f"Price per Carat {carat_range[i]} by Cut")
    ax.set_xlabel("Carat")
    ax.set_ylabel("Price")

  for j in range(i + 1, len(axs)):
    axs[j].set_visible(False)

  plt.tight_layout()
  st.pyplot(fig)

  st.write("Even in a close up it is hard to tell how the cut affects the price. By showing how each cut category disributes over the graf will help visualize how they relate to one another.")

  # carat-price per cut category
  st.write("##### The distrubution of prices per carat per cut categories")
  cut_order = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
  cuts_in_data = diamonds_clean["cut"].unique()
  ordered_cuts = [cut for cut in cut_order if cut in cuts_in_data]

  n = len(ordered_cuts)
  n_cols = 2
  n_rows = (n + n_cols - 1) // n_cols

  fig, axs = plt.subplots(n_rows, n_cols, figsize=(12, 5 * n_rows))
  axs = axs.flatten()

  for i, cut in enumerate(ordered_cuts):
    ax = axs[i]
    subset = diamonds_clean[diamonds_clean["cut"] == cut]
    func.make_scatterplot(subset, "cut", "hls", ax)
    ax.set_title(f"Price per Carat - Cut: {cut}")
    ax.set_xlabel("Carat")
    ax.set_ylabel("Price")

  for j in range(i + 1, len(axs)):
    axs[j].set_visible(False)

  plt.tight_layout()
  st.pyplot(fig)

  st.write("This graf shows how all cuts seems to exist in seemingly every carat and price level. The cut does not seem to have that big of an impact on the price.")

  st.write("#### My conclusion")
  st.write("The conclusion is that carat has a big inpact on the price of the diamond.")
  st.write("The clarity affect the pricing and the better the clarity the more it contibutes to a better price. It is also clear that the bigger the diamond the lesser the clarities quality seems to be.")
  st.write("The color does also affect the pricing in a good way where it is clear that the nicer the color the better the price is. Here is an even bigger effect of how the bigger the diamond the worse the color seems to be.")
  st.write("Cut seems to have some positive effect on the price but not by much.")

