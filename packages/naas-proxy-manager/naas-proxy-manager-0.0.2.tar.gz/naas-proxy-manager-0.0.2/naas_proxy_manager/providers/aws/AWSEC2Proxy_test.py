import pytest
import boto3

def test_AWSEC2Proxy_get_ami(bt_session, logger):
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

    logger.debug(amis)
    assert len(amis.get('Images')) > 0

