import json
import logging
import os
import pandas as pd

FORMAT_READERS = {
    "pkl": pd.read_pickle,
    "csv": pd.read_csv,
    "parquet": pd.read_parquet,
    # Add more mappings as needed
}

FORMAT_WRITERS = {
    "pkl": pd.DataFrame.to_pickle,
    "csv": pd.DataFrame.to_csv,
    "parquet": pd.DataFrame.to_parquet,
    # Add more mappings as needed
}

def load_config(dataframe_name):
    with open('config.json', 'r') as file:
        configs = json.load(file)["dataframes"]
        for config in configs:
            if config["name"] == dataframe_name:
                return config
        raise ValueError(f"No config found for dataframe: {dataframe_name}")
    
def read_data(file_path, file_format):
    if file_format not in FORMAT_READERS:
        raise ValueError(f"Unsupported file format: {file_format}")

    read_func = FORMAT_READERS[file_format]
    return read_func(file_path)

def write_data(data, file_path, file_format, **kwargs):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    if file_format == "pkl":
        # Remove 'index' argument for pickle format
        if 'index' in kwargs:
            del kwargs['index']

    writer_function = FORMAT_WRITERS.get(file_format)
    if writer_function:
        writer_function(data, file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
    
def construct_path(base_path, name, file_format, compression=None):
    """Utility function to construct file paths based on given parameters."""
    if compression:
        return f"{base_path}{name}.{file_format}.{compression}"
    else:
        return f"{base_path}{name}.{file_format}"

def setup_logging(log_filename):
    log_path = f"logs/{log_filename}.log"
    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path))
        
    logging.basicConfig(filename=log_path, 
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%Y %H:%M:%S')

nationality_to_country = {
    'EMIRATI': 'United Arab Emirates',
    'FILIPINO': 'Philippines',
    'AFGHAN': 'Afghanistan',
    'PALESTINIAN': 'Palestine, State of',
    'EGYPTIAN': 'Egypt',
    'INDIAN': 'India',
    'JORDANIAN': 'Jordan',
    'CANADIAN': 'Canada',
    'GERMAN': 'Germany',
    'NEPALESE': 'Nepal',
    'SYRIAN': 'Syrian Arab Republic',
    'GHANAIAN': 'Ghana',
    'BANGLADESHI': 'Bangladesh',
    'PAKISTANI': 'Pakistan',
    'ETHIOPIAN': 'Ethiopia',
    'COLOMBIAN': 'Colombia',
    'SWISS': 'Switzerland',
    'MOROCCAN': 'Morocco',
    'YEMENI': 'Yemen',
    'COMORAN': 'Comoros',
    'SAUDI': 'Saudi Arabia',
    'LEBANESE': 'Lebanon',
    'MAURITANIAN': 'Mauritania',
    'INDIA OCEAN TER': 'British Indian Ocean Territory',
    'SUDANESE': 'Sudan',
    'CHADIAN': 'Chad',
    'SOMALI': 'Somalia',
    'OMANI': 'Oman',
    'AMERICAN': 'United States',
    'NAURUAN': 'Nauru',
    'IRAQI': 'Iraq',
    'SRI LANKAN': 'Sri Lanka',
    'FRENCH': 'France',
    'ARGENTINIAN': 'Argentina',
    'CAPE VERDEAN': 'Cabo Verde',
    'CAMBODIAN': 'Cambodia',
    'MALAYSIAN': 'Malaysia',
    'KENYAN': 'Kenya',
    'BRITISH': 'United Kingdom',
    'QATARI': 'Qatar',
    'SPANISH': 'Spain',
    'IRANIAN': 'Iran, Islamic Republic of',
    'RUSSIAN': 'Russian Federation',
    'UGANDAN': 'Uganda',
    'SWEDISH': 'Sweden',
    'CHINESE': 'China',
    'INDONESIAN': 'Indonesia',
    'AUSTRALIAN': 'Australia',
    'NIGERIAN': 'Nigeria',
    'ALGERIAN': 'Algeria',
    'DUTCH': 'Netherlands',
    'ERITREAN': 'Eritrea',
    'IRISH': 'Ireland',
    'EASTERN TIMORIAN': 'Timor-Leste',
    'DOMINICAN': 'Dominican Republic',
    'NAMIBIAN': 'Namibia',
    'BRAZILIAN': 'Brazil',
    'FINNISH': 'Finland',
    'MACAUAN': 'Macao',
    'MAURITIAN': 'Mauritius',
    'ANDORRAN': 'Andorra',
    'BAHRAINI': 'Bahrain',
    'TUNISIAN': 'Tunisia',
    'MEXICAN': 'Mexico',
    'ESTONIAN': 'Estonia',
    'ITALIAN': 'Italy',
    'PORTUGUESE': 'Portugal',
    'FIJIAN': 'Fiji',
    'KAZAKSTANI': 'Kazakhstan',
    'SOUTH AFRICAN': 'South Africa',
    'CAMEROONIAN': 'Cameroon',
    'ANTIGUAN/BARBUDAN': 'Antigua and Barbuda',
    'TANZANIAN': 'Tanzania, United Republic of',
    'PALAUN': 'Palau',
    'ALBANIAN': 'Albania',
    'SIERRA LEONEAN': 'Sierra Leone',
    'DANISH': 'Denmark',
    'TURKISH': 'Turkey',
    'JAMAICAN': 'Jamaica',
    'GREEK': 'Greece',
    'KYRGYZSTANI': 'Kyrgyzstan',
    'TAIWANESE': 'Taiwan, Province of China',
    'ZIMBABWEAN': 'Zimbabwe',
    'ICELANDER': 'Iceland',
    'LIBYAN': 'Libya',
    'THAI': 'Thailand',
    'MALIAN': 'Mali',
    'CHILEAN': 'Chile',
    'LATVIAN': 'Latvia',
    'UKRANIAN': 'Ukraine',
    'HUNGARIAN': 'Hungary',
    'SAHRAWI': 'Western Sahara',
    'SERBIAN': 'Serbia',
    'GEORGIAN': 'Georgia',
    'KUWAITI': 'Kuwait',
    'NEW ZEALANDER': 'New Zealand',
    'TAJIKISTANI': 'Tajikistan',
    'PITCAIRN ISLANDER': 'Pitcairn',
    'PARAGUAYAN': 'Paraguay',
    'VENEZUALAN': 'Venezuela, Bolivarian Republic of',
    'FALKLAND ISLANDER': 'Falkland Islands (Malvinas)',
    'AZERBAIJANI / AZERI': 'Azerbaijan',
    'SENEGALESE': 'Senegal',
    'JAPANESE': 'Japan',
    'COSTA RICAN': 'Costa Rica',
    'GAMBIAN': 'Gambia',
    'NIGERIEN': 'Niger',
    'ZAMBIAN': 'Zambia',
    'POLE/POLISH': 'Poland',
    'MYANMAR': 'Myanmar',
    'GABONESE': 'Gabon',
    'VIETNAMESE': 'Viet Nam',
    'ROMANIAN': 'Romania',
    'ARMENIAN': 'Armenia',
    'BARBADIAN/BAJAN': 'Barbados',
    'EL SALVADORAN': 'El Salvador',
    'SURINAMESE': 'Suriname',
    'TURK/CAICO ISLANDER': 'Turks and Caicos Islands',
    'BELGIAN': 'Belgium',
    'BAHAMIAN': 'Bahamas',
    'ECUADORIAN': 'Ecuador',
    'MONGOLIAN': 'Mongolia',
    'DJIBOUTIAN': 'Djibouti',
    'ARUBAN': 'Aruba',
    'KOSOVAR': 'Kosovo',
    'POLYNESIAN FRENCH': 'French Polynesia',
    'MOTSWANA/BOTSWANA': 'Botswana',
    'BULGARIAN': 'Bulgaria',
    'LESOTHOAN': 'Lesotho',
    'UZBEKISTANI': 'Uzbekistan',
    'MARTINIQUE': 'Martinique',
    'CONGOLESE': 'Congo',
    'NEW CALEDONIAN': 'New Caledonia',
    'CUBAN': 'Cuba',
    'LIBERIAN': 'Liberia',
    'HAITIAN': 'Haiti',
    'NICARAGUAN': 'Nicaragua',
    'VANUATU': 'Vanuatu',
    'FAROESE': 'Faroe Islands',
    'KOREAN': 'Korea, Republic of',
    'WALLISIAN/ FUTUNAN': 'Wallis and Futuna',
    'MOLDOVAN': 'Moldova, Republic of',
    'GUINEAN': 'Guinea',
    'CROATIAN': 'Croatia',
    'ISRAELI': 'Israel',
    'AUSTRIAN': 'Austria',
    'PERUVIAN': 'Peru',
    'BOSNIAN/HERZEGOVINIAN': 'Bosnia and Herzegovina',
    'CHINESE/HONG KONGER': 'Hong Kong',
    'GRENADIAN': 'Grenada',
    'SLOVAKIAN': 'Slovakia',
    'MICRONESIAN': 'Micronesia, Federated States of',
    'NORWEGIAN': 'Norway',
    'TRINIDADIAN': 'Trinidad and Tobago',
    'SINGAPOREAN': 'Singapore',
    'LUXEMBOURGER': 'Luxembourg',
    'SEYCHELLOIS': 'Seychelles',
    'DOMINICAN REPUBLIC': 'Dominican Republic',
    'BURKINABE': 'Burkina Faso',
    'BRUNEIAN': 'Brunei Darussalam',
    'MOZAMBICAN': 'Mozambique',
    'ANGOLAN': 'Angola',
    'TONGAN': 'Tonga',
    'BRITISH VIRGIN ISLANDER': 'Virgin Islands, British',
    'CYPRIOT': 'Cyprus',
    'MACEDONIAN': 'North Macedonia',
    'MONTENEGRIN': 'Montenegro',
    'SWAZI': 'Eswatini',
    'MALAGASY (MADAGASCAR)': 'Madagascar',
    'EQUATORIAL GUINEAN': 'Equatorial Guinea',
    'KITTIAN': 'Saint Kitts and Nevis',
    'CHRISTMAS ISLANDER': 'Christmas Island',
    'SLOVENIAN': 'Slovenia',
    'SOLOMON ISLANDER': 'Solomon Islands',
    'MARSHALLESE': 'Marshall Islands',
    'BOLIVIAN': 'Bolivia, Plurinational State of',
    'KIRIBATI': 'Kiribati',
    'BELARUSSIAN': 'Belarus',
    'MALTESE': 'Malta',
    'GUINEA-BISSAU': 'Guinea-Bissau',
    'LITHUANIAN': 'Lithuania',
    'BURUNDIAN': 'Burundi',
    'LAOS/LAOTIAN': "Lao People's Democratic Republic",
    'REUNION': 'Réunion',
    'MALAWIAN': 'Malawi',
    'BEDOON': 'Kuwait',  # Stateless persons in Kuwait
    'ST VINCENTIAN': 'Saint Vincent and the Grenadines',
    'ST LUCIAN': 'Saint Lucia',
    'CZECH': 'Czechia',
    'MALDIVIAN': 'Maldives',
    'BELIZEAN': 'Belize',
    'PANAMANIAN': 'Panama',
}

nationality_to_continent_and_region = {
    'EMIRATI': {'continent': 'Asia', 'region': 'Western Asia'},
    'FILIPINO': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'AFGHAN': {'continent': 'Asia', 'region': 'South Asia'},
    'PALESTINIAN': {'continent': 'Asia', 'region': 'Western Asia'},
    'EGYPTIAN': {'continent': 'Africa', 'region': 'Northern Africa'},
    'INDIAN': {'continent': 'Asia', 'region': 'South Asia'},
    'JORDANIAN': {'continent': 'Asia', 'region': 'Western Asia'},
    'CANADIAN': {'continent': 'North America', 'region': 'Northern America'},
    'GERMAN': {'continent': 'Europe', 'region': 'Western Europe'},
    'NEPALESE': {'continent': 'Asia', 'region': 'South Asia'},
    'SYRIAN': {'continent': 'Asia', 'region': 'Western Asia'},
    'GHANAIAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'BANGLADESHI': {'continent': 'Asia', 'region': 'South Asia'},
    'PAKISTANI': {'continent': 'Asia', 'region': 'South Asia'},
    'ETHIOPIAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'COLOMBIAN': {'continent': 'South America', 'region': 'Northern South America'},
    'SWISS': {'continent': 'Europe', 'region': 'Western Europe'},
    'MOROCCAN': {'continent': 'Africa', 'region': 'Northern Africa'},
    'YEMENI': {'continent': 'Asia', 'region': 'Western Asia'},
    'COMORAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'SAUDI': {'continent': 'Asia', 'region': 'Western Asia'},
    'LEBANESE': {'continent': 'Asia', 'region': 'Western Asia'},
    'MAURITANIAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'INDIA OCEAN TER': {'continent': 'Asia', 'region': 'Indian Ocean'},
    'SUDANESE': {'continent': 'Africa', 'region': 'Northern Africa'},
    'CHADIAN': {'continent': 'Africa', 'region': 'Central Africa'},
    'SOMALI': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'OMANI': {'continent': 'Asia', 'region': 'Western Asia'},
    'AMERICAN': {'continent': 'North America', 'region': 'Northern America'},
    'NAURUAN': {'continent': 'Oceania', 'region': 'Micronesia'},
    'IRAQI': {'continent': 'Asia', 'region': 'Western Asia'},
    'SRI LANKAN': {'continent': 'Asia', 'region': 'South Asia'},
    'FRENCH': {'continent': 'Europe', 'region': 'Western Europe'},
    'ARGENTINIAN': {'continent': 'South America', 'region': 'Southern South America'},
    'CAPE VERDEAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'CAMBODIAN': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'MALAYSIAN': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'KENYAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'BRITISH': {'continent': 'Europe', 'region': 'Northern Europe'},
    'QATARI': {'continent': 'Asia', 'region': 'Western Asia'},
    'SPANISH': {'continent': 'Europe', 'region': 'Southern Europe'},
    'IRANIAN': {'continent': 'Asia', 'region': 'Western Asia'},
    'RUSSIAN': {'continent': 'Europe/Asia', 'region': 'Eastern Europe/Northern Asia'},
    'UGANDAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'SWEDISH': {'continent': 'Europe', 'region': 'Northern Europe'},
    'CHINESE': {'continent': 'Asia', 'region': 'Eastern Asia'},
    'INDONESIAN': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'AUSTRALIAN': {'continent': 'Australia', 'region': 'Australasia'},
    'NIGERIAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'ALGERIAN': {'continent': 'Africa', 'region': 'Northern Africa'},
    'DUTCH': {'continent': 'Europe', 'region': 'Western Europe'},
    'ERITREAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'IRISH': {'continent': 'Europe', 'region': 'Northern Europe'},
    'EASTERN TIMORIAN': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'DOMINICAN': {'continent': 'North America', 'region': 'Caribbean'},
    'NAMIBIAN': {'continent': 'Africa', 'region': 'Southern Africa'},
    'BRAZILIAN': {'continent': 'South America', 'region': 'Eastern South America'},
    'FINNISH': {'continent': 'Europe', 'region': 'Northern Europe'},
    'MACAUAN': {'continent': 'Asia', 'region': 'Eastern Asia'},
    'MAURITIAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'ANDORRAN': {'continent': 'Europe', 'region': 'Southern Europe'},
    'BAHRAINI': {'continent': 'Asia', 'region': 'Western Asia'},
    'TUNISIAN': {'continent': 'Africa', 'region': 'Northern Africa'},
    'MEXICAN': {'continent': 'North America', 'region': 'Central America'},
    'ESTONIAN': {'continent': 'Europe', 'region': 'Northern Europe'},
    'ITALIAN': {'continent': 'Europe', 'region': 'Southern Europe'},
    'PORTUGUESE': {'continent': 'Europe', 'region': 'Southern Europe'},
    'FIJIAN': {'continent': 'Oceania', 'region': 'Melanesia'},
    'KAZAKSTANI': {'continent': 'Asia', 'region': 'Central Asia'},
    'SOUTH AFRICAN': {'continent': 'Africa', 'region': 'Southern Africa'},
    'CAMEROONIAN': {'continent': 'Africa', 'region': 'Central Africa'},
    'ANTIGUAN/BARBUDAN': {'continent': 'North America', 'region': 'Caribbean'},
    'TANZANIAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'PALAUN': {'continent': 'Oceania', 'region': 'Micronesia'},
    'ALBANIAN': {'continent': 'Europe', 'region': 'Southern Europe'},
    'SIERRA LEONEAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'DANISH': {'continent': 'Europe', 'region': 'Northern Europe'},
    'TURKISH': {'continent': 'Asia/Europe', 'region': 'Western Asia/Southeastern Europe'},
    'JAMAICAN': {'continent': 'North America', 'region': 'Caribbean'},
    'GREEK': {'continent': 'Europe', 'region': 'Southern Europe'},
    'KYRGYZSTANI': {'continent': 'Asia', 'region': 'Central Asia'},
    'TAIWANESE': {'continent': 'Asia', 'region': 'Eastern Asia'},
    'ZIMBABWEAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'ICELANDER': {'continent': 'Europe', 'region': 'Northern Europe'},
    'LIBYAN': {'continent': 'Africa', 'region': 'Northern Africa'},
    'THAI': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'MALIAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'CHILEAN': {'continent': 'South America', 'region': 'Southern South America'},
    'LATVIAN': {'continent': 'Europe', 'region': 'Northern Europe'},
    'UKRANIAN': {'continent': 'Europe', 'region': 'Eastern Europe'},
    'HUNGARIAN': {'continent': 'Europe', 'region': 'Central Europe'},
    'SAHRAWI': {'continent': 'Africa', 'region': 'Northern Africa'},
    'SERBIAN': {'continent': 'Europe', 'region': 'Southeastern Europe'},
    'GEORGIAN': {'continent': 'Asia/Europe', 'region': 'Western Asia/Eastern Europe'},
    'KUWAITI': {'continent': 'Asia', 'region': 'Western Asia'},
    'NEW ZEALANDER': {'continent': 'Oceania', 'region': 'Australasia'},
    'TAJIKISTANI': {'continent': 'Asia', 'region': 'Central Asia'},
    'PITCAIRN ISLANDER': {'continent': 'Oceania', 'region': 'Polynesia'},
    'PARAGUAYAN': {'continent': 'South America', 'region': 'Southern South America'},
    'VENEZUELAN': {'continent': 'South America', 'region': 'Northern South America'},
    'FALKLAND ISLANDER': {'continent': 'South America', 'region': 'Southern South America'},
    'AZERBAIJANI / AZERI': {'continent': 'Asia/Europe', 'region': 'Western Asia/Southeastern Europe'},
    'SENEGALESE': {'continent': 'Africa', 'region': 'Western Africa'},
    'JAPANESE': {'continent': 'Asia', 'region': 'Eastern Asia'},
    'COSTA RICAN': {'continent': 'North America', 'region': 'Central America'},
    'GAMBIAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'NIGERIEN': {'continent': 'Africa', 'region': 'Western Africa'},
    'ZAMBIAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'POLE/POLISH': {'continent': 'Europe', 'region': 'Central Europe'},
    'MYANMAR': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'GABONESE': {'continent': 'Africa', 'region': 'Central Africa'},
    'VIETNAMESE': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'ROMANIAN': {'continent': 'Europe', 'region': 'Eastern Europe'},
    'ARMENIAN': {'continent': 'Asia', 'region': 'Western Asia'},
    'BARBADIAN/BAJAN': {'continent': 'North America', 'region': 'Caribbean'},
    'EL SALVADORAN': {'continent': 'North America', 'region': 'Central America'},
    'SURINAMESE': {'continent': 'South America', 'region': 'Northern South America'},
    'TURK/CAICO ISLANDER': {'continent': 'North America', 'region': 'Caribbean'},
    'BELGIAN': {'continent': 'Europe', 'region': 'Western Europe'},
    'BAHAMIAN': {'continent': 'North America', 'region': 'Caribbean'},
    'ECUADORIAN': {'continent': 'South America', 'region': 'Western South America'},
    'MONGOLIAN': {'continent': 'Asia', 'region': 'Eastern Asia'},
    'DJIBOUTIAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'ARUBAN': {'continent': 'North America', 'region': 'Caribbean'},
    'KOSOVAR': {'continent': 'Europe', 'region': 'Southeastern Europe'},
    'POLYNESIAN FRENCH': {'continent': 'Oceania', 'region': 'Polynesia'},
    'MOTSWANA/BOTSWANA': {'continent': 'Africa', 'region': 'Southern Africa'},
    'BULGARIAN': {'continent': 'Europe', 'region': 'Eastern Europe'},
    'LESOTHOAN': {'continent': 'Africa', 'region': 'Southern Africa'},
    'UZBEKISTANI': {'continent': 'Asia', 'region': 'Central Asia'},
    'MARTINIQUE': {'continent': 'North America', 'region': 'Caribbean'},
    'CONGOLESE': {'continent': 'Africa', 'region': 'Central Africa'},
    'NEW CALEDONIAN': {'continent': 'Oceania', 'region': 'Melanesia'},
    'CUBAN': {'continent': 'North America', 'region': 'Caribbean'},
    'LIBERIAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'HAITIAN': {'continent': 'North America', 'region': 'Caribbean'},
    'NICARAGUAN': {'continent': 'North America', 'region': 'Central America'},
    'VANUATU': {'continent': 'Oceania', 'region': 'Melanesia'},
    'FAROESE': {'continent': 'Europe', 'region': 'Northern Europe'},
    'KOREAN': {'continent': 'Asia', 'region': 'Eastern Asia'},
    'WALLISIAN/ FUTUNAN': {'continent': 'Oceania', 'region': 'Polynesia'},
    'MOLDOVAN': {'continent': 'Europe', 'region': 'Eastern Europe'},
    'GUINEAN': {'continent': 'Africa', 'region': 'Western Africa'},
    'CROATIAN': {'continent': 'Europe', 'region': 'Southeastern Europe'},
    'ISRAELI': {'continent': 'Asia', 'region': 'Western Asia'},
    'AUSTRIAN': {'continent': 'Europe', 'region': 'Western Europe'},
    'PERUVIAN': {'continent': 'South America', 'region': 'Western South America'},
    'BOSNIAN/HERZEGOVINIAN': {'continent': 'Europe', 'region': 'Southeastern Europe'},
    'CHINESE/HONG KONGER': {'continent': 'Asia', 'region': 'Eastern Asia'},
    'GRENADIAN': {'continent': 'North America', 'region': 'Caribbean'},
    'SLOVAKIAN': {'continent': 'Europe', 'region': 'Central Europe'},
    'MICRONESIAN': {'continent': 'Oceania', 'region': 'Micronesia'},
    'NORWEGIAN': {'continent': 'Europe', 'region': 'Northern Europe'},
    'TRINIDADIAN': {'continent': 'North America', 'region': 'Caribbean'},
    'SINGAPOREAN': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'LUXEMBOURGER': {'continent': 'Europe', 'region': 'Western Europe'},
    'SEYCHELLOIS': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'DOMINICAN REPUBLIC': {'continent': 'North America', 'region': 'Caribbean'},
    'BURKINABE': {'continent': 'Africa', 'region': 'Western Africa'},
    'BRUNEIAN': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'MOZAMBICAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'ANGOLAN': {'continent': 'Africa', 'region': 'Central Africa'},
    'TONGAN': {'continent': 'Oceania', 'region': 'Polynesia'},
    'BRITISH VIRGIN ISLANDER': {'continent': 'North America', 'region': 'Caribbean'},
    'CYPRIOT': {'continent': 'Asia/Europe', 'region': 'Western Asia/Southern Europe'},
    'MACEDONIAN': {'continent': 'Europe', 'region': 'Southeastern Europe'},
    'MONTENEGRIN': {'continent': 'Europe', 'region': 'Southeastern Europe'},
    'SWAZI': {'continent': 'Africa', 'region': 'Southern Africa'},
    'MALAGASY (MADAGASCAR)': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'EQUATORIAL GUINEAN': {'continent': 'Africa', 'region': 'Central Africa'},
    'KITTIAN': {'continent': 'North America', 'region': 'Caribbean'},
    'CHRISTMAS ISLANDER': {'continent': 'Australia', 'region': 'Australasia'},
    'SLOVENIAN': {'continent': 'Europe', 'region': 'Southern Europe'},
    'SOLOMON ISLANDER': {'continent': 'Oceania', 'region': 'Melanesia'},
    'MARSHALLESE': {'continent': 'Oceania', 'region': 'Micronesia'},
    'BOLIVIAN': {'continent': 'South America', 'region': 'Western South America'},
    'KIRIBATI': {'continent': 'Oceania', 'region': 'Micronesia'},
    'BELARUSSIAN': {'continent': 'Europe', 'region': 'Eastern Europe'},
    'MALTESE': {'continent': 'Europe', 'region': 'Southern Europe'},
    'GUINEA-BISSAU': {'continent': 'Africa', 'region': 'Western Africa'},
    'LITHUANIAN': {'continent': 'Europe', 'region': 'Northern Europe'},
    'BURUNDIAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'LAOS/LAOTIAN': {'continent': 'Asia', 'region': 'Southeast Asia'},
    'REUNION': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'MALAWIAN': {'continent': 'Africa', 'region': 'Eastern Africa'},
    'BEDOON': {'continent': 'Asia', 'region': 'Western Asia'},  # Stateless persons in Kuwait
    'ST VINCENTIAN': {'continent': 'North America', 'region': 'Caribbean'},
    'ST LUCIAN': {'continent': 'North America', 'region': 'Caribbean'},
    'CZECH': {'continent': 'Europe', 'region': 'Central Europe'},
    'MALDIVIAN': {'continent': 'Asia', 'region': 'South Asia'},
    'BELIZEAN': {'continent': 'North America', 'region': 'Central America'},
    'PANAMANIAN': {'continent': 'North America', 'region': 'Central America'},
}