#
# Cookbook Name:: kafka-client
# Recipe:: default
#
# For Kafka Clients that do not require the full Kafka cookbook.
# The basic Kafka Client recipe simply makes the broker hostlist available
# to client applications via jetpack or via a conf file.

kafka_cluster = node['kafka']['cluster_name']
brokers = cluster.search(:clusterUID => kafka_cluster, :recipe => "kafka::default").select {|n| not n['kafka'].nil? and not n['kafka']['broker']['port'].nil?}.map  do |n|
  "#{n['cyclecloud']['instance']['ipv4']}:#{n['kafka']['broker']['port']}"
end

brokers.sort!
Chef::Log.info "Kafka cluster: #{brokers.inspect}"


# Clients should use the node['kafka']['brokerlist'] to connect
node.set['kafka']['brokerlist'] = brokers

# create a redis cluster host list that can be used by client applications
file node['kafka']['brokerfile'] do
  content brokers.join("\n")
end

