/********************************************************************************/
/*   Copyright (c) 2021 Realtek Semiconductor Corp. All rights reserved.        */
/*                                                                              */
/*   SPDX-License-Identifier: LicenseRef-Realtek-Proprietary                    */
/*                                                                              */
/*   This software component is confidential and proprietary to Realtek         */
/*   Semiconductor Corp. Disclosure, reproduction, redistribution, in whole     */
/*   or in part, of this work and its derivatives without express permission    */
/*   is prohibited.                                                             */
/********************************************************************************/

//----------------------------------------------------------------------------------------------------
// ID Code      : _TPV_21_715GF225_2H1DP_EDP.h No.0000
// Update Note  :
//----------------------------------------------------------------------------------------------------


//////////////////////////////
// RL6829 Series Pin Share //
//////////////////////////////

//---------------------------------------------------------------------------
// Function : HDMI1_DET
// Pinshare : 0x1000
// MCU Ctrl : 0xFE00 at _PIN_A3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_A3                                 (_PIN_A3_GPI)

typedef enum
{
    _PIN_A3_GPI = 0x00,
    _PIN_A3_GPO_PP = 0x01,
    _PIN_A3_GPO_OD = 0x02,
    _PIN_A3_DCLK = 0x03,
    _PIN_A3_TCON7 = 0x04,
    _PIN_A3_SWDCLK_0_3 = 0x05,
    _PIN_A3_TEST4B_OUT0 = 0x06,
    _PIN_A3_TEST4B_OUT1 = 0x07,
    _PIN_A3_TEST4B_OUT2 = 0x08,
    _PIN_A3_TEST4B_OUT3 = 0x09,
    _PIN_A3_TEST4B_OUT4 = 0x0A,
    _PIN_A3_TEST4B_OUT5 = 0x0B,
    _PIN_A3_TEST4B_OUT6 = 0x0C,
    _PIN_A3_TEST4B_OUT7 = 0x0D,
    _PIN_A3_NC = _PIN_A3_GPO_PP,
} EnumPinshareInfoPINA3;

//---------------------------------------------------------------------------
// Function : EDID_WP
// Pinshare : 0x1001
// MCU Ctrl : 0xFE01 at _PIN_C5_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C5                                 (_PIN_C5_GPO_OD)

typedef enum
{
    _PIN_C5_GPI = 0x00,
    _PIN_C5_GPO_PP = 0x01,
    _PIN_C5_GPO_OD = 0x02,
    _PIN_C5_TTL_DEN = 0x03,
    _PIN_C5_TCON8 = 0x04,
    _PIN_C5_SWDIO_0_3 = 0x05,
    _PIN_C5_TEST4B_OUT0 = 0x06,
    _PIN_C5_TEST4B_OUT1 = 0x07,
    _PIN_C5_TEST4B_OUT2 = 0x08,
    _PIN_C5_TEST4B_OUT3 = 0x09,
    _PIN_C5_TEST4B_OUT4 = 0x0A,
    _PIN_C5_TEST4B_OUT5 = 0x0B,
    _PIN_C5_TEST4B_OUT6 = 0x0C,
    _PIN_C5_TEST4B_OUT7 = 0x0D,
    _PIN_C5_NC = _PIN_C5_GPO_PP,
} EnumPinshareInfoPINC5;

//---------------------------------------------------------------------------
// Function : LEDA
// Pinshare : 0x1002
// MCU Ctrl : 0xFE02 at _PIN_B3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B3                                 (_PIN_B3_GPI)

typedef enum
{
    _PIN_B3_GPI = 0x00,
    _PIN_B3_GPO_PP = 0x01,
    _PIN_B3_GPO_OD = 0x02,
    _PIN_B3_PWM_OUT = 0x03,
    _PIN_B3_PWM3_PP = 0x04,
    _PIN_B3_PWM3_OD = 0x05,
    _PIN_B3_PWM3_DIMMING_PP = 0x06,
    _PIN_B3_PWM3_DIMMING = 0x07,
    _PIN_B3_DCLK = 0x08,
    _PIN_B3_TCON9 = 0x09,
    _PIN_B3_TEST4B_OUT0 = 0x0A,
    _PIN_B3_TEST4B_OUT1 = 0x0B,
    _PIN_B3_TEST4B_OUT2 = 0x0C,
    _PIN_B3_TEST4B_OUT3 = 0x0D,
    _PIN_B3_TEST4B_OUT4 = 0x0E,
    _PIN_B3_TEST4B_OUT5 = 0x0F,
    _PIN_B3_NC = _PIN_B3_GPO_PP,
} EnumPinshareInfoPINB3;

//---------------------------------------------------------------------------
// Function : DDR_PW_EN
// Pinshare : 0x1003
// MCU Ctrl : 0xFE03 at _PIN_B4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B4                                 (_PIN_B4_GPO_OD)

typedef enum
{
    _PIN_B4_GPI = 0x00,
    _PIN_B4_GPO_PP = 0x01,
    _PIN_B4_GPO_OD = 0x02,
    _PIN_B4_EXT_UART_TX_0_4 = 0x03,
    _PIN_B4_EXT_UART_TX_1_4 = 0x04,
    _PIN_B4_EXT_UART_TX_2_4 = 0x05,
    _PIN_B4_TEST4B_OUT0 = 0x06,
    _PIN_B4_TEST4B_OUT1 = 0x07,
    _PIN_B4_TEST4B_OUT2 = 0x08,
    _PIN_B4_TEST4B_OUT3 = 0x09,
    _PIN_B4_TEST4B_OUT4 = 0x0A,
    _PIN_B4_TEST4B_OUT5 = 0x0B,
    _PIN_B4_TEST4B_OUT6 = 0x0C,
    _PIN_B4_TEST4B_OUT7 = 0x0D,
    _PIN_B4_NC = _PIN_B4_GPO_PP,
} EnumPinshareInfoPINB4;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1004
// MCU Ctrl : 0xFE04 at _PIN_B2_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B2                                 (_PIN_B2_NC)

typedef enum
{
    _PIN_B2_GPI = 0x00,
    _PIN_B2_GPO_PP = 0x01,
    _PIN_B2_GPO_OD = 0x02,
    _PIN_B2_EXT_UART_RX_0_4 = 0x03,
    _PIN_B2_EXT_UART_RX_1_4 = 0x04,
    _PIN_B2_EXT_UART_RX_2_4 = 0x05,
    _PIN_B2_TEST4B_OUT0 = 0x06,
    _PIN_B2_TEST4B_OUT1 = 0x07,
    _PIN_B2_TEST4B_OUT2 = 0x08,
    _PIN_B2_TEST4B_OUT3 = 0x09,
    _PIN_B2_TEST4B_OUT4 = 0x0A,
    _PIN_B2_TEST4B_OUT5 = 0x0B,
    _PIN_B2_TEST4B_OUT6 = 0x0C,
    _PIN_B2_TEST4B_OUT7 = 0x0D,
    _PIN_B2_NC = _PIN_B2_GPO_PP,
} EnumPinshareInfoPINB2;

//---------------------------------------------------------------------------
// Function : BKLT_EN
// Pinshare : 0x1005
// MCU Ctrl : 0xFE05 at _PIN_C4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C4                                 (_PIN_C4_GPO_PP)

typedef enum
{
    _PIN_C4_GPI = 0x00,
    _PIN_C4_GPO_PP = 0x01,
    _PIN_C4_GPO_OD = 0x02,
    _PIN_C4_EXT_UART_TX_0_5 = 0x03,
    _PIN_C4_EXT_UART_TX_1_5 = 0x04,
    _PIN_C4_EXT_UART_TX_2_5 = 0x05,
    _PIN_C4_TEST4B_OUT0 = 0x06,
    _PIN_C4_TEST4B_OUT1 = 0x07,
    _PIN_C4_TEST4B_OUT2 = 0x08,
    _PIN_C4_TEST4B_OUT3 = 0x09,
    _PIN_C4_TEST4B_OUT4 = 0x0A,
    _PIN_C4_TEST4B_OUT5 = 0x0B,
    _PIN_C4_TEST4B_OUT6 = 0x0C,
    _PIN_C4_TEST4B_OUT7 = 0x0D,
    _PIN_C4_NC = _PIN_C4_GPO_PP,
} EnumPinshareInfoPINC4;

//---------------------------------------------------------------------------
// Function : HDMI1_HPD
// Pinshare : 0x1006
// MCU Ctrl : 0xFE06 at _PIN_B1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B1                                 (_PIN_B1_GPO_OD)

typedef enum
{
    _PIN_B1_GPI = 0x00,
    _PIN_B1_GPO_PP = 0x01,
    _PIN_B1_GPO_OD = 0x02,
    _PIN_B1_EXT_UART_RX_0_5 = 0x03,
    _PIN_B1_EXT_UART_RX_1_5 = 0x04,
    _PIN_B1_EXT_UART_RX_2_5 = 0x05,
    _PIN_B1_TTL_DEN = 0x06,
    _PIN_B1_TCON10 = 0x07,
    _PIN_B1_TEST4B_OUT0 = 0x08,
    _PIN_B1_TEST4B_OUT1 = 0x09,
    _PIN_B1_TEST4B_OUT2 = 0x0A,
    _PIN_B1_TEST4B_OUT3 = 0x0B,
    _PIN_B1_TEST4B_OUT4 = 0x0C,
    _PIN_B1_TEST4B_OUT5 = 0x0D,
    _PIN_B1_TEST4B_OUT6 = 0x0E,
    _PIN_B1_TEST4B_OUT7 = 0x0F,
    _PIN_B1_NC = _PIN_B1_GPO_PP,
} EnumPinshareInfoPINB1;

//---------------------------------------------------------------------------
// Function : HDMI2_HPD
// Pinshare : 0x1007
// MCU Ctrl : 0xFE07 at _PIN_C1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C1                                 (_PIN_C1_GPO_OD)

typedef enum
{
    _PIN_C1_GPI = 0x00,
    _PIN_C1_GPO_PP = 0x01,
    _PIN_C1_GPO_OD = 0x02,
    _PIN_C1_TTL_DVS = 0x03,
    _PIN_C1_TCON11 = 0x04,
    _PIN_C1_TEST4B_OUT0 = 0x05,
    _PIN_C1_TEST4B_OUT1 = 0x06,
    _PIN_C1_TEST4B_OUT2 = 0x07,
    _PIN_C1_TEST4B_OUT3 = 0x08,
    _PIN_C1_TEST4B_OUT4 = 0x09,
    _PIN_C1_TEST4B_OUT5 = 0x0A,
    _PIN_C1_TEST4B_OUT6 = 0x0B,
    _PIN_C1_TEST4B_OUT7 = 0x0C,
    _PIN_C1_NC = _PIN_C1_GPO_PP,
} EnumPinshareInfoPINC1;

//---------------------------------------------------------------------------
// Function : HDMI2_DET
// Pinshare : 0x1008
// MCU Ctrl : 0xFE08 at _PIN_E4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E4                                 (_PIN_E4_GPI)

typedef enum
{
    _PIN_E4_GPI = 0x00,
    _PIN_E4_GPO_PP = 0x01,
    _PIN_E4_GPO_OD = 0x02,
    _PIN_E4_TTL_DHS = 0x03,
    _PIN_E4_TCON12 = 0x04,
    _PIN_E4_USB_SPI_CLK_0_0 = 0x05,
    _PIN_E4_USB_SPI_CLK_1_0 = 0x06,
    _PIN_E4_USB_SPI_CLK_2_0 = 0x07,
    _PIN_E4_TEST4B_OUT0 = 0x08,
    _PIN_E4_TEST4B_OUT1 = 0x09,
    _PIN_E4_TEST4B_OUT2 = 0x0A,
    _PIN_E4_TEST4B_OUT3 = 0x0B,
    _PIN_E4_TEST4B_OUT4 = 0x0C,
    _PIN_E4_TEST4B_OUT5 = 0x0D,
    _PIN_E4_TEST4B_OUT6 = 0x0E,
    _PIN_E4_TEST4B_OUT7 = 0x0F,
    _PIN_E4_NC = _PIN_E4_GPO_PP,
} EnumPinshareInfoPINE4;

//---------------------------------------------------------------------------
// Function : EESCL
// Pinshare : 0x1009
// MCU Ctrl : 0xFE09 at _PIN_E3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E3                                 (_PIN_E3_EEIICSCL)

typedef enum
{
    _PIN_E3_GPI = 0x00,
    _PIN_E3_GPO_PP = 0x01,
    _PIN_E3_GPO_OD = 0x02,
    _PIN_E3_EEIICSCL = 0x03,
    _PIN_E3_NC = _PIN_E3_GPO_PP,
} EnumPinshareInfoPINE3;

//---------------------------------------------------------------------------
// Function : EESDA
// Pinshare : 0x100A
// MCU Ctrl : 0xFE0A at _PIN_E2_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E2                                 (_PIN_E2_EEIICSDA)

typedef enum
{
    _PIN_E2_GPI = 0x00,
    _PIN_E2_GPO_PP = 0x01,
    _PIN_E2_GPO_OD = 0x02,
    _PIN_E2_EEIICSDA = 0x03,
    _PIN_E2_NC = _PIN_E2_GPO_PP,
} EnumPinshareInfoPINE2;

//---------------------------------------------------------------------------
// Function : EE_WP (H:ON)
// Pinshare : 0x100B
// MCU Ctrl : 0xFE0B at _PIN_C2_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C2                                 (_PIN_C2_GPO_OD)

typedef enum
{
    _PIN_C2_GPI = 0x00,
    _PIN_C2_GPO_PP = 0x01,
    _PIN_C2_GPO_OD = 0x02,
    _PIN_C2_USB_SPI_SI_0_0 = 0x03,
    _PIN_C2_USB_SPI_SI_1_0 = 0x04,
    _PIN_C2_USB_SPI_SI_2_0 = 0x05,
    _PIN_C2_NC = _PIN_C2_GPO_PP,
} EnumPinshareInfoPINC2;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x100C
// MCU Ctrl : 0xFE0C at _PIN_F3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F3                                 (_PIN_F3_NC)

typedef enum
{
    _PIN_F3_GPI = 0x00,
    _PIN_F3_GPO_PP = 0x01,
    _PIN_F3_GPO_OD = 0x02,
    _PIN_F3_EXT_UART_TX_0_0 = 0x03,
    _PIN_F3_EXT_UART_TX_1_0 = 0x04,
    _PIN_F3_EXT_UART_TX_2_0 = 0x05,
    _PIN_F3_USB_SPI_SO_0_0 = 0x06,
    _PIN_F3_USB_SPI_SO_1_0 = 0x07,
    _PIN_F3_USB_SPI_SO_2_0 = 0x08,
    _PIN_F3_CLKO = 0x09,
    _PIN_F3_TEST4B_OUT0 = 0x0A,
    _PIN_F3_TEST4B_OUT1 = 0x0B,
    _PIN_F3_TEST4B_OUT2 = 0x0C,
    _PIN_F3_TEST4B_OUT3 = 0x0D,
    _PIN_F3_TEST4B_OUT4 = 0x0E,
    _PIN_F3_TEST4B_OUT5 = 0x0F,
    _PIN_F3_NC = _PIN_F3_GPO_PP,
} EnumPinshareInfoPINF3;

//---------------------------------------------------------------------------
// Function : USB_ON
// Pinshare : 0x100D
// MCU Ctrl : 0xFE0D at _PIN_F2_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F2                                 (_PIN_F2_GPO_PP)

typedef enum
{
    _PIN_F2_GPI = 0x00,
    _PIN_F2_GPO_PP = 0x01,
    _PIN_F2_GPO_OD = 0x02,
    _PIN_F2_EXT_UART_RX_0_0 = 0x03,
    _PIN_F2_EXT_UART_RX_1_0 = 0x04,
    _PIN_F2_EXT_UART_RX_2_0 = 0x05,
    _PIN_F2_USB_SPI_CEB0_0_0 = 0x06,
    _PIN_F2_USB_SPI_CEB0_1_0 = 0x07,
    _PIN_F2_USB_SPI_CEB0_2_0 = 0x08,
    _PIN_F2_CLKO = 0x09,
    _PIN_F2_TEST4B_OUT0 = 0x0A,
    _PIN_F2_TEST4B_OUT1 = 0x0B,
    _PIN_F2_TEST4B_OUT2 = 0x0C,
    _PIN_F2_TEST4B_OUT3 = 0x0D,
    _PIN_F2_TEST4B_OUT4 = 0x0E,
    _PIN_F2_TEST4B_OUT5 = 0x0F,
    _PIN_F2_NC = _PIN_F2_GPO_PP,
} EnumPinshareInfoPINF2;

//---------------------------------------------------------------------------
// Function : NC(POWER_ON)
// Pinshare : 0x100E
// MCU Ctrl : 0xFE0E at _PIN_C3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C3                                 (_PIN_C3_NC)

typedef enum
{
    _PIN_C3_GPI = 0x00,
    _PIN_C3_GPO_PP = 0x01,
    _PIN_C3_GPO_OD = 0x02,
    _PIN_C3_EXT_UART_TX_0_1 = 0x03,
    _PIN_C3_EXT_UART_TX_1_1 = 0x04,
    _PIN_C3_EXT_UART_TX_2_1 = 0x05,
    _PIN_C3_USB_SPI_CEB1_0_0 = 0x06,
    _PIN_C3_USB_SPI_CEB1_1_0 = 0x07,
    _PIN_C3_USB_SPI_CEB1_2_0 = 0x08,
    _PIN_C3_TEST4B_OUT0 = 0x09,
    _PIN_C3_TEST4B_OUT1 = 0x0A,
    _PIN_C3_TEST4B_OUT2 = 0x0B,
    _PIN_C3_TEST4B_OUT3 = 0x0C,
    _PIN_C3_TEST4B_OUT4 = 0x0D,
    _PIN_C3_TEST4B_OUT5 = 0x0E,
    _PIN_C3_TEST4B_OUT6 = 0x0F,
    _PIN_C3_NC = _PIN_C3_GPO_PP,
} EnumPinshareInfoPINC3;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x100F
// MCU Ctrl : 0xFE0F at _PIN_D4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_D4                                 (_PIN_D4_NC)

