# 1. Template Directives

# 2. Configuration Loading and Defaults

# 3. Header Guards and Includes
#ifndef DEFINITIONS_H
#define DEFINITIONS_H

// *****************************************************************************
// Section: Included Files - Generated from: device_config.json
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

// *****************************************************************************
// *****************************************************************************
// Section: System Service Definitions
// *****************************************************************************
// *****************************************************************************
void SYS_Initialize(void *data);
void CLK_Initialize(void);

// *****************************************************************************
// *****************************************************************************
// Section: Library/Stack Definitions
// *****************************************************************************
// *****************************************************************************
void STACK_Init(void);

// *****************************************************************************
// *****************************************************************************
// Section: Driver Definitions
// *****************************************************************************
// *****************************************************************************
void DRV_TimerInitialize(void);
void DRV_USARTInitialize(void);

// *****************************************************************************
// *****************************************************************************
// Section: System Data Types
// *****************************************************************************
// *****************************************************************************
typedef struct
{
    uint32_t baudRate;
    uint8_t  dataBits;
    uint8_t  stopBits;
    uint8_t  parity;
} USART_CONFIG;

// *****************************************************************************
// *****************************************************************************
// Section: Configuration System Service Definitions
// *****************************************************************************
// *****************************************************************************

// DOM-IGNORE-BEGIN
#ifdef __cplusplus
}
#endif
// DOM-IGNORE-END

#endif /* DEFINITIONS_H */