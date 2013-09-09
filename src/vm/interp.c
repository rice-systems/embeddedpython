/* vm/interp.c
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
#define __FILE_ID__ 0x09


/**
 * \file
 * \brief VM Interpreter
 *
 * VM interpreter operations.
 */


#include "pm.h"

extern PmReturn_t (*std_nat_fxn_table[]) (pPmFrame_t *, int8_t, pPmObj_t *);
extern PmReturn_t (*usr_nat_fxn_table[]) (pPmFrame_t *, int8_t, pPmObj_t *);


extern bool profiler_locked;

#ifdef STACK_PROTECTION
PmReturn_t
pm_push_protected(pPmObj_t pobj) {
    PmReturn_t retval = PM_RET_OK;

    if (((void *) FP->fo_sp) >= ((void *) FP->fo_last_stack_slot))
    {
        PM_RAISE_WITH_INFO(retval, PM_RET_EX_SYS, "stack overflow");
        return retval;
    }
    else
    {
        (*(SP++) = (pobj));
    }
    
    return retval;
}
#endif

/** gets the argument (S16) from the instruction stream 
 *
 *  Pointer craziness to read 16 bits and increment by 2 bytes
 */
#define GET_ARG()       (*(*(int16_t **)&IP)++)

PmReturn_t
interpret(const uint8_t returnOnNoThreads)
{
    PmReturn_t retval = PM_RET_OK;

#ifdef STACK_PROTECTION
    PmReturn_t retval_stackp = PM_RET_OK;
#endif

    pPmObj_t pobj1 = C_NULL;
    pPmObj_t pobj2 = C_NULL;
    pPmObj_t pobj3 = C_NULL;
    int16_t t16 = 0;
    int8_t t8 = 0;
    uint8_t bc;

    /* Activate a thread the first time */
    retval = interp_reschedule();
    PM_RETURN_IF_ERROR(retval);

    /* Interpret loop */
    for (;;)
    {
        
        if (RUNNINGTHREAD == C_NULL)
        {
            if (returnOnNoThreads && (gVmGlobal.threadList->length == 0))
            {
                /* User chose to return on no threads left */
                return retval;
            }

            /*
             * Without a frame there is nothing to execute, so reschedule
             * (possibly activating a recently added thread).
             */
            retval = interp_reschedule();
            PM_BREAK_IF_ERROR(retval);
            continue;
        }

        switch (RUNNINGTHREAD->interpctrl)
        {
        case INTERP_CTRL_ERR:
            PM_REPORT_IF_ERROR(retval);
      
            if (FP->fo_except)
            {

                pobj1 = (pPmObj_t)FP->fo_except;
                while (FP != (pPmFrame_t)pobj1) {
                    if (FP->fo_isImport) {
                        /* Get module name and remove from gVmGlobal.modules */
                        pobj2 = (pPmObj_t)co_getNames(FP->fo_func->f_co);
                        retval = tuple_getItem((pPmTuple_t)pobj2, 
                            ((pPmTuple_t)pobj2)->length-1, &pobj2);
                        retval = dict_delItem(gVmGlobal.modules, pobj2);
                        PM_RETURN_IF_ERROR(retval);
                    }
                    FP = FP->fo_back;
                }

                /*
                 * If a fake "exception handling" frame was installed,
                 * "deliver" the exception by returning to it.
                 *
                 * This would go away if/when real exceptions are
                 * implemented.
                 */
                RUNNINGTHREAD->interpctrl = INTERP_CTRL_RUN;
                PM_PUSH(PM_NONE);
                continue;
            }                
            /* Fall through and exit */

        case INTERP_CTRL_EXIT:
            /* Thread has exited, reschedule */
            retval = thread_destroy(RUNNINGTHREAD);
            PM_BREAK_IF_ERROR(retval);
            RUNNINGTHREAD = C_NULL;
            retval = interp_reschedule();
            PM_BREAK_IF_ERROR(retval);
            continue;

        case INTERP_CTRL_RUN:
            /* Continue running this thread */
            break;

        case INTERP_CTRL_RESCHED:
            /* Reschedule thread */
            RUNNINGTHREAD->interpctrl = INTERP_CTRL_RUN;
            retval = interp_reschedule();
            PM_BREAK_IF_ERROR(retval);
            continue;            

        case INTERP_CTRL_CYIELD:
            /* Reschedule thread */
            RUNNINGTHREAD->interpctrl = INTERP_CTRL_CCONT;
            retval = interp_reschedule();
            PM_BREAK_IF_ERROR(retval);
            continue;

        case INTERP_CTRL_CCONT:
            /* Run C continuation */
            retval = RUNNINGTHREAD->pcfn(&TOS);
            PM_BREAK_IF_ERROR(retval);
            continue;

        case INTERP_CTRL_WAIT:
            // TODO: Fatal error. We need some mechanism to alert those.
            lib_printf("should never get here inside of wait.");
            C_ASSERT(0);
            continue;
        }

        /* Reschedule threads if flag is true? */
        if (gVmGlobal.reschedule)
        {
            retval = interp_reschedule();
            PM_BREAK_IF_ERROR(retval);
        }

        /* Get byte; the func post-incrs IP */
        bc = *IP++;

        RUNNINGTHREAD->bytecodes++;

#ifdef HAVE_PROFILER
        profiler_bytecode(bc);
#endif
        
        switch (bc)
        {
            case POP_TOP:
                pobj1 = PM_POP();
                continue;

            case ROT_TWO:
                pobj1 = TOS;
                TOS = TOS1;
                TOS1 = pobj1;
                continue;

            case ROT_THREE:
                pobj1 = TOS;
                TOS = TOS1;
                TOS1 = TOS2;
                TOS2 = pobj1;
                continue;

            case DUP_TOP:
                pobj1 = TOS;
                PM_PUSH(pobj1);
                continue;

            case ROT_FOUR:
                pobj1 = TOS;
                TOS = TOS1;
                TOS1 = TOS2;
                TOS2 = TOS3;
                TOS3 = pobj1;
                continue;

            case NOP:
                continue;

            case UNARY_POSITIVE:
                /* Raise TypeError if TOS is not an int */
                if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT)
#ifdef HAVE_FLOAT
                    && (OBJ_GET_TYPE(TOS) != OBJ_TYPE_FLT)
#endif /* HAVE_FLOAT */
                    )
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* When TOS is an int, this is a no-op */
                continue;

            case UNARY_NEGATIVE:
#ifdef HAVE_FLOAT
                if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_FLT)
                {
                    retval = float_negative(TOS, &pobj2);
                }
                else
#endif /* HAVE_FLOAT */
                {
                    retval = int_negative((pPmInt_t)TOS, (pPmInt_t *)&pobj2);
                }
                PM_BREAK_IF_ERROR(retval);
                TOS = pobj2;
                continue;

            case UNARY_NOT:
                pobj1 = PM_POP();
                if (obj_isFalse(pobj1))
                {
                    PM_PUSH(PM_TRUE);
                }
                else
                {
                    PM_PUSH(PM_FALSE);
                }
                continue;

            /* #244 Add support for the backtick operation (UNARY_CONVERT) */
            case UNARY_CONVERT:
                /* raise a system error */
                PM_RAISE(retval, PM_RET_EX_SYS);
                break;

            case UNARY_INVERT:
                /* Raise TypeError if it's not an int */
                if (OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT)
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* Otherwise perform bit-wise complement */
                retval = int_bitInvert((pPmInt_t)TOS, (pPmInt_t *)&pobj2);
                PM_BREAK_IF_ERROR(retval);
                TOS = pobj2;
                continue;

            case LIST_APPEND:
                /* list_append will raise a TypeError if TOS1 is not a list */
                t16 = GET_ARG();
                /* List */
                pobj1 = STACK(t16);
                /* Item to append */
                pobj2 = PM_POP();
                retval = list_append((pPmList_t)pobj1, pobj2);
                PM_BREAK_IF_ERROR(retval);
                continue;

            case BINARY_POWER:
            case INPLACE_POWER:

#ifdef HAVE_FLOAT
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FLT)
                    || (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_FLT))
                {
                    /* Calculate float power */
                    retval = float_op(TOS1, TOS, &pobj3, 'P');
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
#endif /* HAVE_FLOAT */

                /* Calculate integer power */
                retval = int_pow((pPmInt_t)TOS1, (pPmInt_t)TOS, 
                                 (pPmInt_t *)&pobj3);
                PM_BREAK_IF_ERROR(retval);

                /* Set return value */
                SP--;
                TOS = pobj3;
                continue;

            case GET_ITER:
#ifdef HAVE_GENERATORS
                /* Raise TypeError if TOS is an instance, but not iterable */
                if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLI)
                {
                    retval = class_getAttr(TOS, CONSTnext, &pobj1);
                    if (retval != PM_RET_OK)
                    {
                        PM_RAISE(retval, PM_RET_EX_TYPE);
                        break;
                    }
                }
                else