typedef enum
{
    _PIN_D4_GPI = 0x00,
    _PIN_D4_GPO_PP = 0x01,
    _PIN_D4_GPO_OD = 0x02,
    _PIN_D4_EXT_UART_RX_0_1 = 0x03,
    _PIN_D4_EXT_UART_RX_1_1 = 0x04,
    _PIN_D4_EXT_UART_RX_2_1 = 0x05,
    _PIN_D4_DISP_FRAME_START_IN = 0x06,
    _PIN_D4_DISP_FRAME_START_OUT = 0x07,
    _PIN_D4_MCK = 0x08,
    _PIN_D4_TEST4B_OUT0 = 0x09,
    _PIN_D4_TEST4B_OUT1 = 0x0A,
    _PIN_D4_TEST4B_OUT2 = 0x0B,
    _PIN_D4_TEST4B_OUT3 = 0x0C,
    _PIN_D4_TEST4B_OUT4 = 0x0D,
    _PIN_D4_TEST4B_OUT5 = 0x0E,
    _PIN_D4_TEST4B_OUT6 = 0x0F,
    _PIN_D4_NC = _PIN_D4_GPO_PP,
} EnumPinshareInfoPIND4;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1010
// MCU Ctrl : 0xFE10 at _PIN_D2_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_D2                                 (_PIN_D2_NC)

typedef enum
{
    _PIN_D2_GPI = 0x00,
    _PIN_D2_GPO_PP = 0x01,
    _PIN_D2_GPO_OD = 0x02,
    _PIN_D2_EXT_UART_TX_0_2 = 0x03,
    _PIN_D2_EXT_UART_TX_1_2 = 0x04,
    _PIN_D2_EXT_UART_TX_2_2 = 0x05,
    _PIN_D2_SCK = 0x06,
    _PIN_D2_TEST4B_OUT0 = 0x07,
    _PIN_D2_TEST4B_OUT1 = 0x08,
    _PIN_D2_TEST4B_OUT2 = 0x09,
    _PIN_D2_TEST4B_OUT3 = 0x0A,
    _PIN_D2_TEST4B_OUT4 = 0x0B,
    _PIN_D2_TEST4B_OUT5 = 0x0C,
    _PIN_D2_TEST4B_OUT6 = 0x0D,
    _PIN_D2_TEST4B_OUT7 = 0x0E,
    _PIN_D2_NC = _PIN_D2_GPO_PP,
} EnumPinshareInfoPIND2;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1011
// MCU Ctrl : 0xFE11 at _PIN_D3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_D3                                 (_PIN_D3_NC)

typedef enum
{
    _PIN_D3_GPI = 0x00,
    _PIN_D3_GPO_PP = 0x01,
    _PIN_D3_GPO_OD = 0x02,
    _PIN_D3_EXT_UART_RX_0_2 = 0x03,
    _PIN_D3_EXT_UART_RX_1_2 = 0x04,
    _PIN_D3_EXT_UART_RX_2_2 = 0x05,
    _PIN_D3_WS = 0x07,
    _PIN_D3_TEST4B_OUT0 = 0x08,
    _PIN_D3_TEST4B_OUT1 = 0x09,
    _PIN_D3_TEST4B_OUT2 = 0x0A,
    _PIN_D3_TEST4B_OUT3 = 0x0B,
    _PIN_D3_TEST4B_OUT4 = 0x0C,
    _PIN_D3_TEST4B_OUT5 = 0x0D,
    _PIN_D3_TEST4B_OUT6 = 0x0E,
    _PIN_D3_TEST4B_OUT7 = 0x0F,
    _PIN_D3_NC = _PIN_D3_GPO_PP,
} EnumPinshareInfoPIND3;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1012
// MCU Ctrl : 0xFE12 at _PIN_D1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_D1                                 (_PIN_D1_NC)

typedef enum
{
    _PIN_D1_GPI = 0x00,
    _PIN_D1_GPO_PP = 0x01,
    _PIN_D1_GPO_OD = 0x02,
    _PIN_D1_IICSCL_0_1 = 0x03,
    _PIN_D1_IICSCL_1_1 = 0x04,
    _PIN_D1_SD0 = 0x05,
    _PIN_D1_SPDIF0 = 0x06,
    _PIN_D1_TEST4B_OUT0 = 0x07,
    _PIN_D1_TEST4B_OUT1 = 0x08,
    _PIN_D1_TEST4B_OUT2 = 0x09,
    _PIN_D1_TEST4B_OUT3 = 0x0A,
    _PIN_D1_TEST4B_OUT4 = 0x0B,
    _PIN_D1_TEST4B_OUT5 = 0x0C,
    _PIN_D1_TEST4B_OUT6 = 0x0D,
    _PIN_D1_TEST4B_OUT7 = 0x0E,
    _PIN_D1_NC = _PIN_D1_GPO_PP,
} EnumPinshareInfoPIND1;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1013
// MCU Ctrl : 0xFE13 at _PIN_E1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E1                                 (_PIN_E1_NC)

typedef enum
{
    _PIN_E1_GPI = 0x00,
    _PIN_E1_GPO_PP = 0x01,
    _PIN_E1_GPO_OD = 0x02,
    _PIN_E1_IICSDA_0_1 = 0x03,
    _PIN_E1_IICSDA_1_1 = 0x04,
    _PIN_E1_TCON6 = 0x05,
    _PIN_E1_SD1 = 0x06,
    _PIN_E1_SPDIF1 = 0x07,
    _PIN_E1_TEST4B_OUT0 = 0x08,
    _PIN_E1_TEST4B_OUT1 = 0x09,
    _PIN_E1_TEST4B_OUT2 = 0x0A,
    _PIN_E1_TEST4B_OUT3 = 0x0B,
    _PIN_E1_TEST4B_OUT4 = 0x0C,
    _PIN_E1_TEST4B_OUT5 = 0x0D,
    _PIN_E1_TEST4B_OUT6 = 0x0E,
    _PIN_E1_TEST4B_OUT7 = 0x0F,
    _PIN_E1_NC = _PIN_E1_GPO_PP,
} EnumPinshareInfoPINE1;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1014
// MCU Ctrl : 0xFE14 at _PIN_J1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_J1                                 (_PIN_J1_NC)

typedef enum
{
    _PIN_J1_GPI = 0x00,
    _PIN_J1_GPO_PP = 0x01,
    _PIN_J1_GPO_OD = 0x02,
    _PIN_J1_CEC = 0x03,
    _PIN_J1_TCON13 = 0x04,
    _PIN_J1_TEST4B_OUT0 = 0x05,
    _PIN_J1_TEST4B_OUT1 = 0x06,
    _PIN_J1_TEST4B_OUT2 = 0x07,
    _PIN_J1_TEST4B_OUT3 = 0x08,
    _PIN_J1_TEST4B_OUT4 = 0x09,
    _PIN_J1_TEST4B_OUT5 = 0x0A,
    _PIN_J1_TEST4B_OUT6 = 0x0B,
    _PIN_J1_TEST4B_OUT7 = 0x0C,
    _PIN_J1_NC = _PIN_J1_GPO_PP,
} EnumPinshareInfoPINJ1;

//---------------------------------------------------------------------------
// Function : PANEL_SCL (reserved)
// Pinshare : 0x1015
// MCU Ctrl : 0xFE15 at _PIN_F4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F4                                 (_PIN_F4_GPO_OD)

typedef enum
{
    _PIN_F4_GPI = 0x00,
    _PIN_F4_GPO_PP = 0x01,
    _PIN_F4_GPO_OD = 0x02,
    _PIN_F4_IICSCL_0_2 = 0x03,
    _PIN_F4_IICSCL_1_2 = 0x04,
    _PIN_F4_SD2 = 0x05,
    _PIN_F4_SPDIF2 = 0x06,
    _PIN_F4_TEST4B_OUT0 = 0x07,
    _PIN_F4_TEST4B_OUT1 = 0x08,
    _PIN_F4_TEST4B_OUT2 = 0x09,
    _PIN_F4_TEST4B_OUT3 = 0x0A,
    _PIN_F4_TEST4B_OUT4 = 0x0B,
    _PIN_F4_TEST4B_OUT5 = 0x0C,
    _PIN_F4_TEST4B_OUT6 = 0x0D,
    _PIN_F4_TEST4B_OUT7 = 0x0E,
    _PIN_F4_NC = _PIN_F4_GPO_PP,
} EnumPinshareInfoPINF4;

//---------------------------------------------------------------------------
// Function : PANEL_SDA (reserved)
// Pinshare : 0x1016
// MCU Ctrl : 0xFE16 at _PIN_G1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G1                                 (_PIN_G1_GPO_OD)

typedef enum
{
    _PIN_G1_GPI = 0x00,
    _PIN_G1_GPO_PP = 0x01,
    _PIN_G1_GPO_OD = 0x02,
    _PIN_G1_IICSDA_0_2 = 0x03,
    _PIN_G1_IICSDA_1_2 = 0x04,
    _PIN_G1_INT0_2 = 0x05,
    _PIN_G1_INT1_2 = 0x06,
    _PIN_G1_TCON1 = 0x07,
    _PIN_G1_TCON0 = 0x08,
    _PIN_G1_SD3 = 0x09,
    _PIN_G1_SPDIF3 = 0x0A,
    _PIN_G1_TEST4B_OUT0 = 0x0B,
    _PIN_G1_TEST4B_OUT1 = 0x0C,
    _PIN_G1_TEST4B_OUT2 = 0x0D,
    _PIN_G1_TEST4B_OUT3 = 0x0E,
    _PIN_G1_NC = _PIN_G1_GPO_PP,
} EnumPinshareInfoPING1;

//---------------------------------------------------------------------------
// Function : LEDG(PWM)
// Pinshare : 0x1017
// MCU Ctrl : 0xFE17 at _PIN_H4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H4                                 (_PIN_H4_GPI)

typedef enum
{
    _PIN_H4_GPI = 0x00,
    _PIN_H4_GPO_PP = 0x01,
    _PIN_H4_GPO_OD = 0x02,
    _PIN_H4_PWM_IN = 0x03,
    _PIN_H4_PWM2_PP = 0x04,
    _PIN_H4_PWM2_OD = 0x05,
    _PIN_H4_PWM2_DIMMING_PP = 0x06,
    _PIN_H4_PWM2_DIMMING = 0x07,
    _PIN_H4_M1_IDOMAIN_DEN_OUT = 0x08,
    _PIN_H4_TCON5 = 0x09,
    _PIN_H4_TEST4B_OUT0 = 0x0A,
    _PIN_H4_TEST4B_OUT1 = 0x0B,
    _PIN_H4_TEST4B_OUT2 = 0x0C,
    _PIN_H4_TEST4B_OUT3 = 0x0D,
    _PIN_H4_TEST4B_OUT4 = 0x0E,
    _PIN_H4_TEST4B_OUT5 = 0x0F,
    _PIN_H4_NC = _PIN_H4_GPO_PP,
} EnumPinshareInfoPINH4;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1018
// MCU Ctrl : 0xFE18 at _PIN_Y5_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_Y5                                 (_PIN_Y5_NC)

typedef enum
{
    _PIN_Y5_GPI = 0x00,
    _PIN_Y5_GPO_PP = 0x01,
    _PIN_Y5_GPO_OD = 0x02,
    _PIN_Y5_USB_SPI_CLK_0_5 = 0x03,
    _PIN_Y5_USB_SPI_CLK_1_5 = 0x04,
    _PIN_Y5_USB_SPI_CLK_2_5 = 0x05,
    _PIN_Y5_TTL_DVS = 0x06,
    _PIN_Y5_INT0_0 = 0x07,
    _PIN_Y5_INT1_0 = 0x08,
    _PIN_Y5_TEST4B_OUT0 = 0x09,
    _PIN_Y5_TEST4B_OUT2 = 0x0B,
    _PIN_Y5_TEST4B_OUT3 = 0x0C,
    _PIN_Y5_TEST4B_OUT4 = 0x0D,
    _PIN_Y5_TEST4B_OUT5 = 0x0E,
    _PIN_Y5_TEST4B_OUT6 = 0x0F,
    _PIN_Y5_NC = _PIN_Y5_GPO_PP,
} EnumPinshareInfoPINY5;

//---------------------------------------------------------------------------
// Function : HDMI1_A0_SEL
// Pinshare : 0x1019
// MCU Ctrl : 0xFE19 at _PIN_Y4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_Y4                                 (_PIN_Y4_GPO_OD)

typedef enum
{
    _PIN_Y4_GPI = 0x00,
    _PIN_Y4_GPO_PP = 0x01,
    _PIN_Y4_GPO_OD = 0x02,
    _PIN_Y4_USB_SPI_CLK_0_6 = 0x03,
    _PIN_Y4_USB_SPI_CLK_1_6 = 0x04,
    _PIN_Y4_USB_SPI_CLK_2_6 = 0x05,
    _PIN_Y4_M1_IDOMAIN_HS_OUT = 0x06,
    _PIN_Y4_TEST4B_OUT0 = 0x07,
    _PIN_Y4_TEST4B_OUT1 = 0x08,
    _PIN_Y4_TEST4B_OUT2 = 0x09,
    _PIN_Y4_TEST4B_OUT3 = 0x0A,
    _PIN_Y4_TEST4B_OUT4 = 0x0B,
    _PIN_Y4_TEST4B_OUT5 = 0x0C,
    _PIN_Y4_TEST4B_OUT6 = 0x0D,
    _PIN_Y4_TEST4B_OUT7 = 0x0E,
    _PIN_Y4_NC = _PIN_Y4_GPO_PP,
} EnumPinshareInfoPINY4;

//---------------------------------------------------------------------------
// Function : NC(VOLUME)
// Pinshare : 0x101A
// MCU Ctrl : 0xFE1A at _PIN_AB5_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AB5                                (_PIN_AB5_NC)

typedef enum
{
    _PIN_AB5_GPI = 0x00,
    _PIN_AB5_GPO_PP = 0x01,
    _PIN_AB5_GPO_OD = 0x02,
    _PIN_AB5_IICSCL_0_6 = 0x03,
    _PIN_AB5_IICSCL_1_6 = 0x04,
    _PIN_AB5_PWM5_PP = 0x05,
    _PIN_AB5_PWM5_OD = 0x06,
    _PIN_AB5_PWM5_DIMMING_PP = 0x07,
    _PIN_AB5_PWM5_DIMMING = 0x08,
    _PIN_AB5_TTL_DHS = 0x09,
    _PIN_AB5_TEST4B_OUT0 = 0x0A,
    _PIN_AB5_TEST4B_OUT1 = 0x0B,
    _PIN_AB5_TEST4B_OUT2 = 0x0C,
    _PIN_AB5_TEST4B_OUT3 = 0x0D,
    _PIN_AB5_TEST4B_OUT4 = 0x0E,
    _PIN_AB5_TEST4B_OUT5 = 0x0F,
    _PIN_AB5_NC = _PIN_AB5_GPO_PP,
} EnumPinshareInfoPINAB5;

//---------------------------------------------------------------------------
// Function : POWER
// Pinshare : 0x101B
// MCU Ctrl : 0xFE1B at _PIN_AB6_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AB6                                (_PIN_AB6_GPI)

typedef enum
{
    _PIN_AB6_GPI = 0x00,
    _PIN_AB6_GPO_PP = 0x01,
    _PIN_AB6_GPO_OD = 0x02,
    _PIN_AB6_IICSDA_0_6 = 0x03,
    _PIN_AB6_IICSDA_1_6 = 0x04,
    _PIN_AB6_INT0_1 = 0x05,
    _PIN_AB6_INT1_1 = 0x06,
    _PIN_AB6_M1_IDOMAIN_VS_OUT = 0x07,
    _PIN_AB6_TEST4B_OUT0 = 0x08,
    _PIN_AB6_TEST4B_OUT1 = 0x09,
    _PIN_AB6_TEST4B_OUT2 = 0x0A,
    _PIN_AB6_TEST4B_OUT3 = 0x0B,
    _PIN_AB6_TEST4B_OUT4 = 0x0C,
    _PIN_AB6_TEST4B_OUT5 = 0x0D,
    _PIN_AB6_TEST4B_OUT6 = 0x0E,
    _PIN_AB6_TEST4B_OUT7 = 0x0F,
    _PIN_AB6_NC = _PIN_AB6_GPO_PP,
} EnumPinshareInfoPINAB6;

//---------------------------------------------------------------------------
// Function : NC(AUDIO_SD)
// Pinshare : 0x101C
// MCU Ctrl : 0xFE1C at _PIN_AC6_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AC6                                (_PIN_AC6_NC)

typedef enum
{
    _PIN_AC6_GPI = 0x00,
    _PIN_AC6_GPO_PP = 0x01,
    _PIN_AC6_GPO_OD = 0x02,
    _PIN_AC6_PWM0_PP = 0x03,
    _PIN_AC6_PWM0_OD = 0x04,
    _PIN_AC6_PWM0_DIMMING_PP = 0x05,
    _PIN_AC6_PWM0_DIMMING = 0x06,
    _PIN_AC6_IICSCL_0_3 = 0x07,
    _PIN_AC6_IICSCL_1_3 = 0x08,
    _PIN_AC6_TCON2 = 0x09,
    _PIN_AC6_TEST4B_OUT0 = 0x0A,
    _PIN_AC6_TEST4B_OUT1 = 0x0B,
    _PIN_AC6_TEST4B_OUT2 = 0x0C,
    _PIN_AC6_TEST4B_OUT3 = 0x0D,
    _PIN_AC6_TEST4B_OUT4 = 0x0E,
    _PIN_AC6_TEST4B_OUT5 = 0x0F,
    _PIN_AC6_NC = _PIN_AC6_GPO_PP,
} EnumPinshareInfoPINAC6;

