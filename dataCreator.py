from faker import Faker
import pandas as pd
import random
import datetime

fake = Faker()


# Generating synthetic player information
def generate_players(num_players):
    players = []
    for _ in range(num_players):
        player_id = fake.uuid4()
        player_name = fake.name()
        hours_played = round(random.uniform(1, 40), 2)  # Generate random hours played
        players.append({
            'PlayerID': player_id,
            'PlayerName': player_name,
            'HoursPlayed': hours_played
        })
    return pd.DataFrame(players)


# Generating synthetic transaction logs
def generate_transactions(players_df):
    transactions = []
    for index, player_row in players_df.iterrows():
        num_transactions = random.randint(10, 200)  # Varying number of transactions per user
        for _ in range(num_transactions):
            transaction_time = fake.date_time_between(start_date='-30d', end_date='now')
            transaction_type = random.choice(['bet', 'win', 'loss', 'payout'])
            amount = round(random.uniform(10, 5000), 2)
            transactions.append({
                'PlayerID': player_row['PlayerID'],
                'TransactionTime': transaction_time,
                'TransactionType': transaction_type,
                'Amount': amount
            })
    return pd.DataFrame(transactions)


# Generate synthetic player data (100 players)
num_players = 100
players_df = generate_players(num_players)

# Generate synthetic transaction data
transactions_df = generate_transactions(players_df)

# Save synthetic data to CSV files
players_df.to_csv('synthetic_players_data.csv', index=False)
transactions_df.to_csv('synthetic_transactions_data.csv', index=False)