#endif /* HAVE_GENERATORS */
                {
                    /* Convert sequence to sequence-iterator */
                    retval = seqiter_new(TOS, &pobj1);
                    PM_BREAK_IF_ERROR(retval);

                    /* Put sequence-iterator on top of stack */
                    TOS = pobj1;
                }
                continue;

            case BINARY_MULTIPLY:
            case INPLACE_MULTIPLY:
                /* If both objs are ints, perform the op */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT))
                {
                    retval = int_new(((pPmInt_t)TOS1)->val *
                                     ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

#ifdef HAVE_FLOAT
                else if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FLT)
                         || (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_FLT))
                {
                    retval = float_op(TOS1, TOS, &pobj3, '*');
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
#endif /* HAVE_FLOAT */

#ifdef HAVE_REPLICATION
                /* If it's a list replication operation */
                else if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                         && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_LST))
                {
                    t16 = (int16_t)((pPmInt_t)TOS)->val;
                    if (t16 < 0)
                    {
                        t16 = 0;
                    }

                    retval = list_replicate((pPmList_t)TOS1, t16, 
                                            (pPmList_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* ...and in the other direction */
                else if ((OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT)
                         && (OBJ_GET_TYPE(TOS) == OBJ_TYPE_LST))
                {
                    t16 = (int16_t)((pPmInt_t)TOS1)->val;
                    if (t16 < 0)
                    {
                        t16 = 0;
                    }

                    retval = list_replicate((pPmList_t)TOS, t16, 
                                            (pPmList_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* If it's a tuple replication operation */
                else if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                         && ((OBJ_GET_TYPE(TOS1) == OBJ_TYPE_TUP)
                             || (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_PTP)))
                {
                    t16 = (int16_t)((pPmInt_t)TOS)->val;
                    if (t16 < 0)
                    {
                        t16 = 0;
                    }

                    retval = tuple_replicate((pPmTuple_t)TOS1, t16, 
                                             &pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
                
                /* ...and in the other direction */
                else if ((OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT)
                         && ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_TUP)
                             || (OBJ_GET_TYPE(TOS) == OBJ_TYPE_PTP)))
                {
                    t16 = (int16_t)((pPmInt_t)TOS1)->val;
                    if (t16 < 0)
                    {
                        t16 = 0;
                    }

                    retval = tuple_replicate((pPmTuple_t)TOS, t16, 
                                             &pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* If it's a string replication operation */
                else if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                         && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_STR))
                {
                    t16 = (int16_t)((pPmInt_t)TOS)->val;
                    if (t16 < 0)
                    {
                        t16 = 0;
                    }

                    retval = string_replicate((pPmString_t)TOS1, t16, 
                                              (pPmString_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* ...and in the other direction */
                else if ((OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT)
                         && (OBJ_GET_TYPE(TOS) == OBJ_TYPE_STR))
                {
                    t16 = (int16_t)((pPmInt_t)TOS1)->val;
                    if (t16 < 0)
                    {
                        t16 = 0;
                    }

                    retval = string_replicate((pPmString_t)TOS, t16, 
                                              (pPmString_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
#endif /* HAVE_REPLICATION */

                /* Otherwise raise a TypeError */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

            case BINARY_DIVIDE:
            case INPLACE_DIVIDE:
            case BINARY_FLOOR_DIVIDE:
            case INPLACE_FLOOR_DIVIDE:

#ifdef HAVE_FLOAT
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FLT)
                    || (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_FLT))
                {
                    retval = float_op(TOS1, TOS, &pobj3, '/');
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
#endif /* HAVE_FLOAT */

                /* Raise TypeError if args aren't ints */
                if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT)
                    || (OBJ_GET_TYPE(TOS1) != OBJ_TYPE_INT))
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* Raise ZeroDivisionError if denominator is zero */
                if (((pPmInt_t)TOS)->val == 0)
                {
                    PM_RAISE(retval, PM_RET_EX_ZDIV);
                    break;
                }

                /* Otherwise perform operation */
                retval = int_new(((pPmInt_t)TOS1)->val /
                                 ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                PM_BREAK_IF_ERROR(retval);
                SP--;
                TOS = pobj3;
                continue;

            case BINARY_MODULO:
            case INPLACE_MODULO:

#ifdef HAVE_STRING_FORMAT
                /* If it's a string, perform string format */
                if (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_STR)
                {
                    retval = string_format((pPmString_t)TOS1, TOS, &pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
#endif /* HAVE_STRING_FORMAT */

#ifdef HAVE_FLOAT
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FLT)
                    || (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_FLT))
                {
                    retval = float_op(TOS1, TOS, &pobj3, '%');
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
#endif /* HAVE_FLOAT */

                /* Raise TypeError if args aren't ints */
                if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT)
                    || (OBJ_GET_TYPE(TOS1) != OBJ_TYPE_INT))
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* Raise ZeroDivisionError if denominator is zero */
                if (((pPmInt_t)TOS)->val == 0)
                {
                    PM_RAISE(retval, PM_RET_EX_ZDIV);
                    break;
                }

                /* Otherwise perform operation */
                retval = int_new(((pPmInt_t)TOS1)->val %
                                 ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                PM_BREAK_IF_ERROR(retval);
                SP--;
                TOS = pobj3;
                continue;

            case STORE_MAP:
                /* #213: Add support for Python 2.6 bytecodes */
                C_ASSERT(OBJ_GET_TYPE(TOS2) == OBJ_TYPE_DIC);
                retval = dict_setItem((pPmDict_t)TOS2, TOS, TOS1);
                PM_BREAK_IF_ERROR(retval);
                SP -= 2;
                continue;

            case BINARY_ADD:
            case INPLACE_ADD:

#ifdef HAVE_FLOAT
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FLT)
                    || (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_FLT))
                {
                    retval = float_op(TOS1, TOS, &pobj3, '+');
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
#endif /* HAVE_FLOAT */

                /* If both objs are ints, perform the op */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT))
                {
                    retval = int_new(((pPmInt_t)TOS1)->val +
                                     ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* #242: If both objs are strings, perform concatenation */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_STR)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_STR))
                {
                    retval = string_concat((pPmString_t)TOS1,
                                           (pPmString_t)TOS,
                                           &pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* Otherwise raise a TypeError */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

            case BINARY_SUBTRACT:
            case INPLACE_SUBTRACT:

#ifdef HAVE_FLOAT
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FLT)
                    || (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_FLT))
                {
                    retval = float_op(TOS1, TOS, &pobj3, '-');
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }
#endif /* HAVE_FLOAT */

                /* If both objs are ints, perform the op */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT))
                {
                    retval = int_new(((pPmInt_t)TOS1)->val -
                                     ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* Otherwise raise a TypeError */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

            case BINARY_SUBSCR:
                /* Implements TOS = TOS1[TOS]. */

                if (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_DIC)
                {
                    retval = dict_getItem((pPmDict_t)TOS1, TOS, &pobj3);
                }
                else
                {
                    /* Raise a TypeError if index is not an Integer or Bool */
                    if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT)
                        && (OBJ_GET_TYPE(TOS) != OBJ_TYPE_BOL))
                    {
                        PM_RAISE(retval, PM_RET_EX_TYPE);
                        break;
                    }

                    /* Ensure the index doesn't overflow */
                    C_ASSERT(((pPmInt_t)TOS)->val <= 0x0000FFFF);
                    t16 = (int16_t)((pPmInt_t)TOS)->val;

                    retval = seq_getSubscript(TOS1, t16, &pobj3);
                }
                PM_BREAK_IF_ERROR(retval);
                SP--;
                TOS = pobj3;
                continue;

#ifdef HAVE_SLICING
            case SLICE_0:
                retval = seq_slice(TOS, 0, -1, true, &pobj3);

                PM_BREAK_IF_ERROR(retval);
                TOS = pobj3;
                continue;

            case SLICE_1:
                /* Raise a TypeError if index is not an Integer */
                if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT))
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* Ensure the index doesn't overflow */
                C_ASSERT(((pPmInt_t)TOS)->val <= 0x0000FFFF);

                retval = seq_slice(TOS1, ((pPmInt_t)TOS)->val, -1, true, &pobj3);

                PM_BREAK_IF_ERROR(retval);
                SP--;
                TOS = pobj3;
                continue;
                
            case SLICE_2:
                /* Raise a TypeError if index is not an Integer */
                if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT))
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* Ensure the index doesn't overflow */
                C_ASSERT(((pPmInt_t)TOS)->val <= 0x0000FFFF);

                retval = seq_slice(TOS1, 0, ((pPmInt_t)TOS)->val, false, &pobj3);

                PM_BREAK_IF_ERROR(retval);
                SP--;
                TOS = pobj3;
                continue;
                
            case SLICE_3:
                /* Raise a TypeError if indexes are not Integers */
                if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT))
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }
                
                if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT))
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* Ensure the index doesn't overflow */
                C_ASSERT(((pPmInt_t)TOS)->val <= 0x0000FFFF);
                C_ASSERT(((pPmInt_t)TOS1)->val <= 0x0000FFFF);

                retval = seq_slice(TOS2, ((pPmInt_t)TOS1)->val, ((pPmInt_t)TOS)->val, false, &pobj3);

                PM_BREAK_IF_ERROR(retval);
                SP--;
                SP--;
                TOS = pobj3;
                continue;
#endif

#ifdef HAVE_FLOAT
            /* #213: Add support for Python 2.6 bytecodes */
            case BINARY_TRUE_DIVIDE:
            case INPLACE_TRUE_DIVIDE:

                /* Perform division; float_op() checks for types and zero-div */
                retval = float_op(TOS1, TOS, &pobj3, '/');
                PM_BREAK_IF_ERROR(retval);
                SP--;
                TOS = pobj3;
                continue;
#endif /* HAVE_FLOAT */

            case STORE_SUBSCR:
                /* Implements TOS1[TOS] = TOS2 */

                /* If it's a list */
                if (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_LST)
                {
                    /* Ensure subscr is an int or bool */
                    if ((OBJ_GET_TYPE(TOS) != OBJ_TYPE_INT)
                        && (OBJ_GET_TYPE(TOS) != OBJ_TYPE_BOL))
                    {
                        PM_RAISE(retval, PM_RET_EX_TYPE);
                        break;
                    }
                    /* Set the list item */
                    retval = list_setItem((pPmList_t)TOS1,
                                          (int16_t)(((pPmInt_t)TOS)->val),
                                          TOS2);
                    PM_BREAK_IF_ERROR(retval);
                    SP -= 3;
                    continue;
                }

                /* If it's a dict */
                if (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_DIC)
                {
                    /* Set the dict item */
                    retval = dict_setItem((pPmDict_t)TOS1, TOS, TOS2);
                    PM_BREAK_IF_ERROR(retval);
                    SP -= 3;
                    continue;
                }

                /* TypeError for all else */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