//---------------------------------------------------------------------------
// Function : NC(AUDIO_MUTE)
// Pinshare : 0x101D
// MCU Ctrl : 0xFE1D at _PIN_AA8_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AA8                                (_PIN_AA8_NC)

typedef enum
{
    _PIN_AA8_GPI = 0x00,
    _PIN_AA8_GPO_PP = 0x01,
    _PIN_AA8_GPO_OD = 0x02,
    _PIN_AA8_PWM_UPD_SYNC_0_1_PP = 0x03,
    _PIN_AA8_IICSDA_0_3 = 0x04,
    _PIN_AA8_IICSDA_1_3 = 0x05,
    _PIN_AA8_INT0_3 = 0x06,
    _PIN_AA8_INT1_3 = 0x07,
    _PIN_AA8_TCON3 = 0x08,
    _PIN_AA8_TEST4B_OUT0 = 0x09,
    _PIN_AA8_TEST4B_OUT1 = 0x0A,
    _PIN_AA8_TEST4B_OUT2 = 0x0B,
    _PIN_AA8_TEST4B_OUT3 = 0x0C,
    _PIN_AA8_TEST4B_OUT4 = 0x0D,
    _PIN_AA8_TEST4B_OUT5 = 0x0E,
    _PIN_AA8_TEST4B_OUT6 = 0x0F,
    _PIN_AA8_NC = _PIN_AA8_GPO_PP,
} EnumPinshareInfoPINAA8;

//---------------------------------------------------------------------------
// Function : USB_DET
// Pinshare : 0x101E
// MCU Ctrl : 0xFE1E at _PIN_AH1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AH1                                (_PIN_AH1_GPI)

typedef enum
{
    _PIN_AH1_GPI = 0x00,
    _PIN_AH1_GPO_PP = 0x01,
    _PIN_AH1_GPO_OD = 0x02,
    _PIN_AH1_TPC_IICSCL_0_0 = 0x03,
    _PIN_AH1_TPC_IICSCL_1_0 = 0x04,
    _PIN_AH1_TEST4B_OUT0 = 0x05,
    _PIN_AH1_TEST4B_OUT1 = 0x06,
    _PIN_AH1_TEST4B_OUT2 = 0x07,
    _PIN_AH1_TEST4B_OUT3 = 0x08,
    _PIN_AH1_TEST4B_OUT4 = 0x09,
    _PIN_AH1_TEST4B_OUT5 = 0x0A,
    _PIN_AH1_TEST4B_OUT6 = 0x0B,
    _PIN_AH1_TEST4B_OUT7 = 0x0C,
    _PIN_AH1_NC = _PIN_AH1_GPO_PP,
} EnumPinshareInfoPINAH1;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x101F
// MCU Ctrl : 0xFE1F at _PIN_AJ1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AJ1                                (_PIN_AJ1_NC)

typedef enum
{
    _PIN_AJ1_GPI = 0x00,
    _PIN_AJ1_GPO_PP = 0x01,
    _PIN_AJ1_GPO_OD = 0x02,
    _PIN_AJ1_TPC_IICSDA_0_0 = 0x03,
    _PIN_AJ1_TPC_IICSDA_1_0 = 0x04,
    _PIN_AJ1_TEST4B_OUT0 = 0x05,
    _PIN_AJ1_TEST4B_OUT1 = 0x06,
    _PIN_AJ1_TEST4B_OUT2 = 0x07,
    _PIN_AJ1_TEST4B_OUT3 = 0x08,
    _PIN_AJ1_TEST4B_OUT4 = 0x09,
    _PIN_AJ1_TEST4B_OUT5 = 0x0A,
    _PIN_AJ1_TEST4B_OUT6 = 0x0B,
    _PIN_AJ1_TEST4B_OUT7 = 0x0C,
    _PIN_AJ1_NC = _PIN_AJ1_GPO_PP,
} EnumPinshareInfoPINAJ1;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1020
// MCU Ctrl : 0xFE20 at _PIN_AD6_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AD6                                (_PIN_AD6_NC)

typedef enum
{
    _PIN_AD6_GPI = 0x00,
    _PIN_AD6_GPO_PP = 0x01,
    _PIN_AD6_GPO_OD = 0x02,
    _PIN_AD6_DPTX_AUX_N_0 = 0x03,
    _PIN_AD6_NC = _PIN_AD6_GPO_PP,
} EnumPinshareInfoPINAD6;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1021
// MCU Ctrl : 0xFE21 at _PIN_AD5_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AD5                                (_PIN_AD5_NC)

typedef enum
{
    _PIN_AD5_GPI = 0x00,
    _PIN_AD5_GPO_PP = 0x01,
    _PIN_AD5_GPO_OD = 0x02,
    _PIN_AD5_DPTX_AUX_P_0 = 0x03,
    _PIN_AD5_NC = _PIN_AD5_GPO_PP,
} EnumPinshareInfoPINAD5;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1022
// MCU Ctrl : 0xFE22 at _PIN_AF7_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AF7                                (_PIN_AF7_NC)

typedef enum
{
    _PIN_AF7_GPI = 0x00,
    _PIN_AF7_GPO_PP = 0x01,
    _PIN_AF7_GPO_OD = 0x02,
    _PIN_AF7_TPC_IICSCL_0_1 = 0x03,
    _PIN_AF7_TPC_IICSCL_1_1 = 0x04,
    _PIN_AF7_TEST4B_OUT0 = 0x05,
    _PIN_AF7_TEST4B_OUT1 = 0x06,
    _PIN_AF7_TEST4B_OUT2 = 0x07,
    _PIN_AF7_TEST4B_OUT3 = 0x08,
    _PIN_AF7_TEST4B_OUT4 = 0x09,
    _PIN_AF7_TEST4B_OUT5 = 0x0A,
    _PIN_AF7_TEST4B_OUT6 = 0x0B,
    _PIN_AF7_TEST4B_OUT7 = 0x0C,
    _PIN_AF7_NC = _PIN_AF7_GPO_PP,
} EnumPinshareInfoPINAF7;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1023
// MCU Ctrl : 0xFE23 at _PIN_AG7_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AG7                                (_PIN_AG7_NC)

typedef enum
{
    _PIN_AG7_GPI = 0x00,
    _PIN_AG7_GPO_PP = 0x01,
    _PIN_AG7_GPO_OD = 0x02,
    _PIN_AG7_TPC_IICSDA_0_1 = 0x03,
    _PIN_AG7_TPC_IICSDA_1_1 = 0x04,
    _PIN_AG7_TEST4B_OUT0 = 0x05,
    _PIN_AG7_TEST4B_OUT1 = 0x06,
    _PIN_AG7_TEST4B_OUT2 = 0x07,
    _PIN_AG7_TEST4B_OUT3 = 0x08,
    _PIN_AG7_TEST4B_OUT4 = 0x09,
    _PIN_AG7_TEST4B_OUT5 = 0x0A,
    _PIN_AG7_TEST4B_OUT6 = 0x0B,
    _PIN_AG7_TEST4B_OUT7 = 0x0C,
    _PIN_AG7_NC = _PIN_AG7_GPO_PP,
} EnumPinshareInfoPINAG7;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1024
// MCU Ctrl : 0xFE24 at _PIN_Y8_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_Y8                                 (_PIN_Y8_NC)

typedef enum
{
    _PIN_Y8_GPI = 0x00,
    _PIN_Y8_GPO_PP = 0x01,
    _PIN_Y8_GPO_OD = 0x02,
    _PIN_Y8_TYPEC_GPIO0_0_PP = 0x03,
    _PIN_Y8_TYPEC_GPIO0_0_OD = 0x04,
    _PIN_Y8_TYPEC_GPIO1_0_PP = 0x05,
    _PIN_Y8_TYPEC_GPIO1_0_OD = 0x06,
    _PIN_Y8_M1_IDOMAIN_HS_OUT = 0x07,
    _PIN_Y8_TEST4B_OUT0 = 0x08,
    _PIN_Y8_TEST4B_OUT1 = 0x09,
    _PIN_Y8_TEST4B_OUT2 = 0x0A,
    _PIN_Y8_TEST4B_OUT3 = 0x0B,
    _PIN_Y8_TEST4B_OUT4 = 0x0C,
    _PIN_Y8_TEST4B_OUT5 = 0x0D,
    _PIN_Y8_TEST4B_OUT6 = 0x0E,
    _PIN_Y8_TEST4B_OUT7 = 0x0F,
    _PIN_Y8_NC = _PIN_Y8_GPO_PP,
} EnumPinshareInfoPINY8;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1025
// MCU Ctrl : 0xFE25 at _PIN_AG6_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AG6                                (_PIN_AG6_NC)

typedef enum
{
    _PIN_AG6_GPI = 0x00,
    _PIN_AG6_GPO_PP = 0x01,
    _PIN_AG6_GPO_OD = 0x02,
    _PIN_AG6_INT0_5 = 0x03,
    _PIN_AG6_INT1_5 = 0x04,
    _PIN_AG6_TYPEC_GPIO2_0_PP = 0x05,
    _PIN_AG6_TYPEC_GPIO2_0_OD = 0x06,
    _PIN_AG6_TYPEC_GPIO3_0_PP = 0x07,
    _PIN_AG6_TYPEC_GPIO3_0_OD = 0x08,
    _PIN_AG6_TEST4B_OUT0 = 0x09,
    _PIN_AG6_TEST4B_OUT1 = 0x0A,
    _PIN_AG6_TEST4B_OUT2 = 0x0B,
    _PIN_AG6_TEST4B_OUT3 = 0x0C,
    _PIN_AG6_TEST4B_OUT4 = 0x0D,
    _PIN_AG6_TEST4B_OUT5 = 0x0E,
    _PIN_AG6_TEST4B_OUT6 = 0x0F,
    _PIN_AG6_NC = _PIN_AG6_GPO_PP,
} EnumPinshareInfoPINAG6;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1026
// MCU Ctrl : 0xFE26 at _PIN_Y6_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_Y6                                 (_PIN_Y6_NC)

typedef enum
{
    _PIN_Y6_GPI = 0x00,
    _PIN_Y6_GPO_PP = 0x01,
    _PIN_Y6_GPO_OD = 0x02,
    _PIN_Y6_MCK = 0x03,
    _PIN_Y6_USB_SPI_CLK_0_2 = 0x04,
    _PIN_Y6_USB_SPI_CLK_1_2 = 0x05,
    _PIN_Y6_USB_SPI_CLK_2_2 = 0x06,
    _PIN_Y6_TCON8 = 0x07,
    _PIN_Y6_TEST4B_OUT0 = 0x08,
    _PIN_Y6_TEST4B_OUT1 = 0x09,
    _PIN_Y6_TEST4B_OUT2 = 0x0A,
    _PIN_Y6_TEST4B_OUT3 = 0x0B,
    _PIN_Y6_TEST4B_OUT4 = 0x0C,
    _PIN_Y6_TEST4B_OUT5 = 0x0D,
    _PIN_Y6_TEST4B_OUT6 = 0x0E,
    _PIN_Y6_TEST4B_OUT7 = 0x0F,
    _PIN_Y6_NC = _PIN_Y6_GPO_PP,
} EnumPinshareInfoPINY6;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1027
// MCU Ctrl : 0xFE27 at _PIN_AC5_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AC5                                (_PIN_AC5_NC)

typedef enum
{
    _PIN_AC5_GPI = 0x00,
    _PIN_AC5_GPO_PP = 0x01,
    _PIN_AC5_GPO_OD = 0x02,
    _PIN_AC5_SCK = 0x03,
    _PIN_AC5_USB_SPI_SI_0_2 = 0x04,
    _PIN_AC5_USB_SPI_SI_1_2 = 0x05,
    _PIN_AC5_USB_SPI_SI_2_2 = 0x06,
    _PIN_AC5_TCON7 = 0x07,
    _PIN_AC5_TEST4B_OUT0 = 0x08,
    _PIN_AC5_TEST4B_OUT1 = 0x09,
    _PIN_AC5_TEST4B_OUT2 = 0x0A,
    _PIN_AC5_TEST4B_OUT3 = 0x0B,
    _PIN_AC5_TEST4B_OUT4 = 0x0C,
    _PIN_AC5_TEST4B_OUT5 = 0x0D,
    _PIN_AC5_TEST4B_OUT6 = 0x0E,
    _PIN_AC5_TEST4B_OUT7 = 0x0F,
    _PIN_AC5_NC = _PIN_AC5_GPO_PP,
} EnumPinshareInfoPINAC5;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1028
// MCU Ctrl : 0xFE28 at _PIN_AE5_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AE5                                (_PIN_AE5_NC)

typedef enum
{
    _PIN_AE5_GPI = 0x00,
    _PIN_AE5_GPO_PP = 0x01,
    _PIN_AE5_GPO_OD = 0x02,
    _PIN_AE5_WS = 0x03,
    _PIN_AE5_USB_SPI_SO_0_2 = 0x04,
    _PIN_AE5_USB_SPI_SO_1_2 = 0x05,
    _PIN_AE5_USB_SPI_SO_2_2 = 0x06,
    _PIN_AE5_TCON6 = 0x07,
    _PIN_AE5_TEST4B_OUT0 = 0x08,
    _PIN_AE5_TEST4B_OUT1 = 0x09,
    _PIN_AE5_TEST4B_OUT2 = 0x0A,
    _PIN_AE5_TEST4B_OUT3 = 0x0B,
    _PIN_AE5_TEST4B_OUT4 = 0x0C,
    _PIN_AE5_TEST4B_OUT5 = 0x0D,
    _PIN_AE5_TEST4B_OUT6 = 0x0E,
    _PIN_AE5_TEST4B_OUT7 = 0x0F,
    _PIN_AE5_NC = _PIN_AE5_GPO_PP,
} EnumPinshareInfoPINAE5;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1029
// MCU Ctrl : 0xFE29 at _PIN_AE6_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AE6                                (_PIN_AE6_NC)

typedef enum
{
    _PIN_AE6_GPI = 0x00,
    _PIN_AE6_GPO_PP = 0x01,
    _PIN_AE6_GPO_OD = 0x02,
    _PIN_AE6_SD0 = 0x03,
    _PIN_AE6_SPDIF0 = 0x04,
    _PIN_AE6_USB_SPI_CEB0_0_2 = 0x05,
    _PIN_AE6_USB_SPI_CEB0_1_2 = 0x06,
    _PIN_AE6_USB_SPI_CEB0_2_2 = 0x07,
    _PIN_AE6_TCON5 = 0x08,
    _PIN_AE6_TEST4B_OUT0 = 0x09,
    _PIN_AE6_TEST4B_OUT1 = 0x0A,
    _PIN_AE6_TEST4B_OUT2 = 0x0B,
    _PIN_AE6_TEST4B_OUT3 = 0x0C,
    _PIN_AE6_TEST4B_OUT4 = 0x0D,
    _PIN_AE6_TEST4B_OUT5 = 0x0E,
    _PIN_AE6_TEST4B_OUT6 = 0x0F,
    _PIN_AE6_NC = _PIN_AE6_GPO_PP,
} EnumPinshareInfoPINAE6;

//---------------------------------------------------------------------------
// Function : NC(AUDIO_SD)
// Pinshare : 0x102A
// MCU Ctrl : 0xFE2A at _PIN_AE7_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AE7                                (_PIN_AE7_NC)

typedef enum
{
    _PIN_AE7_GPI = 0x00,
    _PIN_AE7_GPO_PP = 0x01,
    _PIN_AE7_GPO_OD = 0x02,
    _PIN_AE7_SD1 = 0x03,
    _PIN_AE7_SPDIF1 = 0x04,
    _PIN_AE7_USB_SPI_CEB1_0_2 = 0x05,
    _PIN_AE7_USB_SPI_CEB1_1_2 = 0x06,
    _PIN_AE7_USB_SPI_CEB1_2_2 = 0x07,
    _PIN_AE7_PWM3_PP = 0x08,
    _PIN_AE7_PWM3_OD = 0x09,
    _PIN_AE7_PWM3_DIMMING_PP = 0x0A,
    _PIN_AE7_PWM3_DIMMING = 0x0B,
    _PIN_AE7_TCON4 = 0x0C,
    _PIN_AE7_TEST4B_OUT0 = 0x0D,
    _PIN_AE7_TEST4B_OUT1 = 0x0E,
    _PIN_AE7_TEST4B_OUT2 = 0x0F,
    _PIN_AE7_NC = _PIN_AE7_GPO_PP,
} EnumPinshareInfoPINAE7;

//---------------------------------------------------------------------------
// Function : NC(AUD_MUTE)
// Pinshare : 0x102B
// MCU Ctrl : 0xFE2B at _PIN_AH3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AH3                                (_PIN_AH3_NC)

typedef enum
{
    _PIN_AH3_GPI = 0x00,
    _PIN_AH3_GPO_PP = 0x01,
    _PIN_AH3_GPO_OD = 0x02,
    _PIN_AH3_SD2 = 0x03,
    _PIN_AH3_SPDIF2 = 0x04,
    _PIN_AH3_TPC_IICSCL_0_2 = 0x05,
    _PIN_AH3_TPC_IICSCL_1_2 = 0x06,
    _PIN_AH3_M1_IDOMAIN_HS_OUT = 0x07,
    _PIN_AH3_TYPEC_GPIO6_1_OD = 0x08,
    _PIN_AH3_TYPEC_GPIO6_1_PP = 0x09,
    _PIN_AH3_TYPEC_GPIO7_1_OD = 0x0A,
    _PIN_AH3_TYPEC_GPIO7_1_PP = 0x0B,
    _PIN_AH3_TEST4B_OUT0 = 0x0C,
    _PIN_AH3_TEST4B_OUT1 = 0x0D,
    _PIN_AH3_TEST4B_OUT2 = 0x0E,
    _PIN_AH3_TEST4B_OUT3 = 0x0F,
    _PIN_AH3_NC = _PIN_AH3_GPO_PP,
} EnumPinshareInfoPINAH3;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x102C
// MCU Ctrl : 0xFE2C at _PIN_AJ3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AJ3                                (_PIN_AJ3_NC)

