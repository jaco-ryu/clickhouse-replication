SELECT * FROM system.clusters

CREATE DATABASE pokemon_cluster on cluster pokemon

CREATE TABLE pokemon_cluster.event_local on cluster pokemon
(
  id UInt64,
  time DateTime,
  type UInt16,
  pokemon_id UInt16
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/event_local', '{replica}')
PARTITION BY toYYYYMM(time)
ORDER BY (toYYYYMM(time), id);

CREATE TABLE pokemon_cluster.event_distributed on cluster pokemon
(
  id UInt64,
  time DateTime,
  type UInt16,
  pokemon_id UInt16
)
ENGINE = Distributed(pokemon, pokemon_cluster, event_local, rand())

-- we are connected to ch1
INSERT INTO pokemon_cluster.event_local VALUES(122, '2018-01-01 00:00:00', 33, 2222)

INSERT INTO pokemon_cluster.event_distributed VALUES(22222222, '2019-01-01 00:00:00', 2, 222)
INSERT INTO pokemon_cluster.event_distributed VALUES(44444444, '2019-01-01 00:00:00', 2, 222)
