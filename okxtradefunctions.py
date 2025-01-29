import okx.Trade as Trade
import okx.MarketData as MarketData
import okx.Account as Account
import okx.PublicData as PublicData
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# OKX API credentials from .env file
api_key = os.getenv("OKX_API_KEY")
secret_key = os.getenv("OKX_SECRET_KEY")
passphrase = os.getenv("OKX_PASSPHRASE")
flag = "0"  # 0 = real account, 1 = demo account

# Initialize OKX API clients
accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)
publicDataAPI = PublicData.PublicAPI(flag=flag)
tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

# Set position mode to long/short mode
der_mod = accountAPI.set_position_mode(posMode="long_short_mode")

# ENTER LONG & SHORT POSITIONS

def open_long(coin, step, size):
    price = marketDataAPI.get_tickers(instType="SWAP", uly=f"{coin}-USDT").get("data")[0].get("last")
    contract_value = publicDataAPI.get_instruments(instType="SWAP", instId=f"{coin}-USDT-SWAP").get("data")[0].get("ctVal")
    ctVal = float(price) * float(contract_value)

    accountAPI.set_leverage(instId=f"{coin}-USDT-SWAP", lever="10", posSide="long", mgnMode="isolated")

    step_multipliers = [1, 1.5, 2.5, 5, 10, 20, 60]
    sz = round((size * step_multipliers[int(step)]) * 10 / ctVal)

    return tradeAPI.place_order(instId=f"{coin}-USDT-SWAP", tdMode="isolated", side="buy", posSide="long", ordType="market", sz=f"{sz}")

def open_short(coin, step, size):
    price = marketDataAPI.get_tickers(instType="SWAP", uly=f"{coin}-USDT").get("data")[0].get("last")
    contract_value = publicDataAPI.get_instruments(instType="SWAP", instId=f"{coin}-USDT-SWAP").get("data")[0].get("ctVal")
    ctVal = float(price) * float(contract_value)

    accountAPI.set_leverage(instId=f"{coin}-USDT-SWAP", lever="10", posSide="short", mgnMode="isolated")

    step_multipliers = [1, 1.5, 2.5, 5, 10, 20, 60]
    sz = round((size * step_multipliers[int(step)]) * 10 / ctVal)

    return tradeAPI.place_order(instId=f"{coin}-USDT-SWAP", tdMode="isolated", side="sell", posSide="short", ordType="market", sz=f"{sz}")

# CLOSE LONG & SHORT POSITIONS

def close_long(coin, portion):
    available_position = int(accountAPI.get_positions().get("data")[0].get('availPos').split("-")[0])

    if portion == "full":
        return tradeAPI.close_positions(instId=f"{coin}-USDT-SWAP", mgnMode="isolated", posSide="long")

    portion_sizes = {"25%": 0.25, "50%": 0.50, "75%": 0.75}
    size = round(available_position * portion_sizes[portion])

    return tradeAPI.place_order(instId=f"{coin}-USDT-SWAP", tdMode="isolated", side="sell", posSide="long", ordType="market", sz=f"{size}")

def close_short(coin, portion):
    available_position = int(accountAPI.get_positions().get("data")[0].get('availPos').split("-")[0])

    if portion == "full":
        return tradeAPI.close_positions(instId=f"{coin}-USDT-SWAP", mgnMode="isolated", posSide="short")

    portion_sizes = {"25%": 0.25, "50%": 0.50, "75%": 0.75}
    size = round(available_position * portion_sizes[portion])

    return tradeAPI.place_order(instId=f"{coin}-USDT-SWAP", tdMode="isolated", side="buy", posSide="short", ordType="market", sz=f"{size}")

# MESSAGE GROUPING

def categorize_message(message):
    if '🟣' in message.upper() or '🔴' in message.upper() or '🟡' in message.upper() or '🟢' in message.upper():
        return execute_trade(message)
    if 'add' in message.lower() or 'should I add' in message.lower() or 'ekleme' in message.lower():
        return add_trade(message)
    if 'CLOSED' in message.upper() or 'KAPATTIM' in message.upper():
        return close_trade(message)
    return "Error"

# IMPORTANT: INITIAL POSITION RATIO
initial_position_size = 1.5

add_long = {
    "ekleme": lambda asset: open_long(asset, "1", initial_position_size),
    "ikinci": lambda asset: open_long(asset, "2", initial_position_size),
    "üçüncü": lambda asset: open_long(asset, "3", initial_position_size),
    "dördüncü": lambda asset: open_long(asset, "4", initial_position_size),
    "beşinci": lambda asset: open_long(asset, "5", initial_position_size),
    "altıncı": lambda asset: open_long(asset, "6", initial_position_size),
}
add_short = {
    "ekleme": lambda asset: open_short(asset, "1", initial_position_size),
    "ikinci": lambda asset: open_short(asset, "2", initial_position_size),
    "üçüncü": lambda asset: open_short(asset, "3", initial_position_size),
    "dördüncü": lambda asset: open_short(asset, "4", initial_position_size),
    "beşinci": lambda asset: open_short(asset, "5", initial_position_size),
    "altıncı": lambda asset: open_short(asset, "6", initial_position_size),
}

def add_trade(trade):
    asset = accountAPI.get_positions().get("data")[0].get('instId').split("-")[0]
    side = accountAPI.get_positions().get("data")[0].get('posSide')
    signal = trade.split()[0].lower()

    if side == "long":
        return add_long.get(signal)(asset)
    elif side == "short":
        return add_short.get(signal)(asset)

def close_trade(trade):
    asset = accountAPI.get_positions().get("data")[0].get('instId').split("-")[0]
    side = accountAPI.get_positions().get("data")[0].get('posSide')    
    signal = trade.lower().split()[0]

    if side == "long":
        return close_long(asset, signal) 
    elif side == "short":
        return close_short(asset, signal)

def execute_trade(trade):
    s = trade.split()
    type_ = s[0]
    pair = s[1]
    leverage = s[2]
    coin = pair.split("USDT")[0]

    if type_ in ["🟡", "🟢"]:
        return open_long(coin, "0", initial_position_size)
    elif type_ in ["🟣", "🔴"]:
        return open_short(coin, "0", initial_position_size)