typedef enum
{
    _PIN_AJ3_GPI = 0x00,
    _PIN_AJ3_GPO_PP = 0x01,
    _PIN_AJ3_GPO_OD = 0x02,
    _PIN_AJ3_SD3 = 0x03,
    _PIN_AJ3_SPDIF3 = 0x04,
    _PIN_AJ3_TPC_IICSDA_0_2 = 0x05,
    _PIN_AJ3_TPC_IICSDA_1_2 = 0x06,
    _PIN_AJ3_TEST4B_OUT0 = 0x07,
    _PIN_AJ3_TEST4B_OUT1 = 0x08,
    _PIN_AJ3_TEST4B_OUT2 = 0x09,
    _PIN_AJ3_TEST4B_OUT3 = 0x0A,
    _PIN_AJ3_TEST4B_OUT4 = 0x0B,
    _PIN_AJ3_TEST4B_OUT5 = 0x0C,
    _PIN_AJ3_TEST4B_OUT6 = 0x0D,
    _PIN_AJ3_TEST4B_OUT7 = 0x0E,
    _PIN_AJ3_NC = _PIN_AJ3_GPO_PP,
} EnumPinshareInfoPINAJ3;

//---------------------------------------------------------------------------
// Function : BKLT-VBR
// Pinshare : 0x102D
// MCU Ctrl : 0xFE2D at _PIN_AG5_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AG5                                (_PIN_AG5_TCON13)

typedef enum
{
    _PIN_AG5_GPI = 0x00,
    _PIN_AG5_GPO_PP = 0x01,
    _PIN_AG5_GPO_OD = 0x02,
    _PIN_AG5_PWM_OUT = 0x03,
    _PIN_AG5_PWM1_PP = 0x04,
    _PIN_AG5_PWM1_OD = 0x05,
    _PIN_AG5_PWM1_DIMMING_PP = 0x06,
    _PIN_AG5_PWM1_DIMMING = 0x07,
    _PIN_AG5_TCON13 = 0x08,
    _PIN_AG5_TEST4B_OUT0 = 0x09,
    _PIN_AG5_TEST4B_OUT1 = 0x0A,
    _PIN_AG5_TEST4B_OUT2 = 0x0B,
    _PIN_AG5_TEST4B_OUT3 = 0x0C,
    _PIN_AG5_TEST4B_OUT4 = 0x0D,
    _PIN_AG5_TEST4B_OUT5 = 0x0E,
    _PIN_AG5_TEST4B_OUT6 = 0x0F,
    _PIN_AG5_NC = _PIN_AG5_GPO_PP,
} EnumPinshareInfoPINAG5;

//---------------------------------------------------------------------------
// Function : NC(BIST_EN)
// Pinshare : 0x102E at _OFF_Region
// MCU Ctrl : 0xFE2E at _PIN_AM21_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AM21_OFF_REGION                    (_PIN_AM21_NC)

typedef enum
{
    _PIN_AM21_GPI = 0x00,
    _PIN_AM21_GPO_PP = 0x01,
    _PIN_AM21_GPO_OD = 0x02,
    _PIN_AM21_TTS_CE = 0x03,
    _PIN_AM21_NC = _PIN_AM21_GPO_PP,
} EnumPinshareInfoPINAM21;

//---------------------------------------------------------------------------
// Function : NC(PANEL_WP)
// Pinshare : 0x102F at _OFF_Region
// MCU Ctrl : 0xFE2F at _PIN_AL21_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AL21_OFF_REGION                    (_PIN_AL21_NC)

typedef enum
{
    _PIN_AL21_GPI = 0x00,
    _PIN_AL21_GPO_PP = 0x01,
    _PIN_AL21_GPO_OD = 0x02,
    _PIN_AL21_DPTX_HPD_0_ORG = 0x03,
    _PIN_AL21_TEST4B_OUT0 = 0x04,
    _PIN_AL21_TEST4B_OUT1 = 0x05,
    _PIN_AL21_TEST4B_OUT2 = 0x06,
    _PIN_AL21_TEST4B_OUT3 = 0x07,
    _PIN_AL21_TEST4B_OUT4 = 0x08,
    _PIN_AL21_TEST4B_OUT5 = 0x09,
    _PIN_AL21_TEST4B_OUT6 = 0x0A,
    _PIN_AL21_TEST4B_OUT7 = 0x0B,
    _PIN_AL21_NC = _PIN_AL21_GPO_PP,
} EnumPinshareInfoPINAL21;

//---------------------------------------------------------------------------
// Function : A_ADC_0
// Pinshare : 0x1030
// MCU Ctrl : 0xFE30 at _PIN_AG12_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AG12                               (_PIN_AG12_A_ADC_0)

typedef enum
{
    _PIN_AG12_GPI = 0x00,
    _PIN_AG12_GPO_PP = 0x01,
    _PIN_AG12_GPO_OD = 0x02,
    _PIN_AG12_A_ADC_0 = 0x03,
    _PIN_AG12_TEST4B_OUT0 = 0x04,
    _PIN_AG12_TEST4B_OUT1 = 0x05,
    _PIN_AG12_TEST4B_OUT2 = 0x06,
    _PIN_AG12_TEST4B_OUT3 = 0x07,
    _PIN_AG12_TEST4B_OUT4 = 0x08,
    _PIN_AG12_TEST4B_OUT5 = 0x09,
    _PIN_AG12_TEST4B_OUT6 = 0x0A,
    _PIN_AG12_TEST4B_OUT7 = 0x0B,
    _PIN_AG12_NC = _PIN_AG12_GPO_PP,
} EnumPinshareInfoPINAG12;

//---------------------------------------------------------------------------
// Function : A_ADC_1
// Pinshare : 0x1031
// MCU Ctrl : 0xFE31 at _PIN_AE14_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AE14                               (_PIN_AE14_A_ADC_1)

typedef enum
{
    _PIN_AE14_GPI = 0x00,
    _PIN_AE14_GPO_PP = 0x01,
    _PIN_AE14_GPO_OD = 0x02,
    _PIN_AE14_A_ADC_1 = 0x03,
    _PIN_AE14_TEST4B_OUT0 = 0x04,
    _PIN_AE14_TEST4B_OUT1 = 0x05,
    _PIN_AE14_TEST4B_OUT2 = 0x06,
    _PIN_AE14_TEST4B_OUT3 = 0x07,
    _PIN_AE14_TEST4B_OUT4 = 0x08,
    _PIN_AE14_TEST4B_OUT5 = 0x09,
    _PIN_AE14_TEST4B_OUT6 = 0x0A,
    _PIN_AE14_TEST4B_OUT7 = 0x0B,
    _PIN_AE14_NC = _PIN_AE14_GPO_PP,
} EnumPinshareInfoPINAE14;

//---------------------------------------------------------------------------
// Function : NC(DP1_CONFIG2)
// Pinshare : 0x1032
// MCU Ctrl : 0xFE32 at _PIN_AG14_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AG14                               (_PIN_AG14_NC)

typedef enum
{
    _PIN_AG14_GPI = 0x00,
    _PIN_AG14_GPO_PP = 0x01,
    _PIN_AG14_GPO_OD = 0x02,
    _PIN_AG14_A_ADC_2 = 0x03,
    _PIN_AG14_INT0_6 = 0x04,
    _PIN_AG14_INT1_6 = 0x05,
    _PIN_AG14_TEST4B_OUT0 = 0x06,
    _PIN_AG14_TEST4B_OUT1 = 0x07,
    _PIN_AG14_TEST4B_OUT2 = 0x08,
    _PIN_AG14_TEST4B_OUT3 = 0x09,
    _PIN_AG14_TEST4B_OUT4 = 0x0A,
    _PIN_AG14_TEST4B_OUT5 = 0x0B,
    _PIN_AG14_TEST4B_OUT6 = 0x0C,
    _PIN_AG14_TEST4B_OUT7 = 0x0D,
    _PIN_AG14_NC = _PIN_AG14_GPO_PP,
} EnumPinshareInfoPINAG14;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1033
// MCU Ctrl : 0xFE33 at _PIN_AF15_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AF15                               (_PIN_AF15_NC)

typedef enum
{
    _PIN_AF15_GPI = 0x00,
    _PIN_AF15_GPO_PP = 0x01,
    _PIN_AF15_GPO_OD = 0x02,
    _PIN_AF15_A_ADC_3 = 0x03,
    _PIN_AF15_TEST4B_OUT0 = 0x04,
    _PIN_AF15_TEST4B_OUT1 = 0x05,
    _PIN_AF15_TEST4B_OUT2 = 0x06,
    _PIN_AF15_TEST4B_OUT3 = 0x07,
    _PIN_AF15_TEST4B_OUT4 = 0x08,
    _PIN_AF15_TEST4B_OUT5 = 0x09,
    _PIN_AF15_TEST4B_OUT6 = 0x0A,
    _PIN_AF15_TEST4B_OUT7 = 0x0B,
    _PIN_AF15_NC = _PIN_AF15_GPO_PP,
} EnumPinshareInfoPINAF15;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1034 at _OFF_Region
// MCU Ctrl : 0xFE34 at _PIN_AH22_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AH22_OFF_REGION                    (_PIN_AH22_NC)

typedef enum
{
    _PIN_AH22_GPI = 0x00,
    _PIN_AH22_GPO_PP = 0x01,
    _PIN_AH22_GPO_OD = 0x02,
    _PIN_AH22_LINE_INL = 0x03,
    _PIN_AH22_MCK = 0x04,
    _PIN_AH22_NC = _PIN_AH22_GPO_PP,
} EnumPinshareInfoPINAH22;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1035 at _OFF_Region
// MCU Ctrl : 0xFE35 at _PIN_AJ22_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AJ22_OFF_REGION                    (_PIN_AJ22_NC)

typedef enum
{
    _PIN_AJ22_GPI = 0x00,
    _PIN_AJ22_GPO_PP = 0x01,
    _PIN_AJ22_GPO_OD = 0x02,
    _PIN_AJ22_LINE_INR = 0x03,
    _PIN_AJ22_SCK = 0x04,
    _PIN_AJ22_NC = _PIN_AJ22_GPO_PP,
} EnumPinshareInfoPINAJ22;

//---------------------------------------------------------------------------
// Function : Audio_REF
// Pinshare : 0x1036 at _OFF_Region
// MCU Ctrl : 0xFE36 at _PIN_AF20_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AF20_OFF_REGION                    (_PIN_AF20_AUDIO_REF)

typedef enum
{
    _PIN_AF20_GPI = 0x00,
    _PIN_AF20_GPO_PP = 0x01,
    _PIN_AF20_GPO_OD = 0x02,
    _PIN_AF20_AUDIO_REF = 0x03,
    _PIN_AF20_WS = 0x04,
    _PIN_AF20_NC = _PIN_AF20_GPO_PP,
} EnumPinshareInfoPINAF20;

//---------------------------------------------------------------------------
// Function : AUDIO_SOUTL
// Pinshare : 0x1037 at _OFF_Region
// MCU Ctrl : 0xFE37 at _PIN_AH23_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AH23_OFF_REGION                    (_PIN_AH23_AUDIO_SOUTL)

typedef enum
{
    _PIN_AH23_GPI = 0x00,
    _PIN_AH23_GPO_PP = 0x01,
    _PIN_AH23_GPO_OD = 0x02,
    _PIN_AH23_AUDIO_SOUTL = 0x03,
    _PIN_AH23_SD0 = 0x04,
    _PIN_AH23_SPDIF0 = 0x05,
    _PIN_AH23_NC = _PIN_AH23_GPO_PP,
} EnumPinshareInfoPINAH23;

//---------------------------------------------------------------------------
// Function : AUDIO_SOUTR
// Pinshare : 0x1038 at _OFF_Region
// MCU Ctrl : 0xFE38 at _PIN_AJ23_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AJ23_OFF_REGION                    (_PIN_AJ23_AUDIO_SOUTR)

typedef enum
{
    _PIN_AJ23_GPI = 0x00,
    _PIN_AJ23_GPO_PP = 0x01,
    _PIN_AJ23_GPO_OD = 0x02,
    _PIN_AJ23_AUDIO_SOUTR = 0x03,
    _PIN_AJ23_SD1 = 0x04,
    _PIN_AJ23_SPDIF1 = 0x05,
    _PIN_AJ23_NC = _PIN_AJ23_GPO_PP,
} EnumPinshareInfoPINAJ23;

//---------------------------------------------------------------------------
// Function : AUDIO_HOUTL
// Pinshare : 0x1039 at _OFF_Region
// MCU Ctrl : 0xFE39 at _PIN_AH24_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AH24_OFF_REGION                    (_PIN_AH24_AUDIO_HOUTL)

typedef enum
{
    _PIN_AH24_GPI = 0x00,
    _PIN_AH24_GPO_PP = 0x01,
    _PIN_AH24_GPO_OD = 0x02,
    _PIN_AH24_AUDIO_HOUTL = 0x03,
    _PIN_AH24_SD2 = 0x04,
    _PIN_AH24_SPDIF2 = 0x05,
    _PIN_AH24_NC = _PIN_AH24_GPO_PP,
} EnumPinshareInfoPINAH24;

//---------------------------------------------------------------------------
// Function : AUDIO_HOUTR
// Pinshare : 0x103A at _OFF_Region
// MCU Ctrl : 0xFE3A at _PIN_AJ24_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AJ24_OFF_REGION                    (_PIN_AJ24_AUDIO_HOUTR)

typedef enum
{
    _PIN_AJ24_GPI = 0x00,
    _PIN_AJ24_GPO_PP = 0x01,
    _PIN_AJ24_GPO_OD = 0x02,
    _PIN_AJ24_AUDIO_HOUTR = 0x03,
    _PIN_AJ24_SD3 = 0x04,
    _PIN_AJ24_SPDIF3 = 0x05,
    _PIN_AJ24_NC = _PIN_AJ24_GPO_PP,
} EnumPinshareInfoPINAJ24;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x103B at _OFF_Region
// MCU Ctrl : 0xFE3B at _PIN_AD27_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AD27_OFF_REGION                    (_PIN_AD27_NC)

typedef enum
{
    _PIN_AD27_HI_Z = 0x00,
    _PIN_AD27_GPI = 0x01,
    _PIN_AD27_TXD4P_10B = 0x04,
    _PIN_AD27_NC = _PIN_AD27_GPI,
} EnumPinshareInfoPINAD27;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x103C at _OFF_Region
// MCU Ctrl : 0xFE3C at _PIN_AC27_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AC27_OFF_REGION                    (_PIN_AC27_NC)

typedef enum
{
    _PIN_AC27_HI_Z = 0x00,
    _PIN_AC27_GPI = 0x01,
    _PIN_AC27_TXD4N_10B = 0x04,
    _PIN_AC27_NC = _PIN_AC27_GPI,
} EnumPinshareInfoPINAC27;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x103D at _OFF_Region
// MCU Ctrl : 0xFE3D at _PIN_AD28_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AD28_OFF_REGION                    (_PIN_AD28_NC)

typedef enum
{
    _PIN_AD28_HI_Z = 0x00,
    _PIN_AD28_GPI = 0x01,
    _PIN_AD28_TXD3P_10B = 0x04,
    _PIN_AD28_NC = _PIN_AD28_GPI,
} EnumPinshareInfoPINAD28;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x103E at _OFF_Region
// MCU Ctrl : 0xFE3E at _PIN_AC28_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AC28_OFF_REGION                    (_PIN_AC28_NC)

typedef enum
{
    _PIN_AC28_HI_Z = 0x00,
    _PIN_AC28_GPI = 0x01,
    _PIN_AC28_TXD3N_10B = 0x04,
    _PIN_AC28_NC = _PIN_AC28_GPI,
} EnumPinshareInfoPINAC28;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x103F at _OFF_Region
// MCU Ctrl : 0xFE3F at _PIN_AD29_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AD29_OFF_REGION                    (_PIN_AD29_NC)

typedef enum
{
    _PIN_AD29_HI_Z = 0x00,
    _PIN_AD29_GPI = 0x01,
    _PIN_AD29_TXD2P_10B = 0x04,
    _PIN_AD29_NC = _PIN_AD29_GPI,
} EnumPinshareInfoPINAD29;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1040 at _OFF_Region
// MCU Ctrl : 0xFE40 at _PIN_AC29_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AC29_OFF_REGION                    (_PIN_AC29_NC)

typedef enum
{
    _PIN_AC29_HI_Z = 0x00,
    _PIN_AC29_GPI = 0x01,
    _PIN_AC29_TXD2N_10B = 0x04,
    _PIN_AC29_NC = _PIN_AC29_GPI,
} EnumPinshareInfoPINAC29;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1041 at _OFF_Region
// MCU Ctrl : 0xFE41 at _PIN_AD30_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AD30_OFF_REGION                    (_PIN_AD30_NC)

typedef enum
{
    _PIN_AD30_HI_Z = 0x00,
    _PIN_AD30_GPI = 0x01,
    _PIN_AD30_TXD1P_10B = 0x04,
    _PIN_AD30_NC = _PIN_AD30_GPI,
} EnumPinshareInfoPINAD30;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1042 at _OFF_Region
// MCU Ctrl : 0xFE42 at _PIN_AC30_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AC30_OFF_REGION                    (_PIN_AC30_NC)

typedef enum
{
    _PIN_AC30_HI_Z = 0x00,
    _PIN_AC30_GPI = 0x01,
    _PIN_AC30_TXD1N_10B = 0x04,
    _PIN_AC30_NC = _PIN_AC30_GPI,
} EnumPinshareInfoPINAC30;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1043 at _OFF_Region
// MCU Ctrl : 0xFE43 at _PIN_AE32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AE32_OFF_REGION                    (_PIN_AE32_NC)

