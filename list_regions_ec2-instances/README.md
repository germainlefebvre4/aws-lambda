# List EC2 Instances from all regions

## Handler

You can find the whole code in `handler.py`.

### Running
Running the function will return:
```
Response:
{
  "statusCode": 200,
  "instances": {
    "eu-central-1": [
      "terminated i-0d810a89f25d9791d"
    ],
    "eu-west-1": [
      "running i-01f4eb1fafc4bcd30"
    ]
  }
}

Request ID:
"d8dad7c8-ce31-11e8-8464-071f039cae1b"
```

### Response
The response is composed by `statusCode` and `instances`.

The `instances` attribute will return you all instances from all regions referenced in the AWS Account linked to the API Key used.

```
{
    "statusCode": ...
    "instances": {
        region_name: [
            instance_state instance_id
        ]
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

