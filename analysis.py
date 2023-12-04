import pandas as pd

TOP_PERCENT = 5

# Load synthetic data from CSV files
players_df = pd.read_csv('synthetic_players_data.csv')
transactions_df = pd.read_csv('synthetic_transactions_data.csv')

# Initial row count
initial_row_count_players = len(players_df)
initial_row_count_transactions = len(transactions_df)

# Data cleaning: Remove any rows with missing values
players_df.dropna(inplace=True)
transactions_df.dropna(inplace=True)

# Calculate the number of rows dropped
rows_dropped_players = initial_row_count_players - len(players_df)
rows_dropped_transactions = initial_row_count_transactions - len(transactions_df)

# Convert 'TransactionTime' column to datetime format
transactions_df['TransactionTime'] = pd.to_datetime(transactions_df['TransactionTime'])

# Determine the number of rows dropped, large numbers could indicate issues in data pipeline
print(f"Number of rows dropped in players_df: {rows_dropped_players}")
print(f"Number of rows dropped in transactions_df: {rows_dropped_transactions}")
print("\n")


# Group transactions by PlayerID and aggregate counts and amounts
player_stats = transactions_df.groupby('PlayerID').agg(
    TransactionCount=('TransactionType', 'count'),
    TotalAmount=('Amount', 'sum')
)

# Merge player stats with players' hours played
player_stats = player_stats.merge(players_df[['PlayerID', 'HoursPlayed']], on='PlayerID')


# Sorting the DataFrame in descending order by 'HoursPlayed'
sorted_hours_played = player_stats.sort_values(by='HoursPlayed', ascending=False)
entries = int(len(sorted_hours_played) * (TOP_PERCENT / 100))

if entries < 1:
    entries = 1

print(f"Printing the top {TOP_PERCENT} percent of entries which is {entries} \n")


# Printing the top X% by 'HoursPlayed'
print(f"Top {TOP_PERCENT}% by Hours Played:")
for index, row in sorted_hours_played.head(entries)[['PlayerID', 'HoursPlayed']].iterrows():
    print(f"Player ID: {row['PlayerID']}, HoursPlayed: {row['HoursPlayed']}")
print("\n")

# Sorting the DataFrame in descending order by 'TransactionCount'
sorted_transaction_count = player_stats.sort_values(by='TransactionCount', ascending=False)

# Printing the top X% by 'TransactionCount'
print(f"Top {TOP_PERCENT}% by Transaction Count:")
for index, row in sorted_transaction_count.head(entries)[['PlayerID', 'TransactionCount']].iterrows():
    print(f"Player ID: {row['PlayerID']}, Transaction Count: {row['TransactionCount']}")
print("\n")

# Sorting the DataFrame in descending order by 'TotalAmount'
sorted_total_amount = player_stats.sort_values(by='TotalAmount', ascending=False)


print(f"Top {TOP_PERCENT}% by Total Amount:")
for index, row in sorted_total_amount.head(entries)[['PlayerID', 'TotalAmount']].iterrows():
    print(f"Player ID: {row['PlayerID']}, Total Amount: {row['TotalAmount']}")
print("\n")


# Top percent is probably a poor method of determining if a gambler is problematic or not

# hours played may be more preferable

filtered_rows = player_stats[player_stats['HoursPlayed'] > 35]

# Print the filtered rows
print("Rows with Hours Played > 35:     " + str(len(filtered_rows)))
print(filtered_rows)