typedef enum
{
    _PIN_AE32_HI_Z = 0x00,
    _PIN_AE32_GPI = 0x01,
    _PIN_AE32_TXD0P_10B = 0x04,
    _PIN_AE32_NC = _PIN_AE32_GPI,
} EnumPinshareInfoPINAE32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1044 at _OFF_Region
// MCU Ctrl : 0xFE44 at _PIN_AE31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AE31_OFF_REGION                    (_PIN_AE31_NC)

typedef enum
{
    _PIN_AE31_HI_Z = 0x00,
    _PIN_AE31_GPI = 0x01,
    _PIN_AE31_TXD0N_10B = 0x04,
    _PIN_AE31_NC = _PIN_AE31_GPI,
} EnumPinshareInfoPINAE31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1045 at _OFF_Region
// MCU Ctrl : 0xFE45 at _PIN_AD32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AD32_OFF_REGION                    (_PIN_AD32_NC)

typedef enum
{
    _PIN_AD32_HI_Z = 0x00,
    _PIN_AD32_GPI = 0x01,
    _PIN_AD32_TXC4P_10B = 0x04,
    _PIN_AD32_NC = _PIN_AD32_GPI,
} EnumPinshareInfoPINAD32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1046 at _OFF_Region
// MCU Ctrl : 0xFE46 at _PIN_AD31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AD31_OFF_REGION                    (_PIN_AD31_NC)

typedef enum
{
    _PIN_AD31_HI_Z = 0x00,
    _PIN_AD31_GPI = 0x01,
    _PIN_AD31_TXC4N_10B = 0x04,
    _PIN_AD31_NC = _PIN_AD31_GPI,
} EnumPinshareInfoPINAD31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1047 at _OFF_Region
// MCU Ctrl : 0xFE47 at _PIN_AC32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AC32_OFF_REGION                    (_PIN_AC32_NC)

typedef enum
{
    _PIN_AC32_HI_Z = 0x00,
    _PIN_AC32_GPI = 0x01,
    _PIN_AC32_TXC3P_10B = 0x04,
    _PIN_AC32_NC = _PIN_AC32_GPI,
} EnumPinshareInfoPINAC32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1048 at _OFF_Region
// MCU Ctrl : 0xFE48 at _PIN_AC31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AC31_OFF_REGION                    (_PIN_AC31_NC)

typedef enum
{
    _PIN_AC31_HI_Z = 0x00,
    _PIN_AC31_GPI = 0x01,
    _PIN_AC31_TXC3N_10B = 0x04,
    _PIN_AC31_NC = _PIN_AC31_GPI,
} EnumPinshareInfoPINAC31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1049 at _OFF_Region
// MCU Ctrl : 0xFE49 at _PIN_AB32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AB32_OFF_REGION                    (_PIN_AB32_NC)

typedef enum
{
    _PIN_AB32_HI_Z = 0x00,
    _PIN_AB32_GPI = 0x01,
    _PIN_AB32_TXCCP_10B = 0x04,
    _PIN_AB32_NC = _PIN_AB32_GPI,
} EnumPinshareInfoPINAB32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x104A at _OFF_Region
// MCU Ctrl : 0xFE4A at _PIN_AB31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AB31_OFF_REGION                    (_PIN_AB31_NC)

typedef enum
{
    _PIN_AB31_HI_Z = 0x00,
    _PIN_AB31_GPI = 0x01,
    _PIN_AB31_TXCCN_10B = 0x04,
    _PIN_AB31_NC = _PIN_AB31_GPI,
} EnumPinshareInfoPINAB31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x104B at _OFF_Region
// MCU Ctrl : 0xFE4B at _PIN_AA32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AA32_OFF_REGION                    (_PIN_AA32_NC)

typedef enum
{
    _PIN_AA32_HI_Z = 0x00,
    _PIN_AA32_GPI = 0x01,
    _PIN_AA32_TXC2P_10B = 0x04,
    _PIN_AA32_NC = _PIN_AA32_GPI,
} EnumPinshareInfoPINAA32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x104C at _OFF_Region
// MCU Ctrl : 0xFE4C at _PIN_AA31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AA31_OFF_REGION                    (_PIN_AA31_NC)

typedef enum
{
    _PIN_AA31_HI_Z = 0x00,
    _PIN_AA31_GPI = 0x01,
    _PIN_AA31_TXC2N_10B = 0x04,
    _PIN_AA31_NC = _PIN_AA31_GPI,
} EnumPinshareInfoPINAA31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x104D at _OFF_Region
// MCU Ctrl : 0xFE4D at _PIN_Y32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_Y32_OFF_REGION                     (_PIN_Y32_NC)

typedef enum
{
    _PIN_Y32_HI_Z = 0x00,
    _PIN_Y32_GPI = 0x01,
    _PIN_Y32_TXC1P_10B = 0x04,
    _PIN_Y32_NC = _PIN_Y32_GPI,
} EnumPinshareInfoPINY32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x104E at _OFF_Region
// MCU Ctrl : 0xFE4E at _PIN_Y31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_Y31_OFF_REGION                     (_PIN_Y31_NC)

typedef enum
{
    _PIN_Y31_HI_Z = 0x00,
    _PIN_Y31_GPI = 0x01,
    _PIN_Y31_TXC1N_10B = 0x04,
    _PIN_Y31_NC = _PIN_Y31_GPI,
} EnumPinshareInfoPINY31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x104F at _OFF_Region
// MCU Ctrl : 0xFE4F at _PIN_W32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_W32_OFF_REGION                     (_PIN_W32_NC)

typedef enum
{
    _PIN_W32_HI_Z = 0x00,
    _PIN_W32_GPI = 0x01,
    _PIN_W32_TXC0P_10B = 0x04,
    _PIN_W32_NC = _PIN_W32_GPI,
} EnumPinshareInfoPINW32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1050 at _OFF_Region
// MCU Ctrl : 0xFE50 at _PIN_W31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_W31_OFF_REGION                     (_PIN_W31_NC)

typedef enum
{
    _PIN_W31_HI_Z = 0x00,
    _PIN_W31_GPI = 0x01,
    _PIN_W31_TXC0N_10B = 0x04,
    _PIN_W31_NC = _PIN_W31_GPI,
} EnumPinshareInfoPINW31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1051 at _OFF_Region
// MCU Ctrl : 0xFE51 at _PIN_H31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H31_OFF_REGION                     (_PIN_H31_NC)

typedef enum
{
    _PIN_H31_HI_Z = 0x00,
    _PIN_H31_GPI = 0x01,
    _PIN_H31_TXB4P_10B = 0x04,
    _PIN_H31_NC = _PIN_H31_GPI,
} EnumPinshareInfoPINH31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1052 at _OFF_Region
// MCU Ctrl : 0xFE52 at _PIN_H32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H32_OFF_REGION                     (_PIN_H32_NC)

typedef enum
{
    _PIN_H32_HI_Z = 0x00,
    _PIN_H32_GPI = 0x01,
    _PIN_H32_TXB4N_10B = 0x04,
    _PIN_H32_NC = _PIN_H32_GPI,
} EnumPinshareInfoPINH32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1053 at _OFF_Region
// MCU Ctrl : 0xFE53 at _PIN_G31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G31_OFF_REGION                     (_PIN_G31_NC)

typedef enum
{
    _PIN_G31_HI_Z = 0x00,
    _PIN_G31_GPI = 0x01,
    _PIN_G31_TXB3P_10B = 0x04,
    _PIN_G31_NC = _PIN_G31_GPI,
} EnumPinshareInfoPING31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1054 at _OFF_Region
// MCU Ctrl : 0xFE54 at _PIN_G32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G32_OFF_REGION                     (_PIN_G32_NC)

typedef enum
{
    _PIN_G32_HI_Z = 0x00,
    _PIN_G32_GPI = 0x01,
    _PIN_G32_TXB3N_10B = 0x04,
    _PIN_G32_NC = _PIN_G32_GPI,
} EnumPinshareInfoPING32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1055 at _OFF_Region
// MCU Ctrl : 0xFE55 at _PIN_F31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F31_OFF_REGION                     (_PIN_F31_NC)

typedef enum
{
    _PIN_F31_HI_Z = 0x00,
    _PIN_F31_GPI = 0x01,
    _PIN_F31_TXB2P_10B = 0x04,
    _PIN_F31_NC = _PIN_F31_GPI,
} EnumPinshareInfoPINF31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1056 at _OFF_Region
// MCU Ctrl : 0xFE56 at _PIN_F32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F32_OFF_REGION                     (_PIN_F32_NC)

typedef enum
{
    _PIN_F32_HI_Z = 0x00,
    _PIN_F32_GPI = 0x01,
    _PIN_F32_TXB2N_10B = 0x04,
    _PIN_F32_NC = _PIN_F32_GPI,
} EnumPinshareInfoPINF32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1057 at _OFF_Region
// MCU Ctrl : 0xFE57 at _PIN_E31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E31_OFF_REGION                     (_PIN_E31_NC)

typedef enum
{
    _PIN_E31_HI_Z = 0x00,
    _PIN_E31_GPI = 0x01,
    _PIN_E31_TXB1P_10B = 0x04,
    _PIN_E31_NC = _PIN_E31_GPI,
} EnumPinshareInfoPINE31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1058 at _OFF_Region
// MCU Ctrl : 0xFE58 at _PIN_E32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E32_OFF_REGION                     (_PIN_E32_NC)

typedef enum
{
    _PIN_E32_HI_Z = 0x00,
    _PIN_E32_GPI = 0x01,
    _PIN_E32_TXB1N_10B = 0x04,
    _PIN_E32_NC = _PIN_E32_GPI,
} EnumPinshareInfoPINE32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1059 at _OFF_Region
// MCU Ctrl : 0xFE59 at _PIN_D31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_D31_OFF_REGION                     (_PIN_D31_NC)

typedef enum
{
    _PIN_D31_HI_Z = 0x00,
    _PIN_D31_GPI = 0x01,
    _PIN_D31_TXB0P_10B = 0x04,
    _PIN_D31_NC = _PIN_D31_GPI,
} EnumPinshareInfoPIND31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x105A at _OFF_Region
// MCU Ctrl : 0xFE5A at _PIN_D32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_D32_OFF_REGION                     (_PIN_D32_NC)

typedef enum
{
    _PIN_D32_HI_Z = 0x00,
    _PIN_D32_GPI = 0x01,
    _PIN_D32_TXB0N_10B = 0x04,
    _PIN_D32_NC = _PIN_D32_GPI,
} EnumPinshareInfoPIND32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x105B at _OFF_Region
// MCU Ctrl : 0xFE5B at _PIN_C31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C31_OFF_REGION                     (_PIN_C31_NC)

typedef enum
{
    _PIN_C31_HI_Z = 0x00,
    _PIN_C31_GPI = 0x01,
    _PIN_C31_TXA4P_10B = 0x04,
    _PIN_C31_NC = _PIN_C31_GPI,
} EnumPinshareInfoPINC31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x105C at _OFF_Region
// MCU Ctrl : 0xFE5C at _PIN_C32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C32_OFF_REGION                     (_PIN_C32_NC)

typedef enum
{
    _PIN_C32_HI_Z = 0x00,
    _PIN_C32_GPI = 0x01,
    _PIN_C32_TXA4N_10B = 0x04,
    _PIN_C32_NC = _PIN_C32_GPI,
} EnumPinshareInfoPINC32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x105D at _OFF_Region
// MCU Ctrl : 0xFE5D at _PIN_B31_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B31_OFF_REGION                     (_PIN_B31_NC)

typedef enum
{
    _PIN_B31_HI_Z = 0x00,
    _PIN_B31_GPI = 0x01,
    _PIN_B31_TXA3P_10B = 0x04,
    _PIN_B31_NC = _PIN_B31_GPI,
} EnumPinshareInfoPINB31;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x105E at _OFF_Region
// MCU Ctrl : 0xFE5E at _PIN_B32_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B32_OFF_REGION                     (_PIN_B32_NC)

typedef enum
{
    _PIN_B32_HI_Z = 0x00,
    _PIN_B32_GPI = 0x01,
    _PIN_B32_TXA3N_10B = 0x04,
    _PIN_B32_NC = _PIN_B32_GPI,
} EnumPinshareInfoPINB32;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x105F at _OFF_Region
// MCU Ctrl : 0xFE5F at _PIN_C29_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C29_OFF_REGION                     (_PIN_C29_NC)

typedef enum
{
    _PIN_C29_HI_Z = 0x00,
    _PIN_C29_GPI = 0x01,
    _PIN_C29_TXACP_10B = 0x04,
    _PIN_C29_NC = _PIN_C29_GPI,
} EnumPinshareInfoPINC29;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1060 at _OFF_Region
// MCU Ctrl : 0x2200 at _PIN_B29_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B29_OFF_REGION                     (_PIN_B29_NC)

typedef enum
{
    _PIN_B29_HI_Z = 0x00,
    _PIN_B29_GPI = 0x01,
    _PIN_B29_TXACN_10B = 0x04,
    _PIN_B29_NC = _PIN_B29_GPI,
} EnumPinshareInfoPINB29;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1061 at _OFF_Region
// MCU Ctrl : 0x2201 at _PIN_C28_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C28_OFF_REGION                     (_PIN_C28_NC)

typedef enum
{
    _PIN_C28_HI_Z = 0x00,
    _PIN_C28_GPI = 0x01,
    _PIN_C28_TXA2P_10B = 0x04,
    _PIN_C28_NC = _PIN_C28_GPI,
} EnumPinshareInfoPINC28;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1062 at _OFF_Region
// MCU Ctrl : 0x2202 at _PIN_B28_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B28_OFF_REGION                     (_PIN_B28_NC)

typedef enum
{
    _PIN_B28_HI_Z = 0x00,
    _PIN_B28_GPI = 0x01,
    _PIN_B28_TXA2N_10B = 0x04,
    _PIN_B28_NC = _PIN_B28_GPI,
} EnumPinshareInfoPINB28;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1063 at _OFF_Region
// MCU Ctrl : 0x2203 at _PIN_C27_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C27_OFF_REGION                     (_PIN_C27_NC)

typedef enum
{
    _PIN_C27_HI_Z = 0x00,
    _PIN_C27_GPI = 0x01,
    _PIN_C27_TXA1P_10B = 0x04,
    _PIN_C27_NC = _PIN_C27_GPI,
} EnumPinshareInfoPINC27;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1064 at _OFF_Region
// MCU Ctrl : 0x2204 at _PIN_B27_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B27_OFF_REGION                     (_PIN_B27_NC)

typedef enum
{
    _PIN_B27_HI_Z = 0x00,
    _PIN_B27_GPI = 0x01,
    _PIN_B27_TXA1N_10B = 0x04,
    _PIN_B27_NC = _PIN_B27_GPI,
} EnumPinshareInfoPINB27;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1065 at _OFF_Region
// MCU Ctrl : 0x2205 at _PIN_C26_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C26_OFF_REGION                     (_PIN_C26_NC)

typedef enum
{
    _PIN_C26_HI_Z = 0x00,
    _PIN_C26_GPI = 0x01,
    _PIN_C26_TXA0P_10B = 0x04,
    _PIN_C26_NC = _PIN_C26_GPI,
} EnumPinshareInfoPINC26;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1066 at _OFF_Region
// MCU Ctrl : 0x2206 at _PIN_B26_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_B26_OFF_REGION                     (_PIN_B26_NC)

typedef enum
{
    _PIN_B26_HI_Z = 0x00,
    _PIN_B26_GPI = 0x01,
    _PIN_B26_TXA0N_10B = 0x04,
    _PIN_B26_NC = _PIN_B26_GPI,
} EnumPinshareInfoPINB26;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1067 at _OFF_Region
// MCU Ctrl : 0x2207 at _PIN_G21_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G21_OFF_REGION                     (_PIN_G21_GPI)

typedef enum
{
    _PIN_G21_GPI = 0x00,
    _PIN_G21_GPO_PP = 0x01,
    _PIN_G21_GPO_OD = 0x02,
    _PIN_G21_USB_SPI_CLK_0_1 = 0x03,
    _PIN_G21_USB_SPI_CLK_1_1 = 0x04,
    _PIN_G21_USB_SPI_CLK_2_1 = 0x05,
    _PIN_G21_IICSCL_0_5 = 0x06,
    _PIN_G21_IICSCL_1_5 = 0x07,
    _PIN_G21_TCON9 = 0x08,
    _PIN_G21_TEST4B_OUT0 = 0x09,
    _PIN_G21_TEST4B_OUT1 = 0x0A,
    _PIN_G21_TEST4B_OUT2 = 0x0B,
    _PIN_G21_TEST4B_OUT3 = 0x0C,
    _PIN_G21_TEST4B_OUT4 = 0x0D,
    _PIN_G21_TEST4B_OUT5 = 0x0E,
    _PIN_G21_TEST4B_OUT6 = 0x0F,
    _PIN_G21_NC = _PIN_G21_GPO_PP,
} EnumPinshareInfoPING21;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1068 at _OFF_Region
// MCU Ctrl : 0x2208 at _PIN_E21_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E21_OFF_REGION                     (_PIN_E21_NC)

typedef enum
{
    _PIN_E21_GPI = 0x00,
    _PIN_E21_GPO_PP = 0x01,
    _PIN_E21_GPO_OD = 0x02,
    _PIN_E21_USB_SPI_SI_0_1 = 0x03,
    _PIN_E21_USB_SPI_SI_1_1 = 0x04,
    _PIN_E21_USB_SPI_SI_2_1 = 0x05,
    _PIN_E21_IICSDA_0_5 = 0x06,
    _PIN_E21_IICSDA_1_5 = 0x07,
    _PIN_E21_TCON10 = 0x08,
    _PIN_E21_TEST4B_OUT0 = 0x09,
    _PIN_E21_TEST4B_OUT1 = 0x0A,
    _PIN_E21_TEST4B_OUT2 = 0x0B,
    _PIN_E21_TEST4B_OUT3 = 0x0C,
    _PIN_E21_TEST4B_OUT4 = 0x0D,
    _PIN_E21_TEST4B_OUT5 = 0x0E,
    _PIN_E21_TEST4B_OUT6 = 0x0F,
    _PIN_E21_NC = _PIN_E21_GPO_PP,
} EnumPinshareInfoPINE21;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1069 at _OFF_Region
// MCU Ctrl : 0x2209 at _PIN_E19_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E19_OFF_REGION                     (_PIN_E19_NC)

