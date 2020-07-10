all: backend frontend-build

TEMPLATES = auth product-mock shoppingcart-service

REGION := $(shell python3 -c 'import boto3; print(boto3.Session().region_name)')
ifndef S3_BUCKET
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
	@echo "Checking if S3 bucket exists s3://$(S3_BUCKET)"
	@aws s3api head-bucket --bucket $(S3_BUCKET) || (echo "bucket does not exist at s3://$(S3_BUCKET), creating it..." ; aws s3 mb s3://$(S3_BUCKET) --region $(REGION))

amplify-deploy:
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
