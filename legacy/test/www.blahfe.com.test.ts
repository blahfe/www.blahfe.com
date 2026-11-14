import {
  expect as expectCDK,
  matchTemplate,
  MatchStyle
} from "@aws-cdk/assert";
import cdk = require("@aws-cdk/core");
import { CodepipelineStack } from "../lib/codepipeline-stack";

describe("CodepipelineStack", () => {
  const app = new cdk.App();
  const stack = new CodepipelineStack(app, "MyTestStack");

  it("should match template", () => {
    expectCDK(stack).to(
      matchTemplate(
        {
          Resources: {}
        },
        MatchStyle.EXACT
      )
    );
  });
});