typedef enum
{
    _PIN_E19_GPI = 0x00,
    _PIN_E19_GPO_PP = 0x01,
    _PIN_E19_GPO_OD = 0x02,
    _PIN_E19_USB_SPI_SO_0_1 = 0x03,
    _PIN_E19_USB_SPI_SO_1_1 = 0x04,
    _PIN_E19_USB_SPI_SO_2_1 = 0x05,
    _PIN_E19_TCON11 = 0x06,
    _PIN_E19_TEST4B_OUT0 = 0x07,
    _PIN_E19_TEST4B_OUT1 = 0x08,
    _PIN_E19_TEST4B_OUT2 = 0x09,
    _PIN_E19_TEST4B_OUT3 = 0x0A,
    _PIN_E19_TEST4B_OUT4 = 0x0B,
    _PIN_E19_TEST4B_OUT5 = 0x0C,
    _PIN_E19_TEST4B_OUT6 = 0x0D,
    _PIN_E19_TEST4B_OUT7 = 0x0E,
    _PIN_E19_NC = _PIN_E19_GPO_PP,
} EnumPinshareInfoPINE19;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x106A at _OFF_Region
// MCU Ctrl : 0x220A at _PIN_E20_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E20_OFF_REGION                     (_PIN_E20_NC)

typedef enum
{
    _PIN_E20_GPI = 0x00,
    _PIN_E20_GPO_PP = 0x01,
    _PIN_E20_GPO_OD = 0x02,
    _PIN_E20_USB_SPI_CEB0_0_1 = 0x03,
    _PIN_E20_USB_SPI_CEB0_1_1 = 0x04,
    _PIN_E20_USB_SPI_CEB0_2_1 = 0x05,
    _PIN_E20_PWM4_PP = 0x06,
    _PIN_E20_PWM4_OD = 0x07,
    _PIN_E20_PWM4_DIMMING_PP = 0x08,
    _PIN_E20_PWM4_DIMMING = 0x09,
    _PIN_E20_TCON12 = 0x0A,
    _PIN_E20_TEST4B_OUT0 = 0x0B,
    _PIN_E20_TEST4B_OUT1 = 0x0C,
    _PIN_E20_TEST4B_OUT2 = 0x0D,
    _PIN_E20_TEST4B_OUT3 = 0x0E,
    _PIN_E20_NC = _PIN_E20_GPO_PP,
} EnumPinshareInfoPINE20;

//---------------------------------------------------------------------------
// Function : ENA557_BL
// Pinshare : 0x106B at _OFF_Region
// MCU Ctrl : 0x220B at _PIN_F21_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F21_OFF_REGION                     (_PIN_F21_NC)

typedef enum
{
    _PIN_F21_GPI = 0x00,
    _PIN_F21_GPO_PP = 0x01,
    _PIN_F21_GPO_OD = 0x02,
    _PIN_F21_USB_SPI_CEB1_0_1 = 0x03,
    _PIN_F21_USB_SPI_CEB1_1_1 = 0x04,
    _PIN_F21_USB_SPI_CEB1_2_1 = 0x05,
    _PIN_F21_TEST4B_OUT0 = 0x06,
    _PIN_F21_TEST4B_OUT1 = 0x07,
    _PIN_F21_TEST4B_OUT2 = 0x08,
    _PIN_F21_TEST4B_OUT3 = 0x09,
    _PIN_F21_TEST4B_OUT4 = 0x0A,
    _PIN_F21_TEST4B_OUT5 = 0x0B,
    _PIN_F21_TEST4B_OUT6 = 0x0C,
    _PIN_F21_TEST4B_OUT7 = 0x0D,
    _PIN_F21_NC = _PIN_F21_GPO_PP,
} EnumPinshareInfoPINF21;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x106C at _OFF_Region
// MCU Ctrl : 0x220C at _PIN_F20_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F20_OFF_REGION                     (_PIN_F20_NC)

typedef enum
{
    _PIN_F20_GPI = 0x00,
    _PIN_F20_GPO_PP = 0x01,
    _PIN_F20_GPO_OD = 0x02,
    _PIN_F20_IICSCL_0_4 = 0x03,
    _PIN_F20_IICSCL_1_4 = 0x04,
    _PIN_F20_TEST4B_OUT0 = 0x05,
    _PIN_F20_TEST4B_OUT1 = 0x06,
    _PIN_F20_TEST4B_OUT2 = 0x07,
    _PIN_F20_TEST4B_OUT3 = 0x08,
    _PIN_F20_TEST4B_OUT4 = 0x09,
    _PIN_F20_TEST4B_OUT5 = 0x0A,
    _PIN_F20_TEST4B_OUT6 = 0x0B,
    _PIN_F20_TEST4B_OUT7 = 0x0C,
    _PIN_F20_NC = _PIN_F20_GPO_PP,
} EnumPinshareInfoPINF20;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x106D at _OFF_Region
// MCU Ctrl : 0x220D at _PIN_F19_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F19_OFF_REGION                     (_PIN_F19_NC)

typedef enum
{
    _PIN_F19_GPI = 0x00,
    _PIN_F19_GPO_PP = 0x01,
    _PIN_F19_GPO_OD = 0x02,
    _PIN_F19_IICSDA_0_4 = 0x03,
    _PIN_F19_IICSDA_1_4 = 0x04,
    _PIN_F19_TEST4B_OUT0 = 0x05,
    _PIN_F19_TEST4B_OUT1 = 0x06,
    _PIN_F19_TEST4B_OUT2 = 0x07,
    _PIN_F19_TEST4B_OUT3 = 0x08,
    _PIN_F19_TEST4B_OUT4 = 0x09,
    _PIN_F19_TEST4B_OUT5 = 0x0A,
    _PIN_F19_TEST4B_OUT6 = 0x0B,
    _PIN_F19_TEST4B_OUT7 = 0x0C,
    _PIN_F19_NC = _PIN_F19_GPO_PP,
} EnumPinshareInfoPINF19;

//---------------------------------------------------------------------------
// Function : Model_sel
// Pinshare : 0x106E at _OFF_Region
// MCU Ctrl : 0x220E at _PIN_E18_MCU_REG
//---------------------------------------------------------------------------
#if(_PANEL_DPTX_LANE_NUMBER == _PANEL_DPTX_LANE_NUMBER_16)
#define _PIN_E18_OFF_REGION                     (_PIN_E18_EDPTX_HPD_ORG_3)
#else
#define _PIN_E18_OFF_REGION                     (_PIN_E18_GPO_PP)
#endif

typedef enum
{
    _PIN_E18_GPI = 0x00,
    _PIN_E18_GPO_PP = 0x01,
    _PIN_E18_GPO_OD = 0x02,
    _PIN_E18_EDPTX_HPD_ORG_3 = 0x03,
    _PIN_E18_VBY1_LOCK_N_1_0 = 0x04,
    _PIN_E18_NC = _PIN_E18_GPO_PP,
} EnumPinshareInfoPINE18;

//---------------------------------------------------------------------------
// Function : eDP_HPD_1
// Pinshare : 0x106F at _OFF_Region
// MCU Ctrl : 0x220F at _PIN_AL27_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AL27_OFF_REGION                    (_PIN_AL27_EDPTX_HPD_ORG_2)

typedef enum
{
    _PIN_AL27_GPI = 0x00,
    _PIN_AL27_GPO_PP = 0x01,
    _PIN_AL27_GPO_OD = 0x02,
    _PIN_AL27_EDPTX_HPD_ORG_2 = 0x03,
    _PIN_AL27_VBY1_HTPD_N_1_0 = 0x04,
    _PIN_AL27_NC = _PIN_AL27_GPO_PP,
} EnumPinshareInfoPINAL27;

//---------------------------------------------------------------------------
// Function : eDP_HPD_0
// Pinshare : 0x1070 at _OFF_Region
// MCU Ctrl : 0x2210 at _PIN_AL26_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AL26_OFF_REGION                    (_PIN_AL26_EDPTX_HPD_ORG_1)


typedef enum
{
    _PIN_AL26_GPI = 0x00,
    _PIN_AL26_GPO_PP = 0x01,
    _PIN_AL26_GPO_OD = 0x02,
    _PIN_AL26_EDPTX_HPD_ORG_1 = 0x03,
    _PIN_AL26_VBY1_LOCK_N_0_0 = 0x04,
    _PIN_AL26_NC = _PIN_AL26_GPO_PP,
} EnumPinshareInfoPINAL26;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1071 at _OFF_Region
// MCU Ctrl : 0x2211 at _PIN_AL29_MCU_REG
//---------------------------------------------------------------------------
#if(_PANEL_DPTX_LANE_NUMBER == _PANEL_DPTX_LANE_NUMBER_16)
#define _PIN_AL29_OFF_REGION                    (_PIN_AL29_EDPTX_HPD_ORG_0)
#else
#define _PIN_AL29_OFF_REGION                    (_PIN_AL29_NC)
#endif

typedef enum
{
    _PIN_AL29_GPI = 0x00,
    _PIN_AL29_GPO_PP = 0x01,
    _PIN_AL29_GPO_OD = 0x02,
    _PIN_AL29_EDPTX_HPD_ORG_0 = 0x03,
    _PIN_AL29_VBY1_HTPD_N_0_0 = 0x04,
    _PIN_AL29_NC = _PIN_AL29_GPO_PP,
} EnumPinshareInfoPINAL29;

//---------------------------------------------------------------------------
// Function : NC(VOLUME)
// Pinshare : 0x1072 at _OFF_Region
// MCU Ctrl : 0x2212 at _PIN_AL28_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AL28_OFF_REGION                    (_PIN_AL28_NC)

typedef enum
{
    _PIN_AL28_GPI = 0x00,
    _PIN_AL28_GPO_PP = 0x01,
    _PIN_AL28_GPO_OD = 0x02,
    _PIN_AL28_PWM5_PP = 0x03,
    _PIN_AL28_PWM5_OD = 0x04,
    _PIN_AL28_PWM5_DIMMING_PP = 0x05,
    _PIN_AL28_PWM5_DIMMING = 0x06,
    _PIN_AL28_TEST4B_OUT0 = 0x07,
    _PIN_AL28_TEST4B_OUT1 = 0x08,
    _PIN_AL28_TEST4B_OUT2 = 0x09,
    _PIN_AL28_TEST4B_OUT3 = 0x0A,
    _PIN_AL28_TEST4B_OUT4 = 0x0B,
    _PIN_AL28_TEST4B_OUT5 = 0x0C,
    _PIN_AL28_TEST4B_OUT6 = 0x0D,
    _PIN_AL28_TEST4B_OUT7 = 0x0E,
    _PIN_AL28_NC = _PIN_AL28_GPO_PP,
} EnumPinshareInfoPINAL28;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1073 at _OFF_Region
// MCU Ctrl : 0x2213 at _PIN_AM28_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AM28_OFF_REGION                    (_PIN_AM28_NC)

typedef enum
{
    _PIN_AM28_GPI = 0x00,
    _PIN_AM28_GPO_PP = 0x01,
    _PIN_AM28_GPO_OD = 0x02,
    _PIN_AM28_PWM4_PP = 0x03,
    _PIN_AM28_PWM4_OD = 0x04,
    _PIN_AM28_PWM4_DIMMING_PP = 0x05,
    _PIN_AM28_PWM4_DIMMING = 0x06,
    _PIN_AM28_TEST4B_OUT0 = 0x07,
    _PIN_AM28_TEST4B_OUT1 = 0x08,
    _PIN_AM28_TEST4B_OUT2 = 0x09,
    _PIN_AM28_TEST4B_OUT3 = 0x0A,
    _PIN_AM28_TEST4B_OUT4 = 0x0B,
    _PIN_AM28_TEST4B_OUT5 = 0x0C,
    _PIN_AM28_TEST4B_OUT6 = 0x0D,
    _PIN_AM28_TEST4B_OUT7 = 0x0E,
    _PIN_AM28_NC = _PIN_AM28_GPO_PP,
} EnumPinshareInfoPINAM28;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1074 at _OFF_Region
// MCU Ctrl : 0x2214 at _PIN_AM29_MCU_REG
//---------------------------------------------------------------------------
#if(_PANEL_DPTX_LANE_NUMBER == _PANEL_DPTX_LANE_NUMBER_16)
#define _PIN_AM29_OFF_REGION                    (_PIN_AM29_EDPTX_AUX_P_3)
#else
#define _PIN_AM29_OFF_REGION                    (_PIN_AM29_NC)
#endif

typedef enum
{
    _PIN_AM29_GPI = 0x00,
    _PIN_AM29_GPO_PP = 0x01,
    _PIN_AM29_GPO_OD = 0x02,
    _PIN_AM29_EDPTX_AUX_P_3 = 0x03,
    _PIN_AM29_NC = _PIN_AM29_GPO_PP,
} EnumPinshareInfoPINAM29;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1075 at _OFF_Region
// MCU Ctrl : 0x2215 at _PIN_AM30_MCU_REG
//---------------------------------------------------------------------------
#if(_PANEL_DPTX_LANE_NUMBER == _PANEL_DPTX_LANE_NUMBER_16)
#define _PIN_AM30_OFF_REGION                    (_PIN_AM30_EDPTX_AUX_N_3)
#else
#define _PIN_AM30_OFF_REGION                    (_PIN_AM30_NC)
#endif

typedef enum
{
    _PIN_AM30_GPI = 0x00,
    _PIN_AM30_GPO_PP = 0x01,
    _PIN_AM30_GPO_OD = 0x02,
    _PIN_AM30_EDPTX_AUX_N_3 = 0x03,
    _PIN_AM30_NC = _PIN_AM30_GPO_PP,
} EnumPinshareInfoPINAM30;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1076 at _OFF_Region
// MCU Ctrl : 0x2216 at _PIN_AJ18_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AJ18_OFF_REGION                    (_PIN_AJ18_NC)

typedef enum
{
    _PIN_AJ18_GPI = 0x00,
    _PIN_AJ18_GPO_PP = 0x01,
    _PIN_AJ18_GPO_OD = 0x02,
    _PIN_AJ18_EXT_UART_TX_0_6 = 0x03,
    _PIN_AJ18_EXT_UART_TX_1_6 = 0x04,
    _PIN_AJ18_EXT_UART_TX_2_6 = 0x05,
    _PIN_AJ18_INT0_4 = 0x06,
    _PIN_AJ18_INT1_4 = 0x07,
    _PIN_AJ18_TYPEC_GPIO2_1_PP = 0x08,
    _PIN_AJ18_TYPEC_GPIO2_1_OD = 0x09,
    _PIN_AJ18_TYPEC_GPIO3_1_PP = 0x0A,
    _PIN_AJ18_TYPEC_GPIO3_1_OD = 0x0B,
    _PIN_AJ18_TEST4B_OUT0 = 0x0C,
    _PIN_AJ18_TEST4B_OUT1 = 0x0D,
    _PIN_AJ18_TEST4B_OUT2 = 0x0E,
    _PIN_AJ18_TEST4B_OUT3 = 0x0F,
    _PIN_AJ18_NC = _PIN_AJ18_GPO_PP,
} EnumPinshareInfoPINAJ18;

//---------------------------------------------------------------------------
// Function : PANEL_ENABLE
// Pinshare : 0x1077 at _OFF_Region
// MCU Ctrl : 0x2217 at _PIN_AK20_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AK20_OFF_REGION                    (_PIN_AK20_GPO_PP)

typedef enum
{
    _PIN_AK20_GPI = 0x00,
    _PIN_AK20_GPO_PP = 0x01,
    _PIN_AK20_GPO_OD = 0x02,
    _PIN_AK20_EXT_UART_RX_0_6 = 0x03,
    _PIN_AK20_EXT_UART_RX_1_6 = 0x04,
    _PIN_AK20_EXT_UART_RX_2_6 = 0x05,
    _PIN_AK20_IRDA_IN_0_1 = 0x06,
    _PIN_AK20_TYPEC_GPIO0_1_PP = 0x07,
    _PIN_AK20_TYPEC_GPIO0_1_OD = 0x08,
    _PIN_AK20_TYPEC_GPIO1_1_PP = 0x09,
    _PIN_AK20_TYPEC_GPIO1_1_OD = 0x0A,
    _PIN_AK20_TEST4B_OUT0 = 0x0B,
    _PIN_AK20_TEST4B_OUT1 = 0x0C,
    _PIN_AK20_TEST4B_OUT2 = 0x0D,
    _PIN_AK20_TEST4B_OUT3 = 0x0E,
    _PIN_AK20_TEST4B_OUT4 = 0x0F,
    _PIN_AK20_NC = _PIN_AK20_GPO_PP,
} EnumPinshareInfoPINAK20;

//---------------------------------------------------------------------------
// Function : BL_ADIM
// Pinshare : 0x1078 at _OFF_Region
// MCU Ctrl : 0x2218 at _PIN_AK25_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AK25_OFF_REGION                    (_PIN_AK25_PWM0_PP)

