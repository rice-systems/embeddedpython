#include "rcc_intermd_func.h"
#include "rcc.h"

volatile uint32_t *const clock_enable_reg_map[RCC_ENR_NUM] = {
	&RCC_AHB1ENR,
	&RCC_AHB2ENR,
	&RCC_AHB3ENR,
	&RCC_APB1ENR,
	&RCC_APB2ENR
};

volatile uint32_t *const clock_reset_reg_map[RCC_RSTR_NUM] = {
	&RCC_AHB1RSTR,
	&RCC_AHB2RSTR,
	&RCC_AHB3RSTR,
	&RCC_APB1RSTR,
	&RCC_APB2RSTR
};

const clock_scale_t *clock_scale_map[CLOCK_SCALE_NUM] = {
	hse_8mhz_3v3,
	hse_12mhz_3v3,
	hse_16mhz_3v3
};

void rcc_peripheral_enable_clock_new(clock_enable_reg_t reg, uint32_t en) {
	rcc_peripheral_enable_clock(clock_enable_reg_map[reg], en);
}
void rcc_peripheral_disable_clock_new(clock_enable_reg_t reg, uint32_t en) {
	rcc_peripheral_disable_clock(clock_enable_reg_map[reg], en);
}
void rcc_peripheral_reset_new(clock_reset_reg_t reg, uint32_t reset) {
	rcc_peripheral_reset(clock_reset_reg_map[reg], reset);
}
void rcc_peripheral_clear_reset_new(clock_reset_reg_t reg, uint32_t clear_reset) {
	rcc_peripheral_clear_reset(clock_reset_reg_map[reg], clear_reset);
}
void rcc_clock_setup_hse_3v3_new(clock_scale_enum_t clock) {
	rcc_clock_setup_hse_3v3(clock_scale_map[clock]);
}