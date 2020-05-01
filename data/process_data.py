import pandas as pd
from sqlalchemy import create_engine
import sys


def load_data(messages_filepath, categories_filepath):
    """Function for importing data from CSV files

    Params:
        messages_filepath (string): path to messages.csv
        categories_filepath (string): path to categories.csv

    Returns:
        (DataFrame): DataFrame with loaded data
    """
    # Loading Datasets
    messages = pd.read_csv(f'{messages_filepath}')
    categories = pd.read_csv(f'{categories_filepath}')

    df = pd.merge(messages, categories, how='left', on='id')
    return df


def clean_data(df):
    """ Cleans data

    Params:
        df (DataFrame): Pandas dataframe to be cleaned

    Returns:
        (DataFrame): Cleaned dataframe
    """
    # Split `categories` into separate category columns
    categories = df['categories'].str.split(';', expand=True)
    # Get columns name
    categories_colnames = list(categories.iloc[0].apply(lambda x: str(x)[:-2]))
    categories.columns = categories_colnames
    # Get column values integers
    for col in categories.columns:
        categories[col] = categories[col].apply(lambda x: int(str(x)[-1:]))
        categories[col] = pd.to_numeric(categories[col])

    # Replace `categories` column in `df` with new category columns
    df.drop('categories', axis=1, inplace=True)
    df_clean = pd.concat([df, categories], axis=1)

    # The original columns doesn't contain any useful information,
    # that is not already in the column 'messages'
    df_clean.drop('original', axis=1, inplace=True)

    # Remove duplicates
    # Checking for duplicates ids
    df_clean.drop_duplicates(keep='first', inplace=True)
    # For the same message there are different categories assigned.
    # The resulting row, will be a combination of the duplicates, joining the
    # categories from all the duplicates of the same id.
    # The final dataset contains only unique messages with uniques ids

    df_final = df_clean.groupby(['id', 'message', 'genre']).max().reset_index()

    # Excluding Empty Messages and meagninless phrases. Like: '#NAME!'
    df_final.drop(df_final[df_final['message'].str.len() < 28].index,
                  inplace=True)
    return df_final


def save_data(df, database_filename):
    """ Save the dataset into an sqlite database

    Params:
        df (DataFrame): DataFrame to be saved into database
        database_filename (string): database filename

    Returns:
        None
    """
    engine = create_engine(f'sqlite:///{database_filename}')
    df.to_sql('messages', engine, index=False)


def main():
    """ ETL (Extract, Tranform and Load process). Read, clean and store the
    data into a database
    """
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath \
            = sys.argv[1:]

        print(f'Loading data...\n    MESSAGES: {messages_filepath}\n \
              CATEGORIES: {categories_filepath}')
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '
              'datasets as the first and second argument respectively, as '
              'well as the filepath of the database to save the cleaned data '
              'to as the third argument. \n\nExample: python process_data.py '
              'disaster_messages.csv disaster_categories.csv '
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
