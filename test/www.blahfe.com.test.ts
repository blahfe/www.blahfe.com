import {
  expect as expectCDK,
  matchTemplate,
  MatchStyle
} from "@aws-cdk/assert";
import cdk = require("@aws-cdk/core");
import WwwBlahfeCom = require("../lib/www.blahfe.com-stack");

test("Empty Stack", () => {
  const app = new cdk.App();
  // WHEN
  const stack = new WwwBlahfeCom.WwwBlahfeComStack(app, "MyTestStack");
  // THEN
  expectCDK(stack).to(
    matchTemplate(
      {
        Resources: {}
      },
      MatchStyle.EXACT
    )
  );
});
