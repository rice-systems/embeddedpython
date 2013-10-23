# WinARM template makefile 
# by Martin Thomas, Kaiserslautern, Germany 
# <eversmith@heizung-thomas.de>
#
# based on the WinAVR makefile written by Eric B. Weddington, Jörg Wunsch, et al.
# Released to the Public Domain
# Please read the make user manual!

include Makefile.local

# Owl VM Build Configuration
PLATFORM := $(notdir $(CURDIR))
PM_LIB_ROOT = pmvm_$(PLATFORM)
PM_LIB_FN = lib$(PM_LIB_ROOT).a
PM_LIB_PATH = ../../vm/$(PM_LIB_FN)
PM_USR_SOURCES = main.py build.py # wrapped/gpio.py wrapped/spi.py
PMIMGCREATOR := ../../tools/owl-tools/pmImgCreator.py
PMBUILDINFO := ../../tools/build/release_buildinfo.py
IPM := true
COMPILER = arm-none-eabi

# MCU name and submodel
MCU      = cortex-m4
USE_THUMB_MODE = YES

## Create ROM-Image (final)
RUN_MODE=ROM_RUN
## Create RAM-Image (debugging) - not used in this example
#RUN_MODE=RAM_RUN

# Target file name (without extension).
TARGET = main

# List C source files here. 
SRC  = $(TARGET).c $(TARGET)_nat.c $(TARGET)_img.c
SRC += plat_stm32f4.c
SRC += interrupts.c
SRC += usb/cdcacm.c

# Optimization level, can be [0, 1, 2, 3, s]. 
# 0 = turn off optimization. s = optimize for size.
# (Note: 3 is not always the best optimization level. See avr-libc FAQ.)
OPT = s

# Debugging format.
# Native formats for AVR-GCC's -g are stabs [default], or dwarf-2.
# AVR (extended) COFF requires stabs, plus an avr-objcopy run.
#DEBUG = stabs
DEBUG = true
DEBUG_FMT = dwarf-2

# List any extra directories to look for include files here.
#     Each directory must be seperated by a space.
EXTRAINCDIRS = $(abspath .) ../../vm $(OPENCM3BASE)/include/libopencm3/stm32
EXTRAINCDIRS += $(OPENCM3BASE)/include/

# List any extra directories to look for library files here.
#     Each directory must be seperated by a space.
EXTRA_LIBDIRS  = . ../../vm 
EXTRA_LIBDIRS += $(OPENCM3BASE)/lib/

# Compiler flag to set the C Standard level.
# c89   - "ANSI" C
# gnu89 - c89 plus GCC extensions
# c99   - ISO C99 standard (not yet fully implemented)
# gnu99 - c99 plus GCC extensions
CSTANDARD = -std=gnu99

# Place -D or -U options for C here
CDEFS =  -D$(RUN_MODE) -D$(SUBMDL)
# PyMite CDEFS
ifeq ($(DEBUG),true)
	CDEFS += -g -g$(DEBUG_FMT) -D__DEBUG__=1
endif

# Place -D or -U options for ASM here
ADEFS =  -D$(RUN_MODE)

# Compiler flags.
THUMB    = -mthumb
FLOAT    = -mfloat-abi=hard -mfpu=fpv4-sp-d16

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

CFLAGS += $(FLOAT)

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
EXTRA_LIBS += opencm3_stm32f4
#EXTRA_LIBS += m

# Linker flags.
#  -Wl,...:     tell GCC to pass this to linker.
#    -Map:      create map file
#    --cref:    add cross reference to  map file
LDFLAGS = -Wl,-Map=$(TARGET).map,--cref,--gc-sections
LDFLAGS += -nostartfiles 


#LDFLAGS += -lc -lgcc 
LDFLAGS += $(patsubst %,-l%,$(EXTRA_LIBS))
LDFLAGS += $(patsubst %,-L%,$(EXTRA_LIBDIRS))

LDFLAGS += -mcpu=$(MCU) $(THUMB)

LDFLAGS += $(FLOAT)

# force the linker script from codesourcery
LDFLAGS += -Tld-scripts/$(LINKERSCRIPT)

LDFLAGS += -lm -lc

# Define programs and commands.
SHELL = sh
CC = $(TCHAIN)-gcc
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
	$(CC) $(AOBJ) $(COBJ) $(LDFLAGS) --output $@ 

# Compile: create object files from C source files. ARM/Thumb
$(COBJ) : %.o : %.c
	@echo "  GCC   ${<}"
	$(CC) -c $(THUMB) $(ALL_CFLAGS) $< -o $@ 

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
export CC OBJCOPY NM CFLAGS ALL_CFLAGS AR IPM PM_LIB_FN COMPILER LIB_STYLE
