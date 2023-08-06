import pytest

@pytest.mark.e2e
def test_AWSSquidProxy(aws_access_key_id, aws_secret_access_key, logger):
    from naas_proxy_manager import ProxyManager, AWSProvider, ProxyType

    pxm = ProxyManager()

    logger.info('Configuring provider')    
    pxm.configure_provider('aws-us-east-1', AWSProvider(aws_access_key_id, aws_secret_access_key, 'us-east-1'))
    
    logger.info('Creating proxy')
    proxy = pxm.create_proxy(ProxyType.SQUID)
    
    logger.info('Waiting for proxy to be running')
    proxy.wait_until_running()
    logger.info('Proxy is running')
    
    logger.info('Waiting for proxy to be ready')
    proxy.wait_until_ready()
    logger.info('Proxy is ready')

    logger.info('Waiting for proxy to be deleted')
    proxy.wait_until_deleted()

def test_AWSSquidProxy_ami_exists(bt_session, logger):
    from naas_proxy_manager.providers.aws.AWSEC2Proxy import AWSEC2Proxy

    class DummyClass(AWSEC2Proxy):

        def wait_until_ready(self):
            pass

    aws_ec2_proxy = DummyClass(bt_session)
    amis = aws_ec2_proxy.get_ami(
        [
            {
                "Name": "name",
                "Values": ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20220912"] 
            },
            {
                "Name": "owner-alias",
                "Values": ['amazon']
            },
            {
                "Name": "architecture",
                "Values": ['x86_64']
            }
        ]
    )

    logger.debug(amis.get('Images'))
    assert len(amis.get('Images')) == 1