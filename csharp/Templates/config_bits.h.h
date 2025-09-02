#ifndef DEFINITIONS_H
#define DEFINITIONS_H

// *****************************************************************************
// Section: Included Files
// *****************************************************************************
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <xc.h>
#include <sys/attribs.h>
#include "toolchain_specifics.h"

// DOM-IGNORE-BEGIN
#ifdef __cplusplus
extern "C" {
#endif
// DOM-IGNORE-END

/* Device Information */
#define DEVICE_NAME          "PIC32MZ2048EFH064"
#define DEVICE_ARCH          "MIPS"
#define DEVICE_FAMILY        "PIC32MZEF"
#define DEVICE_SERIES        "PIC32MZ"

/* CPU clock frequency */
#define CPU_CLOCK_FREQUENCY 200000000U

// ... rest of your header file ...
#endif /* DEFINITIONS_H */