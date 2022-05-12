# PROD 레거시 스키마 및 테이블 구조 
## 클러스터명
```
SHOW CLUSTERS ;

# 결과
prod_cluster
stage_cluster
```
 - prod/stage 환경 구성이 나누어져 있는 것이 아니라 물리적인 한 클러스터 안에 2개의 환경이 존재 
 - prod_cluster : prod 환경 클러스터 
 - stage_cluster : stage 환경 클러스터 

## 데이터 베이스 및 관련 테이블 
```
SHOW DATABASES ;

# 결과
ad
default
prod_beluga
prod_datalake
prod_mysql_service_dm
prod_replica
prod_shard
system
```

### default 
 - 클릭하우스 기본 스키마
 - 비지니스 로직과 무관 


### system 
 - 클릭하우스 기본 스키마 중 하나이고 시스템 관련 정보 
 - 비지니스 로직과 무관 


### ad 
```
USE ad ; SHOW TABLES ;

# 결과
temp_ad_action                      - 비어있음 
temp_ad_payment                     - 비어있음
temp_ad_payment_by_creative         - 비어있음
temp_open_listing_filter_log_raw    - 비어있음
temp_search_listing_filter_log_raw  - 비어있음
```
 - 모두 임시로 사용하기 위해 만들 테이블로 보임


### prod_replica
```
USE prod_replica ; SHOW TABLES ;

# 결과
ad_action
ad_payment
ad_payment_by_creative
brand_filter_log_raw
cdc_beluga_modify
deali_actions
open_listing_filter_log_raw
search_listing_filter_log_raw
```
 - ad_action
```
-- ReplicatedMergeTree
-- auto-generated definition
create table ad_action
(
    datetime    String,
    userid Nullable(String),
    platform Nullable(String),
    osversion Nullable(String),
    appversion Nullable(String),
    screenname Nullable(String),
    screenlabel Nullable(String),
    referrer Nullable(String),
    referrerlabel Nullable(String),
    accountid Nullable(String),
    bidprice Nullable(String),
    campaignidx UInt32,
    chargingtype Nullable(String),
    event       String,
    groupidx    UInt32,
    productidx  UInt32,
    selectiongroupid Nullable(String),
    selectionid Nullable(String),
    selectiontime Nullable(String),
    wsidx       UInt32,
    timestamp   UInt64,
    unitidx     UInt32,
    creativeidx UInt32,
    pageidx     UInt32,
    query Nullable(String),
    keywordidx Nullable(String),
    usertype Nullable(String),
    rsidx Nullable(String),
    exposuretime Nullable(String),
    uuid Nullable(String),
    dt          Date,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_02/ad_action', 'replica_02')
        PARTITION BY toYYYYMM(dt)
        ORDER BY (productidx, event, wsidx, creativeidx, datetime)
        SETTINGS index_granularity = 8192;
```
 - ad_payment
```
-- ReplicatedMergeTree
-- auto-generated definition
create table ad_payment
(
    idx              Int64,
    id Nullable(String),
    account_id Nullable(String),
    campaign_idx Nullable(UInt64),
    group_idx Nullable(UInt64),
    product_idx      UInt64,
    ws_idx           UInt64,
    total_amount     Decimal(18, 2),
    total_amount_vat Decimal(18, 2),
    total_payment Nullable(Int64),
    is_payment Nullable(UInt8),
    is_complete Nullable(UInt8),
    method Nullable(String),
    s3_bucket_key Nullable(String),
    window_start     DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    pay_balance Nullable(Int64),
    pay_date Nullable(DateTime('Asia/Seoul')),
    pay_message Nullable(String),
    pay_paid_amount Nullable(UInt64),
    pay_free_amount Nullable(UInt64),
    guid             UUID                   default generateUUIDv4(),
    consumed_at      DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_02/ad_payment', 'replica_02')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (product_idx, ws_idx, window_start)
        SETTINGS index_granularity = 8192;
```
 - ad_payment_by_creative
```
-- ReplicatedMergeTree
-- auto-generated definition
create table ad_payment_by_creative
(
    idx          Int64,
    ws_idx       UInt32,
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    product_idx  UInt32,
    group_idx Nullable(UInt32),
    creative_idx UInt32,
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    charging_type Nullable(String),
    amount       Decimal(10, 2)                  default 0,
    vat          Decimal(10, 2)                  default 0,
    vat_amount   Decimal(10, 2)                  default 0,
    created_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx Nullable(UInt32),
    query Nullable(String),
    guid         UUID                            default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul')          default toDateTime(now(), 'Asia/Seoul'),
    filtered_at Nullable(DateTime('Asia/Seoul')) default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_02/ad_payment_by_creative', 'replica_02')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (product_idx, ws_idx, creative_idx, window_start)
        SETTINGS index_granularity = 8192;
```
 - brand_filter_log_raw
