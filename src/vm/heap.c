/* vm/heap.c
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */


#undef __FILE_ID__
#define __FILE_ID__ 0x06


/**
 * \file
 * \brief VM Heap
 *
 * VM heap operations.
 * All of PyMite's dynamic memory is obtained from this heap.
 * The heap provides dynamic memory on demand.
 */


#include "pm.h"


/** Checks for heap size definition. */
#ifndef PM_HEAP_SIZE
#warning PM_HEAP_SIZE not defined in src/platform/<yourplatform>/pmfeatures.h
#elif PM_HEAP_SIZE & 3
#error PM_HEAP_SIZE is not a multiple of four
#endif


/**
 * The maximum size a live chunk can be (a live chunk is one that is in use).
 * The live chunk size is limited by the size field in the *object* descriptor.
 * That field is nine bits with two assumed least significant bits (zeros):
 * 16-bit: (0x1FF << 2) == 2044
 * 32-bit: (0x3FFF << 2) == 65532
 */
#define HEAP_MAX_LIVE_CHUNK_SIZE 65532

/**
 * The maximum size a free chunk can be (a free chunk is one that is not in use).
 * The free chunk size is limited by the size field in the *heap* descriptor.
 * That field is fourteen bits with two assumed least significant bits (zeros):
 * 16-bit: (0x3FFF << 2) == 65532
 * 32-bit: (0x3FFF << 2) == 65532
 */
#define HEAP_MAX_FREE_CHUNK_SIZE 65532

/** The minimum size a chunk can be (rounded up to a multiple of 4) */
#define HEAP_MIN_CHUNK_SIZE ((sizeof(PmHeapDesc_t) + 3) & ~3)


/**
 * Gets the GC's mark bit for the object.
 * This MUST NOT be called on objects that are free.
 */
#define OBJ_GET_GCVAL(pobj) ((((pPmObj_t)pobj)->od >> OD_MARK_SHIFT) & 1)

/**
 * Sets the GC's mark bit for the object
 * This MUST NOT be called on objects that are free.
 */
#ifdef HAVE_GC
#define OBJ_SET_GCVAL(pobj, gcval) \
    do \
    { \
        ((pPmObj_t)pobj)->od = (gcval) ? ((pPmObj_t)pobj)->od | OD_MARK_BIT \
                                       : ((pPmObj_t)pobj)->od & ~OD_MARK_BIT;\
    } \
    while (0)
#else
#define OBJ_SET_GCVAL(pobj, gcval)
#endif /* HAVE_GC */


/**
 * The following is a diagram of the heap descriptor at the head of the chunk:
 *
 *                MSb          LSb
 *                7 6 5 4 3 2 1 0
 *      pchunk-> +-+-+-+-+-+-+-+-+
 *               |     S[9:2]    |     S := Size of the chunk (2 LSbs dropped)
 *               +-+-+-----------+     F := Chunk free bit (not in use)
 *               |F|R| S[15:10]  |     R := Bit reserved for future use
 *               +-+-+-----------+
 *               |     P(L)      |     P := hd_prev: Pointer to previous node
 *               |     P(H)      |     N := hd_next: Pointer to next node
 *               |     N(L)      |
 *               |     N(H)      |     Theoretical min size == 6
 *               +---------------+     Effective min size == 8
 *               | unused space  |     (12 on 32-bit MCUs)
 *               ...           ...
 *               | end chunk     |
 *               +---------------+
 */
typedef struct PmHeapDesc_s
{
    /** Object descriptor */
    uint32_t od;

    /** Dummy for padding */
    /** uint16_t empty; */

    /** Ptr to prev heap chunk */
    struct PmHeapDesc_s *prev;

    /** Ptr to next heap chunk */
    struct PmHeapDesc_s *next;
} PmHeapDesc_t,
 *pPmHeapDesc_t;

typedef struct PmHeap_s
{
    /*
     * WARNING: Leave 'base' field at the top of struct to increase chance
     * of alignment when compiler doesn't recognize the aligned attribute
     * which is specific to GCC
     */
    /** Global declaration of heap. */
    uint8_t base[PM_HEAP_SIZE];

    /** Ptr to list of free chunks; sorted smallest to largest. */
    pPmHeapDesc_t pfreelist;

    /** The amount of heap space available in free list */
#if PM_HEAP_SIZE > 65535
    uint32_t avail;
#else
    uint16_t avail;
#endif

#ifdef HAVE_GC
    /** Garbage collection mark value */
    uint8_t gcval;

    /** Boolean to indicate if GC should run automatically */
    uint8_t auto_gc;
#endif                          /* HAVE_GC */

} PmHeap_t,
 *pPmHeap_t;


