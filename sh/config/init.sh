#!/bin/bash
echo "----------------------------------"
echo "Initializing HTCondorCE"
echo "----------------------------------"
# Copy HTCondorCE config files
cp $SIMPLE_CONFIG_DIR/config/condor_mapfile $HTCONDOR_CE_CONFIG_DIR/condor_mapfile
cp $SIMPLE_CONFIG_DIR/config/60_configured_attributes.conf $HTCONDOR_CE_CONFIG_DIR/config.d/60_configured_attributes.conf
cp $SIMPLE_CONFIG_DIR/config/98_simple.conf $HTCONDOR_CE_CONFIG_DIR/config.d/98_simple.conf
cp $SIMPLE_CONFIG_DIR/config/59_site_security.conf $HTCONDOR_CE_CONFIG_DIR/config.d/59_site_security.conf
echo "Copied HTCondorCE config files from $SIMPLE_CONFIG_DIR/config to $HTCONDORCE_CONFIG_DIR/config.d. Copied condor_mapfile to $HTCONDORCE_CONFIG_DIR"
# Copy host certificates and set permissions
# Create users
echo "----------------------------------"
echo "Initializing HTCondor SCHEDD"
echo "----------------------------------"
cp $SIMPLE_CONFIG_DIR/config/50_PC.conf $HTCONDOR_CONFIG_DIR/config.d/50PC.conf
cp $SIMPLE_CONFIG_DIR/config/98_simple_condor.conf $HTCONDOR_CONFIG_DIR/config.d/98_simple_condor.conf
echo "Starting HTCondorCE"
systemctl start condor-ce
echo "Starting HTCondor"
systemctl start condor
echo "Initialization Complete!"

