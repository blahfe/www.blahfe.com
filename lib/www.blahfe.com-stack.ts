import cdk = require("@aws-cdk/core");
import s3deploy = require("@aws-cdk/aws-s3-deployment");

export class WwwBlahfeComStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    new s3deploy.BucketDeployment(this, "DeployWithInvalidation", {
      sources: [s3deploy.Source.asset("./website-dist")],
      destinationBucket: bucket,
      distribution,
      distributionPaths: ["/images/*.png"]
    });
  }
}