/** The PyMite heap */
static PmHeap_t pmHeap;

uint8_t *
heap_baseAddr()
{
    return &pmHeap.base[0];
}

bool
heap_addrInHeap(uint8_t const *paddr)
{
    if ((paddr >= &pmHeap.base[0]) && 
        (paddr < &pmHeap.base[PM_HEAP_SIZE]))
    {
        return true;
    }
    else
    {
        return false;
    }
}

void
heap_gcPrintFreelist(void)
{
    pPmHeapDesc_t pchunk = pmHeap.pfreelist;

    lib_printf("DEBUG: pmHeap.avail = %d\n", pmHeap.avail);
    lib_printf("DEBUG: freelist:\n");
    while (pchunk != C_NULL)
    {
        lib_printf("DEBUG:     free chunk (%d bytes) @ 0x%0x\n",
               OBJ_GET_SIZE(pchunk), (int)pchunk);
        pchunk = pchunk->next;
    }
}

#if 0
void
heap_dump(char *filename)
{
    uint8_t *pmem;
    uint32_t i;
    FILE *fp;

    fp = fopen(filename, "wb");
    pmem = heap_baseAddr();

    fprintf(fp, "%p\n", pmem);
    
    for (i=0; i<PM_HEAP_SIZE; i++)
    {
        fprintf(fp, "%02X", *pmem);
        pmem++;
    }

    fclose(fp);
}
#endif



/* Removes the given chunk from the free list; leaves list in sorted order */
static PmReturn_t
heap_unlinkFromFreelist(pPmHeapDesc_t pchunk)
{
    C_ASSERT(pchunk != C_NULL);

    pmHeap.avail -= OBJ_GET_SIZE(pchunk);

    if (pchunk->next != C_NULL)
    {
        pchunk->next->prev = pchunk->prev;
    }

    /* If pchunk was the first chunk in the free list, update the heap ptr */
    if (pchunk->prev == C_NULL)
    {
        pmHeap.pfreelist = pchunk->next;
    }
    else
    {
        pchunk->prev->next = pchunk->next;
    }

    return PM_RET_OK;
}


/* Inserts in order a chunk into the free list.  Caller adjusts heap state */
static PmReturn_t
heap_linkToFreelist(pPmHeapDesc_t pchunk)
{
    uint32_t size;
    pPmHeapDesc_t pscan;

    /* Ensure the object is already free */
    C_ASSERT(OBJ_GET_FREE(pchunk) != 0);

    pmHeap.avail += OBJ_GET_SIZE(pchunk);

    /* If free list is empty, add to head of list */
    if (pmHeap.pfreelist == C_NULL)
    {
        pmHeap.pfreelist = pchunk;
        pchunk->next = C_NULL;
        pchunk->prev = C_NULL;

        return PM_RET_OK;
    }

    /* Scan free list for insertion point */
    pscan = pmHeap.pfreelist;
    size = OBJ_GET_SIZE(pchunk);
    while ((OBJ_GET_SIZE(pscan) < size) && (pscan->next != C_NULL))
    {
        pscan = pscan->next;
    }

    /*
     * Insert chunk after the scan chunk (next is NULL).
     * This is a slightly rare case where the last chunk in the free list
     * is smaller than the chunk being freed.
     */
    if (size > OBJ_GET_SIZE(pscan))
    {
        pchunk->next = pscan->next;
        pscan->next = pchunk;
        pchunk->prev = pscan;
    }

    /* Insert chunk before the scan chunk */
    else
    {
        pchunk->next = pscan;
        pchunk->prev = pscan->prev;

        /* If chunk will be first item in free list */
        if (pscan->prev == C_NULL)
        {
            pmHeap.pfreelist = pchunk;
        }
        else
        {
            pscan->prev->next = pchunk;
        }
        pscan->prev = pchunk;
    }

    return PM_RET_OK;
}


/*
 * Initializes the heap state variables
 */
