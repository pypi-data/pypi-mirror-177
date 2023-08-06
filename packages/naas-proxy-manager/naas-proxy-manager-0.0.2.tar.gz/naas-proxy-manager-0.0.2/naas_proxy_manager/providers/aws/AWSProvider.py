from naas_proxy_manager.classes import *
from naas_proxy_manager.providers.aws import *

import boto3
import pydash
import threading
import copy
from loguru import logger

class AWSProvider(IProxyProvider):

    __proxy_type_rel_map : dict = {
        ProxyType.SQUID : AWSSquidProxy
    }

    proxy_types : AWSProxyType
    bt_session : boto3.Session
    ec2_client : any
    sts_caller_identity : dict

    vpc_id : str
    igw_id : str
    rtb_id : str
    sg_id : str
    subnet_id : str

    lock : threading.Lock

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, aws_region_name: str, ensure_infrastructure:bool = True):
        self.provider = Provider.AWS
        self.proxy_types = AWSProxyType

        self.proxies = []
        self.lock = threading.Lock()

        # Store credentials
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region_name = aws_region_name

        # Create Boto3 Session
        self.bt_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name
        )

        # Create EC2 Client

        self.ec2_client = self.bt_session.client('ec2')

        # Create STS client and store caller identity.
        # This is used to validate that the credentials are valid.
        sts = self.bt_session.client('sts')
        self.sts_caller_identity = sts.get_caller_identity()

        if ensure_infrastructure is True:
            # Deploy needed infrastructure.
            self.__ensure_infrastructure()

    # Private methods

    def __ensure_vpc(self):
        found_vpcs = self.__get_vpcs()
        vpc_id = pydash.get(found_vpcs, '.[0].VpcId', None)
        if vpc_id is None:
            # Let's create a VPC for us.
            logger.debug('Create new VPC for proxy.')
            res = self.ec2_client.create_vpc(
                CidrBlock='10.0.0.0/16',
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'ProxyManager'
                            }
                        ]
                    }
                ]
            )

            vpc_id = pydash.get(res, 'Vpc.VpcId')
        
        logger.debug(f'VPC with id {vpc_id} is going to be used.')
        return vpc_id
        

    def __get_vpcs(self):
        logger.debug('Fetch VPCs named "ProxyManager"')
        return self.ec2_client.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': ['ProxyManager']
                }
            ]
        ).get('Vpcs')
    
    def __ensure_internet_gateway(self):
        igw_id = pydash.get(self.__get_internet_gateways(), '.[0].InternetGatewayId', None)
        if igw_id is None:
            logger.debug(f'Create internet gateway')
            res = self.ec2_client.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType': 'internet-gateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'ProxyManager'
                            },
                        ]
                    },
                ]
            )
            igw_id = pydash.get(res, 'InternetGateway.InternetGatewayId', None)
            if igw_id is not None:
                logger.debug('Internet Gateway successfully created')
            else:
                logger.error('Could not create internet gateway')

        logger.debug(f'Internet Gateway with id {igw_id} is going to be used.')
        return igw_id

    def __get_internet_gateways(self):
        res = self.ec2_client.describe_internet_gateways(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        'ProxyManager',
                    ]
                },
            ]
        )

        return res.get('InternetGateways')

    def __ensure_internet_gateway_attached(self, vpc_id:str, igw_id:str):
        found_igw_id = pydash.get(self.__get_internet_gateways_attached(vpc_id, igw_id), '.[0].InternetGatewayId')
        if found_igw_id is None:
            logger.info(f'Attaching internet gateway {igw_id} to vpc {vpc_id}')
            vpc = self.bt_session.resource('ec2').Vpc(vpc_id)
            res = vpc.attach_internet_gateway(
                InternetGatewayId=igw_id
            )
            if pydash.get(res, 'ResponseMetadata.HTTPStatusCode') != 200:
                print(res)
                raise Exception('❌ Error while attaching internet gateway')
        
        logger.debug(f'Internet Gateway {igw_id} is attached to VPC {vpc_id}.')

        return True


        return igw_id

    def __get_internet_gateways_attached(self, vpc_id:str, igw_id):
        res = self.ec2_client.describe_internet_gateways(
            Filters=[
                {
                    'Name': 'attachment.vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
                {
                    'Name': 'tag:Name',
                    'Values': [
                        "ProxyManager",
                    ] 
                }
            ],
        )

        return res.get('InternetGateways')

    def __ensure_route_to_igw(self, vpc_id:str, igw_id:str):
        route_tables = self.ec2_client.describe_route_tables(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ]
        ).get('RouteTables')

        assert len(route_tables) > 0

        route_table = route_tables[0]
        route_to_igw = pydash.collections.find(route_table['Routes'], lambda x: x['DestinationCidrBlock'] == '0.0.0.0/0' and x['GatewayId'] == igw_id)

        if route_to_igw is None:
            logger.info('Creating route to igw.')
            res = self.ec2_client.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=igw_id,
                RouteTableId=route_table.get('RouteTableId')
            )


            if pydash.get(res, 'ResponseMetadata.HTTPStatusCode') != 200:
                print(res)
                raise Exception('❌ Error while creating route to igw.')
        logger.debug(f'Route 0.0.0.0/0 to internet gateway {igw_id} exists.')

        return route_table.get('RouteTableId')
        

    def __ensure_security_group(self, vpc_id:str):
        sg_id = pydash.get(self.__get_security_group(vpc_id), '.[0].GroupId', None)
        if sg_id is None:
            logger.info('Creating security group for proxy.')
            res = self.ec2_client.create_security_group(
                Description='Security group used for proxies.',
                GroupName='ProxyManager',
                VpcId=vpc_id
            )

            if pydash.get(res, 'ResponseMetadata.HTTPStatusCode') != 200:
                print(res)
                raise Exception('❌ Error while creating security group.')
            sg_id = pydash.get(res, 'GroupId')

        logger.debug(f'Security group {sg_id} is going to be used.')
        
        return sg_id

    def __get_security_group(self, vpc_id:str):
        return self.ec2_client.describe_security_groups(
            Filters=[
                {
                    'Name': 'group-name',
                    'Values': [
                        'ProxyManager',
                    ]
                },
            ]
        ).get('SecurityGroups')


    def __ensure_security_group_rules(self, sg_id:str):
        rules = self.__get_security_group_rules(sg_id)
        rule_found = pydash.collections.find(
            rules,
            lambda x: x['IpProtocol'] == '-1' and pydash.get(x['IpRanges'], '.[0].CidrIp') == '0.0.0.0/0'
        )

        if rule_found is None:
            res = self.ec2_client.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        'IpProtocol': '-1',
                        'IpRanges': [
                            {
                                'CidrIp': '0.0.0.0/0',
                                'Description': 'Allow all traffic from internet.'
                            }
                        ],
                        'FromPort': -1,
                        'ToPort': -1

                    }
                ]
            )

            if pydash.get(res, 'ResponseMetadata.HTTPStatusCode') != 200:
                print(res)
                raise Exception('❌ Error while creating security group rule.')
        logger.debug('Security Group properly configured...')
        return True

    def __get_security_group_rules(self, sg_id:str):
        return pydash.get(self.ec2_client.describe_security_groups(
            GroupIds=[
                sg_id
            ]
        ), '.SecurityGroups[0].IpPermissions')

    def __ensure_subnet(self, vpc_id:str, rtb_id:str):
        subnet_id = pydash.get(self.__get_subnet(vpc_id), '.[0].SubnetId')
        if subnet_id is None:
            logger.debug('Create subnet...')
            res = self.ec2_client.create_subnet(
                VpcId=vpc_id,
                CidrBlock='10.0.0.0/24',
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'ProxyManager'
                            }
                        ]
                    }
                ]
            )

            if pydash.get(res, 'ResponseMetadata.HTTPStatusCode') != 200:
                print(res)
                raise Exception('❌ Error while creating subnet.')
            subnet_id = pydash.get(res, 'Subnet.SubnetId')
        logger.debug(f'Subnet {subnet_id} is going to be used...')
        return subnet_id


    
    def __get_subnet(self, vpc_id:str):
        return self.ec2_client.describe_subnets(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        'ProxyManager',
                    ]
                },
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id
                    ]
                }
            ]
        ).get('Subnets')

    def __ensure_route_table_attached_to_subnet(self, rtb_id:str, subnet_id:str):
        rtbs = self.__get_route_table_attached_to_subnet(rtb_id, subnet_id)

        if len(rtbs) == 0:
            self.__associate_route_table_and_subnet(rtb_id, subnet_id)
        else:
            rtb = rtbs[0]
            association = pydash.collections.find(rtb.get('Associations'), lambda x: pydash.get(x, 'AssociationState.State') == 'associated' and pydash.get(x, 'SubnetId') == subnet_id)
            if association is None or rtb.get('SubnetId') != subnet_id:
                self.__associate_route_table_and_subnet(rtb_id, subnet_id)
                
        return True
    
    def __associate_route_table_and_subnet(self, rtb_id:str, subnet_id:str):
        logger.info(f'Creating Route Table {rtb_id} association with Subnet {subnet_id}')
        
        res = self.ec2_client.associate_route_table(
            RouteTableId=rtb_id,
            SubnetId=subnet_id
        )

        if pydash.get(res, 'ResponseMetadata.HTTPStatusCode') != 200:
            raise Exception(f'❌ Error while creating Route Table {rtb_id} association with Subnet {subnet_id}')
        
    
    def __get_route_table_attached_to_subnet(self, rtb_id:str, subnet_id:str):
        return self.ec2_client.describe_route_tables(
            Filters=[
                {
                    'Name': 'route-table-id',
                    'Values': [
                        rtb_id,
                    ]
                },
                {
                    'Name': 'association.subnet-id',
                    'Values': [
                        subnet_id,
                    ]
                },
            ],
        ).get('RouteTables')


    def __ensure_infrastructure(self):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_vpc
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_internet_gateways
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_internet_gateway
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_route_tables
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_route
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_security_group
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_group_rules
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.authorize_security_group_ingress
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_subnet
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.associate_route_table

        # Make sure VPC exists.
        vpc_id = self.__ensure_vpc()

        # Make sure Internet Gateway exists.
        igw_id = self.__ensure_internet_gateway()

        # Make sure Internet Gateway is attached to VPC.
        self.__ensure_internet_gateway_attached(vpc_id, igw_id)

        # Make sure route table have a route to the internet gateway.
        rtb_id = self.__ensure_route_to_igw(vpc_id, igw_id)

        # Make sure security group exists.
        sg_id = self.__ensure_security_group(vpc_id)

        # Make sure security group has a rule to accept traffic.
        self.__ensure_security_group_rules(sg_id)

        # Make sure subnet exists.
        subnet_id = self.__ensure_subnet(vpc_id, rtb_id)

        # Make sure route table is attached to subnet.
        self.__ensure_route_table_attached_to_subnet(rtb_id, subnet_id)

        self.vpc_id = vpc_id
        self.igw_id = igw_id
        self.rtb_id = rtb_id
        self.sg_id = sg_id
        self.subnet_id = subnet_id


    # Public methods

    def ensure_infrastructure(self):
        self.__ensure_infrastructure()

    def list_proxies(self) -> list:
        raise NotImplementedError
    
    def describe_proxy(self, proxy_id: str) -> dict:
        raise NotImplementedError
    
    def create_proxy(self, proxy_type:AWSProxyType, params:dict = {}) -> IProxy:
        if self.implements_proxy_type(proxy_type) is False:
            raise NotImplementedError
        cls = self.__proxy_type_rel_map[proxy_type]

        p = copy.deepcopy(params)
        p['subnet_id'] = self.subnet_id
        p['sg_ids'] = [self.sg_id] if 'sg_ids' not in p else p['sg_ids'] + self.sg_id

        proxy = cls(self.bt_session, params=p)

        self.lock.acquire()
        self.proxies.append(proxy)
        self.lock.release()

        return proxy

    def delete_proxy(self, proxy_id: str) -> None:
        raise NotImplementedError
    
    def delete_all_proxies(self) -> None:
        raise NotImplementedError
