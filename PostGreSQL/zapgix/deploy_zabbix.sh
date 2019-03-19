#!/bin/bash
SOURCE_DIR=$(dirname $0)
ZABBIX_DIR=/etc/zabbix
SCRIPT_DIR=/usr/local/bin/zabbix
mkdir -p ${SCRIPT_DIR}/scripts/zapgix
cp -r ${SOURCE_DIR}/zapgix/sql ${SCRIPT_DIR}/scripts/zapgix/
cp ${SOURCE_DIR}/zapgix/zapgix.sh ${SCRIPT_DIR}/scripts/zapgix/
cp ${SOURCE_DIR}/zapgix/zabbix_agentd.conf ${ZABBIX_DIR}/zabbix_agentd.d/userparameter_postgresql.conf
