# platform/desktop/Makefile
#
# This file is Copyright 2007, 2009 Dean Hall.
# Copyright 2012 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

# PyMite Configuration
PLATFORM := $(notdir $(CURDIR))
PM_LIB_ROOT = pmvm_$(PLATFORM)
PM_LIB_FN = lib$(PM_LIB_ROOT).a
PM_LIB_PATH = ../../vm/$(PM_LIB_FN)
PM_USR_SOURCES = main.py build.py
PM_HEAP_SIZE = 0x2000
PMIMGCREATOR := ../../tools/owl-tools/pmImgCreator.py
IPM = true
DEBUG = true

# invoke pmFeatures to get list of defines
FEATURES := $(shell ../../tools/build/pmFeatures.py .)

TARGET = main
SOURCES = $(TARGET).c plat.c $(TARGET)_nat.c $(TARGET)_img.c
OBJS = $(SOURCES:.c=.o)

ifeq ($(DEBUG),true)
	CDEFS += -g -ggdb -D__DEBUG__=1
endif
CINCS = -I$(abspath .) -I/usr/include/i686-linux-gnu
CFLAGS  = -Wall -Wextra -Werror
CFLAGS += -Wno-unused-parameter -Wstrict-prototypes -Wdeclaration-after-statement
CFLAGS += -Wpointer-arith -Wredundant-decls
CFLAGS += -Wnested-externs 
CFLAGS += -Wmissing-prototypes -Wmissing-declarations
CFLAGS += -fno-strict-aliasing -ffunction-sections -fdata-sections
CFLAGS += -m32 -I../../vm $(CDEFS) $(CINCS)
CFLAGS += $(FEATURES)

PYTHON ?= python2.7

export CFLAGS IPM PM_LIB_FN PYTHON

.PHONY: all clean $(PM_LIB_PATH)

all : $(TARGET).out $(PM_LIB_PATH)

# Added to clean up output, used to use default rules
%.o: %.c
	@echo "  GCC   ${<}"
	@$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ $<

$(PM_LIB_PATH) : ../../vm/*.c ../../vm/*.h
	make -C ../../vm

$(TARGET).out : $(OBJS) $(PM_LIB_PATH)
	@echo " LINKING    ${@}"
	@$(CC) -o $@ $(OBJS) $(PM_LIB_PATH) -lm -m32 -lffi -lpthread

# Generate native code and module images from the python source
$(TARGET)_nat.c $(TARGET)_img.c: $(PM_USR_SOURCES)
	@$(PYTHON) $(PMIMGCREATOR) -c -u -o $(TARGET)_img.c --native-file=$(TARGET)_nat.c $(PM_USR_SOURCES)

clean :
	$(MAKE) -C ../../vm clean
	$(RM) $(TARGET).out $(OBJS) $(TARGET)_img.* $(TARGET)_nat.*
