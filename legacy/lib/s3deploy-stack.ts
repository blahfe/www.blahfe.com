import cdk = require("@aws-cdk/core");
import s3 = require("@aws-cdk/aws-s3");
import s3deploy = require("@aws-cdk/aws-s3-deployment");

export class WwwBlahfeComS3deployStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const projectName: string = this.node.tryGetContext("project");

    new s3deploy.BucketDeployment(this, "s3deploy", {
      sources: [s3deploy.Source.asset("website-dist")],
      destinationBucket: s3.Bucket.fromBucketName(this, projectName, projectName)
    });
  }
}
