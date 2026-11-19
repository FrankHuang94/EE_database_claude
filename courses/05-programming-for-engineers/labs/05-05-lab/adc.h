/* adc.h - ADC conversion and first-order filtering for Lab 05-05. */
#ifndef ADC_H
#define ADC_H

/* Convert an ADC code to millivolts, rounded to nearest.
 * bits: resolution (1..16); vref_mv: reference voltage in mV (> 0).
 * Returns -1 if any argument is out of range. */
int adc_to_mv(int code, int bits, int vref_mv);

/* Smoothing factor of an exponential moving average with sample period t_s
 * and time constant tau (same units): alpha = 1 - exp(-t_s / tau). */
double ema_alpha(double t_s, double tau);

/* One filter step: move y a fraction alpha of the way toward x. */
double ema_step(double y, double x, double alpha);

/* Number of samples for a unit step to come within tol of 1 (0 < tol < 1),
 * or -1 if the arguments are invalid or the output does not get within tol
 * in EMA_MAX_SAMPLES samples (a loop with no such limit could run forever). */
#define EMA_MAX_SAMPLES 1000000
int ema_settle_samples(double t_s, double tau, double tol);

#endif /* ADC_H */