#ifdef HAVE_DEL
            case DELETE_SUBSCR:

                if ((OBJ_GET_TYPE(TOS1) == OBJ_TYPE_LST)
                    && (OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT))
                {
                    retval = list_delItem((pPmList_t)TOS1,
                                          (int16_t)((pPmInt_t)TOS)->val);
                }

                else if ((OBJ_GET_TYPE(TOS1) == OBJ_TYPE_DIC)
                         && (OBJ_GET_TYPE(TOS) <= OBJ_TYPE_HASHABLE_MAX))
                {
                    retval = dict_delItem((pPmDict_t)TOS1, TOS);
                }

                /* Raise TypeError if obj is not a list or dict */
                else
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                }

                PM_BREAK_IF_ERROR(retval);
                SP -= 2;
                continue;
#endif /* HAVE_DEL */

            case BINARY_LSHIFT:
            case INPLACE_LSHIFT:
                /* If both objs are ints, perform the op */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT))
                {
                    retval = int_new(((pPmInt_t)TOS1)->val <<
                                     ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* Otherwise raise a TypeError */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

            case BINARY_RSHIFT:
            case INPLACE_RSHIFT:
                /* If both objs are ints, perform the op */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT))
                {
                    retval = int_new(((pPmInt_t)TOS1)->val >>
                                     ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* Otherwise raise a TypeError */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

            case BINARY_AND:
            case INPLACE_AND:
                /* If both objs are ints, perform the op */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT))
                {
                    retval = int_new(((pPmInt_t)TOS1)->val &
                                     ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* Otherwise raise a TypeError */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

            case BINARY_XOR:
            case INPLACE_XOR:
                /* If both objs are ints, perform the op */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT))
                {
                    retval = int_new(((pPmInt_t)TOS1)->val ^
                                     ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* Otherwise raise a TypeError */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

            case BINARY_OR:
            case INPLACE_OR:
                /* If both objs are ints, perform the op */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_INT)
                    && (OBJ_GET_TYPE(TOS1) == OBJ_TYPE_INT))
                {
                    retval = int_new(((pPmInt_t)TOS1)->val |
                                     ((pPmInt_t)TOS)->val, (pPmInt_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    TOS = pobj3;
                    continue;
                }

                /* Otherwise raise a TypeError */
                PM_RAISE(retval, PM_RET_EX_TYPE);
                break;

#ifdef HAVE_PRINT
            case PRINT_EXPR:
                /* marshall string */
                t8 = 1;
            case PRINT_ITEM:
                /* Print out topmost stack element */
                if (bc == PRINT_ITEM)
                {
                    t8 = 0;
                }
                retval = obj_print(TOS, t8);
                PM_BREAK_IF_ERROR(retval);
                if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_NON)
                {
                    SP--;
                    continue;
                }
                SP--;
                if (bc != PRINT_EXPR)
                {
                    if (-1 == lib_printf(" "))
                    {
                        PM_RAISE(retval, PM_RET_EX_IO);
                        break;
                    }
                    continue;
                }
                /* If PRINT_EXPR, Fallthrough to print a newline */

            case PRINT_NEWLINE:
                if (-1 == lib_printf("\n"))
                {
                    PM_RAISE(retval, PM_RET_EX_IO);
                    break;
                }
                continue;
#endif /* HAVE_PRINT */

            case BREAK_LOOP:
            {
                pPmBlock_t pb1 = FP->fo_blockstack;

                /* Ensure there's a block */
                C_ASSERT(pb1 != C_NULL);

                /* Delete blocks until first loop block */
                while ((pb1->b_type != B_LOOP) && (pb1->next != C_NULL))
                {
                    pobj2 = (pPmObj_t)pb1;
                    pb1 = pb1->next;
                }

                /* Test again outside while loop */
                PM_BREAK_IF_ERROR(retval);

                /* Restore SP */
                SP = pb1->b_sp;

                /* Goto handler */
                IP = pb1->b_handler;

                /* Pop and delete this block */
                FP->fo_blockstack = pb1->next;
            }
                continue;

            case LOAD_LOCALS:
                /* Pushes locals dict of current frame */
                if (FP->fo_locals != C_NULL)
                {
                    PM_PUSH((pPmObj_t)FP->fo_locals);
                    continue;
                }
                else
                {
                    PM_RAISE_WITH_INFO(retval, PM_RET_EX_SYS,
                                       "no locals. (compiler error?)");
                    break;
                }

            case RETURN_VALUE:
                /* Get expiring frame's TOS */
                pobj2 = PM_POP();

#if 0 /*__DEBUG__*/
                /* #251: This safety check is disabled because it breaks ipm */
                /* #109: Check that stack should now be empty */
                /* If this is regular frame (not native and not a generator) */
                if ((FP != (pPmFrame_t)(&gVmGlobal.nativeframe)) &&
                    !(FP->fo_func->f_co->co_flags & CO_GENERATOR))
                {
                    /* Get this func's number of locals */
                    pobj3 = (pPmObj_t)(((uint8_t *)
                            (FP->fo_func->f_co->co_codeimgaddr))
                            + CI_NLOCALS_FIELD);
                    t8 = mem_getByte(FP->fo_func->f_co->co_memspace,
                                     (uint8_t const **)&pobj3);

                    /* An empty stack points one past end of locals */
                    C_ASSERT(SP == &(FP->fo_stack[t8]));
                }
#endif /* __DEBUG__ */

                /* Keep ref of expiring frame */
                pobj1 = (pPmObj_t)FP;
                C_ASSERT(OBJ_GET_TYPE(pobj1) == OBJ_TYPE_FRM);

                /* If no previous frame, quit thread */
                if (FP->fo_back == C_NULL)
                {
                    RUNNINGTHREAD->interpctrl = INTERP_CTRL_EXIT;
                    retval = PM_RET_OK;
                    break;
                }

                /* Otherwise return to previous frame */
                FP = FP->fo_back;

#ifdef HAVE_GENERATORS
                /* If returning function was a generator */
                if (co_getFlags(((pPmFrame_t)pobj1)->fo_func->f_co) & CO_GENERATOR)
                {
                    /* If a loop handler is in-place, use it and pop it */
                    if ((FP->fo_blockstack != C_NULL)
                        && (FP->fo_blockstack->b_type == B_LOOP))
                    {
                        SP = ((pPmBlock_t)pobj1)->b_sp;
                        IP = ((pPmBlock_t)pobj1)->b_handler;
                        FP->fo_blockstack = FP->fo_blockstack->next;
                    }

                    /* Otherwise, raise a StopIteration exception */
                    else
                    {
                        PM_RAISE(retval, PM_RET_EX_STOP);
                        break;
                    }
                }
                PM_BREAK_IF_ERROR(retval);
#endif /* HAVE_GENERATORS */

#ifdef HAVE_CLASSES
                /*
                 * If returning function was class initializer
                 * do not push a return object
                 */
                if (((pPmFrame_t)pobj1)->fo_isInit)
                {
                    /* Raise TypeError if __init__ did not return None */
                    if (OBJ_GET_TYPE(pobj2) != OBJ_TYPE_NON)
                    {
                        PM_RAISE(retval, PM_RET_EX_TYPE);
                        break;
                    }
                }
                else
#endif /* HAVE_CLASSES */

                /*
                 * Push frame's return val, except if the expiring frame
                 * was due to an import statement
                 */
                if (!(((pPmFrame_t)pobj1)->fo_isImport))
                {
                    PM_PUSH(pobj2);
                }
                continue;

#ifdef HAVE_IMPORTS
            case IMPORT_STAR:
                /* #102: Implement the remaining IMPORT_ bytecodes */
                /* Expect a module on the top of the stack */
                C_ASSERT(OBJ_GET_TYPE(TOS) == OBJ_TYPE_MOD);

                /* Update FP's locals or globals with those of the module on the stack */
                if (FP->fo_locals != C_NULL)
                {
                    retval = dict_update(FP->fo_locals, ((pPmFunc_t)TOS)->f_attrs);
                }
                else
                {
                    retval = dict_update(FP->fo_globals, ((pPmFunc_t)TOS)->f_attrs);
                }
                PM_BREAK_IF_ERROR(retval);

                SP--;
                continue;
#endif /* HAVE_IMPORTS */

#ifdef HAVE_GENERATORS
            case YIELD_VALUE:
                /* #207: Add support for the yield keyword */
                /* Get expiring frame's TOS */
                pobj1 = PM_POP();

                /* Raise TypeError if __init__ did not return None */
                /* (Yield means this is a generator) */
                if ((FP)->fo_isInit)
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* Return to previous frame */
                FP = FP->fo_back;

                /* Push yield value onto caller's TOS */
                PM_PUSH(pobj1);
                continue;
#endif /* HAVE_GENERATORS */

            case POP_BLOCK:
                /* Get ptr to top block */
                pobj1 = (pPmObj_t)FP->fo_blockstack;

                /* If there's no block, raise SystemError */
                C_ASSERT(pobj1 != C_NULL);

                /* Pop block */
                FP->fo_blockstack = FP->fo_blockstack->next;

                /* Set stack to previous level, jump to code outside block */
                SP = ((pPmBlock_t)pobj1)->b_sp;

                /* RIXNER: is POP_BLOCK really supposed to change the
                 *    IP?  I don't think so.  It works for loops, but
                 *    I don't think it works for exceptions.  I'm
                 *    pretty sure loops continue to work if you
                 *    comment out this line.
                 */
                IP = ((pPmBlock_t)pobj1)->b_handler;
                continue;

#ifdef HAVE_CLASSES
            case BUILD_CLASS:
                /* Create and push new class */
                retval = class_new(TOS, TOS1, TOS2, &pobj2);
                PM_BREAK_IF_ERROR(retval);
                SP -= 2;
                TOS = pobj2;
                continue;
#endif /* HAVE_CLASSES */


            /***************************************************
             * All bytecodes after 90 (0x5A) have a 2-byte arg
             * that needs to be swallowed using GET_ARG().
             **************************************************/

            case STORE_NAME:
                /* Get name index */
                t16 = GET_ARG();

                /* Get object to store */
                pobj1 = PM_POP();

                /* Get key */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Set key=val in current frame's locals dict */
                if (FP->fo_locals != C_NULL)
                {
                    retval = dict_setItem(FP->fo_locals, pobj2, pobj1);
                }
                else
                {
                    PM_RAISE_WITH_INFO(retval, PM_RET_EX_SYS, "no locals dict found on STORE_NAME");
                    break;
                }

                PM_BREAK_IF_ERROR(retval);
                continue;

#ifdef HAVE_DEL
            case DELETE_NAME:
                /* Get name index */
                t16 = GET_ARG();

                /* Get key */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Remove key,val pair from current frame's locals dict */
                /* This may not be correct. Should we remove it from the globals? */
                if (FP->fo_locals != C_NULL)
                {
                    retval = dict_delItem(FP->fo_locals, pobj2);
                    PM_BREAK_IF_ERROR(retval);
                }
                continue;
#endif /* HAVE_DEL */

            case UNPACK_SEQUENCE:
                /* Get ptr to sequence */
                pobj1 = PM_POP();

                /*
                 * Get the length of the sequence; this will
                 * raise TypeError if obj is not a sequence.
                 *
                 * #59: Unpacking to a Dict shall not be supported
                 */
                retval = seq_getLength(pobj1, &t16);
                if (retval != PM_RET_OK)
                {
                    t16 = GET_ARG();
                    break;
                }

                /* Raise ValueError if seq length does not match num args */
                if (t16 != GET_ARG())
                {
                    PM_RAISE(retval, PM_RET_EX_VAL);
                    break;
                }

                /* Push sequence's objs onto stack */
                for (; --t16 >= 0;)
                {
                    retval = seq_getSubscript(pobj1, t16, &pobj2);
                    PM_BREAK_IF_ERROR(retval);
                    PM_PUSH(pobj2);
                }

                /* Test again outside the for loop */
                PM_BREAK_IF_ERROR(retval);
                continue;

            case FOR_ITER:
                t16 = GET_ARG();

#ifdef HAVE_GENERATORS
                /* If TOS is an instance, call next method */
                if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLI)
                {
                    /* Get the next() func */
                    retval = class_getAttr(TOS, CONSTnext, &pobj1);
                    PM_BREAK_IF_ERROR(retval);

                    /* Push the func and instance as an arg */
                    pobj2 = TOS;
                    PM_PUSH(pobj1);
                    PM_PUSH(pobj2);
                    t16 = 1;

                    /* Ensure pobj1 is the func */
                    goto CALL_FUNC_FOR_ITER;
                }
                else
