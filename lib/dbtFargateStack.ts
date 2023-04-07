import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ApplicationLoadBalancedFargateService } from 'aws-cdk-lib/aws-ecs-patterns'
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as events from 'aws-cdk-lib/aws-events';
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

export class fargateStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props);


  const { projectName } = props
  const auroraSecurityGroupId = cdk.Fn.importValue('AppClusterSecurityGroupId')
  const auroraArn = cdk.Fn.importValue('AuroraClusterArn')
  const datalakeBucketArn = cdk.Fn.importValue('DatalakeBucketArn')

// Create a new task execution role with the required S3 read permissions
const loadTaskRole = new iam.Role(this, 'TaskExecutionRole', {
  assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
});
// Add a policy statement to the role that grants the necessary permissions to access the database
const auroraPolicyStatement = new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  actions: [
    'rds-db:connect'
  ],
  resources: [
    `${auroraArn}/*`
  ]
});

// Add a policy statement to the role that grants permission to ListAllMyBuckets, GetBucketAcl, GetObjectAcl, ListBucket and GetObject on a specific S3 bucket
const s3PolicyStatement = new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  actions: [
    's3:ListAllMyBuckets',
    's3:PutObject',
    's3:GetObjectAcl',
    's3:ListBucket',
    's3:GetObject'
  ],
  resources: [
    `${datalakeBucketArn}/*`
  ]
});

loadTaskRole.addToPolicy(auroraPolicyStatement);
loadTaskRole.addToPolicy(s3PolicyStatement);


  const securityGroup = SecurityGroup.fromSecurityGroupId(this, 'AppSecurityGroup', auroraSecurityGroupId);
    
  const dbtFargateService = new ApplicationLoadBalancedFargateService(this, `${projectName}FlaskFargateService`, {
    assignPublicIp: false,
    taskImageOptions: {
      image: ContainerImage.fromAsset(path.join(__dirname, 'dbt_app'))
    },
    securityGroups:[securityGroup]
  })

    // Create an AWS Fargate service
    const dbtTaskDefinition = new FargateTaskDefinition(this, 'MyTaskDefinition', {
      memoryLimitMiB: 512,
      cpu: 256,
    });

    // Create a CloudWatch Events rule to trigger the scheduled task
    const rule = new events.Rule(this, 'MyScheduledTaskRule', {
      schedule: events.Schedule.cron({ minute: '0', hour: '1' }), // Run the task every day at 1:00 AM UTC
    });

    // Add the Fargate task as a target for the rule
    rule.addTarget(new targets.EcsTask({
      cluster: dbtFargateService.cluster,
      taskDefinition: dbtTaskDefinition
    }));
}
}
