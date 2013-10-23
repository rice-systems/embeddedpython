# platform/stellaris/programmer/connect.sh
#
# Connects to the target, passing along other arguments.
#
# Copyright 2013 Rice University.
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

source programmer/programmer.local

if $INSTALLED_OPENOCD ; then
	openocd -f interface/stlink-v2.cfg -f target/stm32f4x_stlink.cfg -f programmer/flash.cfg "$@"
else
	$OPENOCD_LOCATION/src/openocd -s $OPENOCD_LOCATION/tcl -f interface/stlink-v2.cfg -f target/stm32f4x_stlink.cfg -f programmer/flash.cfg "$@"
fi
