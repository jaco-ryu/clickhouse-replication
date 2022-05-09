 - zookeeper 
   - i-0f3619b8972eba0ce (whale-bridge-qa-v2) : 10.24.25.138 - ssh -i t.pem ec2-user@10.24.25.138
   - i-0fe14930e2d2d1de2 (image-vector-qa-v1) : 10.24.28.246 - ssh -i t.pem ec2-user@10.24.28.246
   - i-036d684199b169ceb (whale-bridge-dev)   : 10.24.26.195 - ssh -i t.pem ec2-user@10.24.26.195
 - clickhouse 
   - i-05b44b997df0a60e6 (ad-payment-qa)      : 10.24.29.85   - ssh -i t.pem ec2-user@10.24.29.85 - ip-10-24-29-85.ap-northeast-2.compute.internal
   - i-01ba6c56425400373 (ad-payment-dev)     : 10.24.25.112  - ssh -i t.pem ec2-user@10.24.25.112 - ip-10-24-25-112.ap-northeast-2.compute.internal
   - i-0ccfcda74d2e9c130 (ip-api-qa)          : 10.24.27.98   - ssh -i t.pem ec2-user@10.24.27.98 - ip-10-24-27-98.ap-northeast-2.compute.internal
   - i-09d694c45bcd14cfe (whale-indexer-qa)   : 10.24.26.146  - ssh -i t.pem ec2-user@10.24.26.146 - ip-10-24-26-146.ap-northeast-2.compute.internal
   - i-0e4bc2e21d72fdd4e (whale-indexer-qa)   : 10.24.28.206  - ip-10-24-28-206.ap-northeast-2.compute.internal ( no작업 )
   - i-04080435f1747034a (Image-vector-dev)   : 10.24.24.123  - ip-10-24-24-123.ap-northeast-2.compute.internal ( no작업 )

 - zookeeper cluster install ( 3 instance )
   - wget --no-check-certificate https://dlcdn.apache.org/zookeeper/zookeeper-3.8.0/apache-zookeeper-3.8.0-bin.tar.gz
   - tar -xvf apache-zookeeper-3.8.0-bin.tar.gz
   - mkdir -p /home/ec2-user/zookeeper/data
   - vi /home/ec2-user/apache-zookeeper-3.8.0-bin/conf/zoo.cfg
   - cat /home/ec2-user/apache-zookeeper-3.8.0-bin/conf/zoo.cfg
   - echo 1 > /home/ec2-user/zookeeper/data/myid ; cat /home/ec2-user/zookeeper/data/myid
   - echo 2 > /home/ec2-user/zookeeper/data/myid ; cat /home/ec2-user/zookeeper/data/myid
   - echo 3 > /home/ec2-user/zookeeper/data/myid ; cat /home/ec2-user/zookeeper/data/myid
   - cd /home/ec2-user/apache-zookeeper-3.8.0-bin/bin/ ; /home/ec2-user/apache-zookeeper-3.8.0-bin/bin/zkServer.sh start
   - /home/ec2-user/apache-zookeeper-3.8.0-bin/bin/zkServer.sh status
   - /home/ec2-user/apache-zookeeper-3.8.0-bin/bin/zkCli.sh 
   - /home/ec2-user/apache-zookeeper-3.8.0-bin/bin/zkServer.sh stop

 - clickhouse cluster install
   - download
     ```
      wget https://packages.clickhouse.com/tgz/stable/clickhouse-client-22.3.2.2.tgz
      wget https://packages.clickhouse.com/tgz/stable/clickhouse-common-static-22.3.2.2.tgz
      wget https://packages.clickhouse.com/tgz/stable/clickhouse-server-22.3.2.2.tgz
      wget https://packages.clickhouse.com/tgz/stable/clickhouse-common-static-dbg-22.3.2.2.tgz
     
      tar -xzvf  clickhouse-client-22.3.2.2.tgz
      tar -xzvf clickhouse-common-static-22.3.2.2.tgz
      tar -xzvf clickhouse-common-static-dbg-22.3.2.2.tgz
      tar -xzvf clickhouse-server-22.3.2.2.tgz
     
      sudo clickhouse-client-22.3.2.2/install/doinst.sh
      sudo clickhouse-common-static-22.3.2.2/install/doinst.sh
      sudo clickhouse-common-static-dbg-22.3.2.2/install/doinst.sh
      sudo clickhouse-server-22.3.2.2/install/doinst.sh
     
      cd /etc/ ; sudo chmod -R 777 ./clickhouse-server/
     
      sudo clickhouse start    
      
      sudo chmod -R 777 /var/log/clickhouse-server/
      
      tail -f /var/log/clickhouse-server/clickhouse-server.log
     
      clickhouse-client -q "SELECT * FROM system.clusters WHERE cluster='adpaymentsandbox' FORMAT Vertical;"
      sudo clickhouse stop
     
      clickhouse-client -q "select * from system.zookeeper where path='/ai/sandbox/ip/ad-payment'"
     
      clickhouse-client -q "select * from system.zookeeper where path='/clickhouse/task_queue/'"
     
      The choice is saved in file /etc/clickhouse-server/config.d/listen.xml.
 chown -R clickhouse:clickhouse '/etc/clickhouse-server'

ClickHouse has been successfully installed.

Start clickhouse-server with:
 sudo clickhouse start

Start clickhouse-client with:
 clickhouse-client --password****
     ```