#endif /* HAVE_GENERATORS */
                {
                    /* Get the next item in the sequence iterator */
                    retval = seqiter_getNext(TOS, &pobj2);
                }

                /* Catch StopIteration early: pop iterator and break loop */
                if (retval == PM_RET_EX_STOP)
                {
                    SP--;
                    retval = PM_RET_OK;
                    IP += t16;
                    continue;
                }
                PM_BREAK_IF_ERROR(retval);

                /* Push the next item onto the stack */
                PM_PUSH(pobj2);
                continue;

            case STORE_ATTR:
                /* TOS.name = TOS1 */
                /* Get names index */
                t16 = GET_ARG();

                /* Get attrs dict from obj */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FXN)
                    || (OBJ_GET_TYPE(TOS) == OBJ_TYPE_MOD))
                {
                    pobj2 = (pPmObj_t)((pPmFunc_t)TOS)->f_attrs;
                }

#ifdef HAVE_CLASSES
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLO)
                {
                    pobj2 = (pPmObj_t)((pPmClass_t)TOS)->cl_attrs;
                }
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLI)
                {
                    pobj2 = (pPmObj_t)((pPmInstance_t)TOS)->cli_attrs;
                }
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_MTH)
                {
                    pobj2 = (pPmObj_t)((pPmMethod_t)TOS)->m_attrs;
                }
#endif /* HAVE_CLASSES */

                /* Other types result in an AttributeError */
                else
                {
                    PM_RAISE(retval, PM_RET_EX_ATTR);
                    break;
                }

                /* If attrs is not a dict, raise SystemError */
                if (OBJ_GET_TYPE(pobj2) != OBJ_TYPE_DIC)
                {
                    PM_RAISE(retval, PM_RET_EX_SYS);
                    break;
                }

                /* Get name/key obj */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj3);
                PM_BREAK_IF_ERROR(retval);

                /* Set key=val in obj's dict */
                retval = dict_setItem((pPmDict_t)pobj2, pobj3, TOS1);
                PM_BREAK_IF_ERROR(retval);
                SP -= 2;
                continue;

#ifdef HAVE_DEL
            case DELETE_ATTR:
                /* del TOS.name */
                /* Get names index */
                t16 = GET_ARG();

                /* Get attrs dict from obj */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FXN)
                    || (OBJ_GET_TYPE(TOS) == OBJ_TYPE_MOD))
                {
                    pobj2 = (pPmObj_t)((pPmFunc_t)TOS)->f_attrs;
                }

#ifdef HAVE_CLASSES
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLO)
                {
                    pobj2 = (pPmObj_t)((pPmClass_t)TOS)->cl_attrs;
                }
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLI)
                {
                    pobj2 = (pPmObj_t)((pPmInstance_t)TOS)->cli_attrs;
                }
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_MTH)
                {
                    pobj2 = (pPmObj_t)((pPmMethod_t)TOS)->m_attrs;
                }
#endif /* HAVE_CLASSES */

                /* Other types result in an AttributeError */
                else
                {
                    PM_RAISE(retval, PM_RET_EX_ATTR);
                    break;
                }

                /* If attrs is not a dict, raise SystemError */
                if (OBJ_GET_TYPE(pobj2) != OBJ_TYPE_DIC)
                {
                    PM_RAISE(retval, PM_RET_EX_SYS);
                    break;
                }

                /* Get name/key obj */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj3);
                PM_BREAK_IF_ERROR(retval);

                /* Remove key,val from obj's dict */
                retval = dict_delItem((pPmDict_t)pobj2, pobj3);

                /* Raise an AttributeError if key is not found */
                if (retval == PM_RET_EX_KEY)
                {
                    PM_RAISE(retval, PM_RET_EX_ATTR);
                }

                PM_BREAK_IF_ERROR(retval);
                SP--;
                continue;
#endif /* HAVE_DEL */

            case STORE_GLOBAL:
                /* Get name index */
                t16 = GET_ARG();
                
                /* Get object to store */
                pobj1 = PM_POP();

                /* Get key */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Set key=val in global dict */
                retval = dict_setItem(FP->fo_globals, pobj2, pobj1);

                PM_BREAK_IF_ERROR(retval);
                continue;

#ifdef HAVE_DEL
            case DELETE_GLOBAL:
                /* Get name index */
                t16 = GET_ARG();

                /* Get key */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Remove key,val from globals */
                retval = dict_delItem(FP->fo_globals, pobj2);
                PM_BREAK_IF_ERROR(retval);
                continue;
