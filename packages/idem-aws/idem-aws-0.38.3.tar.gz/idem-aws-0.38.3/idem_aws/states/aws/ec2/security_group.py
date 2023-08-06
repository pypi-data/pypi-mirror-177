"""
State module for managing EC2 Security Groups.

hub.exec.boto3.client.ec2.create_security_group
hub.exec.boto3.client.ec2.delete_security_group
hub.exec.boto3.client.ec2.describe_security_groups
hub.tool.boto3.resource.exec(resource, authorize_egress, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, authorize_ingress, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, create_tags, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, delete, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, revoke_egress, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, revoke_ingress, *args, **kwargs)
"""
import copy
from copy import deepcopy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

TREQ = {
    "present": {"require": ["aws.ec2.vpc.present"]},
    "absent": {
        "require": ["aws.eks.cluster.absent", "aws.ec2.security_group_rule.absent"]
    },
}


async def present(
    hub,
    ctx,
    name: str,
    description: str,
    vpc_id: str,
    resource_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
) -> Dict[str, Any]:
    """Creates a security group.

    A security group acts as a virtual firewall for your instance to control inbound and outbound traffic. For more
    information, see Amazon EC2 security groups in the Amazon Elastic Compute Cloud User Guide and Security groups for
    your VPC in the Amazon Virtual Private Cloud User Guide. When you create a security group, you specify a friendly
    name of your choice. You can have a security group for use in EC2-Classic with the same name as a security group for
    use in a VPC. However, you can't have two security groups for use in EC2-Classic with the same name or two security
    groups for use in a VPC with the same name. You have a default security group for use in EC2-Classic and a default
    security group for use in your VPC. If you don't specify a security group when you launch an instance, the instance
    is launched into the appropriate default security group. A default security group includes a default rule that grants
    instances unrestricted network access to each other. You can add or remove rules from your security groups using
    AuthorizeSecurityGroupIngress, AuthorizeSecurityGroupEgress, RevokeSecurityGroupIngress, and RevokeSecurityGroupEgress.
    For more information about VPC security group limits, see Amazon VPC Limits.

    Args:
        name(str):
            The security group name as set on AWS.

        description(str):
            Description of the security group.

        vpc_id(str):
            Id of the VPC security group should be attached to.

        resource_id(str, Optional):
            AWS Security Group ID.

        tags(Dict or List, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of ``[{"Key": tag-key, "Value": tag-value}]``
            to associate with the security group. Each tag consists of a key name and an associated value. Defaults to None.

            * (Key, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * (Value, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
       .. code-block:: sls

          [security_group_id]:
            aws.ec2.security_group.present:
              - resource_id: 'string'
              - name: 'string'
              - vpc_id: 'string'
              - tags:
                    - Key: 'string'
                      Value: 'string'


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            isolation-securitygroup-84c9a893-844b-40ab-86e8-b565dea88b5d:
              aws.ec2.security_group.present:
                - resource_id: sg-0008bd25b7867b5cf
                - name: isolation-securitygroup-84c9a893-844b-40ab-86e8-b565dea88b5d
                - vpc_id: vpc-247e9a5d
                - description: sg-description
                - tags:
                    - Key: Name
                      Value: sg-name
                    - Key: sg-tag-key-2
                      Value: sg-tag-value-2
    """

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    before = None
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        resource = await hub.tool.boto3.resource.create(
            ctx, "ec2", "SecurityGroup", resource_id
        )
        before = await hub.tool.boto3.resource.describe(resource)
    if before:
        try:
            result[
                "old_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_sg_to_present(before)
            plan_state = copy.deepcopy(result["old_state"])
            old_tags = result["old_state"].get("tags")
            resource_updated = False
            if tags is not None and tags != old_tags:
                update_ret = await hub.tool.aws.ec2.tag.update_tags(
                    ctx,
                    resource_id=resource_id,
                    old_tags=old_tags,
                    new_tags=tags,
                )
                if not update_ret["result"]:
                    result["comment"] = result["comment"] + (update_ret["comment"])
                    result["result"] = update_ret["result"]
                    return result
                result["result"] = result["result"] and update_ret["result"]
                resource_updated = resource_updated or update_ret["result"]
                if ctx.get("test", False) and resource_updated:
                    plan_state["tags"] = update_ret["ret"]
                    result["comment"] = result["comment"] + (
                        f"Would update aws.ec2.security_group {name}",
                    )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)
            result["result"] = False
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "description": description,
                    "vpc_id": vpc_id,
                    "tags": tags,
                },
            )
            result["comment"] = result["comment"] + (
                f"Would create aws.ec2.security_group {name}",
            )
            return result
        try:
            ret = await hub.exec.boto3.client.ec2.create_security_group(
                ctx,
                GroupName=name,
                Description=description,
                VpcId=vpc_id,
                TagSpecifications=[
                    {
                        "ResourceType": "security-group",
                        "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                    }
                ]
                if tags is not None
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = result["comment"] + (ret["comment"])
                return result
            result["comment"] = result["comment"] + (f"Created '{name}'",)
            resource_id = ret["ret"]["GroupId"]

        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            resource = await hub.tool.boto3.resource.create(
                ctx, "ec2", "SecurityGroup", resource_id
            )
            after = await hub.tool.boto3.resource.describe(resource)

            result[
                "new_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_sg_to_present(after)
        else:
            result["new_state"] = deepcopy(result["old_state"])

    except Exception as e:
        result["comment"] = result["comment"] + (str(e),)
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes a security group.

    If you attempt to delete a security group that is associated with an instance, or is referenced by another security
    group, the operation fails with InvalidGroup.InUse in EC2-Classic or DependencyViolation in EC2-VPC.

    Args:
        name(str):
            An Idem name to identify the security group resource.

        resource_id(str, Optional):
            AWS Security Group ID. Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [security_group-resource-id]:
              aws.ec2.security_group.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            sg-0008bd25b7867b5cf:
              aws.ec2.security_group.absent:
                - name: isolation-securitygroup-84c9a893-844b-40ab-86e8-b565dea88b5d
                - resource_id: id: sg-0008bd25b7867b5cf
    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.security_group", name=name
        )
        return result
    resource = await hub.tool.boto3.resource.create(
        ctx, "ec2", "SecurityGroup", resource_id
    )
    before = await hub.tool.boto3.resource.describe(resource)

    if not before:
        result["comment"] = result[
            "comment"
        ] + hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.security_group", name=name
        )
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_sg_to_present(before)
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ec2.security_group", name=name
        )
        return result
    else:
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_sg_to_present(before)
        try:
            ret = await hub.exec.boto3.client.ec2.delete_security_group(
                ctx, GroupId=resource_id
            )
            if not ret["result"]:
                result["comment"] = result["comment"] + (ret["comment"])
                result["result"] = ret["result"]
                return result
            result["comment"] = result["comment"] + (
                f"Deleted aws.ec2.security_group '{name}'",
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["result"] = False
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Describes the specified security groups or all of your security groups. A security group is for use with
    instances either in the EC2-Classic platform or in a specific VPC. For more information, see Amazon EC2 security
    groups in the Amazon Elastic Compute Cloud User Guide and Security groups for your VPC in the Amazon Virtual
    Private Cloud User Guide.


    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.ec2.security_group
    """
    result = {}

    ret = await hub.exec.boto3.client.ec2.describe_security_groups(ctx)
    if not ret["result"]:
        hub.log.debug(f"Could not describe security_group {ret['comment']}")
        return {}

    for security_group in ret["ret"]["SecurityGroups"]:
        translated_security_group = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_sg_to_present(security_group)
        )

        result[security_group.get("GroupId")] = {
            "aws.ec2.security_group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_security_group.items()
            ]
        }
    return result


async def search(
    hub,
    ctx,
    name,
    filters: List = None,
    resource_id: str = None,
    vpc_id: str = None,
    tags: List[Dict[str, Any]] or Dict[str, Any] = None,
):
    """
    Provides details about a specific Security Group as a data-source. Supply one of the inputs as the filter.

    Args:
        name(str):
             The name of the Idem state.

        resource_id(str, Optional):
            Security Group id to identify the resource.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups

        vpc_id(str, Optional):
            Id of the VPC security group attached to.

        tags(list or dict, Optional):
            list of tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
            {tag-key: tag-value} for security group.

    Request Syntax:
       .. code-block:: sls

          [Idem-state-name]:
            aws.ec2.security_group.search:
              - name: 'string'
              - resource_id: 'string'
              - filters:
                - name: 'string'
                  values: 'list'
                - name: 'string'
                  values: 'list'
              - vpc_id: 'string'
              - tags:
                 - Key: 'string'
                   Value: 'string'

    Examples:

        .. code-block:: bash

            idem-test-security-group-search:
              aws.ec2.security_group.search:
                - name: idem-test-security-group
                - filters:
                    - name: 'group-name'
                      values: ["idem-test-security-group"]
                - vpc_id: vpc-247e9a5d
                - tags:
                    - Key: Name
                      Value: sg-name
                    - Key: sg-tag-key-2
                      Value: sg-tag-value-2


    This function has been deprecated.  Please use exec.run with aws.ec2.security_group.get or
    aws.ec2.security_group.list instead.
    """
    hub.log.warning(
        f"aws.ec2.security_group.search '{name}' state has been deprecated. Please use exec.run with"
        "aws.ec2.security_group.get or aws.ec2.security_group.list instead."
    )

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["comment"] = syntax_validation["comment"]
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    if isinstance(tags, Dict):
        tags = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
    if tags:
        for tag in tags:
            boto3_filter.append({"Name": "tag:" + tag["Key"], "Values": [tag["Value"]]})
    if vpc_id:
        boto3_filter.append({"Name": "vpc-id", "Values": [vpc_id]})

    security_groups_args = {}
    if boto3_filter:
        security_groups_args["Filters"] = boto3_filter
    # Including None as GroupIds, throws ParamValidationError for describe_security_groups
    if resource_id:
        security_groups_args["GroupIds"] = [resource_id]

    ret = await hub.exec.boto3.client.ec2.describe_security_groups(
        ctx, **security_groups_args
    )

    if not ret["result"]:
        result["result"] = False
        result["comment"] = ret["comment"]
        return result

    if not ret["ret"]["SecurityGroups"]:
        result["comment"] = (f"Unable to find aws.ec2.security_group '{name}'",)
        return result

    security_group = ret["ret"]["SecurityGroups"][0]
    if len(ret["ret"]["SecurityGroups"]) > 1:
        result["comment"] = (
            f"More than one aws.ec2.security_group resource was found. Use resource {security_group.get('GroupId')}",
        )
    result["old_state"] = hub.tool.aws.ec2.conversion_utils.convert_raw_sg_to_present(
        security_group
    )

    # Populate both "old_state" and "new_state" with the same data
    result["new_state"] = copy.deepcopy(result["old_state"])
    return result
