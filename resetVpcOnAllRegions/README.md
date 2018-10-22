# Reset VPC and EC2 services from all regions

This Function will reset the EC2 Service in all available regions on the current AWS Account.

## Handler

You can find the whole code in `handler.py`.

### Running
Running the function will return:
```
Response:
{
  "statusCode": 200,
  "instances": {
    "eu-west-1": {
      "LoadBalancer": [
        "api-daam-k8s-ineat-sandbo-cq951a"
      ],
      "AutoScalingGroup": [
        "master-eu-west-1a.masters.daam-k8s.ineat-sandbox.net",
        "nodes.daam-k8s.ineat-sandbox.net"
      ],
      "LaunchConfig": [
        "master-eu-west-1a.masters.daam-k8s.ineat-sandbox.net-20181021172544",
        "nodes.daam-k8s.ineat-sandbox.net-20181021172544"
      ],
      "NetworkACL": [],
      "NetworkInterface": [
        "eni-0f37a6c21be7b1fff"
      ],
      "Instances": [
        "sg-01e45130506b485b0"
      ],
      "Volumes": [
        "vol-0fc551168bf77c770"
      ]
    }
  }
}

Request ID:
"683f7da9-d5dd-11e8-bd5f-653ca2ef50b1"
```

### Response
The response is composed by `statusCode` and `deleted`.

The `deleted` attribute will return you all objects from all regions referenced in the AWS Account linked to the API Key used.

```
{
    "statusCode": ...
    "deleted": {
        region_name: {
            objectType: [
                object_id
            ]
        }
    }
}
```

## Trigger
You need to configure a Trigger Event to schedule the operation. Add a **CloudWatch Events**. 

Let's create a new rule :
* Rule name: `schedule-weekday-1am`
* Rule description: `Run every weekday at 1am`
* Rule type: `Schedule expression`
* Schedule expression: `cron(0 1 ? * MON-FRI *)`
* Enable trigger: `Yes`

Schedule parameters are detailed [here](https://docs.aws.amazon.com/fr_fr/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html)