#endif /* HAVE_DEL */

            case DUP_TOPX:
                t16 = GET_ARG();
                C_ASSERT(t16 <= 3);

                pobj1 = TOS;
                pobj2 = TOS1;
                pobj3 = TOS2;
                if (t16 >= 3)
                    PM_PUSH(pobj3);
                if (t16 >= 2)
                    PM_PUSH(pobj2);
                if (t16 >= 1)
                    PM_PUSH(pobj1);
                continue;

            case LOAD_CONST:
                /* Get const's index in CO */
                t16 = GET_ARG();

                /* Push const on stack */
                retval = tuple_getItem(co_getConsts(FP->fo_func->f_co), t16, &pobj1);
                PM_BREAK_IF_ERROR(retval);
                PM_PUSH(pobj1);
                continue;

            case LOAD_NAME:
                /* Get name index */
                t16 = GET_ARG();

                /* Get name from names tuple */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj1);
                PM_BREAK_IF_ERROR(retval);

                /* Get value from frame's locals dict if there is one. */
                if (FP->fo_locals != C_NULL)
                {
                    retval = dict_getItem(FP->fo_locals, pobj1, &pobj2);
                }
                else
                {
                    PM_RAISE_WITH_INFO(retval, PM_RET_EX_SYS, "no locals dict found on LOAD_NAME");
                    break;
                }
                
                /* pobj1 not found in frame's locals dict, or no locals */
                if (retval == PM_RET_EX_KEY)
                {
                    /* Get val from globals */
                    retval = dict_getItem(FP->fo_globals, pobj1, &pobj2);
                        
                    /* Check for name in the builtins module if it is loaded */
                    if (retval == PM_RET_EX_KEY) 
                    {
                        if (PM_PBUILTINS != C_NULL)
                        {
                            /* Get val from builtins */
                            retval = dict_getItem(PM_PBUILTINS, pobj1, &pobj2);
                        }

                        if (retval == PM_RET_EX_KEY)
                        {
                            /* Name not defined, raise NameError */
                            PM_RAISE_WITH_OBJ(retval, PM_RET_EX_NAME, pobj1);
                            break;
                        }
                    }
                }
                PM_BREAK_IF_ERROR(retval);
                
                PM_PUSH(pobj2);
                continue;
                
            case BUILD_TUPLE:
                /* Get num items */
                t16 = GET_ARG();
                retval = tuple_new(t16, (pPmTuple_t *)&pobj1);
                PM_BREAK_IF_ERROR(retval);

                /* Fill tuple with ptrs to objs */
                for (; --t16 >= 0;)
                {
                    ((pPmTuple_t)pobj1)->items[t16] = PM_POP();
                }
                PM_PUSH(pobj1);
                continue;

            case BUILD_LIST:
                t16 = GET_ARG();
                retval = list_new((pPmList_t *)&pobj1);
                PM_BREAK_IF_ERROR(retval);

                /* Temporarily store list object in frame to protect from GC */
                FP->liveObj = pobj1;

                for (; --t16 >= 0;)
                {
                    /* Insert obj into list */
                    retval = list_insert((pPmList_t)pobj1, 0, TOS);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                }
                /* No longer need to protect from GC */
                FP->liveObj = C_NULL;
                /* Test again outside for loop */
                PM_BREAK_IF_ERROR(retval);

                /* push list onto stack */
                PM_PUSH(pobj1);
                continue;

            case BUILD_SET:
                t16 = GET_ARG();
                retval = set_new((pPmSet_t *)&pobj1);
                PM_BREAK_IF_ERROR(retval);

                /* Temporarily store set object in frame to protect from GC */
                FP->liveObj = pobj1;

                for (; --t16 >= 0;)
                {
                    /* Add obj to set */
                    retval = set_add((pPmSet_t)pobj1, TOS);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                }
                /* No longer need to protect from GC */
                FP->liveObj = C_NULL;
                /* Test again outside for loop */
                PM_BREAK_IF_ERROR(retval);

                /* push set onto stack */
                PM_PUSH(pobj1);
                continue;

            case BUILD_MAP:
                /* Argument is ignored */
                t16 = GET_ARG();
                retval = dict_new((pPmDict_t *)&pobj1);
                PM_BREAK_IF_ERROR(retval);
                PM_PUSH(pobj1);
                continue;

            case LOAD_ATTR:
                /* Implements TOS.attr */
                t16 = GET_ARG();

#ifdef HAVE_AUTOBOX
                /* Autobox the object, if necessary */
                retval = class_autobox(&TOS);
                PM_BREAK_IF_ERROR(retval);
#endif

                /* Get attrs dict from obj */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_FXN) ||
                    (OBJ_GET_TYPE(TOS) == OBJ_TYPE_MOD))
                {
                    pobj1 = (pPmObj_t)((pPmFunc_t)TOS)->f_attrs;
                }

#ifdef HAVE_CLASSES
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLO)
                {
                    pobj1 = (pPmObj_t)((pPmClass_t)TOS)->cl_attrs;
                }
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLI)
                {
                    pobj1 = (pPmObj_t)((pPmInstance_t)TOS)->cli_attrs;
                }
                else if (OBJ_GET_TYPE(TOS) == OBJ_TYPE_MTH)
                {
                    pobj1 = (pPmObj_t)((pPmMethod_t)TOS)->m_attrs;
                }
#endif /* HAVE_CLASSES */

                /* Other types result in an AttributeError */
                else
                {
                    PM_RAISE(retval, PM_RET_EX_ATTR);
                    break;
                }

                /* If attrs is not a dict, raise SystemError */
                if (OBJ_GET_TYPE(pobj1) != OBJ_TYPE_DIC)
                {
                    PM_RAISE(retval, PM_RET_EX_SYS);
                    break;
                }

                /* Get name */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Get attr with given name */
                retval = dict_getItem((pPmDict_t)pobj1, pobj2, &pobj3);

#ifdef HAVE_CLASSES
                /*
                 * If attr is not found and object is a class or instance,
                 * try to get the attribute from the class attrs or parent(s)
                 */
                if ((retval == PM_RET_EX_KEY) &&
                    ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLO)
                        || (OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLI)))
                {
                    retval = class_getAttr(TOS, pobj2, &pobj3);
                }
#endif /* HAVE_CLASSES */

                /* Raise an AttributeError if key is not found */
                if (retval == PM_RET_EX_KEY)
                {
                    PM_RERAISE(retval, PM_RET_EX_ATTR);
                }
                PM_BREAK_IF_ERROR(retval);

#ifdef HAVE_CLASSES
                /* If obj is an instance and attr is a func, create method */
                if ((OBJ_GET_TYPE(TOS) == OBJ_TYPE_CLI) &&
                    (OBJ_GET_TYPE(pobj3) == OBJ_TYPE_FXN))
                {
                    pobj2 = pobj3;
                    retval = class_method(TOS, pobj2, &pobj3);
                    PM_BREAK_IF_ERROR(retval);
                }
