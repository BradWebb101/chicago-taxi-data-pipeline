import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ApplicationLoadBalancedFargateService } from 'aws-cdk-lib/aws-ecs-patterns'
import { ContainerImage, FargateTaskDefinition, NetworkMode } from 'aws-cdk-lib/aws-ecs'
import { SecurityGroup } from 'aws-cdk-lib/aws-ec2'
import * as iam from 'aws-cdk-lib/aws-iam'
import * as path from 'path'

interface MyStackProps extends cdk.StackProps {
  projectName: string,
  env: {
    account: string;
    region: string;
},
app_token_secret_name:string;
}

export class FlaskFargateStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props);

  const { projectName } = props

  // Create an AWS Fargate service
  const flaskTaskDefinition = new FargateTaskDefinition(this, 'MyTaskDefinition', {
    memoryLimitMiB: 512,
    cpu: 256, 
  });
    
  const flaskFargateService = new ApplicationLoadBalancedFargateService(this, `${projectName}FlaskFargateService`, {
    assignPublicIp: true,
    taskImageOptions: {
      image: ContainerImage.fromAsset(path.join(__dirname, '../','test_app'))
    },
    desiredCount:1
  });
  flaskTaskDefinition
}
}
