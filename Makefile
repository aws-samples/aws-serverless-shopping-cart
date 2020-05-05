all: backend frontend-build

TEMPLATES = auth product-mock shoppingcart-service

backend: 
	$(MAKE) -C backend build_layers
	$(MAKE) -C backend TEMPLATE=auth
	$(MAKE) -C backend TEMPLATE=product-mock
	$(MAKE) -C backend TEMPLATE=shoppingcart-service

backend-delete:
	$(MAKE) -C backend delete TEMPLATE=auth
	$(MAKE) -C backend delete TEMPLATE=product-mock
	$(MAKE) -C backend delete TEMPLATE=shoppingcart-service

frontend-serve: 
	$(MAKE) -C frontend serve

frontend-build: 
	$(MAKE) -C frontend build

.PHONY: all backend frontend
