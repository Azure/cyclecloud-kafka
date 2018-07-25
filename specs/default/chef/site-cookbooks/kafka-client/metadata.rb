name             'kafka-client'
maintainer       'Cycle Computing LLC'
maintainer_email 'suppport@cyclecomputing.com'
license          'All rights reserved'
description      'Provides lightweight Kafka discovery for clients the do not require the full kafka installation from the kafka cookbook.'
version          '1.0.0'

%w{ cyclecloud jdk jetpack }.each {|ckbk| depends ckbk }
