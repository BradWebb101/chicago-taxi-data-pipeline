import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

interface MyStackProps extends cdk.StackProps {
    projectName: string,
    env: {
        account: string;
        region: string;
    }
}

export class DynamoDBStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props);

    const { projectName } = props

    const dynamoPutLambdaARN = cdk.Fn.importValue('DynamoPutLambdaARN')

    const passedEntriesTable = new dynamodb.Table(this, `${projectName}PassedTable`, {
        tableName:`${projectName}DataTable`,
        partitionKey: { name: 'trip_id', type: dynamodb.AttributeType.STRING },
        billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        });

    const authTable = new dynamodb.Table(this, `${projectName}AuthTable`, {
        tableName:`${projectName}FlaskAuthTable`,
        partitionKey: { name: 'secret_key', type: dynamodb.AttributeType.STRING },
        billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        });

    const failedEntriesTable = new dynamodb.Table(this, `${projectName}FailedTable`, {
        tableName:`${projectName}FailedEntriesTable`,
        partitionKey: { name: 'trip_id', type: dynamodb.AttributeType.STRING },
        billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        });

        passedEntriesTable.grantWriteData(lambda.Function.fromFunctionArn(this, 'dataInLambdaFunction', dynamoPutLambdaARN))
        failedEntriesTable.grantWriteData(lambda.Function.fromFunctionArn(this, 'dynamoPutLambdaFunction', dynamoPutLambdaARN))
    
        // Output the cluster endpoint name
        new cdk.CfnOutput(this, 'DataTableName', {
            value: passedEntriesTable.tableName,
            exportName: 'DataTableName',
        });

        // Output the cluster endpoint name
        new cdk.CfnOutput(this, 'FailedTableName', {
            value: failedEntriesTable.tableName,
            exportName: 'FailedTableName',
        });


  }
}
