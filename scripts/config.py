# Description: Configuration file for the scripts

# FINAL COLUMN HEADERS
COLUMN_NAMES = [
    "FIFA",
    "Dial",
    "ISO3166-1-Alpha-3",
    "MARC",
    "is_independent",
    "ISO3166-1-numeric",
    "GAUL",
    "FIPS",
    "WMO",
    "ISO3166-1-Alpha-2",
    "ITU",
    "IOC",
    "DS",
    "UNTERM Spanish Formal",
    "Global Code",
    "Intermediate Region Code",
    "official_name_fr",
    "UNTERM French Short",
    "ISO4217-currency_name",
    "Developed / Developing Countries",
    "UNTERM Russian Formal",
    "UNTERM English Short",
    "ISO4217-currency_alphabetic_code",
    "Small Island Developing States (SIDS)",
    "UNTERM Spanish Short",
    "ISO4217-currency_numeric_code",
    "UNTERM Chinese Formal",
    "UNTERM French Formal",
    "UNTERM Russian Short",
    "M49",
    "Sub-region Code",
    "Region Code",
    "official_name_ar",
    "ISO4217-currency_minor_unit",
    "UNTERM Arabic Formal",
    "UNTERM Chinese Short",
    "Land Locked Developing Countries (LLDC)",
    "Intermediate Region Name",
    "official_name_es",
    "UNTERM English Formal",
    "official_name_cn",
    "official_name_en",
    "ISO4217-currency_country_name",
    "Least Developed Countries (LDC)",
    "Region Name",
    "UNTERM Arabic Short",
    "Sub-region Name",
    "official_name_ru",
    "Global Name",
    "Capital",
    "Continent",
    "TLD",
    "Languages",
    "Geoname ID",
    "CLDR display name",
    "EDGAR"
]

# URLS
CLDR_TERRITORIES_URL = 'https://github.com/unicode-org/cldr-json/blob/d38478855dd8342749f0494332cc8acc2895d20d/cldr-json/cldr-localenames-full/main/ms/territories.json'
EDGAR_URL = 'https://www.sec.gov/submit-filings/filer-support-resources/edgar-state-country-codes'
GEONAMES_URL = 'http://download.geonames.org/export/dump/countryInfo.txt'
ISO4217_URL = 'https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml'
UNTERM_EFSRCA_URL = 'https://www.un.org/dgacm/sites/www.un.org.dgacm/files/Documents_Protocol/unterm-efsrca.xlsx'

# 
CONFIG_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

UNTERM_FILE_NAME = 'unterm-efsrca.xlsx' 
UNTERM_HEADERS = ['official_name_en',
          'UNTERM French Short',
          'UNTERM Spanish Short',
          'UNTERM Russian Short',
          'UNTERM Chinese Short',
          'UNTERM Arabic Short',
          'UNTERM English Formal',
          'UNTERM French Formal',
          'UNTERM Spanish Formal',
          'UNTERM Russian Formal',
          'UNTERM Chinese Formal',
          'UNTERM Arabic Formal'
        ]

# EDGAR configs
EDGAR_FILE_NAME = 'data/edgar.csv'
EDGAR_HEADERS = ['EDGAR', 'name']
EDGAR_URL = 'https://www.sec.gov/submit-filings/filer-support-resources/edgar-state-country-codes'

# ISO4217 configs
ISO3166_FILE_NAME = 'data/iso3166.json'
CURRENCY_TAG_MAP = {
    "CtryNm": "ISO4217-currency_country_name",
    "CcyNm": "ISO4217-currency_name",
    "Ccy": "ISO4217-currency_alphabetic_code",
    "CcyNbr": "ISO4217-currency_numeric_code",
    "CcyMnrUnts": "ISO4217-currency_minor_unit",
    "AddtlInf": "ISO4217-currency_additional_info"
}
CURRENCY_COUNTRY_NAME_MAP = {
    "MACEDONIA, THE FORMER \nYUGOSLAV REPUBLIC OF": "MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF",
    "SAINT HELENA, ASCENSION AND \nTRISTAN DA CUNHA": "SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA",
    "CABO VERDE": "CAPE VERDE",
    "HEARD ISLAND AND McDONALD ISLANDS": "HEARD ISLAND AND MCDONALD ISLANDS",
    "LAO PEOPLE’S DEMOCRATIC REPUBLIC": "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
    "SERBIA ": "SERBIA",
    "PALESTINIAN TERRITORY, OCCUPIED": "PALESTINE, STATE OF",
    "Vatican City State (HOLY SEE)": "HOLY SEE (VATICAN CITY STATE)",
    "VIRGIN ISLANDS (BRITISH)": "VIRGIN ISLANDS, BRITISH",
    "VIRGIN ISLANDS (U.S.)": "VIRGIN ISLANDS, U.S.",
    "BOLIVIA, PLURINATIONAL STATE OF": "Bolivia (Plurinational State of)",
    "HOLY SEE (VATICAN CITY STATE)": "Holy See",
    "IRAN, ISLAMIC REPUBLIC OF": "Iran (Islamic Republic of)",
    "MACAO": "China, Macao Special Administrative Region",
    "MICRONESIA, FEDERATED STATES OF": "Micronesia (Federated States of)",
    "PALESTINE, STATE OF": "State of Palestine",
    "SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA": "Saint Helena",
    "SVALBARD AND JAN MAYEN": "Svalbard and Jan Mayen Islands",
    "TANZANIA, UNITED REPUBLIC OF": "United Republic of Tanzania",
    "UNITED KINGDOM": "United Kingdom of Great Britain and Northern Ireland",
    "UNITED STATES": "United States of America",
    "VENEZUELA, BOLIVARIAN REPUBLIC OF": "Venezuela (Bolivarian Republic of)",
    "WALLIS AND FUTUNA": "Wallis and Futuna Islands",
    "VIRGIN ISLANDS (U.S.)": "UNITED STATES VIRGIN ISLANDS",
    "VIRGIN ISLANDS (BRITISH)": "BRITISH VIRGIN ISLANDS",

    "CONGO (THE DEMOCRATIC REPUBLIC OF THE)": "DEMOCRATIC REPUBLIC OF THE CONGO",
    "KOREA (THE DEMOCRATIC PEOPLE’S REPUBLIC OF)": "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA",
    "KOREA (THE REPUBLIC OF)": "REPUBLIC OF KOREA",
    "FALKLAND ISLANDS [MALVINAS]": "FALKLAND ISLANDS",
    "HONG KONG": u'CHINA, HONG KONG SPECIAL ADMINISTRATIVE REGION',
    "MACEDONIA (THE FORMER YUGOSLAV REPUBLIC OF)": "THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA",
    "MOLDOVA (THE REPUBLIC OF)": "REPUBLIC OF MOLDOVA",
}