#!/bin/bash

set -ex

gcloud app deploy app.yaml --project=$PROJECT_NAME --quiet
