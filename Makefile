all: backend frontend-build

TEMPLATES = auth product-mock shoppingcart-service

backend: 
	$(MAKE) -C backend TEMPLATE=auth
	$(MAKE) -C backend TEMPLATE=product-mock
	$(MAKE) -C backend TEMPLATE=shoppingcart-service

backend-delete:
	$(MAKE) -C backend delete TEMPLATE=auth
	$(MAKE) -C backend delete TEMPLATE=product-mock
	$(MAKE) -C backend delete TEMPLATE=shoppingcart-service

backend-tests:
	$(MAKE) -C backend tests

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

.PHONY: all backend frontend
