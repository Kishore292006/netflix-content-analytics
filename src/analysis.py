from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_FILE = (PROJECT_ROOT / "data" / "processed" / "netflix_cleaned.csv")

def load_cleaned_data(file_path=PROCESSED_FILE):
    df = pd.read_csv(file_path, parse_dates=["date_added"])
    print("Dataset loaded successfully!")
    print("Dataset shape:", df.shape)
    return df

def get_content_type_summary(df):
    summary = (
        df["type"]
        .value_counts()
        .rename_axis("Content Type")
        .reset_index(name="Title Count")
    )
    summary["Percentage"] = (
        summary["Title Count"] / len(df) * 100
    ).round(2)
    return summary

def get_yearly_additions(df):
    yearly = (
        df.dropna(subset=["date_added"])
        .assign(Year=lambda data: data["date_added"].dt.year)
        .groupby("Year")
        .size()
        .reset_index(name="Titles Added")
        .sort_values("Year")
    )
    return yearly

def get_top_countries(df, top_n=10):
    countries = (
        df.loc[df["country"].ne("Unknown") & df["country"].notna(), "country"]
        .str.split(", ")
        .explode()
        .str.strip()
    )
    countries = countries[countries.ne("")]
    return (
        countries.value_counts()
        .head(top_n)
        .rename_axis("Country")
        .reset_index(name="Title Count")
    )

def get_rating_summary(df):
    summary = (
        df["rating"]
        .value_counts()
        .rename_axis("Rating")
        .reset_index(name="Title Count")
    )
    return summary

def get_listed_categories(df, top_n=10):
    categories = (
        df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
        .str.strip()
    )
    categories = categories[categories.ne("")]
    return (
        categories.value_counts()
        .head(top_n)
        .rename_axis("Category")
        .reset_index(name="Title Count")
    )

def print_kpis(df):
    total_titles = len(df)
    movie_count = df["type"].eq("Movie").sum()
    tv_count = df["type"].eq("TV Show").sum()
    movie_share = (
        movie_count / total_titles * 100
        if total_titles > 0
        else 0
    )
    print("\n--- Netflix Catalog KPIs ---")
    print(f"Total titles: {total_titles:,}")
    print(f"Movies: {movie_count:,}")
    print(f"TV Shows: {tv_count:,}")
    print(f"Movie share: {movie_share:.1f}%")

def run_analysis():
    df = load_cleaned_data()
    print_kpis(df)

    print("\n--- Content Type Summary ---")
    print(get_content_type_summary(df).to_string(index=False))

    print("\n--- Yearly Catalog Additions ---")
    print(get_yearly_additions(df).to_string(index=False))

    print("\n--- Top 10 Countries ---")
    print(get_top_countries(df).to_string(index=False))

    print("\n--- Content Ratings ---")
    print(get_rating_summary(df).to_string(index=False))

    print("\n--- Top 10 Individual Categories ---")
    print(get_listed_categories(df).to_string(index=False))

if __name__ == "__main__":
    run_analysis()





