from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE=PROJECT_ROOT / "data" / "raw" / "netflix_titles.csv"
PROCESSED_DIR=PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE=PROCESSED_DIR / "netflix_cleaned.csv"

def load_data(file_path=RAW_FILE):
    """"Load the raw Netflix data"""
    df_raw = pd.read_csv(file_path)
    print('original dataset shape:', df_raw.shape)
    return df_raw.copy()

def correct_duration_values(df):
    corrections={
        "s5542": "74 min",
        "s5795": "84 min",
        "s5814": "66 min"
    }
    for show_id,duration in corrections.items():
        mask=df['show_id'].eq(show_id)
        df.loc[mask,'rating']=np.nan
        df.loc[mask,'duration']=duration

    return df

def handle_missing_values(df):
    for column in ['director','cast','country','rating']:
        df[column]=df[column].fillna('Unknown')

    df['date_added']=pd.to_datetime(
        df['date_added'].astype('string').str.strip(),
    format='%B %d, %Y',
    errors='coerce'
    )
    return df

def normalize_text_fields(df):
    text_columns=df.select_dtypes(
        include=['object','string']
    ).columns
    for column in text_columns:
        df[column]=(
            df[column]
            .str.replace(r'[\r\n]+',' ',regex=True)
            .str.strip()
        )
    return df

def validate_data(df):
    print("\n--- Data Validation ---")

    print("Dataset shape:", df.shape)
    print("Unique show IDs:", df["show_id"].nunique())
    print("Duplicate rows:", df.duplicated().sum())
    print("Duplicate show IDs:", df["show_id"].duplicated().sum())

    movie_mask = df["type"].eq("Movie")
    tv_mask = df["type"].eq("TV Show")
    invalid_movies = df.loc[
        movie_mask
        & ~df["duration"].str.fullmatch(r"\d+ min", na=False)
    ]
    invalid_tv_shows = df.loc[
        tv_mask
        & ~df["duration"].str.fullmatch(r"\d+ Seasons?", na=False)
    ]
    print("Invalid movie durations:", len(invalid_movies))
    print("Invalid TV Show durations:", len(invalid_tv_shows))

    if df.duplicated().any():
        raise ValueError("Validation failed: duplicate rows found.")

    if df["show_id"].duplicated().any():
        raise ValueError("Validation failed: duplicate show IDs found.")

    if len(invalid_movies) > 0:
        raise ValueError("Validation failed: invalid movie durations found.")

    if len(invalid_tv_shows) > 0:
        raise ValueError("Validation failed: invalid TV Show durations found.")

    print("Data validation passed!")

def save_data(df, output_path=OUTPUT_FILE):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print("\nCleaned dataset saved to:", output_path)

def verify_saved_data(file_path=OUTPUT_FILE):
    df_saved = pd.read_csv(file_path)

    print("\n--- Saved File Verification ---")
    print("File exists:", file_path.exists())
    print("Saved dataset shape:", df_saved.shape)
    print("Unique show IDs:", df_saved["show_id"].nunique())

def check_remaining_line_breaks(df):
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns
    remaining_line_breaks = sum(
        df[column]
        .astype("string")
        .str.contains(r"[\r\n]", regex=True, na=False)
        .sum()
        for column in text_columns
    )
    print(
        "\nRemaining line breaks in text fields:",
        remaining_line_breaks
    )

def clean_data():
    df_raw = load_data()
    df_corrected = correct_duration_values(df_raw)
    df_cleaned = handle_missing_values(df_corrected)
    df_cleaned = normalize_text_fields(df_cleaned)
    check_remaining_line_breaks(df_cleaned)

    validate_data(df_cleaned)
    save_data(df_cleaned)
    verify_saved_data()
    return df_cleaned

if __name__ == "__main__":
    df_cleaned = clean_data()
    print("Final dataset shape:", df_cleaned.shape)











































