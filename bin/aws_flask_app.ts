
import * as cdk from 'aws-cdk-lib';
import { DataInStack } from '../lib/dataInStack'
// import { FlaskFargateStack } from '../lib/flaskFargateStack'
import { DynamoDBStack } from '../lib/dynamoStack'

const app = new cdk.App();

const GLOBALS ={
  projectName:'CFDataPipeline',
  //env: { account: process.env.CDK_DEFAULT_ACCOUNT as string, region: process.env.CDK_DEFAULT_REGION as string}
  env: { account: '209947416217', region: 'eu-central-1'}
}

const dataInStackOut = new DataInStack(app, 'DataInStack', GLOBALS);

const dynamoStackOut = new DynamoDBStack(app, 'DynamoStack', GLOBALS);



//const flaskFargateStackOut = new FlaskFargateStack(app, 'flaskAppStack', GLOBALS);

// const fargateStackOut = new fargateStack(app, 'AwsFlaskAppStack', GLOBALS);

// const fargateStackOut = new fargateStack(app, 'AwsFlaskAppStack', GLOBALS);

// const fargateStackOut = new fargateStack(app, 'AwsFlaskAppStack', GLOBALS);