#endif /* HAVE_CLASSES */

                /* Put attr on the stack */
                TOS = pobj3;
                continue;

            case COMPARE_OP:
                retval = PM_RET_OK;
                t16 = GET_ARG();
                switch (t16)
                {
                    case COMP_IS:
                        pobj3 = (TOS == TOS1) ? PM_TRUE : PM_FALSE;
                        break;

                    case COMP_IS_NOT:
                        pobj3 = (TOS != TOS1) ? PM_TRUE : PM_FALSE;
                        break;
                    
                    case COMP_EQ:
                        t8 = obj_isEqual(TOS, TOS1);
                        pobj3 = (t8 == C_EQ) ? PM_TRUE : PM_FALSE;
                        break;

                    case COMP_NE:
                        t8 = obj_isEqual(TOS, TOS1);
                        pobj3 = (t8 == C_EQ) ? PM_FALSE : PM_TRUE;
                        break;

                    case COMP_IN:
                    case COMP_NOT_IN:
                        pobj3 = PM_FALSE;
                        retval = obj_isIn(TOS, TOS1);
                        if (retval == PM_RET_OK)
                        {
                            if (t16 == COMP_IN)
                            {
                                pobj3 = PM_TRUE;
                            }
                        }
                        else if (retval == PM_RET_NO)
                        {
                            retval = PM_RET_OK;
                            if (t16 == COMP_NOT_IN)
                            {
                                pobj3 = PM_TRUE;
                            }
                        }
                        break;

                    case COMP_LT:
                        t8 = obj_compare(TOS, TOS1);
                        if (t8 == C_CMP_ERR)
                        {
                            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "comparing incompatible types");
                            break;
                        }
                        pobj3 = (t8 == C_LT) ? PM_TRUE : PM_FALSE;
                        break;

                    case COMP_LE: 
                        t8 = obj_compare(TOS, TOS1);
                        if (t8 == C_CMP_ERR)
                        {
                            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "comparing incompatible types");
                            break;
                        }
                        pobj3 = (t8 == C_LT || t8 == C_EQ) ? PM_TRUE : PM_FALSE;
                        break;

                    case COMP_GT:
                        t8 = obj_compare(TOS, TOS1);
                        if (t8 == C_CMP_ERR)
                        {
                            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "comparing incompatible types");
                            break;
                        }
                        pobj3 = (t8 == C_GT) ? PM_TRUE : PM_FALSE;
                        break;

                    case COMP_GE: 
                        t8 = obj_compare(TOS, TOS1);
                        if (t8 == C_CMP_ERR)
                        {
                            PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "comparing incompatible types");
                            break;
                        }   
                        pobj3 = (t8 == C_GT || t8 == C_EQ) ? PM_TRUE : PM_FALSE;                      
                        break;

                    default:
                        /* Other comparisons are not implemented */
                        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE, "unsupported comparison type");
                        break;
                }
                PM_BREAK_IF_ERROR(retval);
                SP--;
                TOS = pobj3;
                continue;

            case IMPORT_NAME:
                /* Get name index */
                t16 = GET_ARG();

                /* Get name String obj */
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj1);
                PM_BREAK_IF_ERROR(retval);

                /* Pop unused None object */
                SP--;

                /* Ensure "level" is -1; no support for relative import yet */
                C_ASSERT(obj_isEqual(TOS, PM_NEGONE) == C_EQ);

                /* #110: Prevent importing previously-loaded module */
                /* If the named module is in modules dict, put it on the stack */
                retval = dict_getItem(gVmGlobal.modules, pobj1, &pobj2);
                if ((retval == PM_RET_OK)
                    && (OBJ_GET_TYPE(pobj2) == OBJ_TYPE_MOD))
                {
                    TOS = pobj2;
                    continue;
                }

                /* Load module from image */
                retval = mod_import(pobj1, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Put Module on top of stack */
                TOS = pobj2;

                /* Code after here is a duplicate of CALL_FUNCTION */
                /* Make frame object to interpret the module's root code */
                retval = frame_new(pobj2, &pobj3);
                PM_BREAK_IF_ERROR(retval);

                /* No arguments to pass */

                /* Keep ref to current frame */
                ((pPmFrame_t)pobj3)->fo_back = FP;
                ((pPmFrame_t)pobj3)->fo_except = FP->fo_except;

                /* Handle to have None popped on return */
                ((pPmFrame_t)pobj3)->fo_isImport = (uint8_t)1;

                /* Set new frame */
                FP = (pPmFrame_t)pobj3;

                /* Store module in modules dictionary */
                retval = dict_setItem(gVmGlobal.modules, pobj1, pobj2);
                PM_BREAK_IF_ERROR(retval);

                continue;

#ifdef HAVE_IMPORTS
            case IMPORT_FROM:
                /* #102: Implement the remaining IMPORT_ bytecodes */
                /* Expect the module on the top of the stack */
                C_ASSERT(OBJ_GET_TYPE(TOS) == OBJ_TYPE_MOD);
                pobj1 = TOS;

                /* Get the name of the object to import */
                t16 = GET_ARG();
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Get the object from the module's attributes */
                retval = dict_getItem(((pPmFunc_t)pobj1)->f_attrs,
                                      pobj2, &pobj3);
                PM_BREAK_IF_ERROR(retval);

                /* Push the object onto the top of the stack */
                PM_PUSH(pobj3);
                continue;
#endif /* HAVE_IMPORTS */

            case JUMP_FORWARD:
                t16 = GET_ARG();
                IP += t16;
                continue;

            case JUMP_IF_FALSE_OR_POP:
            case POP_JUMP_IF_FALSE:
                t16 = GET_ARG();

                t8 = obj_isFalse(TOS);
                if (t8)
                {
                    /* Jump to base_ip + arg */
                    IP = co_getCodeaddr(FP->fo_func->f_co) + t16;
                }
                if ((bc == POP_JUMP_IF_FALSE) || (!t8))
                {
                    pobj1 = PM_POP();
                }
                continue;

            case JUMP_IF_TRUE_OR_POP:
            case POP_JUMP_IF_TRUE:
                t16 = GET_ARG();
                t8 = obj_isFalse(TOS);
                if (!t8)
                {
                    /* Jump to base_ip + arg */
                    IP = co_getCodeaddr(FP->fo_func->f_co) + t16;
                }
                if ((bc == POP_JUMP_IF_TRUE) || t8)
                {
                    pobj1 = PM_POP();
                }
                continue;

            case JUMP_ABSOLUTE:
            case CONTINUE_LOOP:
                /* Get target offset (bytes) */
                t16 = GET_ARG();

                /* Jump to base_ip + arg */
                IP = co_getCodeaddr(FP->fo_func->f_co) + t16;
                continue;

            case LOAD_GLOBAL:
                /* Get name */
                t16 = GET_ARG();
                retval = tuple_getItem(co_getNames(FP->fo_func->f_co), t16, &pobj1);
                PM_BREAK_IF_ERROR(retval);

                /* Try globals first */
                retval = dict_getItem(FP->fo_globals, pobj1, &pobj2);

                /* If that didn't work, try builtins */
                if (retval == PM_RET_EX_KEY)
                {
                    retval = dict_getItem(PM_PBUILTINS, pobj1, &pobj2);

                    /* No such global */
                    if (retval == PM_RET_EX_KEY)
                    {
                            /* raise NameError */
                            PM_RAISE_WITH_OBJ(retval, PM_RET_EX_NAME, pobj1);
                            break;
                    }
                }
                PM_BREAK_IF_ERROR(retval);
                PM_PUSH(pobj2);
                continue;

            case SETUP_LOOP:
            {
                uint8_t *pchunk;

                /* Get block span (bytes) */
                t16 = GET_ARG();

                /* Create block */
                retval = heap_getChunk(sizeof(PmBlock_t), &pchunk);
                PM_BREAK_IF_ERROR(retval);
                pobj1 = (pPmObj_t)pchunk;
                OBJ_SET_TYPE(pobj1, OBJ_TYPE_BLK);

                /* Store current stack pointer */
                ((pPmBlock_t)pobj1)->b_sp = SP;

                /* Default handler is to exit block/loop */
                ((pPmBlock_t)pobj1)->b_handler = IP + t16;
                ((pPmBlock_t)pobj1)->b_type = B_LOOP;

                /* Insert block into blockstack */
                ((pPmBlock_t)pobj1)->next = FP->fo_blockstack;
                FP->fo_blockstack = (pPmBlock_t)pobj1;
                continue;
            }

            case LOAD_FAST:
                t16 = GET_ARG();

                // trying to load an unbound local
                if (FP->fo_stack[t16] == C_NULL)
                {
                        PM_RAISE_WITH_INFO(retval, PM_RET_EX_UNBOUND, "local variable referenced without being set");
                        break;
                }
                else
                {
                    PM_PUSH(FP->fo_stack[t16]);
                }
                continue;

            case STORE_FAST:
                t16 = GET_ARG();
                FP->fo_stack[t16] = PM_POP();
                continue;

#ifdef HAVE_DEL
            case DELETE_FAST:
                t16 = GET_ARG();
                FP->fo_stack[t16] = PM_NONE;
                continue;
#endif /* HAVE_DEL */

#ifdef HAVE_ASSERT
            case RAISE_VARARGS:
                t16 = GET_ARG();

                /* Only supports taking 1 arg for now */
                if (t16 != 1)
                {
                    PM_RAISE(retval, PM_RET_EX_SYS);
                    break;
                }

                /* Load Exception class from builtins */
                retval = dict_getItem(PM_PBUILTINS, CONSTException, &pobj2);
                if (retval != PM_RET_OK)
                {
                    PM_RAISE(retval, PM_RET_EX_SYS);
                    break;
                }

                /* Raise TypeError if TOS is not an instance of Exception */
                pobj1 = TOS;
                if ((OBJ_GET_TYPE(pobj1) != OBJ_TYPE_CLO)
                    || !class_isSubclass(pobj1, pobj2))
                {
                    PM_RAISE(retval, PM_RET_EX_TYPE);
                    break;
                }

                /* Push the traceback, parameter and exception object */
                TOS = PM_NONE;
                PM_PUSH(PM_NONE);
                PM_PUSH(pobj1);

                /* Get the exception's code attr */
                retval = dict_getItem(((pPmClass_t)pobj1)->cl_attrs,
                                      CONSTcode, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Raise exception by breaking with retval set to code */
                PM_RAISE(retval, (PmReturn_t)(((pPmInt_t)pobj2)->val & 0xFF));
                break;
#endif /* HAVE_ASSERT */

            case CALL_FUNCTION:
                /* Get num args */
                t16 = GET_ARG();

                /* Ensure no keyword args */
                if ((t16 & (uint16_t)0xFF00) != 0)
                {
                    PM_RAISE_WITH_INFO(retval, PM_RET_EX_SYS, "keyword arguments not supported");
                    break;
                }

                /* Get the callable */
                pobj1 = STACK(t16);

                C_DEBUG_PRINT(VERBOSITY_LOW,
                    "interpret(), CALL_FUNCTION on <obj type=%u @ %p>\n",
                    OBJ_GET_TYPE(pobj1), pobj1);

#ifdef HAVE_FFI
                if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_FOR)
                {
                    /* Collect the arguments into a tuple */
                    retval = tuple_new(t16, (pPmTuple_t *)&pobj2);
                    PM_BREAK_IF_ERROR(retval);

                    while (t16) {
                        pobj3 = PM_POP();
                        ((pPmTuple_t) pobj2)->items[t16-1] = pobj3;
                        t16--;
                    }

                    // remove the callable
                    pobj3 = PM_POP();

                    // make the call
                    retval = foreign_call((pPmForeign_t) pobj1, (pPmTuple_t) pobj2, &pobj3);
                    PM_BREAK_IF_ERROR(retval);

                    // push the result back
                    PM_PUSH(pobj3);

                    continue;
                }
#endif // HAVE_FFI

#ifdef HAVE_GENERATORS
                /* If the callable is a generator function (can't be native) */
                if ((OBJ_GET_TYPE(pobj1) == OBJ_TYPE_FXN)
                    && (IS_CODE_OBJ(((pPmFunc_t)pobj1)->f_co))
                    && (co_getFlags(((pPmFunc_t)pobj1)->f_co) & CO_GENERATOR))
                {
                    /* Collect the function and arguments into a tuple */
                    retval = tuple_new(t16 + 1, (pPmTuple_t *)&pobj2);
                    PM_BREAK_IF_ERROR(retval);
                    memcpy((uint8_t *)&((pPmTuple_t)pobj2)->items,
                               (uint8_t *)&STACK(t16),
                               (t16 + 1) * sizeof(pPmObj_t));

                    /* Remove old args, push func/args tuple as one arg */
                    SP -= t16;
                    PM_PUSH(pobj2);
                    t16 = 1;

                    /* Set pobj1 and stack to create an instance of Generator */
                    retval = dict_getItem(PM_PBUILTINS, CONSTGenerator, &pobj1);
                    PM_RETURN_IF_ERROR(retval);
                    STACK(t16) = pobj1;
                }
#endif /* HAVE_GENERATORS */

#ifdef HAVE_CLASSES
                /* If the callable is a class, create an instance of it */
                if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_CLO)
                {
                    /* This marks that the original callable was a class */
                    bc = 0;

                    /* Replace class with new instance */
                    retval = class_instantiate(pobj1, &pobj2);
                    STACK(t16) = pobj2;

                    /* If __init__ does not exist */
                    pobj3 = C_NULL;
                    retval = class_getAttr(pobj1, CONST__init__, &pobj3);
                    if (retval == PM_RET_EX_KEY)
                    {
                        /* Raise TypeError if there are args */
                        if (t16 > 0)
                        {
                            PM_RAISE_WITH_OBJ(retval, PM_RET_EX_TYPE, pobj1);
                            break;
                        }

                        /* Otherwise, continue with instance */
                        continue;
                    }
                    else if (retval != PM_RET_OK)
                    {
                        PM_BREAK_IF_ERROR(retval);
                    }

                    /* Slide the arguments up 1 slot in the stack */
                    SP++;
                    for (t8 = 0; t8 < t16; t8++)
                    {
                        STACK(t8) = STACK(t8 + 1);
                    }

                    /* Convert __init__ to method, insert it as the callable */
                    retval = class_method(pobj2, pobj3, &pobj1);
                    PM_BREAK_IF_ERROR(retval);
                    STACK(t16) = pobj1;
                    /* Fall through to call the method */
                }

                if (OBJ_GET_TYPE(pobj1) == OBJ_TYPE_MTH)
                {
                    /* Set the method's func to be the callable */
                    STACK(t16) = (pPmObj_t)((pPmMethod_t)pobj1)->m_func;

                    /* Slide the arguments up 1 slot in the stack */
                    SP++;
                    for (t8 = 0; t8 < t16; t8++)
                    {
                        STACK(t8) = STACK(t8 + 1);
                    }

                    /* Insert instance as "self" arg to the method */
                    STACK(t16++) = (pPmObj_t)((pPmMethod_t)pobj1)->m_instance;

                    /* Refresh the callable */
                    pobj1 = (pPmObj_t)((pPmMethod_t)pobj1)->m_func;
                }
