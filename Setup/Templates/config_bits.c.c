# Updated config_bits.tt Template

// ****************************************************************************
// ****************************************************************************
// Section: Configuration Bits Generated from: device_config.json
// ****************************************************************************
// ****************************************************************************

/*** DEVCFG0 ***/
#pragma config DEBUG = OFF
#pragma config JTAGEN = OFF
#pragma config ICESEL = ICS_PGx1
#pragma config TRCEN = OFF
#pragma config BOOTISA = MIPS32
#pragma config FECCCON = OFF_UNLOCKED
#pragma config FSLEEP = OFF
#pragma config DBGPER = PG_ALL
#pragma config SMCLR = MCLR_NORM
#pragma config SOSCGAIN = GAIN_LEVEL_3
#pragma config SOSCBOOST = ON
#pragma config POSCGAIN = GAIN_LEVEL_3
#pragma config POSCBOOST = ON
#pragma config EJTAGBEN = NORMAL
#pragma config CP = OFF
/*** DEVCFG1 ***/
#pragma config FNOSC = SPLL
#pragma config DMTINTV = WIN_127_128
#pragma config FSOSCEN = OFF
#pragma config IESO = OFF
#pragma config POSCMOD = HS
#pragma config OSCIOFNC = OFF
#pragma config FCKSM = CSECME
#pragma config WDTPS = PS1048576
#pragma config WDTSPGM = STOP
#pragma config FWDTEN = OFF
#pragma config WINDIS = NORMAL
#pragma config FWDTWINSZ = WINSZ_25
#pragma config DMTCNT = DMT31
#pragma config FDMTEN = OFF
/*** DEVCFG2 ***/
#pragma config FPLLIDIV = DIV_3
#pragma config FPLLRNG = RANGE_8_16_MHZ
#pragma config FPLLICLK = PLL_POSC
#pragma config FPLLMULT = MUL_50
#pragma config FPLLODIV = DIV_2
#pragma config UPLLFSEL = FREQ_24MHZ
/*** DEVCFG3 ***/
#pragma config USERID = 0xFFFB
#pragma config FMIIEN = ON
#pragma config FETHIO = ON
#pragma config PGL1WAY = ON
#pragma config PMDL1WAY = ON
#pragma config IOL1WAY = ON
#pragma config FUSBIDIO = ON
/*** BF1SEQ0 ***/
#pragma config TSEQ = 0xffff
#pragma config CSEQ = 0x0

// *****************************************************************************
// *****************************************************************************
// Section: Local initialization functions
// *****************************************************************************
// *****************************************************************************
void SYS_Initialize(void* data)
{
    __builtin_disable_interrupts();
    CLK_Initialize();
    
    PRECONbits.PREFEN = 3;
    PRECONbits.PFMWS = 2;
    PRECONbits.ECCCON = 2;

    __builtin_enable_interrupts();
}

void CLK_Initialize(void)
{
    SYSKEY = 0x00000000U;
    SYSKEY = 0xAA996655U;
    SYSKEY = 0x556699AAU;

    CFGCONbits.PMDLOCK = 0;

    PMD1 = 0x1000U;  // TIMERS ENABLED

    PMD2 = 0x3U;
    PMD3 = 0x1F701FFU;
    PMD4 = 0x1FDU;
    PMD5 = 0x301F3F3CU;  // UART ENABLED

    PMD6 = 0x10830001U;
    PMD7 = 0x500000U;

    CFGCONbits.PMDLOCK = 1;
    PB3DIVbits.PBDIV = 3;
    SYSKEY = 0x33333333U;
}

