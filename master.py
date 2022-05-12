from clickhouse_driver import Client
from datetime import datetime

if __name__ == "__main__":
    client = Client("127.0.0.1", port="9000")

    client.execute("CREATE DATABASE IF NOT EXISTS billing")

    # CREATE
    # TABLE
    # IF
    # NOT
    # EXISTS
    # billing.transactions_local(
    #     timestamp
    # DateTime,
    # currency
    # String,
    # value
    # Float64)
    # ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/billing.transactions', '{replica}')
    # PARTITION
    # BY
    # currency
    # ORDER
    # BY
    # timestamp
    #
    # CREATE
    # TABLE
    # IF
    # NOT
    # EXISTS
    # billing.transactions(
    #     timestamp
    # DateTime,
    # currency
    # String,
    # value
    # Float64)
    # ENGINE = Distributed(example_cluster, billing, transactions_local, rand())

    client.execute('''CREATE TABLE IF NOT EXISTS billing_remote.transactions(
                      timestamp DateTime,
                      currency String,
                      value Float64)
                      ENGINE = Distributed(adpaymentsandbox, billing, transactions, rand())''')
    client.execute('''CREATE TABLE IF NOT EXISTS billing.transactions(
                          timestamp DateTime,
                          currency String,
                          value Float64)
                          ENGINE = Distributed(example_cluster, billing, transactions, rand())''')
    client.execute("INSERT INTO billing.transactions (timestamp, currency, value) VALUES", \
        [(datetime.utcnow(), "integrity", 38.9), (datetime.utcnow(), "voltage", 27.2), \
            (datetime.utcnow(), "resilience", 19.8)])

    data = client.execute("SELECT * FROM billing.transactions")

    for row in data:
        print("Timestamp", row[0], sep=": ")
        print("Currency", row[1], sep=": ")
        print("Value", row[2], sep=": ")
        print()