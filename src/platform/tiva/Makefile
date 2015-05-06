# Hey Emacs, this is a -*- makefile -*-
#
# WinARM template makefile 
# by Martin Thomas, Kaiserslautern, Germany 
# <eversmith@heizung-thomas.de>
#
# based on the WinAVR makefile written by Eric B. Weddington, Jörg Wunsch, et al.
# Released to the Public Domain
#
#
# On command line:
#
# make all = Make software.
# make clean = Clean out built project files.
# To rebuild project do "make clean" then "make all".
#
# Changelog:
# - 17. Feb. 2005  - added thumb-interwork support (mth)
# - 28. Apr. 2005  - added C++ support (mth)
# - 29. Arp. 2005  - changed handling for lst-Filename (mth)
# -  1. Nov. 2005  - exception-vector placement options (mth)
# - 15. Nov. 2005  - added library-search-path (EXTRA_LIB...) (mth)
# -  2. Dec. 2005  - fixed ihex and binary file extensions (mth)
# - 22. Feb. 2006  - added AT91LIBNOWARN setting (mth)
# - 19. Apr. 2006  - option FLASH_TOOL (default lpc21isp); variable IMGEXT (mth)
# - 23. Jun. 2006  - option USE_THUMB_MODE -> THUMB/THUMB_IW
# -  3. Aug. 2006  - added -ffunction-sections -fdata-sections to CFLAGS
#                    and --gc-sections to LDFLAGS. Only available for gcc 4 (mth)
# -  4. Aug. 2006  - pass SUBMDL-define to frontend (mth)
# - 11. Nov. 2006  - FLASH_TOOL-config, TCHAIN-config (mth)
# - 28. Mar. 2007  - remove .dep-Directory with rm -r -f and force "no error"
# - 24. Aprl 2007  - added "both" option for format (.bin and .hex)

include Makefile.local

# PyMite Configuration
PLATFORM := $(notdir $(CURDIR))
PM_LIB_ROOT = pmvm_$(PLATFORM)
PM_LIB_FN = lib$(PM_LIB_ROOT).a
PM_LIB_PATH = ../../vm/$(PM_LIB_FN)
PM_USR_SOURCES = main.py  
PM_USR_SOURCES +=  build.py

LIB_TYPE = TIVAWARE

# TivaWare will require its own copy of the peripheral library
PM_USR_SOURCES += autowrapped-tivaware/adc.py autowrapped-tivaware/gpio.py autowrapped-tivaware/i2c.py autowrapped-tivaware/interrupt.py autowrapped-tivaware/pwm.py autowrapped-tivaware/sysctl.py autowrapped-tivaware/uart.py
PM_USR_SOURCES += autowrapped-tiva/sysctl.py autowrapped-tiva/simplegpio.py lib/spi.py 

#PM_USR_SOURCES += ip/ip.py
PMIMGCREATOR := ../../tools/owl-tools/pmImgCreator.py
PMBUILDINFO := ../../tools/build/pmBuildInfo.py
IPM := true
COMPILER = gcc

# MCU name and submodel
MCU      = cortex-m4
USE_THUMB_MODE = YES

# Float
FPU = -mfpu=fpv4-sp-d16 -mfloat-abi=hard

## Create ROM-Image (final)
RUN_MODE=ROM_RUN
## Create RAM-Image (debugging) - not used in this example
#RUN_MODE=RAM_RUN

# Target file name (without extension).
TARGET = main

# List C source files here. 
SRC  = $(TARGET).c $(TARGET)_nat.c $(TARGET)_img.c
SRC += interrupts.c plat_tm4c.c usb/plat_usb.c

# include the FFI source
SRC += ffi/ffi_arm.c
SRC += ffi/prep_cif.c
SRC += ffi/types.c

# We need to include the uIP stuff here, because it gets compiled
# using our local uip-conf.h
#SRC += ip/uip/uip.c
#SRC += ip/ip.c 
#SRC += ip/uip/uip_arp.c
#SRC += ip/uip/uip_timer.c
#SRC += ip/uip/dhcpc.c

# List Assembler source files here.
ASRC = ffi/ffi_arm_asm.S

# Optimization level, can be [0, 1, 2, 3, s]. 
# 0 = turn off optimization. s = optimize for size.
# (Note: 3 is not always the best optimization level. See avr-libc FAQ.)
OPT = s
#OPT = 0
#OPT = 2

# Debugging format.
# Native formats for AVR-GCC's -g are stabs [default], or dwarf-2.
# AVR (extended) COFF requires stabs, plus an avr-objcopy run.
#DEBUG = stabs
DEBUG = true
DEBUG_FMT = dwarf-2

