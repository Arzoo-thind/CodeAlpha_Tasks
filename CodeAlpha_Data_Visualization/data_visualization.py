import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("books_dataset.csv")

price_clean = (
    df["Price"]
    .astype(str)
    .str.replace("£", "", regex=False)
    .str.replace(r"[^0-9.\-]", "", regex=True)
    .str.strip()
)
df["Price"] = pd.to_numeric(price_clean, errors="coerce")


rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["Rating"] = df["Rating"].map(rating_map).astype(float)
df = df.dropna(subset=["Price", "Rating"]) 
sns.set_style("whitegrid")


plt.figure(figsize=(8,5))
sns.countplot(x="Rating", data=df)
plt.title("Book Rating Distribution")
plt.tight_layout()
plt.savefig("book_rating_distribution.png")
plt.close()


plt.figure(figsize=(8,5))
plt.hist(df["Price"], bins=15)
plt.title("Book Price Distribution")
plt.xlabel("Price (£)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("book_price_distribution.png")
plt.close()


plt.figure(figsize=(8,5))
sns.scatterplot(x="Price", y="Rating", data=df)
plt.title("Price vs Rating")
plt.tight_layout()
plt.savefig("book_price_vs_rating.png")
plt.close()


plt.figure(figsize=(6,4))
sns.heatmap(
    df[["Price","Rating"]].corr(),
    annot=True
)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig("book_correlation_heatmap.png")
plt.close()

print("Books visualizations generated successfully!")