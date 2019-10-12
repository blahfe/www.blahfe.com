#!/usr/bin/env node
import "source-map-support/register";
import cdk = require("@aws-cdk/core");
import { WwwBlahfeComStack } from "../lib/www.blahfe.com-stack";

const app = new cdk.App();
new WwwBlahfeComStack(app, "WwwBlahfeComStack");
