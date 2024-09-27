import pandas as pd

def cleanup():
    # Load the CSV into a DataFrame
    df = pd.read_csv('data/country-codes.csv')
    
    # Check for exact duplicate rows (global duplicates)
    duplicates = df[df.duplicated()]
    
    if not duplicates.empty:
        print(f"Found {len(duplicates)} exact duplicate rows:")
        print(duplicates)
    
    # Drop duplicates
    df_cleaned = df.drop_duplicates()
    
    # Define the desired column order
    desired_order = [
        "FIFA", "Dial", "ISO3166-1-Alpha-3", "MARC", "is_independent", "ISO3166-1-numeric", "GAUL", "FIPS", 
        "WMO", "ISO3166-1-Alpha-2", "ITU", "IOC", "DS", "UNTERM Spanish Formal", "Global Code", 
        "Intermediate Region Code", "official_name_fr", "UNTERM French Short", "ISO4217-currency_name", 
         "UNTERM Russian Formal", "UNTERM English Short", 
        "ISO4217-currency_alphabetic_code", "Small Island Developing States (SIDS)", "UNTERM Spanish Short", 
        "ISO4217-currency_numeric_code", "UNTERM Chinese Formal", "UNTERM French Formal", "UNTERM Russian Short", 
        "M49", "Sub-region Code", "Region Code", "official_name_ar", "ISO4217-currency_minor_unit", 
        "UNTERM Arabic Formal", "UNTERM Chinese Short", "Land Locked Developing Countries (LLDC)", 
        "Intermediate Region Name", "official_name_es", "UNTERM English Formal", "official_name_cn", 
        "official_name_en", "ISO4217-currency_country_name", "Least Developed Countries (LDC)", "Region Name", 
        "UNTERM Arabic Short", "Sub-region Name", "official_name_ru", "Global Name", "Capital", 
        "Continent", "TLD", "Languages", "Geoname ID", "CLDR display name", "EDGAR"
    ]
    
    # Only reorder the columns that exist in both the dataframe and the desired order
    existing_columns = [col for col in desired_order if col in df_cleaned.columns]
    
    # Reorder the columns based on the desired order
    df_reordered = df_cleaned[existing_columns]
    
    # Write the reordered DataFrame back to the same file
    df_reordered.to_csv('data/country-codes.csv', index=False)
    print(f"Saved cleaned and reordered data to 'data/country-codes.csv'. Total rows after cleanup: {len(df_reordered)}")

if __name__ == '__main__':
    cleanup()