PmReturn_t
heap_init(void)
{
    pPmHeapDesc_t pchunk;

#if PM_HEAP_SIZE > 65535
    uint32_t hs;
#else
    uint16_t hs;
#endif

    /* Init heap globals */
    pmHeap.pfreelist = C_NULL;
    pmHeap.avail = 0;
#ifdef HAVE_GC
    pmHeap.gcval = (uint8_t)0;
    pmHeap.auto_gc = C_TRUE;
#endif /* HAVE_GC */

    /* Create as many max-sized chunks as possible in the freelist */
    for (pchunk = (pPmHeapDesc_t)pmHeap.base, hs = PM_HEAP_SIZE;
         hs >= HEAP_MAX_FREE_CHUNK_SIZE; hs -= HEAP_MAX_FREE_CHUNK_SIZE)
    {
        OBJ_SET_FREE(pchunk, 1);
        OBJ_SET_SIZE(pchunk, HEAP_MAX_FREE_CHUNK_SIZE);
        heap_linkToFreelist(pchunk);
        pchunk =
            (pPmHeapDesc_t)((uint8_t *)pchunk + HEAP_MAX_FREE_CHUNK_SIZE);
    }

    /* Add any leftover memory to the freelist */
    if (hs >= HEAP_MIN_CHUNK_SIZE)
    {
        /* Round down to a multiple of four */
        hs = hs & ~3;
        OBJ_SET_FREE(pchunk, 1);
        OBJ_SET_SIZE(pchunk, hs);
        heap_linkToFreelist(pchunk);
    }

    C_DEBUG_PRINT(VERBOSITY_LOW, "heap_init(), id=%p, s=%u\n",
                  pmHeap.base, pmHeap.avail);

    return PM_RET_OK;
}


/**
 * Obtains a chunk of memory from the free list
 *
 * Performs the Best Fit algorithm.
 * Iterates through the freelist to see if a chunk of suitable size exists.
 * Shaves a chunk to perfect size iff the remainder is greater than
 * the minimum chunk size.
 *
 * @param size Requested chunk size
 * @param r_pchunk Return ptr to chunk
 * @return Return status
 */
static PmReturn_t
heap_getChunkImpl(uint16_t size, uint8_t **r_pchunk)
{
    PmReturn_t retval;
    pPmHeapDesc_t pchunk;
    pPmHeapDesc_t premainderChunk;

    C_ASSERT(r_pchunk != C_NULL);

    /* Skip to the first chunk that can hold the requested size */
    pchunk = pmHeap.pfreelist;
    while ((pchunk != C_NULL) && (OBJ_GET_SIZE(pchunk) < size))
    {
        pchunk = pchunk->next;
    }

    /* No chunk of appropriate size was found, raise OutOfMemory exception */
    if (pchunk == C_NULL)
    {
        *r_pchunk = C_NULL;
        PM_RAISE(retval, PM_RET_EX_MEM);
        return retval;
    }

    /* Remove the chunk from the free list */
    retval = heap_unlinkFromFreelist(pchunk);
    PM_RETURN_IF_ERROR(retval);

    /* Check if a chunk should be carved from what is available */
    if (OBJ_GET_SIZE(pchunk) - size >= HEAP_MIN_CHUNK_SIZE)
    {
        /* Create the heap descriptor for the remainder chunk */
        premainderChunk = (pPmHeapDesc_t)((uint8_t *)pchunk + size);
        OBJ_SET_FREE(premainderChunk, 1);
        OBJ_SET_SIZE(premainderChunk, OBJ_GET_SIZE(pchunk) - size);

        /* Put the remainder chunk back in the free list */
        retval = heap_linkToFreelist(premainderChunk);
        PM_RETURN_IF_ERROR(retval);

        /* Convert the chunk from a heap descriptor to an object descriptor */
        OBJ_SET_SIZE(pchunk, 0);
        OBJ_SET_FREE(pchunk, 0);
        OBJ_SET_SIZE(pchunk, size);

        C_DEBUG_PRINT(VERBOSITY_HIGH,
                      "heap_getChunkImpl()carved, id=%p, s=%d\n", pchunk,
                      size);
    }
    else
    {
        /* Set chunk's type to none (overwrites size field's high byte) */
        OBJ_SET_TYPE((pPmObj_t)pchunk, OBJ_TYPE_NON);
        OBJ_SET_FREE(pchunk, 0);

        C_DEBUG_PRINT(VERBOSITY_HIGH,
                      "heap_getChunkImpl()exact, id=%p, s=%u\n", pchunk,
                      OBJ_GET_SIZE(pchunk));
    }

    /*
     * Set the chunk's GC mark so it will be collected during the next GC cycle
     * if it is not reachable
     */
    OBJ_SET_GCVAL(pchunk, pmHeap.gcval);

    /* Return the chunk */
    *r_pchunk = (uint8_t *)pchunk;

    return retval;
}


