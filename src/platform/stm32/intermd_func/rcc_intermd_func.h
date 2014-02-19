#include <libopencm3/cm3/common.h>

typedef enum {
	AHB1_ENR,
	AHB2_ENR,
	AHB3_ENR,
	APB1_ENR,
	APB2_ENR,
	RCC_ENR_NUM
} clock_enable_reg_t;

typedef enum {
	AHB1_RSTR,
	AHB2_RSTR,
	AHB3_RSTR,
	APB1_RSTR,
	APB2_RSTR,
	RCC_RSTR_NUM
} clock_reset_reg_t;

typedef enum {
	CLOCK_8MHZ_3V3,
	CLOCK_12MHZ_3V3,
	CLOCK_16MHZ_3V3,
	CLOCK_SCALE_NUM
} clock_scale_enum_t;


void rcc_peripheral_enable_clock_new(clock_enable_reg_t reg, uint32_t en);
void rcc_peripheral_disable_clock_new(clock_enable_reg_t reg, uint32_t en);
void rcc_peripheral_reset_new(clock_reset_reg_t reg, uint32_t reset);
void rcc_peripheral_clear_reset_new(clock_reset_reg_t reg, uint32_t clear_reset);
void rcc_clock_setup_hse_3v3_new(clock_scale_enum_t clock);