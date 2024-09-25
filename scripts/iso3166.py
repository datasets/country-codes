import os
import pandas as pd

from functools import reduce

# Path to the folders
source_dir = 'tmp/'

# List of UNSD CSV files (for different languages) and the corresponding official name column
languages = ['fr', 'ar', 'cn', 'es', 'ru']
lang_column_names = {
    'fr': 'official_name_fr',
    'ar': 'official_name_ar',
    'cn': 'official_name_cn',
    'es': 'official_name_es',
    'ru': 'official_name_ru'
}


def run():
    df_en = pd.read_csv(os.path.join(source_dir, 'UNSD-en.csv'))

    # Load the previously processed CSVs
    dfs_to_join = []
    for lang in languages:
        cut_file = os.path.join(source_dir, f'UNSD-{lang}.csv')
        df_lang = pd.read_csv(cut_file, usecols=['Country or Area', 'M49 Code'])
        df_lang = df_lang.rename(columns={'Country or Area': lang_column_names[lang]})
        # Merge with the English dataframe on "M49 Code" (assuming it's in both files)
        dfs_to_join.append(df_lang)
    new_df = reduce(lambda x, y: pd.merge(x, y, on = 'M49 Code'), dfs_to_join)
    df_final = df_en.merge(new_df, on = 'M49 Code', how = 'left')
    
    df_final = df_final.rename(columns={
        'M49 Code': 'M49',
        'Country or Area': 'official_name_en',
        'ISO-alpha3 Code': 'ISO3166-1-Alpha-3'
    })
    df_final.to_csv(os.path.join(source_dir, 'iso3166.csv'), index=False)

if __name__ == '__main__':
    run()