all: build

serve:
	yarn install
	yarn fetchConfig
	yarn serve

build:
	yarn install
	yarn fetchConfig prod
	yarn build

.PHONY: build serve