```
-- ReplicatedMergeTree
-- auto-generated definition
create table brand_filter_log_raw
(
    idx Nullable(UInt32),
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx Nullable(UInt32),
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    query Nullable(String),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx Nullable(UInt32),
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_02/brand_filter_log_raw', 'replica_02')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (window_start, ws_idx, event)
        SETTINGS index_granularity = 8192;
```
 - cdc_beluga_modify
```
-- ReplicatedMergeTree
-- auto-generated definition
create table cdc_beluga_modify
(
    table_name  String,
    json_data   String,
    dml_type    String,
    completed   UInt8,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_02/cdc_beluga_modify', 'replica_02')
        PARTITION BY toYYYYMM(consumed_at)
        ORDER BY consumed_at
        SETTINGS index_granularity = 8192;


```
 - deali_actions
```
-- 현재 데이터 미존재 
-- ReplicatedMergeTree
-- auto-generated definition
create table deali_actions
(
    timestamp   String,
    datetime    String,
    usertype Nullable(String),
    userid Nullable(String),
    platform Nullable(String),
    osversion Nullable(String),
    appversion Nullable(String),
    uuid Nullable(String),
    screenname Nullable(String),
    screenlabel Nullable(String),
    referrer Nullable(String),
    referrerlabel Nullable(String),
    event       String,
    target Nullable(String),
    rsidx Nullable(String),
    wsidx Nullable(UInt32),
    wgidx Nullable(UInt32),
    id Nullable(Int32),
    currentpage Nullable(UInt32),
    totalcount Nullable(UInt32),
    query Nullable(String),
    conditions Nullable(String),
    sourceid Nullable(String),
    requestid Nullable(String),
    feature Nullable(String),
    dt          Date,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_02/deali_actions', 'replica_02')
        PARTITION BY toYYYYMM(dt)
        ORDER BY (event, timestamp)
        SETTINGS index_granularity = 8192;


```
 - open_listing_filter_log_raw
```
-- ReplicatedMergeTree
-- auto-generated definition
create table open_listing_filter_log_raw
(
    idx Nullable(Int64),
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx UInt32,
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_02/open_listing_filter_log_raw', 'replica_02')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (event, ws_idx, creative_idx, window_start)
        SETTINGS index_granularity = 8192;


```
 - search_listing_filter_log_raw
```
-- ReplicatedMergeTree
-- auto-generated definition
create table search_listing_filter_log_raw
(
    idx          Int64,
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx UInt32,
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    query Nullable(String),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx  UInt32,
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_02/search_listing_filter_log_raw', 'replica_02')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (event, ws_idx, creative_idx, keyword_idx, window_start)
        SETTINGS index_granularity = 8192;


```

### prod_shard
```
USE prod_shard ; SHOW TABLES ;

# 결과
ad_action
ad_payment
ad_payment_by_creative
brand_filter_log_raw
cdc_beluga_modify
deali_actions
open_listing_filter_log_raw
search_listing_filter_log_raw
```
 - ad_action
```
-- ReplicatedMergeTree
-- auto-generated definition
create table ad_action
(
    datetime    String,
    userid Nullable(String),
    platform Nullable(String),
    osversion Nullable(String),
    appversion Nullable(String),
    screenname Nullable(String),
    screenlabel Nullable(String),
    referrer Nullable(String),
    referrerlabel Nullable(String),
    accountid Nullable(String),
    bidprice Nullable(String),
    campaignidx UInt32,
    chargingtype Nullable(String),
    event       String,
    groupidx    UInt32,
    productidx  UInt32,
    selectiongroupid Nullable(String),
    selectionid Nullable(String),
    selectiontime Nullable(String),
    wsidx       UInt32,
    timestamp   UInt64,
    unitidx     UInt32,
    creativeidx UInt32,
    pageidx     UInt32,
    query Nullable(String),
    keywordidx Nullable(String),
    usertype Nullable(String),
    rsidx Nullable(String),
    exposuretime Nullable(String),
    uuid Nullable(String),
    dt          Date,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_01/ad_action', 'replica_01')
        PARTITION BY toYYYYMM(dt)
        ORDER BY (productidx, event, wsidx, creativeidx, datetime)
        SETTINGS index_granularity = 8192;


```
 - ad_payment
