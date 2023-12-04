import pandas as pd


from datetime import datetime
import calendar

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

# Example usage:
# dt = convert_to_datetime(2023, 'Jan')
# print(dt)

# Load your CSV data into a DataFrame
# data = pd.read_csv('your_data.csv')

def analyze_ransomware_data(data):
    # Capitalize 'month' and 'YEAR' columns
    data['month'] = data['month'].str.title().apply(lambda x: x.strip())
    data['YEAR'] = data['YEAR'].astype(int)
    print(data['month'].unique())
    print(data['YEAR'].unique())

    # Combine 'YEAR' and 'month' for a single time column
    data['date'] = data['YEAR'].astype(str) + '-' + data['month']
    # Initialize an empty list to store datetime objects
    datetime_values = []

    # Iterate over each row in the DataFrame
    for index, row in data.iterrows():
        print(row['YEAR'], row['month'])
        datetime_value = convert_to_datetime(row['YEAR'], row['month'])
        datetime_values.append(datetime_value)

    # Add the list as a new column to the DataFrame
    data['datetime'] = datetime_values

    data = data.sort_values(by='datetime')

    # Convert 'ransom paid' and 'cost' to numeric, handle errors
    data['cost'] = pd.to_numeric(data['ransom cost'], errors='coerce')

    # Define success as having a non-zero 'ransom paid' value
    data['attack_success'] = data['ransom paid'] == 'ransom paid'
    data['cost_paid'] = data.apply(lambda x: x['cost'] if x['attack_success'] else 0, axis=1)
    
    # Group by the new 'date' column
    grouped_data = data.groupby('datetime').agg(
        total_attacks=('date', 'count'),
        successful_attacks=('attack_success', 'sum'),
        cost=('cost', 'sum'),
        cost_paid=('cost_paid','sum')
    ).reset_index()

    return grouped_data

if __name__ == "__main__":
    df = pd.read_csv("data/ransomware-attacks.csv")
    grouped = analyze_ransomware_data(df)
    print(grouped[0:20])

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.figure(figsize=(10, 6))  # Adjust the size as needed
    df = grouped
    plt.scatter(df['datetime'], df['cost_paid'])
    plt.scatter(df['datetime'], df['cost'])

    # Set x-axis to display each January
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(month=1, day=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('Jan %Y'))
    # Hide axes details
    plt.yticks([])  # Hide y-axis ticks
    plt.ylabel('')  # Hide y-axis label
    plt.tick_params(axis='y', which='both', bottom=True, top=False, labelbottom=False, right=False, left=False, labelleft=False)

    plt.show()
