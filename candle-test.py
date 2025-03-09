import ollama
from langchain_ollama import OllamaEmbeddings

# Step 1: Initialize OllamaEmbeddings with the DeepSeek-R1 model
embedding_function = OllamaEmbeddings(model="deepseek-r1:14b")

# Step 2: Load historical 5-minute OHLCV data (can be loaded from JSON or CSV)
# Example: Load data from a JSON file or define manually
historical_data = [
    {"timestamp": "2025-03-01 00:00", "open": 1.345, "high": 1.355, "low": 1.340, "close": 1.350, "volume": 5000},
    {"timestamp": "2025-03-01 00:05", "open": 1.350, "high": 1.360, "low": 1.345, "close": 1.355, "volume": 5200},
    {"timestamp": "2025-03-01 00:10", "open": 1.355, "high": 1.370, "low": 1.350, "close": 1.365, "volume": 5400}
]

# Step 3: Format the data into text representation suitable for embedding
formatted_data = [
    f"Timestamp: {candle['timestamp']}, Open: {candle['open']}, High: {candle['high']}, Low: {candle['low']}, Close: {candle['close']}, Volume: {candle['volume']}"
    for candle in historical_data
]

# Step 4: Generate embeddings for each 5-minute candle data point
embeddings = embedding_function.embed(formatted_data)

# Step 5: Prepare a question about the data
question = "Based on the last three 5-minute candles, what is the expected trend for the next candle?"

# Step 6: Query the model with the question
response = ollama.chat(
    model="deepseek-r1:14b",
    messages=[{
        "role": "system", "content": "You are a financial analyst that predicts trends based on historical market data."},
        {"role": "user", "content": f"Data: {formatted_data}. Question: {question}"}
    ])

# Step 7: Print the response
print("Model's Response:")
print(response['text'])
