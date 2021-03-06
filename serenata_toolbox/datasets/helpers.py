import os

from datetime import datetime

CSV_PARAMS = {
    'compression': 'xz',
    'encoding': 'utf-8',
    'index': False
}


# Utilities for extracting data from XML files

def xml_extract_text(node, xpath):
    """
    :param node: the node to be queried
    :param xpath: the path to fetch the child node that has the wanted text
    """
    text = node.find(xpath).text
    if text is not None:
        text = text.strip()
    return text


def xml_extract_date(node, xpath, date_format='%d/%m/%Y'):
    """
    :param node: the node to be queried
    :param xpath: the path to fetch the child node that has the wanted date
    """
    return datetime.strptime(xml_extract_text(node, xpath), date_format)


def xml_extract_datetime(node, xpath, datetime_format='%d/%m/%Y %H:%M:%S'):
    """
    :param node: the node to be queried
    :param xpath: the path to fetch the child node that has the wanted datetime
    """
    return datetime.strptime(xml_extract_text(node, xpath), datetime_format)


# Utilities for dealing with Dataframes

def translate_column(df, column, translations):
    """
    :param df: (pandas.Dataframe) the dataframe to be translated
    :param column: (str) the column to be translated
    :param translations: (dict) a dictionary of the strings to be categorized and translated
    """
    df[column] = df[column].astype('category')
    translations = [translations[cat]
                    for cat in df[column].cat.categories]
    df[column].cat.rename_categories(translations, inplace=True)


def save_to_csv(df, data_dir, name):
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_path = os.path.join(data_dir, '{}-{}.xz'.format(today, name))
    df.to_csv(file_path, **CSV_PARAMS)


# Utility for config file lookup (credits to fabric fabfile lookup)

def find_config(name='config.ini'):
    """
    :param name: config file name (defaults to 'config.ini')
    """
    # start in cwd and work downwards towards filesystem root
    path = '.'
    # Stop before falling off root of filesystem (should be platform
    # agnostic)
    while os.path.split(os.path.abspath(path))[1]:
        joined = os.path.join(path, name)

        # return config file absolute path if exists
        if os.path.exists(joined) and os.path.isfile(joined):
            return os.path.abspath(joined)

        path = os.path.join('..', path)

    # if config not found fallback on tests expected behavior
    # wich is to return the filename to be used at remote
    # config_exists class property.
    # a future refactor could be to return None and not use
    # config exists anymore
    return name