/*
 * Allocates chunk of memory.
 * Filters out invalid sizes.
 * Rounds the size up to the next multiple of 4.
 * Obtains a chunk of at least the desired size.
 */
PmReturn_t
heap_getChunk(uint16_t requestedsize, uint8_t **r_pchunk)
{
    PmReturn_t retval;
    uint16_t adjustedsize;

#ifdef HAVE_PROFILER
    gVmGlobal.profiler_flags[IN_ALLOC] = true;
    profiler_alloc();
#endif

    /* Ensure size request is valid */
    if (requestedsize > HEAP_MAX_LIVE_CHUNK_SIZE)
    {
        PM_RAISE(retval, PM_RET_EX_MEM);
        return retval;
    }

    else if (requestedsize < HEAP_MIN_CHUNK_SIZE)
    {
        requestedsize = HEAP_MIN_CHUNK_SIZE;
    }

    /*
     * Round up the size to a multiple of 4 bytes.
     * This maintains alignment on 32-bit platforms (required).
     */
    adjustedsize = ((requestedsize + 3) & ~3);

    /* Attempt to get a chunk */
    retval = heap_getChunkImpl(adjustedsize, r_pchunk);

#ifdef HAVE_GC
    /* Perform GC if out of memory, gc is enabled and not in native session */
    if ((retval == PM_RET_EX_MEM) && (pmHeap.auto_gc == C_TRUE)
        && (gVmGlobal.nf_active == C_FALSE))
    {
        retval = heap_gcRun();
        PM_RETURN_IF_ERROR(retval);

        /* Attempt to get a chunk */
        retval = heap_getChunkImpl(adjustedsize, r_pchunk);
    }
#endif /* HAVE_GC */

    /* Ensure that the pointer is 4-byte aligned */
    if (retval == PM_RET_OK)
    {
        C_ASSERT(((intptr_t)*r_pchunk & 3) == 0);
    }

#ifdef HAVE_PROFILER
    gVmGlobal.profiler_flags[IN_ALLOC] = false;
#endif

    return retval;
}


/* Releases chunk to the free list */
PmReturn_t
heap_freeChunk(pPmObj_t ptr)
{
    PmReturn_t retval;

    C_DEBUG_PRINT(VERBOSITY_HIGH, "heap_freeChunk(), id=%p, s=%u\n",
                  ptr, OBJ_GET_SIZE(ptr));

    /* Ensure the chunk falls within the heap */
    C_ASSERT(((uint8_t *)ptr >= pmHeap.base)
             && ((uint8_t *)ptr < pmHeap.base + PM_HEAP_SIZE));

    /* Insert the chunk into the freelist */
    OBJ_SET_FREE(ptr, 1);

    /* Clear type so that heap descriptor's size's upper byte is zero */
    OBJ_SET_TYPE(ptr, 0);
    retval = heap_linkToFreelist((pPmHeapDesc_t)ptr);
    PM_RETURN_IF_ERROR(retval);

    return retval;
}


/* Returns, by reference, the number of bytes available in the heap */
#if PM_HEAP_SIZE > 65535
uint32_t
#else
uint16_t
#endif
heap_getAvail(void)
{
    return pmHeap.avail;
}


#ifdef HAVE_GC
/*
 * Marks the given object and the objects it references.
 *
 * @param   pobj Any non-free heap object
 * @return  Return code
 */
#if 0
/* Use to print out GC trace */
#define heap_gcMarkObj(pobj) \
       heap_gcMarkObj2((pobj)); \
       USBprintf("mark from: %p\n", (pobj))