```
-- ReplicatedMergeTree
-- auto-generated definition
create table ad_payment
(
    idx              Int64,
    id Nullable(String),
    account_id Nullable(String),
    campaign_idx Nullable(UInt64),
    group_idx Nullable(UInt64),
    product_idx      UInt64,
    ws_idx           UInt64,
    total_amount     Decimal(18, 2),
    total_amount_vat Decimal(18, 2),
    total_payment Nullable(Int64),
    is_payment Nullable(UInt8),
    is_complete Nullable(UInt8),
    method Nullable(String),
    s3_bucket_key Nullable(String),
    window_start     DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    pay_balance Nullable(Int64),
    pay_date Nullable(DateTime('Asia/Seoul')),
    pay_message Nullable(String),
    pay_paid_amount Nullable(UInt64),
    pay_free_amount Nullable(UInt64),
    guid             UUID                   default generateUUIDv4(),
    consumed_at      DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_01/ad_payment', 'replica_01')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (product_idx, ws_idx, window_start)
        SETTINGS index_granularity = 8192;


```
 - ad_payment_by_creative
```
-- ReplicatedMergeTree
-- auto-generated definition
create table ad_payment_by_creative
(
    idx          Int64,
    ws_idx       UInt32,
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    product_idx  UInt32,
    group_idx Nullable(UInt32),
    creative_idx UInt32,
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    charging_type Nullable(String),
    amount       Decimal(10, 2)                  default 0,
    vat          Decimal(10, 2)                  default 0,
    vat_amount   Decimal(10, 2)                  default 0,
    created_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx Nullable(UInt32),
    query Nullable(String),
    guid         UUID                            default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul')          default toDateTime(now(), 'Asia/Seoul'),
    filtered_at Nullable(DateTime('Asia/Seoul')) default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_01/ad_payment_by_creative', 'replica_01')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (product_idx, ws_idx, creative_idx, window_start)
        SETTINGS index_granularity = 8192;


```
 - brand_filter_log_raw
```
-- ReplicatedMergeTree
-- auto-generated definition
create table brand_filter_log_raw
(
    idx Nullable(UInt32),
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx Nullable(UInt32),
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    query Nullable(String),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx Nullable(UInt32),
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_01/brand_filter_log_raw', 'replica_01')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (window_start, ws_idx, event)
        SETTINGS index_granularity = 8192;


```
 - cdc_beluga_modify
```
-- ReplicatedMergeTree
-- auto-generated definition
create table cdc_beluga_modify
(
    table_name  String,
    json_data   String,
    dml_type    String,
    completed   UInt8,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_01/cdc_beluga_modify', 'replica_01')
        PARTITION BY toYYYYMM(consumed_at)
        ORDER BY consumed_at
        SETTINGS index_granularity = 8192;


```
 - deali_actions
```
-- 현재 데이터 미존재 
-- ReplicatedMergeTree
-- auto-generated definition
create table deali_actions
(
    timestamp   String,
    datetime    String,
    usertype Nullable(String),
    userid Nullable(String),
    platform Nullable(String),
    osversion Nullable(String),
    appversion Nullable(String),
    uuid Nullable(String),
    screenname Nullable(String),
    screenlabel Nullable(String),
    referrer Nullable(String),
    referrerlabel Nullable(String),
    event       String,
    target Nullable(String),
    rsidx Nullable(String),
    wsidx Nullable(UInt32),
    wgidx Nullable(UInt32),
    id Nullable(Int32),
    currentpage Nullable(UInt32),
    totalcount Nullable(UInt32),
    query Nullable(String),
    conditions Nullable(String),
    sourceid Nullable(String),
    requestid Nullable(String),
    feature Nullable(String),
    dt          Date,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_01/deali_actions', 'replica_01')
        PARTITION BY toYYYYMM(dt)
        ORDER BY (event, timestamp)
        SETTINGS index_granularity = 8192;


```
 - open_listing_filter_log_raw
```
-- ReplicatedMergeTree
-- auto-generated definition
create table open_listing_filter_log_raw
(
    idx Nullable(Int64),
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx UInt32,
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_01/open_listing_filter_log_raw', 'replica_01')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (event, ws_idx, creative_idx, window_start)
        SETTINGS index_granularity = 8192;


```
 - search_listing_filter_log_raw
