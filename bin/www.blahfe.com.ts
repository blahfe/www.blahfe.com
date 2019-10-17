#!/usr/bin/env node
import "source-map-support/register";
import cdk = require("@aws-cdk/core");
import { WwwBlahfeComCodepipelineStack } from "../lib/codepipeline-stack";
import { WwwBlahfeComS3deployStack } from "../lib/s3deploy-stack";

const app = new cdk.App();
new WwwBlahfeComCodepipelineStack(app, "WwwBlahfeComCodepipelineStack");
new WwwBlahfeComS3deployStack(app, "WwwBlahfeComS3deployStack");