static PmReturn_t
heap_gcMarkObj2(pPmObj_t pobj)
#else
static PmReturn_t
heap_gcMarkObj(pPmObj_t pobj)
#endif
{
    PmReturn_t retval = PM_RET_OK;
    int16_t i = 0;
    PmType_t type;

#ifdef CORTEX_C_STACK_PROTECT
    // make sure we're not about to overflow the stack.
    uint8_t *sp;
    extern uint8_t __end;

    asm("mov %[result], sp" : [result] "=r" (sp) : );

    if (sp < (&__end + 500)) // give enough space to make the call to fatal
    {
        except_fatal("garbage collection has overflowed the C stack");
        return retval;
    }
#endif

    /* Return if ptr is null or object is already marked */
    if ((pobj == C_NULL) || (OBJ_GET_GCVAL(pobj) == pmHeap.gcval))
    {
        return retval;
    }

#if 0
    /* Use to print out GC trace */
    lib_printf("pobj ptr: %p\n", pobj);
    obj_print(pobj, 1);
    lib_printf("\n");
#endif

    /* The pointer must be within the heap */
    /*
    C_ASSERT((((uint8_t *)pobj >= &pmHeap.base[0])
              && ((uint8_t *)pobj <= &pmHeap.base[PM_HEAP_SIZE])));
    */

    /* Do not follow pointers outside of the heap */
    if (!heap_addrInHeap((uint8_t *) pobj))
    {
        /*
        lib_printf("object not in heap: (%p) (0x%08x)", pobj, *((uint32_t *) pobj));
        obj_print(pobj, 1);
        lib_printf("\n");
        */
        return retval;
    }

    /* The object must not already be free */
    C_ASSERT(OBJ_GET_FREE(pobj) == 0);

    type = (PmType_t)OBJ_GET_TYPE(pobj);
    switch (type)
    {
            /* Objects with no references to other objects */
        case OBJ_TYPE_NON:
        case OBJ_TYPE_ANY:
        case OBJ_TYPE_INT:
        case OBJ_TYPE_FLT:
        case OBJ_TYPE_STR:

        case OBJ_TYPE_NOB:
        case OBJ_TYPE_BOL:
        case OBJ_TYPE_PRO:
        case OBJ_TYPE_XRA:
        case OBJ_TYPE_PTP:
        case OBJ_TYPE_PCO:
        case OBJ_TYPE_FOR:
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);
            break;

        case OBJ_TYPE_TUP:
            i = ((pPmTuple_t)pobj)->length;

            /* Mark tuple head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark each obj in tuple */
            while (--i >= 0)
            {
                retval = heap_gcMarkObj(((pPmTuple_t)pobj)->items[i]);
                PM_RETURN_IF_ERROR(retval);
            }
            break;

        case OBJ_TYPE_LST:

            /* Mark the list */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the seglist */
            retval = heap_gcMarkObj((pPmObj_t)((pPmList_t)pobj)->val);
            break;

        case OBJ_TYPE_SET:
            
            /* Mark the set */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the seglist */
            retval = heap_gcMarkObj((pPmObj_t)((pPmSet_t)pobj)->val);
            break;

        case OBJ_TYPE_DIC:
            /* Mark the dict head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the keys seglist */
            retval = heap_gcMarkObj((pPmObj_t)((pPmDict_t)pobj)->d_keys);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the vals seglist */
            retval = heap_gcMarkObj((pPmObj_t)((pPmDict_t)pobj)->d_vals);
            break;

        case OBJ_TYPE_COB:
            /* Mark the code obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the names tuple */
            retval = heap_gcMarkObj((pPmObj_t)co_getNames((pPmCo_t)pobj));
            PM_RETURN_IF_ERROR(retval);

            /* Mark the varnames tuple */
            retval = heap_gcMarkObj((pPmObj_t)co_getVarNames((pPmCo_t)pobj));
            PM_RETURN_IF_ERROR(retval);

            /* Mark the consts tuple */
            retval = heap_gcMarkObj((pPmObj_t)co_getConsts((pPmCo_t)pobj));
            PM_RETURN_IF_ERROR(retval);

            /* Mark the Python file name */
            retval = heap_gcMarkObj((pPmObj_t)co_getFilename((pPmCo_t)pobj));
            PM_RETURN_IF_ERROR(retval);
            
            /* Mark the line number table */
            retval = heap_gcMarkObj((pPmObj_t)co_getLnotab((pPmCo_t)pobj));
            PM_RETURN_IF_ERROR(retval);

            /* Mark the code */
            retval = heap_gcMarkObj((pPmObj_t)co_getCode((pPmCo_t)pobj));
            PM_RETURN_IF_ERROR(retval);
            
#ifdef HAVE_CLOSURES
            /* #256: Add support for closures */
            /* Mark the cellvars tuple */
            retval = heap_gcMarkObj((pPmObj_t)co_getCellvars((pPmCo_t)pobj));
#endif /* HAVE_CLOSURES */
            break;

        case OBJ_TYPE_MOD:
        case OBJ_TYPE_FXN:
            /* Module and Func objs are implemented via the PmFunc_t */
            /* Mark the func obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the code obj */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFunc_t)pobj)->f_co);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the attr dict */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFunc_t)pobj)->f_attrs);
            PM_RETURN_IF_ERROR(retval);

