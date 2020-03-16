.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

list-images:
	python3 make_utils.py --list-images

build:
	python3 make_utils.py --build $(filter-out $@,$(MAKECMDGOALS))
%:
	@:

push:
	python3 make_utils.py --push $(filter-out $@,$(MAKECMDGOALS))
%:
	@:
