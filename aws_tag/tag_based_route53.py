import boto3

Zone_ID = <>
Zone_DN = <>

ec2client = boto3.client('ec2')
route53client = boto3.client('route53')

def list_instances_by_tag_value(tagkey, tagvalue):
    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+tagkey,
                'Values': [tagvalue]
            }
        ]
    )
    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            if instance.get(u'PublicIpAddress') is not None:
                instancelist.append({"Value":instance.get(u'PublicIpAddress')})
    return instancelist


# print(list_instances_by_tag_value('Name', 'sre-candidate'))

def push_IP_to_zone(ip_list=list_instances_by_tag_value('Name', 'sre-candidate')):
    response = route53client.change_resource_record_sets(
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': 'udp.' + Zone_DN,
                        'ResourceRecords': ip_list,
                    'TTL': 60,
                    'Type': 'A',
                },
            },
        ],
        'Comment': 'Ketan Patel',
        },
        HostedZoneId = Zone_ID,
    )
    return(response)

print(push_IP_to_zone())
