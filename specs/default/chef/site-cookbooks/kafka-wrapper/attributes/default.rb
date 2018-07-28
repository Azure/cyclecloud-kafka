# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# this value cannot be set via a cluster template because it has
# a '.' in the attribute name 'zookeeper.connect'
default['kafka']['broker']['zookeeper.connect'] = %w[localhost:2181]
# DO NOT use /opt/kafka/logs as that will cause the symlinked directory /opt/kafka
# to be created as a regular directory before it is created as a symlink
default['kafka']['broker']['log.dirs'] = %w[/opt/kafka-logs]
