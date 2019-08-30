FROM cern/cc7-base

## Install condor ##
RUN yum install -y wget
RUN wget https://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor
RUN rpm --import RPM-GPG-KEY-HTCondor
WORKDIR /etc/yum.repos.d/
RUN wget https://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo
RUN yum -y install condor htcondor-ce-condor 
#COPY config/batch7-stable.repo /etc/yum.repos.d/batch7-stable.repo

## Install certs ##
RUN yum -y install fetch-crl globus-rsl empty-ca-certs

## Install utils ##
RUN yum install -y vim less 

## net tools ##
RUN yum install -y net-tools iproute openssh openssh-server openssh-clients openssl-libs tcpdump

## default users ##
RUN useradd -m test
RUN adduser -m condor_user
RUN mkdir -p /etc/grid-security/
RUN rpm -Uvh http://yum.puppet.com/puppet5-release-el-7.noarch.rpm
RUN yum install -y puppet-agent
RUN /opt/puppetlabs/bin/puppet module install HEPPuppet-argus --version 0.0.3
RUN /opt/puppetlabs/bin/puppet module install HEPPuppet-htcondor --version 2.4.3


## mount point for SIMPLE Grid Framework ##
VOLUME ["/etc/simple_grid"]

## init system inside the container ##
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]