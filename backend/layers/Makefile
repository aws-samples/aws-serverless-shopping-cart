all: build

build:
	@mkdir -p ./build/shared-utils/python/
	@python3 -m pip install --upgrade --isolated --disable-pip-version-check -r ./requirements.txt -t ./build/shared-utils/python/
	@cp *.py ./build/shared-utils/python/

.PHONY: build