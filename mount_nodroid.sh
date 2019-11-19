#!/bin/bash
# THIS DOESNT WORK
export EMPTY_MOUNT_DIR=/home/user/lnd/
sshfs $EMPTY_MOUNT_DIR root@192.168.1.8:/root -p 22222