typedef enum
{
    _PIN_AK25_GPI = 0x00,
    _PIN_AK25_GPO_PP = 0x01,
    _PIN_AK25_GPO_OD = 0x02,
    _PIN_AK25_PWM_OUT = 0x03,
    _PIN_AK25_PWM0_PP = 0x04,
    _PIN_AK25_PWM0_OD = 0x05,
    _PIN_AK25_PWM0_DIMMING_PP = 0x06,
    _PIN_AK25_PWM0_DIMMING = 0x07,
    _PIN_AK25_TEST4B_OUT0 = 0x08,
    _PIN_AK25_TEST4B_OUT1 = 0x09,
    _PIN_AK25_TEST4B_OUT2 = 0x0A,
    _PIN_AK25_TEST4B_OUT3 = 0x0B,
    _PIN_AK25_TEST4B_OUT4 = 0x0C,
    _PIN_AK25_TEST4B_OUT5 = 0x0D,
    _PIN_AK25_TEST4B_OUT6 = 0x0E,
    _PIN_AK25_TEST4B_OUT7 = 0x0F,
    _PIN_AK25_NC = _PIN_AK25_GPO_PP,
} EnumPinshareInfoPINAK25;

//---------------------------------------------------------------------------
// Function : EDP_AUXTX1P
// Pinshare : 0x1079 at _OFF_Region
// MCU Ctrl : 0x2219 at _PIN_AM26_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AM26_OFF_REGION                    (_PIN_AM26_EDPTX_AUX_P_2)

typedef enum
{
    _PIN_AM26_GPI = 0x00,
    _PIN_AM26_GPO_PP = 0x01,
    _PIN_AM26_GPO_OD = 0x02,
    _PIN_AM26_EDPTX_AUX_P_2 = 0x03,
    _PIN_AM26_NC = _PIN_AM26_GPO_PP,
} EnumPinshareInfoPINAM26;

//---------------------------------------------------------------------------
// Function : EDP_AUXTX1N
// Pinshare : 0x107A at _OFF_Region
// MCU Ctrl : 0x221A at _PIN_AM27_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AM27_OFF_REGION                    (_PIN_AM27_EDPTX_AUX_N_2)

typedef enum
{
    _PIN_AM27_GPI = 0x00,
    _PIN_AM27_GPO_PP = 0x01,
    _PIN_AM27_GPO_OD = 0x02,
    _PIN_AM27_EDPTX_AUX_N_2 = 0x03,
    _PIN_AM27_NC = _PIN_AM27_GPO_PP,
} EnumPinshareInfoPINAM27;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x107B at _OFF_Region
// MCU Ctrl : 0x221B at _PIN_AJ25_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AJ25_OFF_REGION                    (_PIN_AJ25_NC)

typedef enum
{
    _PIN_AJ25_GPI = 0x00,
    _PIN_AJ25_GPO_PP = 0x01,
    _PIN_AJ25_GPO_OD = 0x02,
    _PIN_AJ25_IICSCL_0_7 = 0x03,
    _PIN_AJ25_IICSCL_1_7 = 0x04,
    _PIN_AJ25_TYPEC_GPIO6_0_PP = 0x05,
    _PIN_AJ25_TYPEC_GPIO6_0_OD = 0x06,
    _PIN_AJ25_TYPEC_GPIO7_0_PP = 0x07,
    _PIN_AJ25_TYPEC_GPIO7_0_OD = 0x08,
    _PIN_AJ25_TEST4B_OUT0 = 0x09,
    _PIN_AJ25_TEST4B_OUT1 = 0x0A,
    _PIN_AJ25_TEST4B_OUT2 = 0x0B,
    _PIN_AJ25_TEST4B_OUT3 = 0x0C,
    _PIN_AJ25_TEST4B_OUT4 = 0x0D,
    _PIN_AJ25_TEST4B_OUT5 = 0x0E,
    _PIN_AJ25_TEST4B_OUT6 = 0x0F,
    _PIN_AJ25_NC = _PIN_AJ25_GPO_PP,
} EnumPinshareInfoPINAJ25;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x107C at _OFF_Region
// MCU Ctrl : 0x221C at _PIN_AK21_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AK21_OFF_REGION                    (_PIN_AK21_NC)

typedef enum
{
    _PIN_AK21_GPI = 0x00,
    _PIN_AK21_GPO_PP = 0x01,
    _PIN_AK21_GPO_OD = 0x02,
    _PIN_AK21_IICSDA_0_7 = 0x03,
    _PIN_AK21_IICSDA_1_7 = 0x04,
    _PIN_AK21_TYPEC_GPIO4_0_PP = 0x05,
    _PIN_AK21_TYPEC_GPIO4_0_OD = 0x06,
    _PIN_AK21_TYPEC_GPIO5_0_PP = 0x07,
    _PIN_AK21_TYPEC_GPIO5_0_OD = 0x08,
    _PIN_AK21_TEST4B_OUT0 = 0x09,
    _PIN_AK21_TEST4B_OUT1 = 0x0A,
    _PIN_AK21_TEST4B_OUT2 = 0x0B,
    _PIN_AK21_TEST4B_OUT3 = 0x0C,
    _PIN_AK21_TEST4B_OUT4 = 0x0D,
    _PIN_AK21_TEST4B_OUT5 = 0x0E,
    _PIN_AK21_TEST4B_OUT6 = 0x0F,
    _PIN_AK21_NC = _PIN_AK21_GPO_PP,
} EnumPinshareInfoPINAK21;

//---------------------------------------------------------------------------
// Function : EDP_AUXTX0P
// Pinshare : 0x107D at _OFF_Region
// MCU Ctrl : 0x221D at _PIN_AM25_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AM25_OFF_REGION                    (_PIN_AM25_EDPTX_AUX_P_1)

typedef enum
{
    _PIN_AM25_GPI = 0x00,
    _PIN_AM25_GPO_PP = 0x01,
    _PIN_AM25_GPO_OD = 0x02,
    _PIN_AM25_EDPTX_AUX_P_1 = 0x03,
    _PIN_AM25_NC = _PIN_AM25_GPO_PP,
} EnumPinshareInfoPINAM25;

//---------------------------------------------------------------------------
// Function : EDP_AUXTX0N
// Pinshare : 0x107E at _OFF_Region
// MCU Ctrl : 0x221E at _PIN_AL25_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_AL25_OFF_REGION                    (_PIN_AL25_EDPTX_AUX_N_1)

typedef enum
{
    _PIN_AL25_GPI = 0x00,
    _PIN_AL25_GPO_PP = 0x01,
    _PIN_AL25_GPO_OD = 0x02,
    _PIN_AL25_EDPTX_AUX_N_1 = 0x03,
    _PIN_AL25_NC = _PIN_AL25_GPO_PP,
} EnumPinshareInfoPINAL25;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x107F at _OFF_Region
// MCU Ctrl : 0x221F at _PIN_AK17_MCU_REG
//---------------------------------------------------------------------------
#if(_PANEL_DPTX_LANE_NUMBER == _PANEL_DPTX_LANE_NUMBER_16)
#define _PIN_AK17_OFF_REGION                    (_PIN_AK17_EDPTX_AUX_P_0)
#else
#define _PIN_AK17_OFF_REGION                    (_PIN_AK17_NC)
#endif

typedef enum
{
    _PIN_AK17_GPI = 0x00,
    _PIN_AK17_GPO_PP = 0x01,
    _PIN_AK17_GPO_OD = 0x02,
    _PIN_AK17_EDPTX_AUX_P_0 = 0x03,
    _PIN_AK17_NC = _PIN_AK17_GPO_PP,
} EnumPinshareInfoPINAK17;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1080 at _OFF_Region
// MCU Ctrl : 0x2220 at _PIN_AK18_MCU_REG
//---------------------------------------------------------------------------
#if(_PANEL_DPTX_LANE_NUMBER == _PANEL_DPTX_LANE_NUMBER_16)
#define _PIN_AK18_OFF_REGION                    (_PIN_AK18_EDPTX_AUX_N_0)
#else
#define _PIN_AK18_OFF_REGION                    (_PIN_AK18_NC)
#endif

typedef enum
{
    _PIN_AK18_GPI = 0x00,
    _PIN_AK18_GPO_PP = 0x01,
    _PIN_AK18_GPO_OD = 0x02,
    _PIN_AK18_EDPTX_AUX_N_0 = 0x03,
    _PIN_AK18_NC = _PIN_AK18_GPO_PP,
} EnumPinshareInfoPINAK18;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1081
// MCU Ctrl : 0x2221 at _PIN_J4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_J4                                 (_PIN_J4_NC)

typedef enum
{
    _PIN_J4_GPI = 0x00,
    _PIN_J4_GPO_PP = 0x01,
    _PIN_J4_GPO_OD = 0x02,
    _PIN_J4_PWM_IN = 0x03,
    _PIN_J4_PWM1_PP = 0x04,
    _PIN_J4_PWM1_OD = 0x05,
    _PIN_J4_PWM1_DIMMING_PP = 0x06,
    _PIN_J4_PWM1_DIMMING = 0x07,
    _PIN_J4_TEST4B_OUT0 = 0x08,
    _PIN_J4_TEST4B_OUT1 = 0x09,
    _PIN_J4_TEST4B_OUT2 = 0x0A,
    _PIN_J4_TEST4B_OUT3 = 0x0B,
    _PIN_J4_TEST4B_OUT4 = 0x0C,
    _PIN_J4_TEST4B_OUT5 = 0x0D,
    _PIN_J4_TEST4B_OUT6 = 0x0E,
    _PIN_J4_TEST4B_OUT7 = 0x0F,
    _PIN_J4_NC = _PIN_J4_GPO_PP,
} EnumPinshareInfoPINJ4;

//---------------------------------------------------------------------------
// Function : DP1_SINK_ASS_P
// Pinshare : 0x1082
// MCU Ctrl : 0x2222 at _PIN_H11_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H11                                (_PIN_H11_GPI)

typedef enum
{
    _PIN_H11_GPI = 0x00,
    _PIN_H11_GPO_PP = 0x01,
    _PIN_H11_GPO_OD = 0x02,
    _PIN_H11_TEST4B_OUT0 = 0x03,
    _PIN_H11_TEST4B_OUT1 = 0x04,
    _PIN_H11_TEST4B_OUT2 = 0x05,
    _PIN_H11_TEST4B_OUT3 = 0x06,
    _PIN_H11_TEST4B_OUT4 = 0x07,
    _PIN_H11_TEST4B_OUT5 = 0x08,
    _PIN_H11_TEST4B_OUT6 = 0x09,
    _PIN_H11_TEST4B_OUT7 = 0x0A,
    _PIN_H11_NC = _PIN_H11_GPO_PP,
} EnumPinshareInfoPINH11;

//---------------------------------------------------------------------------
// Function : DP1_SINK_ASS_N
// Pinshare : 0x1083
// MCU Ctrl : 0x2223 at _PIN_G11_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G11                                (_PIN_G11_GPI)

typedef enum
{
    _PIN_G11_GPI = 0x00,
    _PIN_G11_GPO_PP = 0x01,
    _PIN_G11_GPO_OD = 0x02,
    _PIN_G11_TEST4B_OUT0 = 0x03,
    _PIN_G11_TEST4B_OUT1 = 0x04,
    _PIN_G11_TEST4B_OUT2 = 0x05,
    _PIN_G11_TEST4B_OUT3 = 0x06,
    _PIN_G11_TEST4B_OUT4 = 0x07,
    _PIN_G11_TEST4B_OUT5 = 0x08,
    _PIN_G11_TEST4B_OUT6 = 0x09,
    _PIN_G11_TEST4B_OUT7 = 0x0A,
    _PIN_G11_NC = _PIN_G11_GPO_PP,
} EnumPinshareInfoPING11;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1084
// MCU Ctrl : 0x2224 at _PIN_E7_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E7                                 (_PIN_E7_NC)

typedef enum
{
    _PIN_E7_GPI = 0x00,
    _PIN_E7_GPO_PP = 0x01,
    _PIN_E7_GPO_OD = 0x02,
    _PIN_E7_TEST4B_OUT0 = 0x03,
    _PIN_E7_TEST4B_OUT1 = 0x04,
    _PIN_E7_TEST4B_OUT2 = 0x05,
    _PIN_E7_TEST4B_OUT3 = 0x06,
    _PIN_E7_TEST4B_OUT4 = 0x07,
    _PIN_E7_TEST4B_OUT5 = 0x08,
    _PIN_E7_TEST4B_OUT6 = 0x09,
    _PIN_E7_TEST4B_OUT7 = 0x0A,
    _PIN_E7_NC = _PIN_E7_GPO_PP,
} EnumPinshareInfoPINE7;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1085
// MCU Ctrl : 0x2225 at _PIN_G7_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G7                                 (_PIN_G7_NC)

typedef enum
{
    _PIN_G7_GPI = 0x00,
    _PIN_G7_GPO_PP = 0x01,
    _PIN_G7_GPO_OD = 0x02,
    _PIN_G7_TEST4B_OUT0 = 0x03,
    _PIN_G7_TEST4B_OUT1 = 0x04,
    _PIN_G7_TEST4B_OUT2 = 0x05,
    _PIN_G7_TEST4B_OUT3 = 0x06,
    _PIN_G7_TEST4B_OUT4 = 0x07,
    _PIN_G7_TEST4B_OUT5 = 0x08,
    _PIN_G7_TEST4B_OUT6 = 0x09,
    _PIN_G7_TEST4B_OUT7 = 0x0A,
    _PIN_G7_NC = _PIN_G7_GPO_PP,
} EnumPinshareInfoPING7;

//---------------------------------------------------------------------------
// Function : DP1_CONFIG1(NC)
// Pinshare : 0x1086
// MCU Ctrl : 0x2226 at _PIN_G10_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G10                                (_PIN_G10_NC)

typedef enum
{
    _PIN_G10_GPI = 0x00,
    _PIN_G10_GPO_PP = 0x01,
    _PIN_G10_GPO_OD = 0x02,
    _PIN_G10_DPRX_AUX_P_2 = 0x03,
    _PIN_G10_NC = _PIN_G10_GPO_PP,
} EnumPinshareInfoPING10;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1087
// MCU Ctrl : 0x2227 at _PIN_F10_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F10                                (_PIN_F10_NC)

typedef enum
{
    _PIN_F10_GPI = 0x00,
    _PIN_F10_GPO_PP = 0x01,
    _PIN_F10_GPO_OD = 0x02,
    _PIN_F10_DPRX_AUX_N_2 = 0x03,
    _PIN_F10_NC = _PIN_F10_GPO_PP,
} EnumPinshareInfoPINF10;

//---------------------------------------------------------------------------
// Function : HDMI_1_DDCCK
// Pinshare : 0x1088
// MCU Ctrl : 0x2228 at _PIN_G9_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G9                                 (_PIN_G9_DDCSCL_3)

typedef enum
{
    _PIN_G9_GPI = 0x00,
    _PIN_G9_GPO_OD = 0x02,
    _PIN_G9_DDCSCL_3 = 0x03,
    _PIN_G9_SWDCLK_0_1 = 0x04,
    _PIN_G9_NC = _PIN_G9_GPI,
} EnumPinshareInfoPING9;

//---------------------------------------------------------------------------
// Function : HDMI_1_DDCDA
// Pinshare : 0x1089
// MCU Ctrl : 0x2229 at _PIN_E8_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E8                                 (_PIN_E8_DDCSDA_3)

typedef enum
{
    _PIN_E8_GPI = 0x00,
    _PIN_E8_GPO_OD = 0x02,
    _PIN_E8_DDCSDA_3 = 0x03,
    _PIN_E8_SWDIO_0_1 = 0x04,
    _PIN_E8_NC = _PIN_E8_GPI,
} EnumPinshareInfoPINE8;

//---------------------------------------------------------------------------
// Function : HDMI2_A0_SEL
// Pinshare : 0x108A
// MCU Ctrl : 0x222A at _PIN_E10_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E10                                (_PIN_E10_GPO_OD)

typedef enum
{
    _PIN_E10_GPI = 0x00,
    _PIN_E10_GPO_PP = 0x01,
    _PIN_E10_GPO_OD = 0x02,
    _PIN_E10_USB_SPI_CLK_0_3 = 0x03,
    _PIN_E10_USB_SPI_CLK_1_3 = 0x04,
    _PIN_E10_USB_SPI_CLK_2_3 = 0x05,
    _PIN_E10_TEST4B_OUT0 = 0x06,
    _PIN_E10_TEST4B_OUT1 = 0x07,
    _PIN_E10_TEST4B_OUT2 = 0x08,
    _PIN_E10_TEST4B_OUT3 = 0x09,
    _PIN_E10_TEST4B_OUT4 = 0x0A,
    _PIN_E10_TEST4B_OUT5 = 0x0B,
    _PIN_E10_TEST4B_OUT6 = 0x0C,
    _PIN_E10_TEST4B_OUT7 = 0x0D,
    _PIN_E10_NC = _PIN_E10_GPO_PP,
} EnumPinshareInfoPINE10;

//---------------------------------------------------------------------------
// Function : DP1_CABLE_DET
// Pinshare : 0x108B
// MCU Ctrl : 0x222B at _PIN_D9_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_D9                                 (_PIN_D9_GPI)

typedef enum
{
    _PIN_D9_GPI = 0x00,
    _PIN_D9_GPO_PP = 0x01,
    _PIN_D9_GPO_OD = 0x02,
    _PIN_D9_USB_SPI_SI_0_3 = 0x03,
    _PIN_D9_USB_SPI_SI_1_3 = 0x04,
    _PIN_D9_USB_SPI_SI_2_3 = 0x05,
    _PIN_D9_TEST4B_OUT0 = 0x06,
    _PIN_D9_TEST4B_OUT1 = 0x07,
    _PIN_D9_TEST4B_OUT2 = 0x08,
    _PIN_D9_TEST4B_OUT3 = 0x09,
    _PIN_D9_TEST4B_OUT4 = 0x0A,
    _PIN_D9_TEST4B_OUT5 = 0x0B,
    _PIN_D9_TEST4B_OUT6 = 0x0C,
    _PIN_D9_TEST4B_OUT7 = 0x0D,
    _PIN_D9_NC = _PIN_D9_GPO_PP,
} EnumPinshareInfoPIND9;

