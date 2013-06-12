/* vm/seq.h
 *
 * This file is Copyright 2003, 2006, 2007, 2009 Dean Hall.
 * Copyright 2012 Rice University.
 *
 * This file is part of the Owl Embedded Python System and is provided under
 * the MIT open-source license. See the LICENSE and COPYING files for details
 * about your rights to use, modify, and distribute Owl.
 *
 */

#ifndef __SEQ_H__
#define __SEQ_H__


/**
 * \file
 * \brief Sequence Header
 */


/**
 * Sequence Iterator Object
 *
 * Instances of this object are created by GET_ITER and used by FOR_ITER.
 * Stores a pointer to a sequence and an index int16_t.
 */
typedef struct PmSeqIter_s
{
    /** Object descriptor */
    PmObjDesc_t od;

    /** Sequence object */
    pPmObj_t si_sequence;

    /** Index value */
    int16_t si_index;
} PmSeqIter_t,
 *pPmSeqIter_t;


/**
 * Compares two sequences for equality
 *
 * @param   pobj1 Ptr to first sequence.
 * @param   pobj2 Ptr to second sequence.
 * @return  C_EQ if the sequences are equivalent, C_NEQ otherwise.
 */
int8_t seq_isEqual(pPmObj_t pobj1, pPmObj_t pobj2);

/**
 * Compares two sequences for ordering.
 *
 * @param   pobj1 Ptr to first sequence.
 * @param   pobj2 Ptr to second sequence.
 * @param   match True if called from obj_match and False if not
 * @param   punb_dict C_NULL if not called from obj_match, else dictionary of unbound objects
 * @return  C_EQ if the seuqences are equivalent, C_GT if pobj2 > pobj1, C_LT otherwise.
 */
int8_t seq_compare(pPmObj_t pobj1, pPmObj_t pobj2, int8_t match, pPmObj_t punb_dict);

/**
 * Returns the length of the sequence
 *
 * @param   pobj Ptr to  sequence.
 * @param   r_index Return arg, length of sequence
 * @return  Return status
 */
PmReturn_t seq_getLength(pPmObj_t pobj, int16_t *r_index);

/**
 * Returns the object from sequence[index]
 *
 * @param   pobj Ptr to sequence object to get object from
 * @param   index Int index into the sequence
 * @param   r_pobj Return arg, object from sequence
 * @return  Return status
 */
PmReturn_t seq_getSubscript(pPmObj_t pobj, int16_t index, pPmObj_t *r_pobj);

/**
 * Returns the object from sequence at index, for internal VM use only
 *  (will return values from non-subscriptable sequences)
 *
 * @param   pobj Ptr to sequence object to get object from
 * @param   index Int index into the sequence
 * @param   r_pobj Return arg, object from sequence
 * @return  Return status
 */
PmReturn_t seq_getItem(pPmObj_t pobj, int16_t index, pPmObj_t *r_pobj);

/**
 * Returns the next item from the sequence iterator object
 *
 * @param   pobj Ptr to sequence iterator.
 * @param   r_pitem Return arg, pointer to next item from sequence.
 * @return  Return status.
 */
PmReturn_t seqiter_getNext(pPmObj_t pobj, pPmObj_t *r_pitem);


/**
 * Returns a new sequence iterator object
 *
 * @param   pobj Ptr to sequence.
 * @param   r_pobj Return by reference, new sequence iterator
 * @return  Return status.
 */
PmReturn_t seqiter_new(pPmObj_t pobj, pPmObj_t *r_pobj);


#ifdef HAVE_PRINT
/**
 * Print sequence
 *
 * @param   pobj Ptr to sequence.
 * @return  Return status.
 */
PmReturn_t seq_print(pPmObj_t pobj);
#endif /* HAVE_PRINT */

#ifdef HAVE_SLICING
/**
 * Returns a new sequence iterator object
 *
 * @param   pobj Ptr to sequence.
 * @param   start start of slice
 * @param   end end of slice
 * @param   to_end true if slice should go to the end of the sequence
 * @param   r_pobj Return by reference, new slice
 * @return  Return status.
 */
PmReturn_t seq_slice(pPmObj_t pobj, int16_t start, int16_t end, bool to_end, pPmObj_t *r_pobj);
#endif /* HAVE_SLICING */

#endif /* __SEQ_H__ */
