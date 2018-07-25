# Kafka Cluster for clients to use
default['kafka']['cluster_name'] = node['cyclecloud']['cluster']['id']

# Client configuration file (alternately use: jetpack config kafka.brokerlist)
default['kafka']['brokerlist'] = []
default['kafka']['brokerfile'] = File.join(node['cyclecloud']['home'], "config", "kafka_brokers.txt")

