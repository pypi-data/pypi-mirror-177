import copy
from collections import OrderedDict
from typing import Any
from typing import Dict


async def get(hub, ctx, name) -> Dict[str, Any]:
    """
    Details about the IAM user or role whose credentials are used to call the operation.

    Args:
        name(str): An Idem name of the resource.

    Request Syntax:
        [Idem-resource-state-name]:
          aws.caller_identity.get:
          - name: 'string'

    Examples:

            my-caller-account:
              aws.caller_identity.get:
                - name: value

    Response Syntax:
          {
            name: 'string',
            user_id: 'string',
            account_id: 'string',
            arn: 'string'
          }

    Response Structure:
        name(str): An Idem name of the resource.
        user_id(str): The unique identifier of the calling entity.
        account_id(str): AWS account ID number of the account that owns or contains the calling entity.
        arn(str): AWS ARN associated with the calling entity.

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    ret = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    if not ret["result"]:
        result["result"] = False
        result["comment"] = ret["comment"]
        return result
    resource_parameters = OrderedDict(
        {"UserId": "user_id", "Account": "account_id", "Arn": "arn"}
    )
    resource_translated = {"name": name}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in ret["ret"]:
            resource_translated[parameter_present] = ret["ret"][parameter_raw]
    result["old_state"] = resource_translated
    result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def search(hub, ctx, name) -> Dict[str, Any]:
    """
    Since search() and get() would be functionally the same, display a deprecation message here and call get()
    """
    hub.log.warning(
        f"aws.route53.hosted_zone.search '{name}' state has been deprecated. Please use exec.run with aws.route53.hosted_zone.get instead."
    )
    return await get(hub, ctx, name)
