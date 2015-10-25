#!/bin/sh

s3cmd sync \
      --delete-removed \
      --exclude-from ./deploy.exclude \
      ../src/ s3://www.blahfe.com/
