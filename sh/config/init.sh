#!/bin/bash
echo "----------------------------------"
echo "Initializing HTCondorCE"
echo "----------------------------------"
# Copy HTCondorCE config files
cp $SIMPLE_CONFIG_DIR/config/condor_mapfile $HTCONDOR_CE_CONFIG_DIR/condor_mapfile
cp $SIMPLE_CONFIG_DIR/config/60_configured_attributes.conf $HTCONDOR_CE_CONFIG_DIR/config.d/60_configured_attributes.conf
cp $SIMPLE_CONFIG_DIR/config/98_simple.conf $HTCONDOR_CE_CONFIG_DIR/config.d/98_simple.conf
cp $SIMPLE_CONFIG_DIR/config/59_site_security.conf $HTCONDOR_CE_CONFIG_DIR/config.d/59_site_security.conf

echo "Copying supplemental configs..."
while IFS=":" read -r source dest; do
  mkdir -p $(dirname ${dest}) && cat "$SIMPLE_CONFIG_DIR/config/$source" >> ${dest}
done < ${SIMPLE_CONFIG_DIR}/config/supplemental_mapfile

# Copy host certificates and set permissions
echo "Copying host certificates..."
cp /etc/simple_grid/host_certificates/hostcert.pem /etc/grid-security/
cp /etc/simple_grid/host_certificates/hostkey.pem /etc/grid-security/

#set permissions
echo "Setting permissions for host certificates..."
chmod 600 /etc/grid-security/hostkey.pem
chmod 644 /etc/grid-security/hostcert.pem
echo "Done"

# Create users dynamically
while IFS=" = " read -r key value; do
	case "$key" in
		SUPPORTED_VO_USERS)
    for user in ${value//,/ }
    do
	    adduser -m $user
    done ;;
	esac
  done < $SIMPLE_CONFIG_DIR/config/supported_vo_users.conf

chmod 777 /home/*

echo "----------------------------------"
echo "Set Timezone"
echo "----------------------------------"
if [ ! -s $SIMPLE_CONFIG_DIR/config/timezone ]
then
    echo "No timezone info available in site_level_config_file."
else
    mv /etc/localtime /etc/localtime.backup
    ln -s /usr/share/zoneinfo/$(cat $SIMPLE_CONFIG_DIR/config/timezone) /etc/localtime
fi

echo "----------------------------------"
echo "Initializing HTCondor SCHEDD"
echo "----------------------------------"
cp $SIMPLE_CONFIG_DIR/config/50_PC.conf $HTCONDOR_CONFIG_DIR/config.d/50PC.conf
cp $SIMPLE_CONFIG_DIR/config/98_simple_condor.conf $HTCONDOR_CONFIG_DIR/config.d/98_simple_condor.conf

# fix issue#11 on github. Sometimes permissions on this file are incorrect
#mkdir -p /run/lock/condor-ce
#chown -R condor:condor /var/lock/condor-ce
#chown -R condor:condor /run/lock/condor-ce

echo "----------------------------------"
echo "Starting daemons"
echo "----------------------------------"
echo "Starting HTCondor"
systemctl start condor
echo "Starting HTCondorCE"
systemctl start condor-ce
echo "Starting crond"
systemctl start crond
echo "Fetch CRL config"
systemctl start fetch-crl-cron
fetch-crl

echo "----------------------------------"
echo "Retry starting HTCondorCE "
echo "----------------------------------"
sleep 10
chown condor:condor /var/lock/condor-ce
chown condor:condor /run/lock/condor-ce
systemctl restart condor-ce

echo "----------------------------------"
echo "Prepare for restarts "
echo "----------------------------------"
systemctl enable condor-ce
systemctl enable condor
systemctl enable crond
systemctl enable fetch-crl-cron

echo "Initialization Complete!"