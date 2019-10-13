import cdk = require("@aws-cdk/core");
import codepipeline = require("@aws-cdk/aws-codepipeline");
import codepipeline_actions = require("@aws-cdk/aws-codepipeline-actions");
import codebuild = require("@aws-cdk/aws-codebuild");

export class CodepipelineStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    let stageName: string = "prod";
    if (this.node.tryGetContext("stage") !== undefined) {
      stageName = this.node.tryGetContext("stage");
    }
    const projectName: string = this.node.tryGetContext("project");
    const ownerName: string = this.node.tryGetContext("owner");
    const awsAccessKeyId: string = cdk.SecretValue.secretsManager(projectName, {
      jsonField: "aws-access-key-id"
    }).toString();
    const awsSecretAccessKey: string = cdk.SecretValue.secretsManager(projectName, {
      jsonField: "aws-secret-access-key"
    }).toString();
    const region: string = cdk.SecretValue.secretsManager(projectName, {
      jsonField: "region"
    }).toString();
    const pipeline = new codepipeline.Pipeline(this, "pipeline", {
      pipelineName: `${projectName}-${stageName}`
    });
    const sourceOutput = new codepipeline.Artifact();

    pipeline.addStage({
      stageName: "Source",
      actions: [
        new codepipeline_actions.GitHubSourceAction({
          actionName: "GitHub_Source",
          owner: ownerName,
          repo: projectName,
          oauthToken: cdk.SecretValue.secretsManager(projectName, { jsonField: "github-token" }),
          output: sourceOutput,
          branch: "feature/aws-codepipeline-actions",
          trigger: codepipeline_actions.GitHubTrigger.POLL
        })
      ]
    });

    pipeline.addStage({
      stageName: "Build",
      actions: [
        new codepipeline_actions.CodeBuildAction({
          actionName: "NpmAndS3deploy_Build",
          project: new codebuild.PipelineProject(this, projectName, {
            environment: {
              buildImage: codebuild.LinuxBuildImage.UBUNTU_14_04_NODEJS_10_1_0,
              privileged: true
            },
            buildSpec: codebuild.BuildSpec.fromObject({
              version: "0.2",
              phases: {
                install: { commands: ["npm install"] },
                pre_build: {
                  commands: [
                    "mkdir ~/.aws",
                    `cat <<EOF >~/.aws/credentials
[default]
aws_access_key_id = ${awsAccessKeyId}
aws_secret_access_key = ${awsSecretAccessKey}
EOF`,
                    `cat <<EOF >~/.aws/config
[default]
region = ${region}
EOF`
                  ]
                },
                build: { commands: ["npm run build"] },
                post_build: {
                  commands: ["npm run cdk deploy -v S3deployStack --require-approval=never"]
                }
              }
            })
          }),
          input: sourceOutput
        })
      ]
    });
  }
}
