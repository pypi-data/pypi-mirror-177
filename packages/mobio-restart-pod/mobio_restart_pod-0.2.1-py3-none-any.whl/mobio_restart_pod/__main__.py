#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
               ..
              ( '`<
               )(
        ( ----'  '.
        (         ;
         (_______,' 
    ~^~^~^~^~^~^~^~^~^~^~
    Author: thong
    Company: M O B I O
    Date Created: 11/08/2022
"""

import os
import sys

from mobio_restart_pod.config.check_kafka_group_liveness import checK_status_consumer


def main(kafka_group):
    """
    check consumer kafka alive?
    :return:
    """
    checK_status_consumer(kafka_group)


if __name__ == '__main__':
    kafka_group = sys.argv[1] if len(sys.argv) > 0 else None
    if kafka_group:
        main(kafka_group)
    else:
        print("Not config kafka group")