# List any extra directories to look for include files here.
#     Each directory must be seperated by a space.
EXTRAINCDIRS = $(abspath .) ../../vm $(TIVABASE) usb lib $(abspath .)/ffi

# List any extra directories to look for library files here.
#     Each directory must be seperated by a space.
EXTRA_LIBDIRS  = . ../../vm 


EXTRA_LIBDIRS += $(LIBOPENCM3BASE)/lib

# Compiler flag to set the C Standard level.
# c89   - "ANSI" C
# gnu89 - c89 plus GCC extensions
# c99   - ISO C99 standard (not yet fully implemented)
# gnu99 - c99 plus GCC extensions
CSTANDARD = -std=gnu99

# Place -D or -U options for C here
CDEFS =  -D$(RUN_MODE)
# PyMite CDEFS
ifeq ($(DEBUG),true)
	CDEFS += -g -g$(DEBUG_FMT) -D__DEBUG__=1
endif

# Place -D or -U options for ASM here
ADEFS =  -D$(RUN_MODE)

# Compiler flags.

ifeq ($(USE_THUMB_MODE),YES)
THUMB    = -mthumb
#THUMB_IW = -mthumb-interwork
THUMB_IW = 
else 
THUMB    = 
THUMB_IW = 
endif

#  -g*:          generate debugging information
#  -O*:          optimization level
#  -f...:        tuning, see GCC manual and avr-libc documentation
#  -Wall...:     warning level
#  -Wa,...:      tell GCC to pass this to the assembler.
#    -adhlns...: create assembler listing
#
# Flags for C and C++ (arm-elf-gcc/arm-elf-g++)
CFLAGS  = $(CDEFS) 
CFLAGS += -O$(OPT)
#CFLAGS += -Wcast-align
CFLAGS += -Wall -Wextra
CFLAGS += -Wno-unused-parameter -Wstrict-prototypes -Wdeclaration-after-statement
CFLAGS += -Wpointer-arith -Wredundant-decls
CFLAGS += -Wnested-externs
CFLAGS += -Wmissing-prototypes -Wmissing-declarations
CFLAGS += -fno-strict-aliasing -ffunction-sections -fdata-sections
CFLAGS += -DPART_${SUBMDL} -D${COMPILER} $(CSTANDARD)
CFLAGS += $(FPU)

ifeq ($(SUBMDL), TM4C129XNCZAD)
CFLAGS += -DTARGET_IS_SNOWFLAKE_RA0
endif

ifeq ($(SUBMDL), TM4C1294NCPDT)
CFLAGS += -DTARGET_IS_SNOWFLAKE_RA0
endif

CFLAGS += $(patsubst %,-I%,$(EXTRAINCDIRS))

# parse the features files
FEATURES := $(shell ../../tools/build/pmFeatures.py .)
CFLAGS += $(FEATURES)

# Assembler flags.
#  -Wa,...:    tell GCC to pass this to the assembler.
#  -ahlns:     create listing
#  -g$(DEBUG_FMT): have the assembler create line number information
ASFLAGS  = $(ADEFS) 
ifeq ($(DEBUG),true)
	ASFLAGS += -Wa,--g$(DEBUG_FMT)
endif

#Additional libraries.

# Extra libraries
#    Each library-name must be seperated by a space.
#    To add libxyz.a, libabc.a and libefsl.a: 
#    EXTRA_LIBS = xyz abc efsl
EXTRA_LIBS = $(PM_LIB_ROOT)

EXTRA_LIBDIRS += $(TIVABASE)/driverlib/gcc
EXTRA_LIBDIRS += $(TIVABASE)/usblib/gcc
EXTRA_LIBS += usb
EXTRA_LIBS += driver
EXTRA_LIBS += opencm3_lm4f
EXTRA_LIBS += m

# Linker flags.
#  -Wl,...:     tell GCC to pass this to linker.
#    -Map:      create map file
#    --cref:    add cross reference to  map file
LDFLAGS = -Wl,-Map=$(TARGET).map,--cref
LDFLAGS = -Wl,-Map=$(TARGET).map,--cref,--gc-sections
LDFLAGS += -nostartfiles 
#LDFLAGS += -lc -lgcc 
LDFLAGS += $(patsubst %,-L%,$(EXTRA_LIBDIRS))
LDFLAGS += $(patsubst %,-l%,$(EXTRA_LIBS))
LDFLAGS += -mcpu=$(MCU) $(THUMB)
LDFLAGS += $(FPU)

