MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := serve

# all targets are phony
.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

HOST=http://localhost
PORT=1313

# .env
ifneq ("$(wildcard ./.env)","")
  include ./.env
endif

install: ## Install Python package
	@pip install -r requirements.txt

serve: ## Run server
	@hugo server --bind="0.0.0.0" --baseUrl="${HOST}" --port=${PORT} --buildDrafts --watch

serve-without-draft: ## Run server without draft posts
	@hugo server --watch

fetch-serve: fetch serve ## Fetch contents and serve

build: clean ## Build static html
	@hugo

run: ## Run script
	@python -m app -h

fetch: ## Fetch contents
	@python -m app --fetch

deploy: build ## Deploy on Github Pages
	@git add .
	@git commit -m 'modified'
	@git push

clean: ## Clean old files
	@hugo --cleanDestinationDir
	rm -fr public/*

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