#ifdef HAVE_DEFAULTARGS
            /* Mark the default args tuple */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFunc_t)pobj)->f_defaultargs);
#endif /* HAVE_DEFAULTARGS */

#ifdef HAVE_CLOSURES
            /* #256: Mark the closure tuple */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFunc_t)pobj)->f_closure);
#endif /* HAVE_CLOSURES */
            break;

#ifdef HAVE_CLASSES
        case OBJ_TYPE_CLI:
            /* Mark the obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the class */
            retval = heap_gcMarkObj((pPmObj_t)((pPmInstance_t)pobj)->cli_class);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the attrs dict */
            retval = heap_gcMarkObj((pPmObj_t)((pPmInstance_t)pobj)->cli_attrs);
            PM_RETURN_IF_ERROR(retval);
            break;

        case OBJ_TYPE_MTH:
            /* Mark the obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the instance */
            retval = heap_gcMarkObj((pPmObj_t)((pPmMethod_t)pobj)->m_instance);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the func */
            retval = heap_gcMarkObj((pPmObj_t)((pPmMethod_t)pobj)->m_func);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the attrs dict */
            retval = heap_gcMarkObj((pPmObj_t)((pPmMethod_t)pobj)->m_attrs);
            PM_RETURN_IF_ERROR(retval);
            break;

        case OBJ_TYPE_CLO:
            /* Mark the obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the attrs dict */
            retval = heap_gcMarkObj((pPmObj_t)((pPmClass_t)pobj)->cl_attrs);

            /* Mark the bases tuple */
            retval = heap_gcMarkObj((pPmObj_t)((pPmClass_t)pobj)->cl_bases);
            break;
#endif /* HAVE_CLASSES */

        case OBJ_TYPE_FRM:
        {
            pPmObj_t *ppobj2 = C_NULL;

            /* Mark the frame obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the previous frame */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFrame_t)pobj)->fo_back);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the exception frame */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFrame_t)pobj)->fo_except);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the fxn obj */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFrame_t)pobj)->fo_func);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the blockstack */
            retval = heap_gcMarkObj((pPmObj_t)
                                    ((pPmFrame_t)pobj)->fo_blockstack);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the locals dict */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFrame_t)pobj)->fo_locals);
            PM_RETURN_IF_ERROR(retval);

            /* Mark the globals dict */
            retval = heap_gcMarkObj((pPmObj_t)((pPmFrame_t)pobj)->fo_globals);
            PM_RETURN_IF_ERROR(retval);

            /* Mark temporary live object */
            if (((pPmFrame_t)pobj)->liveObj) {
                retval = heap_gcMarkObj((pPmObj_t)((pPmFrame_t)pobj)->liveObj);
                PM_RETURN_IF_ERROR(retval);
            }

            /* Mark each obj in the stack */
            ppobj2 = ((pPmFrame_t)pobj)->fo_stack;
            while (ppobj2 < ((pPmFrame_t)pobj)->fo_sp)
            {
                retval = heap_gcMarkObj(*ppobj2);
                PM_RETURN_IF_ERROR(retval);
                ppobj2++;
            }
            break;
        }

        case OBJ_TYPE_BLK:
            /* Mark the block obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the next block in the stack */
            retval = heap_gcMarkObj((pPmObj_t)((pPmBlock_t)pobj)->next);
            break;

        case OBJ_TYPE_SEG:
            /* Mark the segment obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark each obj in the segment */
            for (i = 0; i < SEGLIST_OBJS_PER_SEG; i++)
            {
                retval = heap_gcMarkObj(((pSegment_t)pobj)->s_val[i]);
                PM_RETURN_IF_ERROR(retval);
            }

            /* Mark the next segment */
            retval = heap_gcMarkObj((pPmObj_t)((pSegment_t)pobj)->next);
            break;

        case OBJ_TYPE_SGL:
            /* Mark the seglist obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the root segment */
            retval = heap_gcMarkObj((pPmObj_t)((pSeglist_t)pobj)->sl_rootseg);
            break;

        case OBJ_TYPE_SQI:
            /* Mark the sequence iterator obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the sequence */
            retval = heap_gcMarkObj(((pPmSeqIter_t)pobj)->si_sequence);
            break;

        case OBJ_TYPE_THR:
            /* Mark the thread obj head */
            OBJ_SET_GCVAL(pobj, pmHeap.gcval);

            /* Mark the current frame */
            retval = heap_gcMarkObj((pPmObj_t)((pPmThread_t)pobj)->pframe);

            /* Mark the thread ID */
            retval = heap_gcMarkObj((pPmObj_t)((pPmThread_t)pobj)->ptid);

            break;

        default:
            /* There should be no invalid types */
            PM_RAISE_WITH_OBJ(retval, PM_RET_EX_SYS, pobj);
            break;
    }
    return retval;
}


