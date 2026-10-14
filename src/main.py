from data_cleaning import clean_data
from analysis import run_analysis

def main():
    print("Starting Netflix Content Analytics Project...")
    df_cleaned = clean_data()

    print("\nData cleaning completed successfully!")
    run_analysis()

if __name__ == "__main__":
    main()