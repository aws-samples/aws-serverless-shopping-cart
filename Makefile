all: backend frontend-build

TEMPLATES = auth product-mock shoppingcart-service

ifndef S3_BUCKET
REGION := $(shell python3 -c 'import boto3; print(boto3.Session().region_name)')
ACCOUNT_ID := $(shell aws sts get-caller-identity --query Account --output text)
S3_BUCKET = aws-serverless-shopping-cart-src-$(ACCOUNT_ID)-$(REGION)
endif


backend: create-bucket
	$(MAKE) -C backend TEMPLATE=auth S3_BUCKET=$(S3_BUCKET)
	$(MAKE) -C backend TEMPLATE=product-mock S3_BUCKET=$(S3_BUCKET)
	$(MAKE) -C backend TEMPLATE=shoppingcart-service S3_BUCKET=$(S3_BUCKET)

backend-delete:
	$(MAKE) -C backend delete TEMPLATE=auth
	$(MAKE) -C backend delete TEMPLATE=product-mock
	$(MAKE) -C backend delete TEMPLATE=shoppingcart-service

backend-tests:
	$(MAKE) -C backend tests

create-bucket:
	@echo "Creating S3 bucket if it doesn't already exist: s3://$(S3_BUCKET)"
	$(shell aws s3api head-bucket --bucket ${S3_BUCKET} || aws s3 mb s3://${S3_BUCKET} --region ${REGION})

amplify-deploy: create-bucket
	aws cloudformation deploy \
		--template-file ./amplify-ci/amplify-template.yaml \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides \
			OauthToken=$(GITHUB_OAUTH_TOKEN) \
			Repository=$(GITHUB_REPO) \
			BranchName=$(GITHUB_BRANCH) \
			SrcS3Bucket=$(S3_BUCKET) \
		--stack-name CartApp

frontend-serve: 
	$(MAKE) -C frontend serve

frontend-build: 
	$(MAKE) -C frontend build

.PHONY: all backend backend-delete backend-tests create-bucket amplify-deploy frontend-serve frontend-build
