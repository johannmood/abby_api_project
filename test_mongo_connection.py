from pymongo import MongoClient

# Replace with your connection string
connection_string = "mongodb+srv://abbby:OfkYFyefugSneoce@cluster0.34s7z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)

try:
    # Attempt to list databases
    print(client.list_database_names())
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)