#endif /* HAVE_CLASSES */

#ifdef HAVE_GENERATORS
CALL_FUNC_FOR_ITER:
#endif /* HAVE_GENERATORS */
                /* Raise a TypeError if object is not callable */
                if (OBJ_GET_TYPE(pobj1) != OBJ_TYPE_FXN)
                {
                    PM_RAISE_WITH_OBJ(retval, PM_RET_EX_TYPE, pobj1);
                    break;
                }

                /* If the profiler is running, increment the call count */
                if (profiler_isactive()) 
                {
                    ((pPmFunc_t)pobj1)->calls++;
                }

                /* If it is a regular func (not native) */
                if (IS_CODE_OBJ(((pPmFunc_t)pobj1)->f_co))
                {
                    /*
                     * #132 Raise TypeError if num args does not match the
                     * code object's expected argcount
                     */

#if defined(HAVE_DEFAULTARGS) || defined(HAVE_VARARGS)
                    t8 = co_getArgcount(((pPmFunc_t)pobj1)->f_co);
#endif /* HAVE_DEFAULTARGS || HAVE_VARARGS */
 
#ifdef HAVE_DEFAULTARGS
                    if (((pPmFunc_t)pobj1)->f_defaultargs != C_NULL)
                    {
                        /* Num required args := argcount - num default args */
                        t8 -= ((pPmTuple_t)((pPmFunc_t)pobj1)->f_defaultargs)->
                            length;
                    }

                    /*
                     * Raise a TypeError if num args passed
                     * is more than allowed and no *args or less than required
                     */
                    if ((((t16 & ((uint8_t)0xFF))
                          > (co_getArgcount(((pPmFunc_t)pobj1)->f_co)))
#ifdef HAVE_VARARGS
                         && ((co_getFlags(((pPmFunc_t)pobj1)->f_co) & CO_VARARGS) == 0)
#endif /* HAVE_VARARGS */
                            )
                        || (((t16 & ((uint8_t)0xFF)) < t8)))
#else
                    if (((t16 & ((uint8_t)0xFF)) !=
                         (co_getArgcount((pPmFunc_t)pobj1)->f_co))
#ifdef HAVE_VARARGS
                        && (co_getFlags(((pPmFunc_t)pobj1)->f_co) & CO_VARARGS == 0)
#endif /* HAVE_VARARGS */
                        )
#endif /* HAVE_DEFAULTARGS */
                    {
                        PM_RAISE_WITH_INFO(retval, PM_RET_EX_TYPE,
                            "function passed incorrect number of arguments");
                        break;
                    }

                    /* Make frame object to run the func object */
                    retval = frame_new(pobj1, &pobj2);
                    PM_BREAK_IF_ERROR(retval);

#ifdef HAVE_CLASSES
                    /*
                     * If the original callable was a class, indicate that
                     * the frame is running the initializer so that
                     * its return object is checked for None and ignored.
                     */
                    if (bc == 0)
                    {
                        ((pPmFrame_t)pobj2)->fo_isInit = C_TRUE;
                    }
#endif /* HAVE_CLASSES */

#ifdef HAVE_DEFAULTARGS
                    /* If this func has default arguments, put them in place */
                    if (((pPmFunc_t)pobj1)->f_defaultargs != C_NULL)
                    {
                        int8_t i = 0;

                        /* Copy default args into the new frame's locals */
                        for ( /* t8 set above */ ;
                             t8 < co_getArgcount(((pPmFunc_t)pobj1)->f_co); t8++)
                        {
                            retval = tuple_getItem((pPmTuple_t)((pPmFunc_t)pobj1)->f_defaultargs, i++, &pobj3);
                            PM_BREAK_IF_ERROR(retval);
                            ((pPmFrame_t)pobj2)->fo_stack[t8] = pobj3;
                        }
                    }
#endif /* HAVE_DEFAULTARGS */

#ifdef HAVE_VARARGS
                    if (co_getFlags(((pPmFunc_t)pobj1)->f_co) & CO_VARARGS) /* *args */
                    {
                        /* Create the empty tuple and add to fo_stack */
                        /* If default args are included, t16 can be smaller than argcount */
                        if (t16 > co_getArgcount(((pPmFunc_t)pobj1)->f_co))
                        {
                            retval = tuple_new((t16 - co_getArgcount(((pPmFunc_t)pobj1)->f_co)), 
                                               (pPmTuple_t *)&pobj3);
                        }
                        else
                        {
                            retval = tuple_new(0, (pPmTuple_t *)&pobj3);
                        }
                        PM_BREAK_IF_ERROR(retval);
                        ((pPmFrame_t)pobj2)->fo_stack[t8] = pobj3;
                    }
#endif /* HAVE_VARARGS */
                    
                    /* Pass args to new frame */
                    while (--t16 >= 0)
                    {
                        /*
                         * Pop args from stack right to left,
                         * since args are pushed left to right,
                         */
#ifdef HAVE_VARARGS
                        if ((co_getFlags(((pPmFunc_t)pobj1)->f_co) & CO_VARARGS)
                            && (t16 >= co_getArgcount(((pPmFunc_t)pobj1)->f_co)))
                        {
                            /* add arg to the *args tuple */ 
                            ((pPmTuple_t)pobj3)->items[t16 - co_getArgcount(((pPmFunc_t)pobj1)->f_co)] = PM_POP();
                        }                                      
                        else
#endif /* HAVE_VARARGS */
                        {
                            /* add arg to local frame */
                            ((pPmFrame_t)pobj2)->fo_stack[t16] = PM_POP();
                        }                                    
                    }

#ifdef HAVE_CLOSURES
                    /* #256: Add support for closures */
                    /* Copy arguments that become cellvars */
                    if (co_getCellvars(((pPmFunc_t)pobj1)->f_co) != C_NULL)
                    {
                        for (t8 = 0;
                             t8 < tuple_getLength(co_getCellvars(((pPmFunc_t)pobj1)->f_co));
                             t8++)
                        {
                            retval = tuple_getItem(co_getCellvars(((pPmFunc_t)pobj1)->f_co), t8, &pobj3);
                            PM_BREAK_IF_ERROR(retval);
                            if (((pPmInt_t)pobj3)->val >= 0)
                            {
                                ((pPmFrame_t)pobj2)->fo_stack[
                                    co_getNlocals(((pPmFunc_t)pobj1)->f_co) + t8] =
                                       ((pPmFrame_t)pobj2)->fo_stack[((pPmInt_t)pobj3)->val];
                            }
                        }

                        /* Test again outside for loop */
                        PM_BREAK_IF_ERROR(retval);
                    }

                    /* Fill frame's freevars with references from closure */
                    for (t8 = 0;
                         t8 < co_getNfreevars(((pPmFunc_t)pobj1)->f_co);
                         t8++)
                    {
                        C_ASSERT(((pPmFunc_t)pobj1)->f_closure != C_NULL);
                        retval = tuple_getItem(((pPmFunc_t)pobj1)->f_closure, t8, &pobj3);
                        PM_BREAK_IF_ERROR(retval);

                        ((pPmFrame_t)pobj2)->fo_stack[
                            co_getNlocals(((pPmFunc_t)pobj1)->f_co)
                            + ((co_getCellvars(((pPmFunc_t)pobj1)->f_co) == C_NULL) ? 0 : 
                                tuple_getLength(co_getCellvars(((pPmFunc_t)pobj1)->f_co)))
                            + t8] = pobj3;
                    }

                    /* Test again outside for loop */
                    PM_BREAK_IF_ERROR(retval);
#endif /* HAVE_CLOSURES */

                    /* Pop func obj */
                    pobj3 = PM_POP();

                    if (bc == TAIL_CALL_FUNCTION) {
                        /* Discard ref to current frame */
                        ((pPmFrame_t)pobj2)->fo_back = FP->fo_back;
                    }
                    else
                    {
                        /* Keep ref to current frame */
                        ((pPmFrame_t)pobj2)->fo_back = FP;
                    }
                    ((pPmFrame_t)pobj2)->fo_except = FP->fo_except;

                    /* Set new frame */
                    FP = (pPmFrame_t)pobj2;
                }

                /* If it's native func */
                else if (OBJ_GET_TYPE(((pPmFunc_t)pobj1)->f_co) ==
                         OBJ_TYPE_NOB)
                {
                    /* Save the number of locals (arguments) */
                    t8 = (int8_t) t16;

#ifdef HAVE_GC
                    /* If the heap is low on memory, run the GC */
                    if (heap_getAvail() < HEAP_GC_NF_THRESHOLD)
                    {
                        retval = heap_gcRun();
                        PM_BREAK_IF_ERROR(retval);
                    }
#endif /* HAVE_GC */

                    /* Get native function index */
                    pobj2 = (pPmObj_t)((pPmFunc_t)pobj1)->f_co;
                    t16 = ((pPmNo_t)pobj2)->no_funcindx;

#ifdef HAVE_PROFILER
                    gVmGlobal.profiler_flags[IN_NATIVE] = true;
#endif

                    /*
                     * CALL NATIVE FXN: pass caller's frame and numargs
                     *
                     * Function arguments and the function object
                     * remain on the caller's stack.  The native
                     * function can access them there.  Save the frame
                     * pointer in case the native function switches
                     * it, so they can be removed afterwards.
                     *
                     * pobj3 will be the return value from the native
                     * function.
                     */

                    RUNNINGTHREAD->nativecalls++;

                    pobj2 = (pPmObj_t) FP;
                    pobj3 = C_NULL;

                    gVmGlobal.nf_active = C_TRUE;

                    /* Positive index is a stdlib func */
                    if (t16 >= 0)
                    {
                        retval = std_nat_fxn_table[t16] (&FP, t8, &pobj3);
                    }

                    /* Negative index is a usrlib func */
                    else
                    {
                        retval = usr_nat_fxn_table[-t16] (&FP, t8, &pobj3);
                    }

                    gVmGlobal.nf_active = C_FALSE;

#ifdef HAVE_PROFILER
                    gVmGlobal.profiler_flags[IN_NATIVE] = false;
#endif

                    /*
                     * RETURN FROM NATIVE FXN
                     */

                    /* Pop arguments and function object from stack of
                     * the original frame.
                     */
                    while (t8-- >= 0)
                    {
                        ((pPmFrame_t) pobj2)->fo_sp--;
                    }

#ifdef HAVE_CLASSES
                    /* If class's __init__ called, do not push a return obj */
                    if (bc == 0)
                    {
                        /* Raise TypeError if returned obj was not None */
                        if ((retval == PM_RET_OK) && (OBJ_GET_TYPE(pobj3) != OBJ_TYPE_NON))
                        {
                            PM_RAISE(retval, PM_RET_EX_TYPE);
                            break;
                        }
                    }
                    else
#endif /* HAVE_CLASSES */

                    /* If the frame pointer was switched, do nothing to TOS */
                    if (retval == PM_RET_FRAME_SWITCH)
                    {
                        retval = PM_RET_OK;
                    }

                    /* Otherwise, return the result from the native function */
                    else
                    {
                        PM_PUSH(pobj3);
                    }
                    PM_BREAK_IF_ERROR(retval);
                }
                continue;

            case MAKE_FUNCTION:
                /* Get num default args to fxn */
                t16 = GET_ARG();

                /*
                 * The current frame's globals become the function object's
                 * globals.  The current frame is the container object
                 * of this new function object
                 */
                retval = func_new(TOS, (pPmObj_t)FP->fo_globals, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Put any default args in a tuple */
                if (t16 > 0)
                {

#ifdef HAVE_DEFAULTARGS
                    retval = tuple_new(t16, (pPmTuple_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);
                    SP--;
                    while (--t16 >= 0)
                    {
                        ((pPmTuple_t)pobj3)->items[t16] = PM_POP();
                    }

                    /* Set func's default args */
                    ((pPmFunc_t)pobj2)->f_defaultargs = (pPmTuple_t)pobj3;
#else
                    /* Default arguments not configured in pmfeatures.h */
                    PM_RAISE(retval, PM_RET_EX_SYS);
                    break;
#endif /* HAVE_DEFAULTARGS */

                }
                else
                {
                    SP--;
                }

                /* Push func obj */
                PM_PUSH(pobj2);
                continue;

#ifdef HAVE_CLOSURES
            case MAKE_CLOSURE:
                /* Get number of default args */
                t16 = GET_ARG();
                retval = func_new(TOS, (pPmObj_t)FP->fo_globals, &pobj2);
                PM_BREAK_IF_ERROR(retval);

                /* Set closure of the new function */
                ((pPmFunc_t)pobj2)->f_closure = (pPmTuple_t)TOS1;
                SP -= 2;

                /* Collect any default arguments into tuple */
                if (t16 > 0)
                {
                    retval = tuple_new(t16, (pPmTuple_t *)&pobj3);
                    PM_BREAK_IF_ERROR(retval);

                    while (--t16 >= 0)
                    {
                        ((pPmTuple_t)pobj3)->items[t16] = PM_POP();
                    }
                    ((pPmFunc_t)pobj2)->f_defaultargs = (pPmTuple_t)pobj3;
                }

                /* Push new func with closure */
                PM_PUSH(pobj2);
                continue;

            case LOAD_CLOSURE:
            case LOAD_DEREF:
                /* Loads the i'th cell of free variable storage onto TOS */
                t16 = GET_ARG();
                pobj1 = FP->fo_stack[co_getNlocals(FP->fo_func->f_co) + t16];
                if (pobj1 == C_NULL)
                {
                    PM_RAISE(retval, PM_RET_EX_SYS);
                    break;
                }
                PM_PUSH(pobj1);
                continue;

            case STORE_DEREF:
                /* Stores TOS into the i'th cell of free variable storage */
                t16 = GET_ARG();
                FP->fo_stack[co_getNlocals(FP->fo_func->f_co) + t16] = PM_POP();
                continue;
#endif /* HAVE_CLOSURES */

            case SET_ADD:
                t16 = GET_ARG();
                /* Set */
                pobj1 = STACK(t16);
                /* Item */
                pobj2 = PM_POP();

                retval = set_add((pPmSet_t)pobj1, pobj2);
                PM_BREAK_IF_ERROR(retval);
                continue;

            case MAP_ADD:
                t16 = GET_ARG();
                /* Key */
                pobj2 = PM_POP();
                /* Value */
                pobj3 = PM_POP();
                /* Dictionary */
                pobj1 = STACK(t16-1);

                retval = dict_setItem((pPmDict_t)pobj1, pobj2, pobj3);
                PM_BREAK_IF_ERROR(retval);
                continue;

            default:
                /* SystemError, unknown or unimplemented opcode */
                PM_RAISE_WITH_INFO(retval, PM_RET_EX_SYS, "invalid opcode");
                break;
        }

#ifdef HAVE_GENERATORS
        /* If got a StopIteration exception, check for a B_LOOP block */
        if (retval == PM_RET_EX_STOP)
        {
            pobj1 = (pPmObj_t)FP;
            pobj3 = pobj1;
            while (pobj1 != C_NULL)
            {
                pobj2 = (pPmObj_t)((pPmFrame_t)pobj1)->fo_blockstack;
                while (pobj2 != C_NULL)
                {
                    if (((pPmBlock_t)pobj2)->b_type == B_LOOP)
                    {
                        /* Resume execution where the block handler says */
                        /* Set FP first, so SP and IP are set in the frame */
                        FP = (pPmFrame_t)pobj1;
                        SP = ((pPmBlock_t)pobj2)->b_sp;
                        IP = ((pPmBlock_t)pobj2)->b_handler;
                        ((pPmFrame_t)pobj1)->fo_blockstack =
                            ((pPmFrame_t)pobj1)->fo_blockstack->next;
                        retval = PM_RET_OK;
                        break;
                    }

                    pobj2 = (pPmObj_t)((pPmBlock_t)pobj2)->next;
                }
                if (retval == PM_RET_OK)
                {
                    break;
                }
                pobj1 = (pPmObj_t)((pPmFrame_t)pobj1)->fo_back;
            }

            /* 
             * The generator sticks around, but the calling frame goes
             * away.  The generator contains a reference to it's frame
             * in it's attributes dictionary which points back to the
             * calling frame.
             *
             * Clearing these back references solves the case when a
             * generator is used in a loop.
             */
            ((pPmFrame_t)pobj3)->fo_back = C_NULL;
            ((pPmFrame_t)pobj3)->fo_except = C_NULL;

            if (retval == PM_RET_OK)
            {
                continue;
            }
        }
#endif /* HAVE_GENERATORS */

        /*
         * If execution reaches this point, it is because
         * a return value (from above) is not OK or we should exit the thread
         * (return of the function). In any case, remove the
         * current thread and reschedule.
         */
        if (retval != PM_RET_OK)
        {
            RUNNINGTHREAD->interpctrl = INTERP_CTRL_ERR;
        }
        else
        {
            RUNNINGTHREAD->interpctrl = INTERP_CTRL_EXIT;
        }
    }

    return retval;
}


