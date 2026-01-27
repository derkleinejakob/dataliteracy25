import preamble
import src.constants as const
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np#
from tueplots import bundles
import seaborn as sns

# import data
df = pd.read_parquet(const.PATH_MIGRATION_SPEECHES_SIMILARITIES)

selected_categories = [
    "immigrants_as_threat",
    "immigrants_as_burden",
    "immigrants_as_problematic"
    # "immigrants_as_victims"
]

category_labels = {
    "immigrants_as_threat": "`Immigration is a Threat'",
    "immigrants_as_burden": "`Immigration is a Burden'",
    "immigrants_as_problematic": "`Immigrants' Culture is Problematic'"
}

# update plotting params for multiple subplots
params = bundles.icml2024(column = "full",nrows=1,ncols=3) 
params.update({"figure.dpi": 350})
plt.rcParams.update(params)

# build plot
fig, axes = plt.subplots(1, 3)
for ax, category in zip(axes.flatten(), selected_categories):
    sns.lineplot(data=df, x='year', y=category, hue='block', markers = False, palette=const.COLOR_MAP_BLOCK, ax=ax, errorbar='ci', alpha=0.75)
    ax.set_title(category_labels[category])
    ax.set_xlabel("")
    ax.set_ylim(0.14, 0.31)   
    ax.set_xlim(2014, 2024)
    if ax == axes.flatten()[0]:
        ax.set_ylabel("Mean Cosine Similarity")
        handles, labels = ax.get_legend_handles_labels()
    else:
        ax.set_yticklabels([])
        ax.set_ylabel("")
    ax.get_legend().remove()
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

fig.legend(handles=handles, labels=[const.LEGEND_BLOCK[label] for label in labels], loc='upper center', ncol=len(const.ORDER_BLOCK), frameon=True, bbox_to_anchor=(0.5, 0.91), fancybox=True, shadow=False)

# fig.tight_layout()
fig.savefig("report/fig/fig4_search.pdf")