/*
 * Marks the root objects so they won't be collected during the sweep phase.
 * Recursively marks all objects reachable from the roots.
 */
static PmReturn_t
heap_gcMarkRoots(void)
{
    PmReturn_t retval;
    int16_t i; // loop iterator

    /* Toggle the GC marking value so it differs from the last run */
    pmHeap.gcval ^= 1;

    /* Mark the constant objects */
    retval = heap_gcMarkObj(PM_NONE);
    PM_RETURN_IF_ERROR(retval);

    retval = heap_gcMarkObj(PM_FALSE);
    PM_RETURN_IF_ERROR(retval);
    retval = heap_gcMarkObj(PM_TRUE);
    PM_RETURN_IF_ERROR(retval);
    retval = heap_gcMarkObj(PM_ZERO);
    PM_RETURN_IF_ERROR(retval);
    retval = heap_gcMarkObj(PM_ONE);
    PM_RETURN_IF_ERROR(retval);
    retval = heap_gcMarkObj(PM_NEGONE);
    PM_RETURN_IF_ERROR(retval);
    
    /* Mark the builtins dict */
    retval = heap_gcMarkObj((pPmObj_t)PM_PBUILTINS);
    PM_RETURN_IF_ERROR(retval);

    /* Mark the thread list */
    retval = heap_gcMarkObj((pPmObj_t)gVmGlobal.threadList);
    PM_RETURN_IF_ERROR(retval);

    /* Mark the running thread */
    retval = heap_gcMarkObj((pPmObj_t)gVmGlobal.prunningThread);
    PM_RETURN_IF_ERROR(retval);

    /* Mark the exception object */
    retval = heap_gcMarkObj(gVmGlobal.errObj);
    PM_RETURN_IF_ERROR(retval);
    
    /* Mark the Python file name */
    retval = heap_gcMarkObj((pPmObj_t)gVmGlobal.pyErrFilename);
    PM_RETURN_IF_ERROR(retval);

#ifdef HAVE_PROFILER
    /* Mark the profiler array, if we currently have one */
    retval = heap_gcMarkObj((pPmObj_t)gVmGlobal.profilerArray);
    PM_RETURN_IF_ERROR(retval);
#endif

    /* Mark the module dictionary */
    retval = heap_gcMarkObj((pPmObj_t)gVmGlobal.modules);
    PM_RETURN_IF_ERROR(retval);

#ifdef HAVE_IP
    /* Mark the unclaimed incoming data */
    retval = heap_gcMarkObj((pPmObj_t)gVmGlobal.incoming_packets);
    PM_RETURN_IF_ERROR(retval);
#endif /* HAVE_IP */

    /* Mark all the constants */
    for (i=0; i<NUM_CONSTANTS; i++) {
        retval = heap_gcMarkObj(gVmGlobal.consts[i]);
        PM_RETURN_IF_ERROR(retval);
    }
    
    return retval;
}

