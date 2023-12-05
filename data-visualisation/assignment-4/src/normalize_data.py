import pandas as pd
import json
import calendar
from datetime import datetime

keep_columns = [
        'year',
        'month',
        'date',
        'datetime',
        'attack_successful',
        'ransom_response_paid',
        'ransom_response_refused',
        'ransom_response_unknown',
        'target',
        ]

def convert_to_datetime(year: int, month: str):
    """
    Convert year and three-letter month string to a datetime object.
    Args:
    - year (int): The year.
    - month (str): The three-letter abbreviation of the month.

    Returns:
    - datetime object representing the first day of the given month and year.
    """
    # Convert the three-letter month to a number
    month_number = list(calendar.month_abbr).index(month.title().strip())
    # Create a datetime object for the first day of the specified month and year
    return datetime(year, month_number, 1)

def process(data):
    data['month'] = data['month'].str.title().apply(lambda x: x.strip())
    data['YEAR'] = data['YEAR'].astype(int)
    data['year'] = data['YEAR']
    print(data['month'].unique())
    print(data['YEAR'].unique())

    data['date'] = data['YEAR'].astype(str) + '-' + data['month']
    datetime_values = []

    for index, row in data.iterrows():
        print(row['YEAR'], row['month'])
        datetime_value = convert_to_datetime(row['YEAR'], row['month'])
        datetime_values.append(datetime_value)

    data['datetime'] = datetime_values
    data = data.sort_values(by='datetime')

    data['cost'] = pd.to_numeric(data['ransom cost'], errors='coerce')

    data['ransom_response_paid'] = data['ransom paid'] == 'ransom paid'
    data['ransom_response_refused'] = data['ransom paid'] == 'refused'
    data['ransom_response_unknown'] = data['ransom paid'] == 'unknown'
    data['cost_paid'] = data.apply(lambda x: x['cost'] if x['ransom_response_paid'] else 0, axis=1)
    def parse_json(str_json):
        print(str_json)
        try:
            return json.loads(str_json)
        except:
            return None
    data['target'] = data['Target'].apply(parse_json)
    
    # grouped_data = data.groupby('datetime').agg(
    #     total_attacks=('date', 'count'),
    #     successful_attacks=('attack_success', 'sum'),
    #     cost=('cost', 'sum'),
    #     cost_paid=('cost_paid','sum')
    # ).reset_index()

    return data

if __name__ == "__main__":
    df = pd.read_csv("data/ransomware-attacks.csv")
    df = process(df)
    print(df['target'])
