import os
from dotenv import load_dotenv
from tastytrade_sdk import Tastytrade
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pandas as pd
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
scheduler = AsyncIOScheduler()

# Initialize the Tastytrade client
tasty = Tastytrade()
ACCOUNT_NUMBER = os.getenv('ACCOUNT_NUMBER')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
TOKEN = os.getenv('NASSAU_BOT_TOKEN')
CHANNEL_ID = int(
    os.getenv('PORTFOLIO_CHANNEL')
)  # Make sure this is converted to an integer
nassau_gpt = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
model = 'gpt-4-1106-preview'
tasty.login(login=LOGIN, password=PASSWORD)
positions = tasty.api.get(f'/accounts/{ACCOUNT_NUMBER}/positions')
positions_df = pd.DataFrame(positions['data'])
mock_data = [
    {
        'instrument-type': 'Equity',
        'multiplier': 1,
        'realized-today': 500.00,
        'is-frozen': False,
        'updated-at': '2023-11-27T17:00:00.000Z',
        'average-daily-market-close-price': 154.00,
        'deliverable-type': 'Stock',
        'underlying-symbol': 'AAPL',
        'mark-price': 155.00,
        'account-number': 'XXXXXX',
        'fixing-price': 150.00,
        'quantity': {'long': 50, 'short': 0},
        'realized-day-gain-date': '2023-11-27',
        'expires-at': None,
        'mark': 155.00,
        'realized-day-gain': 250.00,
        'realized-day-gain-effect': 'Profit',
        'cost-effect': 'Debit',
        'close-price': 155.00,
    },
    {
        'instrument-type': 'Equity Option',
        'multiplier': 100,
        'realized-today': 3000.00,
        'is-frozen': False,
        'updated-at': '2023-11-27T17:00:00.000Z',
        'average-daily-market-close-price': 5.00,
        'deliverable-type': 'Option',
        'underlying-symbol': 'AAPL 191004P00275000',
        'mark-price': 8.00,
        'account-number': 'XXXXXX',
        'fixing-price': 5.00,
        'quantity': {'long': 10, 'short': 0},
        'realized-day-gain-date': '2023-11-27',
        'expires-at': '2022-01-21T20:00:00.000Z',
        'mark': 8.00,
        'realized-day-gain': 300.00,
        'realized-day-gain-effect': 'Profit',
        'cost-effect': 'Debit',
        'close-price': 8.00,
    },
]

positions_df = pd.json_normalize(mock_data)

# Formatting DataFrame for pretty display in Discord
formatted_positions = positions_df.to_markdown(index=False)

# Print the pretty table
print(formatted_positions)


# Discord-specific formatting function
def format_for_discord(df):
    discord_msg = '```'  # Start a code block
    discord_msg += (
        'Instrument Type | Symbol | Quantity | Average Price | Current Price | PnL\n'
    )
    discord_msg += (
        '---------------------------------------------------------------------------\n'
    )
    for _, row in df.iterrows():
        symbol = row['underlying-symbol']
        quantity = row['quantity.long'] - row['quantity.short']
        average_price = row['average-daily-market-close-price']
        current_price = row['mark-price']
        pnl = row['realized-day-gain']
        discord_msg += f"{row['instrument-type']:<15} | {symbol:<6} | {quantity:>8} | {average_price:>13} | {current_price:>14} | {pnl:>7}\n"
    discord_msg += '```'  # End code block
    return discord_msg


# Use this function to format the mock positions
formatted_positions_discord = format_for_discord(positions_df)
print(formatted_positions_discord)
