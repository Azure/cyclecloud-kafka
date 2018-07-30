# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

name             'kafka-client'
description      'Provides lightweight Kafka discovery for clients the do not require the full kafka installation from the kafka cookbook.'
version          '1.0.0'

%w{ cyclecloud jdk jetpack }.each {|ckbk| depends ckbk }