# force the linker script from codesourcery
LDFLAGS += -Tld_scripts/$(LINKERSCRIPT)

# Define programs and commands.
SHELL = sh
CC = ccache $(TCHAIN)-gcc
AR = $(TCHAIN)-ar
OBJCOPY = $(TCHAIN)-objcopy
OBJDUMP = $(TCHAIN)-objdump
SIZE = $(TCHAIN)-size
NM = $(TCHAIN)-nm
AR = $(TCHAIN)-ar
LD = $(TCHAIN)-ld
REMOVE = rm -f
REMOVEDIR = rm -f -r
COPY = cp

# Define Messages
# English
MSG_BEGIN = "-------- begin (mode: $(RUN_MODE)) --------"
MSG_END = "--------  end  --------"
MSG_COMPILER = "Compiler:"
MSG_SIZE = "Size:"

# Define all object files.
COBJ      = $(SRC:.c=.o) 
AOBJ      = $(ASRC:.S=.o)

# Combine all necessary flags and optional flags.
# Add target processor to flags.
ALL_CFLAGS  = -mcpu=$(MCU) $(THUMB) $(THUMB_IW) -I. $(CFLAGS)
ALL_ASFLAGS = -mcpu=$(MCU) $(THUMB) $(THUMB_IW) -I. -x assembler-with-cpp $(ASFLAGS)

# Default target.
all: begin pmvm build sizeafter gccversion end

# PyMite: Build the VM archive if it doesn't exist
pmvm : $(PM_LIB_PATH)

$(PM_LIB_PATH) :
	make -C ../../vm

# Actual binary
build: axf bin
axf: $(TARGET).axf
bin: $(TARGET).bin

# Eye candy.
begin:
	@echo
	@echo $(MSG_BEGIN)

end:
	@echo $(MSG_END)
	@echo


# Display size of file.
AXFSIZE = $(SIZE) $(TARGET).axf
sizeafter:
	@if [ -f $(TARGET).axf ]; then echo; echo $(MSG_SIZE); echo; $(AXFSIZE); echo; fi


# Display compiler version information.
gccversion : 
	@echo $(MSG_COMPILER); echo; $(CC) --version

# Create final output file (.bin) from ELF output file.
%.bin: %.axf
	@echo " OBJCOPY    ${@}"
	@$(OBJCOPY) -O binary $< $@

%.axf:  $(AOBJ) $(COBJ)
	@echo " LINKING    ${@}"
	@echo $(LDFLAGS)
	@$(CC) $(AOBJ) $(COBJ) $(LDFLAGS) --output $@ 

# Compile: create object files from C source files. ARM/Thumb
$(COBJ) : %.o : %.c
	@echo "  GCC   ${<}"
	@$(CC) -c $(THUMB) $(ALL_CFLAGS) $< -o $@ 

# Assemble: create object files from assembler source files. ARM/Thumb
$(AOBJ) : %.o : %.S
	@echo "  GCC   ${<}"
	@$(CC) -c $(THUMB) $(ALL_ASFLAGS) $< -o $@


# PyMite: Generate native code and module images from the python source
$(TARGET)_nat.c $(TARGET)_img.c : $(PM_USR_SOURCES)
	$(PMIMGCREATOR) -c -u -o $(TARGET)_img.c --native-file=$(TARGET)_nat.c $(PM_USR_SOURCES)

../../vm/pmstdlib_img.c ../../vm/pmstdlib_nat.c : 
	$(MAKE) -C ../../vm pmstdlib_img.c pmstdlib_nat.c



# Target: clean project.
clean: begin clean_list end

clean_list :
	$(MAKE) -C ../../vm clean
	$(REMOVE) $(TARGET).axf
	$(REMOVE) $(TARGET).bin
	$(REMOVE) $(TARGET).map
	$(REMOVE) $(COBJ)
	$(REMOVE) $(AOBJ)
	$(REMOVE) symbols.nm
	$(REMOVE) $(SRC:.c=.s)
	$(REMOVE) $(TARGET)_img.c
	$(REMOVE) $(TARGET)_nat.c


# listing of precious targets.
.PRECIOUS : $(AOBJ) $(COBJ)

# Listing of phony targets.
.PHONY : all begin end sizeafter gccversion \
build elf hex bin lss sym clean clean_list program pmvm zip

# Exports for VM build
export CC OBJCOPY NM CFLAGS ALL_CFLAGS AR IPM PM_LIB_FN COMPILER FEATURES
