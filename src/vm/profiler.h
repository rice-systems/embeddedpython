/* vm/profiler.h
 *
 * Copyright 2011 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#define NUM_PROFILER_FLAGS 5

// be careful redefining IN_SLEEP!
// the value is hardcoded into sys.py
#define IN_SLEEP 0
#define IN_GC 1
#define IN_ALLOC 2
#define IN_NATIVE 3
#define IN_GETITEM 4

typedef struct pyLineSamples_s
{
    int32_t top;
    int32_t all;
} pyLineSamples_t;

typedef struct PmProfilerArray_s
{
    /** Object descriptor */
    PmObjDesc_t od;
    
    // number of lines
    int16_t length;

    /** Array of sample counts */
    pyLineSamples_t samples[1];

} PmProfilerArray_t,
 *pPmProfilerArray_t;

typedef struct dictionary_profile
{
    int32_t lookups;
    int32_t hits;
    int32_t entries_total;
    int32_t entries_walked;
} dictionary_profile;

PmReturn_t profiler_init(void);
int profiler_isactive(void);
void profiler_tick(void);
void profiler_vmstats(void);
void profiler_pystats(void);
PmReturn_t profiler_dictstats(pPmList_t *pl);
void profiler_bytecode(uint8_t bc);
void profiler_startstop(int state);
void profiler_gcrun(void);
void profiler_alloc(void);
PmReturn_t profiler_set_context(void);
void profiler_get_line(bool line_number);
PmReturn_t profiler_callstats(void);
PmReturn_t profiler_reset_counts_callback(pPmObj_t pobj);
PmReturn_t profiler_print_counts_callback(pPmObj_t pobj);


#define NUM_DICTPROFILES 4
volatile dictionary_profile *profiler_get_dictprofile(void);