```
-- ReplicatedMergeTree
-- auto-generated definition
create table search_listing_filter_log_raw
(
    idx          Int64,
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx UInt32,
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    query Nullable(String),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx  UInt32,
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = ReplicatedMergeTree('/clickhouse/prod/shard_01/search_listing_filter_log_raw', 'replica_01')
        PARTITION BY toYYYYMM(window_start)
        ORDER BY (event, ws_idx, creative_idx, keyword_idx, window_start)
        SETTINGS index_granularity = 8192;
```


### prod_beluga
```
USE prod_beluga ; SHOW TABLES ;

# 결과
ad_action
ad_payment
ad_payment_by_creative
brand_filter_log_raw
cdc_beluga_modify
open_listing_filter_log_raw
search_listing_filter_log_raw
```
 - ad_action
```
-- Distributed
-- auto-generated definition
create table ad_action
(
    datetime    String,
    userid Nullable(String),
    platform Nullable(String),
    osversion Nullable(String),
    appversion Nullable(String),
    screenname Nullable(String),
    screenlabel Nullable(String),
    referrer Nullable(String),
    referrerlabel Nullable(String),
    accountid Nullable(String),
    bidprice Nullable(String),
    campaignidx UInt32,
    chargingtype Nullable(String),
    event       String,
    groupidx    UInt32,
    productidx  UInt32,
    selectiongroupid Nullable(String),
    selectionid Nullable(String),
    selectiontime Nullable(String),
    wsidx       UInt32,
    timestamp   UInt64,
    unitidx     UInt32,
    creativeidx UInt32,
    pageidx     UInt32,
    query Nullable(String),
    keywordidx Nullable(String),
    usertype Nullable(String),
    rsidx Nullable(String),
    exposuretime Nullable(String),
    uuid Nullable(String),
    dt          Date,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = Distributed('prod_cluster', '', 'ad_action', rand());
```
 - ad_payment
```
-- Distributed
-- auto-generated definition
create table ad_payment
(
    idx              Int64,
    id Nullable(String),
    account_id Nullable(String),
    campaign_idx Nullable(UInt64),
    group_idx Nullable(UInt64),
    product_idx      UInt64,
    ws_idx           UInt64,
    total_amount     Decimal(18, 2),
    total_amount_vat Decimal(18, 2),
    total_payment Nullable(Int64),
    is_payment Nullable(UInt8),
    is_complete Nullable(UInt8),
    method Nullable(String),
    s3_bucket_key Nullable(String),
    window_start     DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    pay_balance Nullable(Int64),
    pay_date Nullable(DateTime('Asia/Seoul')),
    pay_message Nullable(String),
    pay_paid_amount Nullable(UInt64),
    pay_free_amount Nullable(UInt64),
    guid             UUID                   default generateUUIDv4(),
    consumed_at      DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = Distributed('prod_cluster', '', 'ad_payment', rand());

```
 - ad_payment_by_creative
```
-- Distributed
-- auto-generated definition
create table ad_payment_by_creative
(
    idx          Int64,
    ws_idx       UInt32,
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    product_idx  UInt32,
    group_idx Nullable(UInt32),
    creative_idx UInt32,
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    charging_type Nullable(String),
    amount       Decimal(10, 2)                  default 0,
    vat          Decimal(10, 2)                  default 0,
    vat_amount   Decimal(10, 2)                  default 0,
    created_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx Nullable(UInt32),
    query Nullable(String),
    guid         UUID                            default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul')          default toDateTime(now(), 'Asia/Seoul'),
    filtered_at Nullable(DateTime('Asia/Seoul')) default toDateTime(now(), 'Asia/Seoul')
)
    engine = Distributed('prod_cluster', '', 'ad_payment_by_creative', rand());


```
 - brand_filter_log_raw
```
-- Distributed
-- auto-generated definition
create table brand_filter_log_raw
(
    idx Nullable(UInt32),
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx Nullable(UInt32),
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    query Nullable(String),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx Nullable(UInt32),
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = Distributed('prod_cluster', '', 'brand_filter_log_raw', rand());


```
 - cdc_beluga_modify
```
-- Distributed
-- auto-generated definition
create table cdc_beluga_modify
(
    table_name  String,
    json_data   String,
    dml_type    String,
    completed   UInt8,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = Distributed('prod_cluster', '', 'cdc_beluga_modify', rand());
```
 - open_listing_filter_log_raw
```
-- auto-generated definition
create table open_listing_filter_log_raw
(
    idx Nullable(Int64),
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx UInt32,
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = Distributed('prod_cluster', '', 'open_listing_filter_log_raw', rand());
```
 - search_listing_filter_log_raw
