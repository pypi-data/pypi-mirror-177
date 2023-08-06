from naas_proxy_manager.classes import *
from naas_proxy_manager.providers.aws import *

import boto3
import requests
from loguru import logger
from datetime import datetime, timedelta
import time

class AWSSquidProxy(AWSEC2Proxy):

    ami_name : str = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20220912"
    ami : dict = None
    params : dict = None

    script : str = """#!/bin/bash
sudo su
apt update --yes
apt install --yes wget curl
wget https://raw.githubusercontent.com/serverok/squid-proxy-installer/master/squid3-install.sh -O squid3-install.sh
bash squid3-install.sh
#kill -9 `ps -aux | grep "/usr/sbin/squid --foreground" | head -n 1 | awk '{ print $2 }'`
echo 'naas:$apr1$bvQsqJ3w$GFOX4yyAchIzi8EO4bcdW1' > /etc/squid/passwd
#service squid start
service reload squid
    """

    def __init__(self, bt_session:boto3.Session, params:dict = {}):
        super().__init__(bt_session)

        self.port = 3128
        self.params = params
    
        self.__load_ami()
        super().create_instance(self.ami.get('ImageId'), user_data=self.script, params=self.params)

    ## Private methods

    def __load_ami(self):
        """Search for exact ami id to use based on ami_name property.
        """
        matched_ami = super().get_ami([
            {
                "Name": "name",
                "Values": [self.ami_name] 
            },
            {
                "Name": "owner-alias",
                "Values": ['amazon']
            },
            {
                "Name": "architecture",
                "Values": ['x86_64']
            }
        ])
        assert len(matched_ami.get('Images')) == 1
        self.ami = matched_ami.get('Images')[0]

    def __is_squid_running(self):
        if self.ip is not None and self.port is not None:
            try:
                res = requests.get(f'http://{self.ip}:{self.port}')
                if res.status_code == 400:
                    return True
            except:
                pass
        return False
    
    ## Public methods

    def refresh(self):
        super().refresh()
        if self.status in [ProxyStatus.RUNNING]:
            if self.__is_squid_running() is True:
                self.status = ProxyStatus.READY
            else:
                self.status = ProxyStatus.RUNNING
        elif self.status == ProxyStatus.READY and self.__is_squid_running() is False:
            logger.error('❌ It seems that Squid is not available anymore.')
            self.status = ProxyStatus.MARKED_FOR_DELETION
            self.delete()
            self.wait_until_deleted()

    def wait_until_ready(self, timeout:int = 300):
        self.wait_until_running()

        if self.ip is None:
            logger.error('❌ No public ip found. Deleting the instance.!')
            self.status = ProxyStatus.MARKED_FOR_DELETION
            super().terminate(wait=True)
            return

        logger.info(f'Waiting for proxy {self.ip}:{self.port} to be ready...')
        start_time = datetime.now()
        successful_success = 0
        while datetime.now() < start_time + timedelta(seconds=timeout):
            if self.__is_squid_running() is True:
                successful_success += 1
                if successful_success == 5:
                    self.refresh()
                    return
            else:
                successful_success = 0
            time.sleep(1)
        
        logger.error('❌ Squid was not able to be ready in time! Deleting proxy!')
        self.status = ProxyStatus.MARKED_FOR_DELETION
        super().terminate(wait=True)
     