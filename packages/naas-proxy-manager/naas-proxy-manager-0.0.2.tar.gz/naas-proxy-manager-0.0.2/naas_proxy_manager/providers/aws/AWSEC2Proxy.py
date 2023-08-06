from naas_proxy_manager.classes import *

import boto3
from loguru import logger

class AWSEC2Proxy(IProxy):
    bt_session : boto3.Session
    ec2_client : boto3.session.Session.client
    ec2_resource : any
    instance:dict
    instance_id : str

    def __init__(self, bt_session : boto3.Session):
        super().__init__()
        self.bt_session = bt_session
        self.ec2_client = self.bt_session.client('ec2')
        self.ec2_resource = self.bt_session.resource('ec2')

        self.instance = None
        self.instance_id = None

    def get_ami(self, filters:list):
        ami = self.ec2_client.describe_images(Filters=filters)
        return ami
    
    def get_instance_state(self):
        return self.instance.state.get('Name')

    def create_instance(self, ami_id: str, user_data:str = None, params:dict = {}):
        # Load params
        instance_type = params.get('instance_type', 't3.micro')
        key_name = params.get('key_name', None)
        extra_tags = params.get('extra_tags', [])
        sg_ids = params.get('sg_ids', [])
        subnet_id = params.get('subnet_id', None)

        logger.info(f'Creating EC2 instance...')

        instances = self.ec2_resource.create_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            UserData=user_data,
            #KeyName=key_name,
            NetworkInterfaces=[{
                "AssociatePublicIpAddress": True,
                "DeleteOnTermination": True,
                "DeviceIndex": 0,
                "SubnetId": subnet_id,
                "Groups": sg_ids
            }],
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [
                    {
                        "Key": "Name",
                        "Value": "ProxyManager"
                    }
                ] + extra_tags
            }]
        )
        self.instance = instances[0]

        self.status = ProxyStatus.STARTING

        logger.info('EC2 instance created...')

        return self.instance
    
    def refresh(self):
        logger.debug('Refreshing EC2 instance state...')
        self.instance.reload()
        ec2_instance_state = self.get_instance_state()
        if self.status == ProxyStatus.STARTING and ec2_instance_state == 'running':
            self.status = ProxyStatus.RUNNING
        self.ip = self.instance.public_ip_address

    def wait_until_running(self):
        logger.info('Waiting for EC2 instance to be running...')
        error = self.instance.wait_until_running()
        if error is not None:
            logger.error('❌ We got an error while waiting for the EC2 instance to be running')
        self.refresh()

    def delete(self):
        logger.info('Terminating EC2 instance...')
        self.instance.terminate()
        self.status = ProxyStatus.DELETING

    def wait_until_deleted(self):
        if self.status is not ProxyStatus.DELETING:
            self.delete()
        logger.info('Waiting for instance to be terminated...')
        error = self.instance.wait_until_terminated()
        if error is not None:
            logger.error('❌ We got an error while waiting for the EC2 instance to be deleted')
            return
        self.status = ProxyStatus.DELETED
        logger.info('EC2 instance successfully deleted...')