PmReturn_t
interp_reschedule(void)
{
    PmReturn_t  retval = PM_RET_OK;
    pPmThread_t pthread;
    int i;

    // if we fail out of this function with an exception, we hang onto the lock
    // for a while. but, we're pretty hopelessly screwed in that case anyways.
    profiler_locked = true;

    /* If there is a currently running thread, enqueue it on the runnable thread list */
    if (RUNNINGTHREAD != C_NULL)
    {
        retval = list_append(gVmGlobal.threadList, (pPmObj_t) RUNNINGTHREAD);
        RUNNINGTHREAD = C_NULL;
        PM_RETURN_IF_ERROR(retval);
    }

    /* Get next runnable thread */
    for (i = 0; i < gVmGlobal.threadList->length; i++)
    {
        retval = list_getItem(gVmGlobal.threadList, i, (pPmObj_t *)&pthread);
        PM_RETURN_IF_ERROR(retval);

        if (pthread->interpctrl != INTERP_CTRL_WAIT)
        {
            retval = list_delItem(gVmGlobal.threadList, i);
            PM_RETURN_IF_ERROR(retval);

            RUNNINGTHREAD = pthread;
            break;
        }
    }

    /* Clear flag to indicate a reschedule has occurred */
    interp_setRescheduleFlag(0);
    profiler_locked = false;
    return retval;
}

void
interp_setRescheduleFlag(uint8_t boolean)
{
    gVmGlobal.reschedule = boolean;
}
