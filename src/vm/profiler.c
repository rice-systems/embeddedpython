/* vm/profiler.c
 *
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#include "pm.h"
#include "plat.h"

#undef __FILE_ID__
#define __FILE_ID__ 0x20

#define NUM_BYTECODES 256

#ifdef HAVE_PROFILER
static int profiler_ticks;
static int profiler_active;
bool profiler_locked = false;
static int total_bytecodes;

static int gc_runs;
static int gc_in_sleep;
static int allocations;

static int ticks_with_flag[NUM_PROFILER_FLAGS];
static int ticks_with_flag_exclusive[NUM_PROFILER_FLAGS];

static int bytecodes_run[NUM_BYTECODES];
static int bytecodes_sampled[NUM_BYTECODES];

uint8_t current_bytecode;

// god help you if you let this get GC'd
static pPmCo_t profiler_context = C_NULL;

void profiler_startstop(int state) {
    profiler_active = state;
}

int profiler_isactive(void) {
    return profiler_active;
}

void profiler_gcrun(void) {
    gc_runs++;
    bytecodes_run[255]++;
}

void profiler_alloc(void) {
    if (profiler_active)
    {
        allocations++;
    }
}

PmReturn_t profiler_reset_counts_callback(pPmObj_t pobj) {
    // This gets called by the garbage collector to init the call counters
    if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_FXN) {
        ((pPmFunc_t) pobj)->calls = 0;
        ((pPmFunc_t) pobj)->samples = 0;
        ((pPmFunc_t) pobj)->samples_nested = 0;
    }

    return PM_RET_OK;
}

PmReturn_t profiler_print_counts_callback(pPmObj_t pobj) {
    // this is also called by the garbage collector and prints the call
    // frequency for any FXN object
    pPmCo_t pcob;
    pPmString_t pfn, pname;
    uint16_t first_line_no;
    PmReturn_t retval = PM_RET_OK;

    if (OBJ_GET_TYPE(pobj) == OBJ_TYPE_FXN) {
        pcob = ((pPmFunc_t) pobj)->f_co;

        // since NOBs don't contain the data we need to print info about the
        // call, we just skip them
        if (OBJ_GET_TYPE(pcob) == OBJ_TYPE_NOB) {
            return PM_RET_OK;
        }
        
        // file name where function is defined
        pfn = co_getFilename(pcob);
        C_ASSERT(pfn != C_NULL);

        // get the line of pfn where the function definition starts
        first_line_no = co_getFirstlineno(pcob);
        
        // get the name of the function
        retval = tuple_getItem(co_getNames(pcob), -1, (pPmObj_t *) &pname);
        PM_RETURN_IF_ERROR(retval);
        
        // print it all out in TSV
        obj_print((pPmObj_t) pname, 0);
        lib_printf(" (");
        obj_print((pPmObj_t) pfn, 0);
        lib_printf(":%d)\t%d\t%d\t%d\n", first_line_no,
                                      ((pPmFunc_t) pobj)->calls,
                                      ((pPmFunc_t) pobj)->samples,
                                      ((pPmFunc_t) pobj)->samples_nested);
    }

    return retval;
}

PmReturn_t profiler_callstats(void) {
    PmReturn_t retval = PM_RET_OK;

    lib_printf("-start-\n");
    
    lib_printf("call graph stats:\n");
    lib_printf("profiler frequency: %d\n", gVmGlobal.profiler_frequency);
    
    retval = heap_gcWalk(profiler_print_counts_callback);
    PM_RETURN_IF_ERROR(retval);

    lib_printf("-end-\n");
    
    return retval;
}

PmReturn_t
profiler_init(void) {
    int i;
    PmReturn_t retval = PM_RET_OK;
    
    profiler_ticks = 0;
    profiler_active = 0;
    total_bytecodes = 0;
    gc_in_sleep = 0;
    gc_runs = 0;
    allocations = 0;

    profiler_locked = false;

    // reset VM flags
    for (i=0; i<NUM_PROFILER_FLAGS; i++) {
        ticks_with_flag[i] = 0;
        ticks_with_flag_exclusive[i] = 0;
        gVmGlobal.profiler_flags[i] = false;
    }

    for (i=0; i<NUM_BYTECODES; i++) {
        bytecodes_run[i] = 0;
        bytecodes_sampled[i] = 0;
    }

    // clear all the dictionary profile info
    for (i=0; i<NUM_DICTPROFILES; i++) {
        gVmGlobal.dictprofiles[i].hits = 0;
        gVmGlobal.dictprofiles[i].lookups = 0;
        gVmGlobal.dictprofiles[i].entries_total = 0;
        gVmGlobal.dictprofiles[i].entries_walked = 0;
    }
    
    // reset the call profile data in all function objects
    retval = heap_gcWalk(profiler_reset_counts_callback);
    PM_RETURN_IF_ERROR(retval);
    
    return retval;
}

void profiler_tick(void) {
    int i;
    bool line_number;

    if (profiler_active && (!profiler_locked)) {
        profiler_ticks++;

        // we're now hard coding GC as 255
        if (gVmGlobal.profiler_flags[IN_GC])
        {
            bytecodes_sampled[255]++;
        }
        else
        {
            bytecodes_sampled[current_bytecode]++;
        }
        
        // keep track of all the profiler flags
        for (i=0; i<NUM_PROFILER_FLAGS; i++) {
            if (gVmGlobal.profiler_flags[i] == true) {
                ticks_with_flag[i]++;
            }
        }

        // only mark the first flag if more than one is set
        // in the exclusive counters
        for (i=0; i<NUM_PROFILER_FLAGS; i++) {
            if (gVmGlobal.profiler_flags[i] == true) {
                ticks_with_flag_exclusive[i]++;
                break;
            }
        }
        // special case gc in sleep
        if (gVmGlobal.profiler_flags[IN_GC] && 
                gVmGlobal.profiler_flags[IN_SLEEP]) {
            gc_in_sleep++;
        }

        // if we have a current profile context, go gather line
        // number data
        if (profiler_context != C_NULL) {
            line_number = true;
        } else {
            line_number = false;
        }
        
        profiler_get_line(line_number);
    }

}

void profiler_vmstats(void) {
    int i;
    
    lib_printf("-start-\n");
    
    lib_printf("profiler stats:\n");
    lib_printf("profiler frequency: %d\n", gVmGlobal.profiler_frequency);
    lib_printf("ticks: %d\n", profiler_ticks);
    lib_printf("bytecodes: %d\n", total_bytecodes);
    lib_printf("gc: %d\n", gc_runs);
    lib_printf("alloc: %d\n", allocations);

    for (i=0; i<NUM_BYTECODES; i++) {
        if (bytecodes_run[i] > 0) {
            lib_printf("bc %d: %d/%d\n", i, bytecodes_sampled[i], bytecodes_run[i]);
        }
    }

    for (i=0; i<NUM_PROFILER_FLAGS; i++) {
        lib_printf("flag %d: %d/%d\n", i, ticks_with_flag_exclusive[i], ticks_with_flag[i]);
    }
    
    lib_printf("gc_in_sleep: %d\n", gc_in_sleep);
    
    lib_printf("-end-\n");
}

void profiler_pystats(void) {
    int16_t i;

    lib_printf("-start-\n");

    // look to see what we have in the python line number profiler
    if (gVmGlobal.profilerArray == C_NULL) {
        lib_printf("no context set for line number analysis!\n");
    } else {
        lib_printf("python profiler (%d lines):\n", gVmGlobal.profilerArray->length);

        lib_printf("ticks: %d\n", profiler_ticks);
        lib_printf("profiler frequency: %d\n", gVmGlobal.profiler_frequency);
        
        for (i=0; i<gVmGlobal.profilerArray->length; i++) {
            lib_printf("l %d: %d/%d\n", i+1,
                        gVmGlobal.profilerArray->samples[i].top, 
                        gVmGlobal.profilerArray->samples[i].all);
        }
    }
    
    lib_printf("-end-\n");
}

PmReturn_t
profiler_dictstats(pPmList_t *pl) {
    PmReturn_t retval = PM_RET_OK;

    int32_t i;
    pPmTuple_t pt;
    pPmInt_t pi;

    retval = list_new(pl);
    PM_RETURN_IF_ERROR(retval);

#ifdef HAVE_PROFILER
    // for each context (load_name, etc) , grab all of the marked data.
    for (i=0; i<NUM_DICTPROFILES; i++) {
        retval = tuple_new(4, &pt);
        PM_RETURN_IF_ERROR(retval);

        retval = int_new(gVmGlobal.dictprofiles[i].lookups, &pi);
        PM_RETURN_IF_ERROR(retval);
        pt->items[0] = (pPmObj_t) pi;

        retval = int_new(gVmGlobal.dictprofiles[i].hits, &pi);
        PM_RETURN_IF_ERROR(retval);
        pt->items[1] = (pPmObj_t) pi;
        
        retval = int_new(gVmGlobal.dictprofiles[i].entries_walked, &pi);
        PM_RETURN_IF_ERROR(retval);
        pt->items[2] = (pPmObj_t) pi;
        
        retval = int_new(gVmGlobal.dictprofiles[i].entries_total, &pi);
        PM_RETURN_IF_ERROR(retval);
        pt->items[3] = (pPmObj_t) pi;

        retval = list_append(*pl, (pPmObj_t) pt);
        PM_RETURN_IF_ERROR(retval);
    }
#endif

    return retval;
}

// called from the top of the interpreter loop.
// it may make sense to inline this if the profiler
// overhead is too high.
void profiler_bytecode(uint8_t bc) {
    current_bytecode = bc;

    if (profiler_active) {
        total_bytecodes++;

        // we copy the bytecode so that any tick that happens
        // here gets captured
        bytecodes_run[bc]++;
    }
}

// sets context for python line number profiler
PmReturn_t
profiler_set_context(void) {
    pPmCo_t co;
    int16_t obj_size, i;
    int lines;
    PmReturn_t retval;
    
    lib_printf("python profiler starting...\n");
   
    // find the top non-native frame (this is the context
    // we're trying to profile)
    co = FP->fo_func->f_co;
    profiler_context = co;

    lib_printf("fn: ");
    obj_print((pPmObj_t) co_getFilename(co), 0);
    lib_printf("\n");

    // calculate the maximum line number so we can 
    // properly size the array
    lines = co_getMaxlineno(co);

    lib_printf("max line: %d\n", lines);
   
    // the structure already holds one element, so we add the size of the 
    // remaining to the allocation
    obj_size = sizeof(PmProfilerArray_t) + ((lines - 1) * sizeof(pyLineSamples_t));
    
    // pass the allocator a reference straight into the gVmGlobal structure
    retval = heap_getChunk(obj_size, (uint8_t **)&gVmGlobal.profilerArray);
    PM_RETURN_IF_ERROR(retval);
    OBJ_SET_TYPE(gVmGlobal.profilerArray, OBJ_TYPE_PRO);

    // initalize array with zeros
    gVmGlobal.profilerArray->length = lines;
    for (i=0; i<gVmGlobal.profilerArray->length; i++) {
        gVmGlobal.profilerArray->samples[i].all = 0;
        gVmGlobal.profilerArray->samples[i].top = 0;
    }

    // reset timing
    profiler_init();

    return retval;
}

void profiler_get_line(bool line_number) {
    pPmFrame_t frame;
    pPmCo_t codeobj;
    bool at_top = true;
    uint16_t line;
    
    frame = FP;
    
    // walk back until we either fall off the bottom
    // of the call stack
    while (frame != C_NULL) {
        // see if we're in the profiler context
        // we do this every time so we hit multiple places in the file.
        // since each function is in a different code object, we have to do
        // this by comparing file names.
        if (line_number) {
            if (string_compare(co_getFilename(frame->fo_func->f_co),
                               co_getFilename(profiler_context)) == C_EQ) {
                line = 0;

                codeobj = frame->fo_func->f_co;
                line = co_getLineno(codeobj, frame->fo_ip);

                // internally, we index lines from zero
                line--;

                // make sure we don't march out of the array.
                // something BAD is happening if we see this.
                if (line > gVmGlobal.profilerArray->length) {
                    lib_printf("error. line number out of context?\n");
                    return;
                }
                
                if (at_top) {
                    gVmGlobal.profilerArray->samples[line].top++;
                }

                gVmGlobal.profilerArray->samples[line].all++;
            }
        }

        // now mark the function objects themselves for the call graph profile
        frame->fo_func->samples_nested++;
        
        if (at_top) {
            frame->fo_func->samples++;
        }

        // walk back
        frame = frame->fo_back;
        
        // we're no longer at the top of the call stack
        at_top = false;
    }
}

volatile dictionary_profile *profiler_get_dictprofile(void) {
    // this gets called by dict_getItem to record what context we're in.
    if (current_bytecode == LOAD_ATTR) { 
        return &(gVmGlobal.dictprofiles[1]);
    }
    
    else if (current_bytecode == BINARY_SUBSCR) {
        return &(gVmGlobal.dictprofiles[2]);
    }
    
    else if (current_bytecode == LOAD_GLOBAL) {
        return &(gVmGlobal.dictprofiles[3]);
    }
    
    else {
        return &(gVmGlobal.dictprofiles[0]);
    }
}

#endif
