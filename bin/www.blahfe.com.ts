#!/usr/bin/env node
import "source-map-support/register";
import cdk = require("@aws-cdk/core");
import { CodepipelineStack } from "../lib/codepipeline-stack";
import { S3deployStack } from "../lib/s3deploy-stack";

const app = new cdk.App();
new CodepipelineStack(app, "CodepipelineStack");
new S3deployStack(app, "S3deployStack");