```
-- Distributed
-- auto-generated definition
create table search_listing_filter_log_raw
(
    idx          Int64,
    ad_payment_raw_idx Nullable(UInt32),
    account_id Nullable(String),
    campaign_idx Nullable(UInt32),
    group_idx Nullable(UInt32),
    ws_idx       UInt32,
    product_idx Nullable(UInt32),
    unit_idx Nullable(UInt32),
    page_idx Nullable(UInt32),
    platform Nullable(String),
    os_version Nullable(String),
    app_version Nullable(String),
    creative_idx UInt32,
    bid_price Nullable(Decimal(9, 2)),
    count Nullable(UInt32),
    created_at Nullable(DateTime('Asia/Seoul')),
    updated_at Nullable(DateTime('Asia/Seoul')),
    selection_id Nullable(String),
    event        String,
    rs_idx Nullable(UInt32),
    user_id Nullable(String),
    window_start DateTime('Asia/Seoul'),
    window_end Nullable(DateTime('Asia/Seoul')),
    query Nullable(String),
    charging_type Nullable(String),
    filter_code Nullable(String),
    filtered_at Nullable(DateTime('Asia/Seoul')),
    keyword_idx  UInt32,
    cd_idx Nullable(UInt32),
    guid         UUID                   default generateUUIDv4(),
    consumed_at  DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = Distributed('prod_cluster', '', 'search_listing_filter_log_raw', rand());
```

### prod_datalake
```
USE prod_datalake ; SHOW TABLES ;

# 결과
deali_actions                       - 비어있음
```
 - deali_actions
```
-- Distributed
-- auto-generated definition
create table deali_actions
(
    timestamp   String,
    datetime    String,
    usertype Nullable(String),
    userid Nullable(String),
    platform Nullable(String),
    osversion Nullable(String),
    appversion Nullable(String),
    uuid Nullable(String),
    screenname Nullable(String),
    screenlabel Nullable(String),
    referrer Nullable(String),
    referrerlabel Nullable(String),
    event       String,
    target Nullable(String),
    rsidx Nullable(String),
    wsidx Nullable(UInt32),
    wgidx Nullable(UInt32),
    id Nullable(Int32),
    currentpage Nullable(UInt32),
    totalcount Nullable(UInt32),
    query Nullable(String),
    conditions Nullable(String),
    sourceid Nullable(String),
    requestid Nullable(String),
    feature Nullable(String),
    dt          Date,
    guid        UUID                   default generateUUIDv4(),
    consumed_at DateTime('Asia/Seoul') default toDateTime(now(), 'Asia/Seoul')
)
    engine = Distributed('prod_cluster', '', 'deali_actions', rand());
```

### prod_mysql_service_dm
```
USE prod_mysql_service_dm ; SHOW TABLES ;

# 결과
brand_ad_conversion
flyway_schema_history
target_keywordwholesales_agg
```
 - brand_ad_conversion
```
-- MySQL
-- auto-generated definition
create table brand_ad_conversion
(
    idx          Int64,
    ws_idx       Int32,
    creative_idx Int32,
    like_count Nullable(Int32),
    ws_visit_count Nullable(Int32),
    trade_request_count Nullable(Int32),
    viewer_count Nullable(Int32),
    dt Nullable(DateTime),
    updated_at   DateTime,
    created_at   DateTime
)
    engine = MySQL('datamart-read.di.sinsang.market:3306', 'service_dm', 'brand_ad_conversion', 'master',
             'o%gnQVPA?84G66MR');
```
 - flyway_schema_history
```
-- MySQL
-- auto-generated definition
create table flyway_schema_history
(
    installed_rank Int32,
    version Nullable(String),
    description    String,
    type           String,
    script         String,
    checksum Nullable(Int32),
    installed_by   String,
    installed_on   DateTime,
    execution_time Int32,
    success        Int8
)
    engine = MySQL('datamart-read.di.sinsang.market:3306', 'service_dm', 'flyway_schema_history', 'master',
             'o%gnQVPA?84G66MR');


```
 - target_keywordwholesales_agg
```
-- MySQL
-- auto-generated definition
create table target_keywordwholesales_agg
(
    userid     String,
    rsidx Nullable(Int32),
    keyword_list Nullable(String),
    wsidx_list Nullable(String),
    created_at DateTime,
    updated_at DateTime
)
    engine = MySQL('datamart-read.di.sinsang.market:3306', 'service_dm', 'target_keywordwholesales_agg', 'master',
             'o%gnQVPA?84G66MR');


```