//---------------------------------------------------------------------------
// Function : DP1_HOT_PLUG
// Pinshare : 0x108C
// MCU Ctrl : 0x222C at _PIN_D10_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_D10                                (_PIN_D10_GPO_PP)

typedef enum
{
    _PIN_D10_GPI = 0x00,
    _PIN_D10_GPO_PP = 0x01,
    _PIN_D10_GPO_OD = 0x02,
    _PIN_D10_USB_SPI_SO_0_3 = 0x03,
    _PIN_D10_USB_SPI_SO_1_3 = 0x04,
    _PIN_D10_USB_SPI_SO_2_3 = 0x05,
    _PIN_D10_TEST4B_OUT0 = 0x06,
    _PIN_D10_TEST4B_OUT1 = 0x07,
    _PIN_D10_TEST4B_OUT2 = 0x08,
    _PIN_D10_TEST4B_OUT3 = 0x09,
    _PIN_D10_TEST4B_OUT4 = 0x0A,
    _PIN_D10_TEST4B_OUT5 = 0x0B,
    _PIN_D10_TEST4B_OUT6 = 0x0C,
    _PIN_D10_TEST4B_OUT7 = 0x0D,
    _PIN_D10_NC = _PIN_D10_GPO_PP,
} EnumPinshareInfoPIND10;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x108D
// MCU Ctrl : 0x222D at _PIN_G8_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G8                                 (_PIN_G8_NC)

typedef enum
{
    _PIN_G8_GPI = 0x00,
    _PIN_G8_GPO_PP = 0x01,
    _PIN_G8_GPO_OD = 0x02,
    _PIN_G8_USB_SPI_CEB0_0_3 = 0x03,
    _PIN_G8_USB_SPI_CEB0_1_3 = 0x04,
    _PIN_G8_USB_SPI_CEB0_2_3 = 0x05,
    _PIN_G8_TEST4B_OUT0 = 0x06,
    _PIN_G8_TEST4B_OUT1 = 0x07,
    _PIN_G8_TEST4B_OUT2 = 0x08,
    _PIN_G8_TEST4B_OUT3 = 0x09,
    _PIN_G8_TEST4B_OUT4 = 0x0A,
    _PIN_G8_TEST4B_OUT5 = 0x0B,
    _PIN_G8_TEST4B_OUT6 = 0x0C,
    _PIN_G8_TEST4B_OUT7 = 0x0D,
    _PIN_G8_NC = _PIN_G8_GPO_PP,
} EnumPinshareInfoPING8;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x108E
// MCU Ctrl : 0x222E at _PIN_H9_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H9                                 (_PIN_H9_NC)

typedef enum
{
    _PIN_H9_GPI = 0x00,
    _PIN_H9_GPO_PP = 0x01,
    _PIN_H9_GPO_OD = 0x02,
    _PIN_H9_USB_SPI_CEB1_0_3 = 0x03,
    _PIN_H9_USB_SPI_CEB1_1_3 = 0x04,
    _PIN_H9_USB_SPI_CEB1_2_3 = 0x05,
    _PIN_H9_TEST4B_OUT0 = 0x06,
    _PIN_H9_TEST4B_OUT1 = 0x07,
    _PIN_H9_TEST4B_OUT2 = 0x08,
    _PIN_H9_TEST4B_OUT3 = 0x09,
    _PIN_H9_TEST4B_OUT4 = 0x0A,
    _PIN_H9_TEST4B_OUT5 = 0x0B,
    _PIN_H9_TEST4B_OUT6 = 0x0C,
    _PIN_H9_TEST4B_OUT7 = 0x0D,
    _PIN_H9_NC = _PIN_H9_GPO_PP,
} EnumPinshareInfoPINH9;

//---------------------------------------------------------------------------
// Function : AUX1_CHP
// Pinshare : 0x108F
// MCU Ctrl : 0x222F at _PIN_E9_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E9                                 (_PIN_E9_DPRX_AUX_P_1)

typedef enum
{
    _PIN_E9_GPI = 0x00,
    _PIN_E9_GPO_PP = 0x01,
    _PIN_E9_GPO_OD = 0x02,
    _PIN_E9_DPRX_AUX_P_1 = 0x03,
    _PIN_E9_NC = _PIN_E9_GPO_PP,
} EnumPinshareInfoPINE9;

//---------------------------------------------------------------------------
// Function : AUX1_CHN
// Pinshare : 0x1090
// MCU Ctrl : 0x2230 at _PIN_F9_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F9                                 (_PIN_F9_DPRX_AUX_N_1)

typedef enum
{
    _PIN_F9_GPI = 0x00,
    _PIN_F9_GPO_PP = 0x01,
    _PIN_F9_GPO_OD = 0x02,
    _PIN_F9_DPRX_AUX_N_1 = 0x03,
    _PIN_F9_NC = _PIN_F9_GPO_PP,
} EnumPinshareInfoPINF9;

//---------------------------------------------------------------------------
// Function : HDMI_2_DDCCK
// Pinshare : 0x1091
// MCU Ctrl : 0x2231 at _PIN_J3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_J3                                 (_PIN_J3_DDCSCL_4)

typedef enum
{
    _PIN_J3_GPI = 0x00,
    _PIN_J3_GPO_OD = 0x02,
    _PIN_J3_DDCSCL_4 = 0x03,
    _PIN_J3_SWDCLK_0_2 = 0x04,
    _PIN_J3_NC = _PIN_J3_GPI,
} EnumPinshareInfoPINJ3;

//---------------------------------------------------------------------------
// Function : HDMI_2_DDCDA
// Pinshare : 0x1092
// MCU Ctrl : 0x2232 at _PIN_J2_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_J2                                 (_PIN_J2_DDCSDA_4)

typedef enum
{
    _PIN_J2_GPI = 0x00,
    _PIN_J2_GPO_OD = 0x02,
    _PIN_J2_DDCSDA_4 = 0x03,
    _PIN_J2_SWDIO_0_2 = 0x04,
    _PIN_J2_NC = _PIN_J2_GPI,
} EnumPinshareInfoPINJ2;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1093
// MCU Ctrl : 0x2233 at _PIN_H3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H3                                 (_PIN_H3_NC)

typedef enum
{
    _PIN_H3_GPI = 0x00,
    _PIN_H3_GPO_PP = 0x01,
    _PIN_H3_GPO_OD = 0x02,
    _PIN_H3_DPRX_AUX_P_0 = 0x03,
    _PIN_H3_NC = _PIN_H3_GPO_PP,
} EnumPinshareInfoPINH3;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1094
// MCU Ctrl : 0x2234 at _PIN_H2_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H2                                 (_PIN_H2_NC)

typedef enum
{
    _PIN_H2_GPI = 0x00,
    _PIN_H2_GPO_PP = 0x01,
    _PIN_H2_GPO_OD = 0x02,
    _PIN_H2_DPRX_AUX_N_0 = 0x03,
    _PIN_H2_NC = _PIN_H2_GPO_PP,
} EnumPinshareInfoPINH2;

//---------------------------------------------------------------------------
// Function : HP_DET
// Pinshare : 0x1095
// MCU Ctrl : 0x2235 at _PIN_E11_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_E11                                (_PIN_E11_GPI)

typedef enum
{
    _PIN_E11_GPI = 0x00,
    _PIN_E11_GPO_PP = 0x01,
    _PIN_E11_GPO_OD = 0x02,
    _PIN_E11_PWM2_PP = 0x03,
    _PIN_E11_PWM2_OD = 0x04,
    _PIN_E11_PWM2_DIMMING_PP = 0x05,
    _PIN_E11_PWM2_DIMMING = 0x06,
    _PIN_E11_EXT_UART_TX_0_3 = 0x07,
    _PIN_E11_EXT_UART_TX_1_3 = 0x08,
    _PIN_E11_EXT_UART_TX_2_3 = 0x09,
    _PIN_E11_TEST4B_OUT0 = 0x0A,
    _PIN_E11_TEST4B_OUT1 = 0x0B,
    _PIN_E11_TEST4B_OUT2 = 0x0C,
    _PIN_E11_TEST4B_OUT3 = 0x0D,
    _PIN_E11_TEST4B_OUT4 = 0x0E,
    _PIN_E11_TEST4B_OUT5 = 0x0F,
    _PIN_E11_NC = _PIN_E11_GPO_PP,
} EnumPinshareInfoPINE11;

//---------------------------------------------------------------------------
// Function : VCCK_OFF_EN
// Pinshare : 0x1096
// MCU Ctrl : 0x2236 at _PIN_F8_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F8                                 (_PIN_F8_GPO_OD)

typedef enum
{
    _PIN_F8_GPI = 0x00,
    _PIN_F8_GPO_PP = 0x01,
    _PIN_F8_GPO_OD = 0x02,
    _PIN_F8_EXT_UART_RX_0_3 = 0x03,
    _PIN_F8_EXT_UART_RX_1_3 = 0x04,
    _PIN_F8_EXT_UART_RX_2_3 = 0x05,
    _PIN_F8_TEST4B_OUT0 = 0x06,
    _PIN_F8_TEST4B_OUT1 = 0x07,
    _PIN_F8_TEST4B_OUT2 = 0x08,
    _PIN_F8_TEST4B_OUT3 = 0x09,
    _PIN_F8_TEST4B_OUT4 = 0x0A,
    _PIN_F8_TEST4B_OUT5 = 0x0B,
    _PIN_F8_TEST4B_OUT6 = 0x0C,
    _PIN_F8_TEST4B_OUT7 = 0x0D,
    _PIN_F8_NC = _PIN_F8_GPO_PP,
} EnumPinshareInfoPINF8;

//---------------------------------------------------------------------------
// Function : HUBISPSCL
// Pinshare : 0x1097
// MCU Ctrl : 0x2237 at _PIN_F1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F1                                 (_PIN_F1_DDCSCL_ISP)

typedef enum
{
    _PIN_F1_GPI = 0x00,
    _PIN_F1_GPO_PP = 0x01,
    _PIN_F1_GPO_OD = 0x02,
    _PIN_F1_DDCSCL_ISP = 0x03,
    _PIN_F1_IICSCL_0_0 = 0x04,
    _PIN_F1_IICSCL_1_0 = 0x05,
    _PIN_F1_SWDCLK_0_0 = 0x06,
    _PIN_F1_USB_SPI_CLK_0_4 = 0x07,
    _PIN_F1_USB_SPI_CLK_1_4 = 0x08,
    _PIN_F1_USB_SPI_CLK_2_4 = 0x09,
    _PIN_F1_TEST4B_OUT0 = 0x0A,
    _PIN_F1_TEST4B_OUT1 = 0x0B,
    _PIN_F1_TEST4B_OUT2 = 0x0C,
    _PIN_F1_TEST4B_OUT3 = 0x0D,
    _PIN_F1_TEST4B_OUT4 = 0x0E,
    _PIN_F1_TEST4B_OUT5 = 0x0F,
    _PIN_F1_NC = _PIN_F1_GPO_PP,
} EnumPinshareInfoPINF1;

//---------------------------------------------------------------------------
// Function : HUBISPSDA
// Pinshare : 0x1098
// MCU Ctrl : 0x2238 at _PIN_G4_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G4                                 (_PIN_G4_DDCSDA_ISP)

typedef enum
{
    _PIN_G4_GPI = 0x00,
    _PIN_G4_GPO_PP = 0x01,
    _PIN_G4_GPO_OD = 0x02,
    _PIN_G4_DDCSDA_ISP = 0x03,
    _PIN_G4_IICSDA_0_0 = 0x04,
    _PIN_G4_IICSDA_1_0 = 0x05,
    _PIN_G4_SWDIO_0_0 = 0x06,
    _PIN_G4_TEST4B_OUT0 = 0x07,
    _PIN_G4_TEST4B_OUT1 = 0x08,
    _PIN_G4_TEST4B_OUT2 = 0x09,
    _PIN_G4_TEST4B_OUT3 = 0x0A,
    _PIN_G4_TEST4B_OUT4 = 0x0B,
    _PIN_G4_TEST4B_OUT5 = 0x0C,
    _PIN_G4_TEST4B_OUT6 = 0x0D,
    _PIN_G4_TEST4B_OUT7 = 0x0E,
    _PIN_G4_NC = _PIN_G4_GPO_PP,
} EnumPinshareInfoPING4;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1099
// MCU Ctrl : 0x2239 at _PIN_H1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H1                                 (_PIN_H1_NC)

typedef enum
{
    _PIN_H1_GPI = 0x00,
    _PIN_H1_GPO_PP = 0x01,
    _PIN_H1_GPO_OD = 0x02,
    _PIN_H1_IRDA_IN_0_2 = 0x03,
    _PIN_H1_TCON0 = 0x04,
    _PIN_H1_TCON1 = 0x05,
    _PIN_H1_TEST4B_OUT0 = 0x06,
    _PIN_H1_TEST4B_OUT1 = 0x07,
    _PIN_H1_TEST4B_OUT2 = 0x08,
    _PIN_H1_TEST4B_OUT3 = 0x09,
    _PIN_H1_TEST4B_OUT4 = 0x0A,
    _PIN_H1_TEST4B_OUT5 = 0x0B,
    _PIN_H1_TEST4B_OUT6 = 0x0C,
    _PIN_H1_TEST4B_OUT7 = 0x0D,
    _PIN_H1_NC = _PIN_H1_GPO_PP,
} EnumPinshareInfoPINH1;

//---------------------------------------------------------------------------
// Function : NC(con_off)
// Pinshare : 0x109A
// MCU Ctrl : 0x223A at _PIN_F7_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_F7                                 (_PIN_F7_NC)

typedef enum
{
    _PIN_F7_GPI = 0x00,
    _PIN_F7_GPO_PP = 0x01,
    _PIN_F7_GPO_OD = 0x02,
    _PIN_F7_PWM_UPD_SYNC_0_0_PP = 0x03,
    _PIN_F7_TEST4B_OUT0 = 0x04,
    _PIN_F7_TEST4B_OUT1 = 0x05,
    _PIN_F7_TEST4B_OUT2 = 0x06,
    _PIN_F7_TEST4B_OUT3 = 0x07,
    _PIN_F7_TEST4B_OUT4 = 0x08,
    _PIN_F7_TEST4B_OUT5 = 0x09,
    _PIN_F7_TEST4B_OUT6 = 0x0A,
    _PIN_F7_TEST4B_OUT7 = 0x0B,
    _PIN_F7_NC = _PIN_F7_GPO_PP,
} EnumPinshareInfoPINF7;

//---------------------------------------------------------------------------
// Function : FLASH_WP
// Pinshare : 0x109B
// MCU Ctrl : 0x223B at _PIN_H7_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_H7                                 (_PIN_H7_GPO_PP)

typedef enum
{
    _PIN_H7_GPI = 0x00,
    _PIN_H7_GPO_PP = 0x01,
    _PIN_H7_GPO_OD = 0x02,
    _PIN_H7_IRQB = 0x03,
    _PIN_H7_TCON2 = 0x04,
    _PIN_H7_TEST4B_OUT0 = 0x05,
    _PIN_H7_TEST4B_OUT1 = 0x06,
    _PIN_H7_TEST4B_OUT2 = 0x07,
    _PIN_H7_TEST4B_OUT3 = 0x08,
    _PIN_H7_TEST4B_OUT4 = 0x09,
    _PIN_H7_TEST4B_OUT5 = 0x0A,
    _PIN_H7_TEST4B_OUT6 = 0x0B,
    _PIN_H7_TEST4B_OUT7 = 0x0C,
    _PIN_H7_NC = _PIN_H7_GPO_PP,
} EnumPinshareInfoPINH7;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x109C
// MCU Ctrl : 0x223C at _PIN_G2_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G2                                 (_PIN_G2_NC)

typedef enum
{
    _PIN_G2_GPI = 0x00,
    _PIN_G2_GPO_PP = 0x01,
    _PIN_G2_GPO_OD = 0x02,
    _PIN_G2_IRDA_IN_0_0 = 0x03,
    _PIN_G2_TCON3 = 0x04,
    _PIN_G2_TEST4B_OUT0 = 0x05,
    _PIN_G2_TEST4B_OUT1 = 0x06,
    _PIN_G2_TEST4B_OUT2 = 0x07,
    _PIN_G2_TEST4B_OUT3 = 0x08,
    _PIN_G2_TEST4B_OUT4 = 0x09,
    _PIN_G2_TEST4B_OUT5 = 0x0A,
    _PIN_G2_TEST4B_OUT6 = 0x0B,
    _PIN_G2_TEST4B_OUT7 = 0x0C,
    _PIN_G2_NC = _PIN_G2_GPO_PP,
} EnumPinshareInfoPING2;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x109D
// MCU Ctrl : 0x223D at _PIN_G3_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_G3                                 (_PIN_G3_NC)

typedef enum
{
    _PIN_G3_GPI = 0x00,
    _PIN_G3_GPO_PP = 0x01,
    _PIN_G3_GPO_OD = 0x02,
    _PIN_G3_TYPEC_GPIO4_1_PP = 0x03,
    _PIN_G3_TYPEC_GPIO4_1_OD = 0x04,
    _PIN_G3_TYPEC_GPIO5_1_PP = 0x05,
    _PIN_G3_TYPEC_GPIO5_1_OD = 0x06,
    _PIN_G3_TCON4 = 0x07,
    _PIN_G3_TEST4B_OUT0 = 0x08,
    _PIN_G3_TEST4B_OUT1 = 0x09,
    _PIN_G3_TEST4B_OUT2 = 0x0A,
    _PIN_G3_TEST4B_OUT3 = 0x0B,
    _PIN_G3_TEST4B_OUT4 = 0x0C,
    _PIN_G3_TEST4B_OUT5 = 0x0D,
    _PIN_G3_TEST4B_OUT6 = 0x0E,
    _PIN_G3_TEST4B_OUT7 = 0x0F,
    _PIN_G3_NC = _PIN_G3_GPO_PP,
} EnumPinshareInfoPING3;

