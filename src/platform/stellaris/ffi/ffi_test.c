#include "pm.h"
#include "ffi.h"

#define MAXARGS 8

uint8_t test_fn(int32_t a, int32_t b, int32_t c, int32_t d, int32_t e) {

    lib_printf("%d, %d, %d, %d, %d\n", a, b, c, d, e);

    if ((a==42) && (b==43) && (c==-44)) {
        lib_printf("passed\n");
    } else {
        lib_printf("failed\n");
    }

    return 45;
}

int ffi_test()
{
    ffi_cif cif;
    int rc = 0xffffffff;
    ffi_type *args[MAXARGS];
    void *values[MAXARGS];

    int a = 42;
    int b = 43;
    int c = -44;
    int d = 45;
    int e = 46;

    /* Initialize the argument info vectors */
    args[0] = &ffi_type_sint32;
    args[1] = &ffi_type_sint32;
    args[2] = &ffi_type_sint32;
    args[3] = &ffi_type_sint32;
    args[4] = &ffi_type_sint32;

    values[0] = &a;
    values[1] = &b;
    values[2] = &c;
    values[3] = &d;
    values[4] = &e;

    /* Initialize the cif */
    if (ffi_prep_cif(&cif, FFI_DEFAULT_ABI, 5, &ffi_type_uint32, args) == FFI_OK) {
        ffi_call(&cif, test_fn, &rc, values);
    } else {
        lib_printf("ffi_prep_cif failed\n");
    }

    lib_printf("rc: %d\n", rc);
    return 0;
}

