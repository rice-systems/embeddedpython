# Tools configuration
SHELL = /bin/sh
CP := cp
MKDIR := mkdir -p
PMTYPES := src/tools/build/pmMakeTypes.py
PMCONSTS := src/tools/build/pmMakeConstStrings.py

pathsearch = $(firstword $(wildcard $(addsuffix /$(1),$(subst :, ,$(PATH)))))

VPATH := . src/vm src/lib docs/src

# Default target
PLATFORM ?= desktop

.PHONY: all vm ipm clean types consts

all :
	$(MAKE) -C src/platform/$(PLATFORM)

ipm :
	$(MAKE) -C src/platform/desktop all
	cd src/tools/owl-tools && ./owl

types :
	python2.7 $(PMTYPES) src/vm/obj.h > src/lib/types.py
	cp src/lib/types.py src/tools/user/pmTypes.py

consts :
	python2.7 $(PMCONSTS) src/tools/strings
	mv consts.h src/vm
	mv __consts.py src/lib

# Removes all files created during default make
clean :
	$(MAKE) -C src/platform/$(PLATFORM) clean

# Remove files made by html / dox
html-clean :
	$(RM) -rf docs/html
