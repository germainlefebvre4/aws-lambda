import json
import boto3
from boto3.session import Session


def lambda_handler(event, context):
    API_KEY="AKIAIMVH7P7R4ZNNBCRA"
    API_PWD="ilXtbPWO4MqILOlpdCzItm7b0Nyki8zdgLC/h8nn"
    
    deleted = {}

    session = boto3.Session(aws_access_key_id=API_KEY,
                            aws_secret_access_key=API_PWD)
    
    regions = session.get_available_regions(service_name='ec2')
    regions = ["eu-west-1"]
    
    for region_name in regions:
        deleted[region_name] = {}
        
        # Browse LoadBalancer items
        elbc = boto3.client('elb', region_name=region_name,
                            aws_access_key_id=API_KEY,
                            aws_secret_access_key=API_PWD)
        print(elbc.describe_load_balancers())
        elbs = elbc.describe_load_balancers().get('LoadBalancerDescriptions')
        if len(elbs) > 0:
            deleted[region_name]["LoadBalancer"] = []
        for elb in elbs:
            elb_name = elb.get('LoadBalancerName')
            elb_dns = elb.get('DNSName')
            deleted[region_name]["LoadBalancer"].append(elb_name)
            #elbc.delete_load_balancer(LoadBalancerName=elb_name)
        del elbc
        
        
        # Browse LoadBalancerV2 items
        elbv2c = boto3.client('elbv2', region_name=region_name,
                            aws_access_key_id=API_KEY,
                            aws_secret_access_key=API_PWD)
        elbs = elbv2c.describe_load_balancers().get('LoadBalancers')
        if len(elbs) > 0:
            deleted[region_name]["LoadBalancerV2"] = []
        for elb in elbs:
            elb_name = elb.get('LoadBalancerName')
            elb_arn = elb.get('LoadBalancerArn')
            elb_dns = elb.get('DNSName')
        
            # Listeners
            elb_lsn = elbv2c.describe_listeners(LoadBalancerArn=elb_arn).get('Listeners')
            for tg in elb_lsn:
                lsn_name = tg.get('ListenerName')
                lsn_arn = tg.get('ListenerArn')
                deleted[region_name]["LoadBalancerV2Listener"].append(lsn_name)
                #elbv2c.delete_listener(ListenerArn=lsn_arn)
        
            # Target Groups
            elb_tg = elbv2c.describe_target_groups(LoadBalancerArn=elb_arn).get('TargetGroups')
            for tg in elb_tg:
                tg_name = tg.get('TargetGroupName')
                tg_arn = tg.get('TargetGroupArn')('     Target Group %s...' % tg_name)
                deleted[region_name]["LoadBalancerV2TargetGroup"].append(tg_name)
                #elbv2c.delete_target_group(TargetGroupArn=tg_arn)

            deleted[region_name]["LoadBalancerV2"].append(elb)
            #elbv2c.delete_load_balancer(LoadBalancerArn=elb_arn)

    # Standalone entities
    # Browse Target Groups
    tgs = elbv2c.describe_target_groups().get('TargetGroups')
    if len(tgs) > 0:
        deleted[region_name]["LoadBalancerTargetGroup"] = []
    for tg in tgs:
        tg_name = tg.get('TargetGroupName')
        tg_arn = tg.get('TargetGroupArn')
        deleted[region_name]["LoadBalancerTargetGroups"].append(elb)
        #elbv2c.delete_target_group(TargetGroupArn=tg_arn)
    del elbv2c
    
    
    # Browse Auto Scaling
    ascac = boto3.client('autoscaling', region_name=region_name,
                            aws_access_key_id=API_KEY,
                            aws_secret_access_key=API_PWD)
    asgs = ascac.describe_auto_scaling_groups().get('AutoScalingGroups')
    if len(asgs) > 0:
        deleted[region_name]["AutoScalingGroup"] = []
    for asg in asgs:
        asg_name = asg.get('AutoScalingGroupName')
        asg_arn = asg.get('AutoScalingGroupArn')
        deleted[region_name]["AutoScalingGroup"].append(asg_name)
        #ascac.delete_auto_scaling_group(AutoScalingGroupName=asg_name, ForceDelete=True)
    
    # Browse Launch Configuration
    ascac = boto3.client('autoscaling', region_name=region_name,
                            aws_access_key_id=API_KEY,
                            aws_secret_access_key=API_PWD)
    lncs = ascac.describe_launch_configurations().get('LaunchConfigurations')
    if len(lncs)>0:
        deleted[region_name]["LaunchConfig"] = []
    for lnc in lncs:
        lnc_name = lnc.get('LaunchConfigurationName')
        lnc_arn = lnc.get('LaunchConfigurationArn')
        deleted[region_name]["LaunchConfig"].append(lnc_name)
        #ascac.delete_launch_configuration(LaunchConfigurationName=lnc_name)


    # Browse EC2 Instances
    ec2c = boto3.client('ec2', region_name=region_name,
                            aws_access_key_id=API_KEY,
                            aws_secret_access_key=API_PWD)
    nacls = ec2c.describe_network_acls().get('NetworkAcls')
    if len(nacls) > 0:
        deleted[region_name]["NetworkACL"] = []
    for nacl in nacls:
        if not nacl.get('IsDefault'):
            nacl_id = nacl.get('NetworkAclId')
            nacl_name = nacl.get('NetworkAclName')
            deleted[region_name]["NetworkACL"].append(nacl_id)
            #ec2c.delete_network_acl(NetworkAclId=nacl_id)

    # Browse Network interfaces
    nics = ec2c.describe_network_interfaces().get('NetworkInterfaces')
    if len(nics) > 0:
        deleted[region_name]["NetworkInterface"] = []
    for nic in nics:
        nic_id = nic.get('NetworkInterfaceId')
        #deleted[region_name]["NetworkInterface"].append(nic_id)
        #ec2c.delete_network_interface(NetworkInterfaceId=nic_id)

    # Browse EC2 Instances
    reservs = ec2c.describe_instances().get('Reservations')
    for reserv in reservs:
        insts = reserv.get('Instances')
        if len(insts) > 0:
            deleted[region_name]["Instances"] = []
        for inst in insts:
            inst_state = inst.get('State').get('Name')
            if inst_state not in    ["shutting-down", "terminated"]:
                inst_id = inst.get('InstanceId')
                deleted[region_name]["Instances"].append(inst_id)
                #ec2c.terminate_instances(InstanceIds=[inst_id])


    # Browse Security Groups
    sgs = ec2c.describe_security_groups().get('SecurityGroups')
    if len(sgs) > 0:
        deleted[region_name]["Instances"] = []
    for sg in sgs:
        if not sg.get('GroupName') == "default":
            sg_id = sg.get('GroupId')
            sg_name = sg.get('GroupName')
            deleted[region_name]["Instances"].append(sg_id)
            #ec2c.delete_security_group(GroupId=sg_id)
    del sgs
    
    # Browse Volumes
    vols = ec2c.describe_volumes().get('Volumes')
    if len(vols) > 0:
        deleted[region_name]["Volumes"] = []
    for vol in vols:
        vol_id = vol.get('VolumeId')
        vol_name = vol.get('VolumeName') if vol.get('VolumeName') else vol.get('VolumeId')
        deleted[region_name]["Volumes"].append(vol_id)
        #ec2c.delete_volume(VolumeId=vol_id)
    del vols



    return {
        "statusCode": 200,
        "instances": deleted
    }