// walk through the entire heap
PmReturn_t
heap_gcWalk(PmReturn_t (*pfIterator)(pPmObj_t))
{
    PmReturn_t retval;
    pPmObj_t pobj;
    pPmHeapDesc_t pchunk;
    uint32_t totalchunksize;

    /* Start at the base of the heap */
    pobj = (pPmObj_t)pmHeap.base;
    while ((uint8_t *)pobj < &pmHeap.base[PM_HEAP_SIZE])
    {
        /* Skip to the next unmarked or free chunk within the heap */
        while (true)
        {
            if (!OBJ_GET_FREE(pobj) 
                && (OBJ_GET_GCVAL(pobj) == pmHeap.gcval)
                && ((uint8_t *)pobj < &pmHeap.base[PM_HEAP_SIZE])) {
            
                // we're at a valid object. run the iterator if we've got one.
                if (pfIterator != NULL) {
                    retval = (*pfIterator)(pobj);
                    PM_RETURN_IF_ERROR(retval);
                }
            } else {
                break;
            }
            
            pobj = (pPmObj_t)((uint8_t *)pobj + OBJ_GET_SIZE(pobj));
        }

        /* Stop if reached the end of the heap */
        if ((uint8_t *)pobj >= &pmHeap.base[PM_HEAP_SIZE])
        {
            break;
        }

        /* Accumulate the sizes of all consecutive unmarked or free chunks */
        totalchunksize = 0;

        /* Coalesce all contiguous free chunks */
        pchunk = (pPmHeapDesc_t)pobj;
        while (OBJ_GET_FREE(pchunk)
               || (!OBJ_GET_FREE(pchunk)
                   && (OBJ_GET_GCVAL(pchunk) != pmHeap.gcval)))
        {
            if ((totalchunksize + OBJ_GET_SIZE(pchunk))
                > HEAP_MAX_FREE_CHUNK_SIZE)
            {
                break;
            }
            totalchunksize = totalchunksize + OBJ_GET_SIZE(pchunk);

            /*
             * If the chunk is already free, unlink it because its size
             * is about to change
             */
            if (OBJ_GET_FREE(pchunk))
            {
                retval = heap_unlinkFromFreelist(pchunk);
                PM_RETURN_IF_ERROR(retval);
            }

            /* Otherwise free and reclaim the unmarked chunk */
            else
            {
                OBJ_SET_TYPE(pchunk, 0);
                OBJ_SET_FREE(pchunk, 1);
            }

            C_DEBUG_PRINT(VERBOSITY_HIGH, "heap_gcSweep(), id=%p, s=%u\n",
                          pchunk, OBJ_GET_SIZE(pchunk));

            /* Proceed to the next chunk */
            pchunk = (pPmHeapDesc_t)
                ((uint8_t *)pchunk + OBJ_GET_SIZE(pchunk));

            /* Stop if it's past the end of the heap */
            if ((uint8_t *)pchunk >= &pmHeap.base[PM_HEAP_SIZE])
            {
                break;
            }
        }

        /* Set the heap descriptor data */
        OBJ_SET_FREE(pobj, 1);
        OBJ_SET_SIZE(pobj, totalchunksize);

        /* Insert chunk into free list */
        retval = heap_linkToFreelist((pPmHeapDesc_t)pobj);
        PM_RETURN_IF_ERROR(retval);

        /* Continue to the next chunk */
        pobj = (pPmObj_t)pchunk;
    }
    
    return PM_RET_OK;
}

PmReturn_t
heap_gcRun(void)
{
    PmReturn_t retval;

#ifdef HAVE_PROFILER
    gVmGlobal.profiler_flags[IN_GC] = true;
    profiler_gcrun();
#endif

    C_DEBUG_PRINT(VERBOSITY_LOW, "heap_gcRun()\n");
    /*heap_dump();*/

    retval = heap_gcMarkRoots();
    PM_RETURN_IF_ERROR(retval);
    retval = heap_gcWalk(NULL);
    
#ifdef HAVE_PROFILER
    gVmGlobal.profiler_flags[IN_GC] = false;
#endif

    /*heap_dump();*/
    return retval;
}


/* Enables or disables automatic garbage collection */
PmReturn_t
heap_gcSetAuto(uint8_t auto_gc)
{
    pmHeap.auto_gc = auto_gc;
    return PM_RET_OK;
}


PmReturn_t
heap_verify(pPmObj_t *r_pbool)
{
    PmReturn_t retval = PM_RET_OK;
    uint8_t *paddr;
    uint8_t *pend;
    uint32_t size;
    pPmObj_t pobj;

    paddr = &pmHeap.base[0];
    pend  = paddr + PM_HEAP_SIZE;
    
    while (paddr < pend)
    {
        pobj = (pPmObj_t) paddr;
        size = OBJ_GET_SIZE(pobj);
        /*
        lib_printf("addr: %p, size: %d (%x), od: 0x%08X\n", 
                     paddr, size, size >> 2, pobj->od);
        */
        if (size == 0)
        {
            break;
        }
        paddr += size;
    }

    if (paddr == pend)
    {
        *r_pbool = PM_TRUE;
    }
    else
    {
        *r_pbool = PM_FALSE;
    }

    return retval;
}
#endif /* HAVE_GC */
