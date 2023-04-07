import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';
import * as s3 from 'aws-cdk-lib/aws-s3'
import * as s3Notifications from 'aws-cdk-lib/aws-s3-notifications';



interface MyStackProps extends cdk.StackProps {
    projectName: string,
    env: {
        account: string;
        region: string;
    }
}

export class DataInStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props);

    const { projectName } = props

    const passedTable = cdk.Fn.importValue('DataTableName')
    const failedTable = cdk.Fn.importValue('FailedTableName')

     // Create a new S3 bucket
     const datalakeBucket = new s3.Bucket(this, `${projectName}Bucket`, {
      bucketName:'cfdatabucket',
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: true, // Enable versioning for the bucket
      encryption: s3.BucketEncryption.S3_MANAGED, // Enable server-side encryption for the bucket
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Automatically delete the bucket when the CloudFormation stack is deleted
      }); 
    
      const dataInLambdaFn = new lambda.Function(this, `${projectName}DataInLambdaFunction`, {
        runtime: lambda.Runtime.PYTHON_3_9,
        handler: 'main.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../', 'data_in')),
      // code: lambda.Code.fromDockerBuild(path.join(__dirname, '../','data_in')),
      timeout: cdk.Duration.minutes(15),
      environment:{
        'S3_DATA_LAKE_BUCKET':datalakeBucket.bucketName
      }
      });

      const fnUrl = dataInLambdaFn.addFunctionUrl()

      const dynamoPutLambda = new lambda.Function(this, `${projectName}DynamoPutLambdaFunction`, {
        runtime: lambda.Runtime.PYTHON_3_9,
        handler: 'main.handler',
        code: lambda.Code.fromAsset(path.join(__dirname, '../', 'dynamo_put')),
        //code: lambda.Code.fromDockerBuild(path.join(__dirname, '../','dynamo_put')),
        timeout: cdk.Duration.minutes(15)
        });

        dynamoPutLambda.addLayers(lambda.LayerVersion.fromLayerVersionArn(this, 'DynamoPutLayer', 'arn:aws:lambda:eu-central-1:209947416217:layer:my_lambda_layer:1'))
        dataInLambdaFn.addLayers(lambda.LayerVersion.fromLayerVersionArn(this, 'DataInLayer', 'arn:aws:lambda:eu-central-1:209947416217:layer:my_lambda_layer:1'))
        
        dynamoPutLambda.addEnvironment('PASSED_VALIDATION_TABLE', passedTable)
        dynamoPutLambda.addEnvironment('FAILED_VALIDATION_TABLE', failedTable)
  
        datalakeBucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3Notifications.LambdaDestination(dynamoPutLambda));

        datalakeBucket.grantWrite(dataInLambdaFn)
        datalakeBucket.grantRead(dynamoPutLambda)

        // Output the cluster endpoint name
        new cdk.CfnOutput(this, 'DynamoPutLambdaARN', {
          value: dynamoPutLambda.functionArn,
          exportName: 'DynamoPutLambdaARN',
      });

    }
  }

