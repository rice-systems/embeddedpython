/* vm/heap.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */


#ifndef __HEAP_H__
#define __HEAP_H__


/**
 * \file
 * \brief VM Heap
 *
 * VM heap header.
 */


/**
 * The threshold of heap.avail under which the interpreter will run the GC
 * just before starting a native session.
 */
#define HEAP_GC_NF_THRESHOLD (4096)


#ifdef __DEBUG__
#define DEBUG_PRINT_HEAP_AVAIL(s) \
    do { uint16_t n; heap_getAvail(&n); printf(s "heap avail = %d\n", n); } \
    while (0)
#else
#define DEBUG_PRINT_HEAP_AVAIL(s)
#endif


/**
 * Initializes the heap for use.
 *
 * @return  nothing.
 */
PmReturn_t heap_init(void);


/**
 * Returns a pointer to the heap.
 *
 * @return base address of heap
 */
uint8_t *heap_baseAddr(void);

/**
 * Tests if pointer is within the heap
 *
 * @return Boolean result
 */

bool heap_addrInHeap(uint8_t const *paddr);

/**
 * Returns a free chunk from the heap.
 *
 * The chunk will be at least the requested size.
 * The actual size can be found in the return chunk's od.od_size.
 *
 * @param   requestedsize Requested size of the chunk in bytes.
 * @param   r_pchunk Addr of ptr to chunk (return).
 * @return  Return code
 */
PmReturn_t heap_getChunk(uint16_t requestedsize, uint8_t **r_pchunk);

/**
 * Places the chunk back in the heap.
 *
 * @param   ptr Pointer to object to free.
 */
PmReturn_t heap_freeChunk(pPmObj_t ptr);

/** @return  Return number of bytes available in the heap */
#if PM_HEAP_SIZE > 65535
uint32_t
#else
uint16_t
#endif
  heap_getAvail(void);

/** Print the free list */
void heap_gcPrintFreelist(void);


#ifdef HAVE_GC
/**
 * Runs the mark-sweep garbage collector
 *
 * @return  Return code
 */
PmReturn_t heap_gcRun(void);

// walk through the entire heap.
PmReturn_t heap_gcWalk(PmReturn_t (*pfIterator)(pPmObj_t));

/**
 * Enables (if true) or disables automatic garbage collection
 *
 * @param   bool Value to enable or disable auto GC
 * @return  Return code
 */
PmReturn_t heap_gcSetAuto(uint8_t auto_gc);

PmReturn_t heap_verify(pPmObj_t *r_pbool);
#endif /* HAVE_GC */

#endif /* __HEAP_H__ */
