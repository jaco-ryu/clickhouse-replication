from clickhouse_driver import Client
from datetime import datetime

if __name__ == "__main__":
    client = Client("127.0.0.1", port="9004")

    client.execute("CREATE DATABASE IF NOT EXISTS billing")

    client.execute(r'''CREATE TABLE IF NOT EXISTS billing.transactions(
                      timestamp DateTime,
                      currency String,
                      value Float64)
                      ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/billing.transactions', '{replica}')
                      PARTITION BY currency
                      ORDER BY timestamp''')

    client.execute("INSERT INTO billing.transactions (timestamp, currency, value) VALUES", \
        [(datetime.utcnow(), "transitivity", 38.9), (datetime.utcnow(), "velocity", 27.2), \
            (datetime.utcnow(), "ferocity", 19.8)])
    
    data = client.execute("SELECT * FROM billing.transactions")

    for row in data:
        print("Timestamp", row[0], sep=": ")
        print("Currency", row[1], sep=": ")
        print("Value", row[2], sep=": ")
        print()