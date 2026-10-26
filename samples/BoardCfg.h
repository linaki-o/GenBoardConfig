/*
 * BoardCfg.h
 *
 *  Created on: 2020/2/10
 *      Author: nvt02113
 */

#ifndef BOARDCFG_H_
#define BOARDCFG_H_

#include "drv_STBCIO.h"
#include "ModelAppCfgList.h"

//Crystal Clock
#define REF_CLK                 12000000

//Vendor
#define PCB_VENDOR              PCB_TPV

//Combine 8 bits into 1 byte
#define BitsToByte(b7,b6,b5,b4,b3,b2,b1,b0) ((b7<<7)|(b6<<6)|(b5<<5)|(b4<<4)|(b3<<3)|(b2<<2)|(b1<<1)|b0)

//Mcu I/O port default output         bit:   7     6     5     4     3     2     1     0
#define PORT_A_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH,  LOW)
#define PORT_B_DEFAULT_OUT     BitsToByte(HIGH,  LOW, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_C_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH,  LOW,  LOW, HIGH)
#define PORT_D_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_E_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_F_DEFAULT_OUT     BitsToByte( LOW, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_G_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_H_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_I_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_J_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_K_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH,  LOW, HIGH, LOW, LOW, HIGH)
#define PORT_L_DEFAULT_OUT     BitsToByte(HIGH,  LOW, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_M_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_N_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_Q_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_R_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)
#define PORT_S_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH)


//Mcu I/O port default direction    bit:    7    6    5    4    3    2    1    0
#define PORT_A_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, IN, OUT,  IN,  IN)
#define PORT_B_DEFAULT_DIR     BitsToByte( IN, OUT,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_C_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN,  IN, OUT, OUT,  IN)
#define PORT_D_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, OUT, OUT, OUT,  IN)
#define PORT_E_DEFAULT_DIR     BitsToByte( IN, IN, OUT,  IN, OUT, OUT, OUT,  IN)
#define PORT_F_DEFAULT_DIR     BitsToByte(OUT,  IN,  IN,  IN, IN, IN,  IN, OUT)
#define PORT_G_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_H_DEFAULT_DIR     BitsToByte(OUT,  IN, OUT,  IN, OUT,  IN, OUT,  IN)
#define PORT_I_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_J_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_K_DEFAULT_DIR     BitsToByte( IN,  IN,  IN, IN,  IN,  OUT, OUT, IN)
#define PORT_L_DEFAULT_DIR     BitsToByte(IN, IN,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_M_DEFAULT_DIR     BitsToByte(IN, IN,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_N_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_Q_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_R_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN,  IN,  IN,  IN,  IN)
#define PORT_S_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN,  IN,  IN,  IN,  IN)


// Push-Pull : 1 / Open-Drain : 0
//Mcu I/O port Push-Pull Configuration bit: 7     6     5     4     3     2     1     0
#define PORT_A_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW, HIGH,  LOW,  LOW,  LOW)
#define PORT_B_DEFAULT_PP     BitsToByte( LOW, HIGH,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_C_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW, HIGH, HIGH,  LOW)
#define PORT_D_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_E_DEFAULT_PP     BitsToByte( LOW, HIGH,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_F_DEFAULT_PP     BitsToByte(HIGH,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_G_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_H_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_I_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_J_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_K_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  HIGH, HIGH,  LOW)
#define PORT_L_DEFAULT_PP     BitsToByte(HIGH, HIGH,  LOW,  LOW,  LOW,  LOW,  LOW, LOW)
#define PORT_M_DEFAULT_PP     BitsToByte(LOW, LOW, HIGH,  LOW, HIGH, HIGH,  LOW,  LOW)
#define PORT_N_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_Q_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_R_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_S_DEFAULT_PP     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)

// Pull-Hight : 1 / Non-Pull-High : 0
//Mcu I/O port Pull-Up Configuration   bit:   7     6     5     4     3     2     1     0
#define PORT_A_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_B_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_C_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_D_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_E_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_F_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_G_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_H_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_I_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_J_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_K_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_L_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_M_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_N_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_Q_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_R_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_S_DEFAULT_PU     BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)

//Each bit indicates one ADC channel,      ADC7  ADC6  ADC5  ADC4  ADC3  ADC2  ADC1  ADC0
#define STBC_ADC_CON_DEFAULT    BitsToByte( LOW,  LOW,  LOW,  LOW, HIGH, HIGH,  LOW,  LOW)

//Each bit indicates one DDCCI channel,    NONE  NONE  IIC5  IIC4  IIC3  IIC2  IIC1  IIC0
#define STBC_DDCCI_CON_DEFAULT  BitsToByte( LOW,  HIGH, LOW,  LOW,  LOW, LOW, HIGH, HIGH)
#define STBC_IIC_ADDRESS        0x6E
#define STBC_SCDC_ADDRESS       0xA8
#define EEDID_CS0_PORT          STBC_PORT_NULL
#define EEDID_CS0_BIT           BIT5
#define EEDID_CS0_ACTIVE        HIGH
#define EEDID_CS1_PORT          STBC_PORT_NULL
#define EEDID_CS1_BIT           BIT4
#define EEDID_CS1_ACTIVE        HIGH
//--------------------------------------------------------------------------------//
//                      EDID
//--------------------------------------------------------------------------------//
#define EEPageWriteUnit         8 // 8 or 16 by eeprom
#define EEWriteRetryCnt         1

//--------------------------------------------------------------------------------//
//                      RX Port Information
//--------------------------------------------------------------------------------//
// VGA
#define VGA_PORT_TYPE           VGA_PORT
#define VGA_DDCIIC_CH           0x0F
#define VGA_CABLE_PORT          STBC_PORT_NULL
#define VGA_CABLE_BIT           BIT4
#define VGA_CABLE_ACTIVE        LOW
#define VGA_HPD_PORT            STBC_PORT_NULL
#define VGA_HPD_BIT             BIT0
#define VGA_HPD_ACTIVE          HIGH
#define VGA_ZP_DET_TIMER        1
#define VGA_EDID_EN             DISABLE
#define VGA_EDID_MAXLEN         128
#define VGA_EDID_ADDR           0x0600  // 0xFE00
#define VGA_EDID_WP_PORT        STBC_PORT_NULL
#define VGA_EDID_WP_BIT         BIT7
#define VGA_EDID_WP_ACTIVE      HIGH

// Digital Interface 0
#define DIG0_PORT_TYPE          HDMI_PORT
#define DIG0_DDCIIC_CH          0
#define DIG0_CABLE_PORT         STBC_PORT_C//HDMI1_DET
#define DIG0_CABLE_BIT          BIT7
#define DIG0_CABLE_ACTIVE       LOW
#define DIG0_HPD_PORT           STBC_PORT_E//HDMI1_HPD
#define DIG0_HPD_BIT            BIT5
#define DIG0_HPD_ACTIVE         LOW
#define DIG0_ZP_DET_TIMER       1
#define DIG0_EDID_EN            ENABLE
#define DIG0_EDID_MAXLEN        384
#define DIG0_EDID_ADDR          0x0000
#define DIG0_EDID_WP_PORT       STBC_PORT_NULL//STBC_PORT_C
#define DIG0_EDID_WP_BIT        BIT1
#define DIG0_EDID_WP_ACTIVE     HIGH
// -------- HDMI PORT ONLY --------
#if DIG0_PORT_TYPE == HDMI_PORT
#define DIG0_DPMS_SCDC_CH       0x0F
#define DIG0_CABLE5V_PORT       STBC_PORT_C//STBC_PORT_D
#define DIG0_CABLE5V_PIN        BIT6
#define DIG0_CABLE5V_ACTIVE     HIGH
#else
// -------- DP PORT ONLY --------
#define DIG0_PLUG_ADC           STBC_ADC_NULL
#define DIG0_LANE0              DP_ML_LANE0
#define DIG0_LANE1              DP_ML_LANE1
#define DIG0_LANE2              DP_ML_LANE2
#define DIG0_LANE3              DP_ML_LANE3
#define DIG0_LANE0_PN_SWAP      FALSE
#define DIG0_LANE1_PN_SWAP      FALSE
#define DIG0_LANE2_PN_SWAP      FALSE
#define DIG0_LANE3_PN_SWAP      FALSE
#define DIG0_AUX_PN_SWAP        FALSE
#define DIG0_USBCC_ACTIVE       FALSE
#endif

// Digital Interface 1
#define DIG1_PORT_TYPE          DP_PORT
#define DIG1_DDCIIC_CH          1  // set a unused ddc channel when port type is DP
#define DIG1_CABLE_PORT         STBC_PORT_B//DP_DET
#define DIG1_CABLE_BIT          BIT7
#define DIG1_CABLE_ACTIVE       LOW
#define DIG1_HPD_PORT           STBC_PORT_B//DP_HPD
#define DIG1_HPD_BIT            BIT6
#define DIG1_HPD_ACTIVE         HIGH
#define DIG1_ZP_DET_TIMER       1
#define DIG1_EDID_EN            ENABLE
#define DIG1_EDID_MAXLEN        384
#define DIG1_EDID_ADDR          0x0600
#define DIG1_EDID_WP_PORT       STBC_PORT_NULL
#define DIG1_EDID_WP_BIT        BIT7
#define DIG1_EDID_WP_ACTIVE     HIGH
// -------- HDMI PORT ONLY --------
#if DIG1_PORT_TYPE == HDMI_PORT
#define DIG1_DPMS_SCDC_CH       5
#define DIG1_CABLE5V_PORT       STBC_PORT_NULL
#define DIG1_CABLE5V_PIN        BIT2
#define DIG1_CABLE5V_ACTIVE     HIGH
#else
// -------- DP PORT ONLY --------
#define DIG1_PLUG_ADC           STBC_ADC_4
#define DIG1_LANE0              DP_ML_LANE0
#define DIG1_LANE1              DP_ML_LANE1
#define DIG1_LANE2              DP_ML_LANE2
#define DIG1_LANE3              DP_ML_LANE3
#define DIG1_LANE0_PN_SWAP      TRUE
#define DIG1_LANE1_PN_SWAP      FALSE
#define DIG1_LANE2_PN_SWAP      FALSE
#define DIG1_LANE3_PN_SWAP      FALSE
#define DIG1_AUX_PN_SWAP        FALSE
#define DIG1_USBCC_ACTIVE       FALSE
#endif

// Digital Interface 2
#define DIG2_PORT_TYPE          DP_PORT //TYPEC
#define DIG2_DDCIIC_CH          0x0F	// set a unused ddc channel when port type is DP
#define DIG2_CABLE_PORT         STBC_PORT_NULL //DET_TYPEC
#define DIG2_CABLE_BIT          BIT4
#define DIG2_CABLE_ACTIVE       LOW
#define DIG2_HPD_PORT           STBC_PORT_NULL //DPALT_HPD
#define DIG2_HPD_BIT            BIT6
#define DIG2_HPD_ACTIVE         HIGH
#define DIG2_ZP_DET_TIMER       1
#define DIG2_EDID_EN            DISABLE
#define DIG2_EDID_MAXLEN        384
#define DIG2_EDID_ADDR          0x0600
#define DIG2_EDID_WP_PORT       STBC_PORT_NULL
#define DIG2_EDID_WP_BIT        BIT6
#define DIG2_EDID_WP_ACTIVE     HIGH
// -------- HDMI PORT ONLY --------
#if DIG2_PORT_TYPE == HDMI_PORT
#define DIG2_DPMS_SCDC_CH       0x0F
#define DIG2_CABLE5V_PORT       STBC_PORT_NULL
#define DIG2_CABLE5V_PIN        BIT4
#define DIG2_CABLE5V_ACTIVE     HIGH
#else
// -------- DP PORT ONLY --------
#define DIG2_PLUG_ADC           STBC_ADC_NULL //SMARTPD_ALT
#define DIG2_LANE0              DP_ML_LANE3
#define DIG2_LANE1              DP_ML_LANE2
#define DIG2_LANE2              DP_ML_LANE1
#define DIG2_LANE3              DP_ML_LANE0
#define DIG2_LANE0_PN_SWAP      TRUE
#define DIG2_LANE1_PN_SWAP      TRUE
#define DIG2_LANE2_PN_SWAP      TRUE
#define DIG2_LANE3_PN_SWAP      TRUE
#define DIG2_AUX_PN_SWAP        FALSE
#define DIG2_USBCC_ACTIVE       FALSE
#endif

// Digital Interface 3
#define DIG3_PORT_TYPE          HDMI_PORT
#define DIG3_DDCIIC_CH          0x0F
#define DIG3_CABLE_PORT         STBC_PORT_NULL //HDMI2_DET
#define DIG3_CABLE_BIT          BIT1
#define DIG3_CABLE_ACTIVE       LOW
#define DIG3_HPD_PORT           STBC_PORT_NULL //HDMI2_HPD
#define DIG3_HPD_BIT            BIT4
#define DIG3_HPD_ACTIVE         LOW
#define DIG3_ZP_DET_TIMER       1
#define DIG3_EDID_EN            ENABLE
#define DIG3_EDID_MAXLEN        384
#define DIG3_EDID_ADDR          0x0200
#define DIG3_EDID_WP_PORT       STBC_PORT_NULL
#define DIG3_EDID_WP_BIT        BIT1
#define DIG3_EDID_WP_ACTIVE     HIGH
// -------- HDMI PORT ONLY --------
#if DIG3_PORT_TYPE == HDMI_PORT
#define DIG3_DPMS_SCDC_CH       0x0F
#define DIG3_CABLE5V_PORT       STBC_PORT_NULL
#define DIG3_CABLE5V_PIN        BIT0
#define DIG3_CABLE5V_ACTIVE     HIGH
#else
// -------- DP PORT ONLY --------
#define DIG3_PLUG_ADC           STBC_ADC_NULL
#define DIG3_LANE0              DP_ML_LANE0
#define DIG3_LANE1              DP_ML_LANE1
#define DIG3_LANE2              DP_ML_LANE2
#define DIG3_LANE3              DP_ML_LANE3
#define DIG3_LANE0_PN_SWAP      FALSE
#define DIG3_LANE1_PN_SWAP      FALSE
#define DIG3_LANE2_PN_SWAP      FALSE
#define DIG3_LANE3_PN_SWAP      FALSE
#define DIG3_AUX_PN_SWAP        FALSE
#define DIG3_USBCC_ACTIVE       FALSE
#endif

// Digital Interface 4
#define DIG4_PORT_TYPE          DP_PORT
#define DIG4_DDCIIC_CH          0x0F
#define DIG4_CABLE_PORT         STBC_PORT_NULL
#define DIG4_CABLE_BIT          BIT5
#define DIG4_CABLE_ACTIVE       LOW
#define DIG4_HPD_PORT           STBC_PORT_NULL
#define DIG4_HPD_BIT            BIT1
#define DIG4_HPD_ACTIVE         HIGH
#define DIG4_ZP_DET_TIMER       1
#define DIG4_EDID_EN            DISABLE
#define DIG4_EDID_MAXLEN        384
#define DIG4_EDID_ADDR          0x0000
#define DIG4_EDID_WP_PORT       STBC_PORT_NULL
#define DIG4_EDID_WP_BIT        BIT6
#define DIG4_EDID_WP_ACTIVE     HIGH
// -------- HDMI PORT ONLY --------
#if DIG4_PORT_TYPE == HDMI_PORT
#define DIG4_DPMS_SCDC_CH       0x0F
#define DIG4_CABLE5V_PORT       STBC_PORT_NULL
#define DIG4_CABLE5V_PIN        BIT2
#define DIG4_CABLE5V_ACTIVE     HIGH
#else
// -------- DP PORT ONLY --------
#define DIG4_PLUG_ADC           STBC_ADC_NULL
#define DIG4_LANE0              DP_ML_LANE3
#define DIG4_LANE1              DP_ML_LANE2
#define DIG4_LANE2              DP_ML_LANE1
#define DIG4_LANE3              DP_ML_LANE0
#define DIG4_LANE0_PN_SWAP      FALSE
#define DIG4_LANE1_PN_SWAP      FALSE
#define DIG4_LANE2_PN_SWAP      FALSE
#define DIG4_LANE3_PN_SWAP      FALSE
#define DIG4_AUX_PN_SWAP        FALSE
#define DIG4_USBCC_ACTIVE       FALSE
#endif

// Digital Interface 5
#define DIG5_PORT_TYPE          DP_PORT
#define DIG5_DDCIIC_CH          0x0F
#define DIG5_CABLE_PORT         STBC_PORT_NULL
#define DIG5_CABLE_BIT          BIT4
#define DIG5_CABLE_ACTIVE       LOW
#define DIG5_HPD_PORT           STBC_PORT_NULL
#define DIG5_HPD_BIT            BIT0
#define DIG5_HPD_ACTIVE         HIGH
#define DIG5_ZP_DET_TIMER       1
#define DIG5_EDID_EN            DISABLE
#define DIG5_EDID_MAXLEN        384
#define DIG5_EDID_ADDR          0x0200
#define DIG5_EDID_WP_PORT       STBC_PORT_NULL
#define DIG5_EDID_WP_BIT        BIT6
#define DIG5_EDID_WP_ACTIVE     HIGH
// -------- HDMI PORT ONLY --------
#if DIG5_PORT_TYPE == HDMI_PORT
#define DIG5_DPMS_SCDC_CH       0x0F
#define DIG5_CABLE5V_PORT       STBC_PORT_NULL
#define DIG5_CABLE5V_PIN        BIT2
#define DIG5_CABLE5V_ACTIVE     HIGH
#else
// -------- DP PORT ONLY --------
#define DIG5_PLUG_ADC           STBC_ADC_NULL
#define DIG5_LANE0              DP_ML_LANE0
#define DIG5_LANE1              DP_ML_LANE1
#define DIG5_LANE2              DP_ML_LANE2
#define DIG5_LANE3              DP_ML_LANE3
#define DIG5_LANE0_PN_SWAP      FALSE
#define DIG5_LANE1_PN_SWAP      FALSE
#define DIG5_LANE2_PN_SWAP      FALSE
#define DIG5_LANE3_PN_SWAP      FALSE
#define DIG5_AUX_PN_SWAP        FALSE
#define DIG5_USBCC_ACTIVE       FALSE
#endif

// VX1 Interface
#define VX1_PORT_TYPE           VX1_PORT
#define VX1_DDCIIC_CH           0x0F
#define VX1_CABLE_PORT          STBC_PORT_NULL
#define VX1_CABLE_BIT           BIT5
#define VX1_CABLE_ACTIVE        LOW
#define VX1_HPD_PORT            STBC_PORT_NULL
#define VX1_HPD_BIT             BIT7
#define VX1_HPD_ACTIVE          HIGH
#define VX1_ZP_DET_TIMER        1
#define VX1_EDID_EN             DISABLE
#define VX1_EDID_MAXLEN         256
#define VX1_EDID_ADDR           0x0100 // 0xF900
#define VX1_EDID_WP_PORT        STBC_PORT_NULL
#define VX1_EDID_WP_BIT         BIT7
#define VX1_EDID_WP_ACTIVE      HIGH
#define VX1_PREEMPAHSIS         PREEMPHASIS_OFF
#define VX1_LEVELSWING          VX1_SWING_900

//--------------------------------------------------------------------------------//
//                      TX HPD
//--------------------------------------------------------------------------------//
#define HDMITX0_HPD_PORT        STBC_PORT_NULL//STBC_PORT_M
#define HDMITX0_HPD_BIT         BIT4
#define HDMITX1_HPD_PORT        STBC_PORT_NULL//STBC_PORT_M
#define HDMITX1_HPD_BIT         BIT5
//--------------------------------------------------------------------------------//
//                      NVRAM configuration
//--------------------------------------------------------------------------------//
#define EEPORM1_SDA_PORT          STBC_PORT_D
#define EEPORM1_SDA_BIT           BIT3
#define EEPORM1_SCL_PORT          STBC_PORT_D
#define EEPORM1_SCL_BIT           BIT2
#define EEPORM1_WP_PORT           STBC_PORT_E
#define EEPORM1_WP_BIT            BIT1
#define EEPORM1_WP_ACTIVE         HIGH
#define EEPROM1_SW_I2C            ON
#define EEPROM1_P3_USE            OFF
#define EEPROM1_SLAVE             0xA0
#define EEPROM1_ADDR_LEN          2
#define EEPROM1_PAGEWRITE_LEN     16 ////

#define EEPORM2_SDA_PORT          STBC_PORT_NULL
#define EEPORM2_SDA_BIT           BIT0
#define EEPORM2_SCL_PORT          STBC_PORT_NULL
#define EEPORM2_SCL_BIT           BIT1
#define EEPORM2_WP_PORT           STBC_PORT_NULL
#define EEPORM2_WP_BIT            BIT0
#define EEPORM2_WP_ACTIVE         HIGH
#define EEPROM2_SW_I2C            ON
#define EEPROM2_P3_USE            OFF
#define EEPROM2_SLAVE             0xA0
#define EEPROM2_ADDR_LEN          2
#define EEPROM2_PAGEWRITE_LEN     16 ////

#define EEPORM3_SDA_PORT          STBC_PORT_NULL
#define EEPORM3_SDA_BIT           BIT0
#define EEPORM3_SCL_PORT          STBC_PORT_NULL
#define EEPORM3_SCL_BIT           BIT1
#define EEPORM3_WP_PORT           STBC_PORT_NULL
#define EEPORM3_WP_BIT            BIT0
#define EEPORM3_WP_ACTIVE         HIGH
#define EEPROM3_SW_I2C            ON
#define EEPROM3_P3_USE            OFF
#define EEPROM3_SLAVE             0xA0
#define EEPROM3_ADDR_LEN          2
#define EEPROM3_PAGEWRITE_LEN     16 ////

//FLASH
#define FLASH_WP_PORT           STBC_PORT_L
#define FLASH_WP_BIT            BIT6
#define FLASH_WP_ACTIVE         LOW

////
//DUALFALSH IO (Select 2nd Flash)
#define DUALFLASH_PORT          STBC_PORT_NULL
#define DUALFLASH_BIT           BIT6
#define DUALFLASH_ACTIVE        LOW
////

//DIM configuration
#define BKL_PDIM_PORT            STBC_PORT_K
#define BKL_PDIM_POL             HIGH
#define BKL_PDIM_OUTPUT_PIN      PSM2_PIN_PK2
#define PDIM_REF_DBC             ON
#define BKL_ADIM_PORT            PWM_B
#define BKL_ADIM_POL             HIGH
#define BKL_ADIM_OUTPUT_PIN      PWMB_PIN_PK1

#define BKL_PWM_PORT            BKL_ADIM_PORT
#define BKL_PWM_POL             BKL_ADIM_POL
#define BKL_PWM_OUTPUT_PIN      BKL_ADIM_OUTPUT_PIN
#define PWM_REF_DBC             ON

//PSM control
#define BFREE_PSM_OUTPUT_PORT   STBC_PORT_K  //BlurFree PSM IO port

#define BFREE_PSM0_PORT         PSM_PORT0  //STBC_PORT_NULL
#define BFREE_PSM0_POL          HIGH
#define BFREE_PSM0_OUTPUT_PIN   PWM_PIN_NULL  //PWM_PIN_NULL
#define BFREE_PSM1_PORT         STBC_PORT_NULL//PSM_PORT1
#define BFREE_PSM1_POL          HIGH
#define BFREE_PSM1_OUTPUT_PIN   PWM_PIN_NULL
#define BFREE_PSM2_PORT         STBC_PORT_NULL//PSM_PORT2
#define BFREE_PSM2_POL          HIGH
#define BFREE_PSM2_OUTPUT_PIN   PSM2_PIN_PK2
#define BFREE_PSM3_PORT         STBC_PORT_NULL//PSM_PORT3
#define BFREE_PSM3_POL          HIGH
#define BFREE_PSM3_OUTPUT_PIN   PWM_PIN_NULL
#define BFREE_PSM4_PORT         STBC_PORT_NULL
#define BFREE_PSM4_POL          HIGH
#define BFREE_PSM4_OUTPUT_PIN   PWM_PIN_NULL
#define BFREE_PSM5_PORT         STBC_PORT_NULL
#define BFREE_PSM5_POL          HIGH
#define BFREE_PSM5_OUTPUT_PIN   PWM_PIN_NULL
#define BFREE_PSM6_PORT         STBC_PORT_NULL
#define BFREE_PSM6_POL          HIGH
#define BFREE_PSM6_OUTPUT_PIN   PWM_PIN_NULL
#define BFREE_PSM7_PORT         STBC_PORT_NULL
#define BFREE_PSM7_POL          HIGH
#define BFREE_PSM7_OUTPUT_PIN   PWM_PIN_NULL

#define MPRT_PORT               STBC_PORT_NULL
#define MPRT_BIT                BIT5
#define MPRT_ACTIVE             HIGH

//Backlight control
#define BACKLIGHT_PORT          STBC_PORT_C//ON_BACKLIGHT
#define BACKLIGHT_BIT           BIT1
#define BACKLIGHT_ACTIVE        HIGH

#define CONVERTER_POWER_PORT    STBC_PORT_NULL
#define CONVERTER_POWER_BIT     BIT4
#define CONVERTER_POWER_ACTIVE  HIGH

//Panel power control
#define PANEL_POWER_PORT        STBC_PORT_C
#define PANEL_POWER_BIT         BIT2
#define PANEL_POWER_ACTIVE      HIGH

// LED driver
#define LDM_HSYNC_PORT          STBC_PORT_NULL
#define LDM_HSYNC_BIT           BIT6
#define LDM_HSYNC_ACTIVE        HIGH

//Audio configuration
#define AUDIO_OUT               (LINE_OUT)
#define LINE_OUT_SWAP           DISABLE
#define AUDIO_IN                (LINE_IN1) //(LINE_IN1/LINE_IN2)
#define ANALOG_AUDIO_GAIN       0x1E

//Volume control
#define VOLUME_PWM_PORT         PWM_D
#define VOLUME_PWM_POL          HIGH
#define VOLUME_PWM_OUTPUT_PIN   PWMD_PIN_PA3
//Audio mute control
#define AMP_MUTE_PORT           STBC_PORT_M
#define AMP_MUTE_BIT            BIT6
#define AMP_MUTE_ACTIVE         HIGH
//Audio power control
#define AMP_PWR_PORT            STBC_PORT_NULL
#define AMP_PWR_BIT             BIT7
#define AMP_PWR_ACTIVE          HIGH

////
#define AMP_SHUTDOWN_PORT       STBC_PORT_M
#define AMP_SHUTDOWN_BIT        BIT7
#define AMP_SHUTDOWN_ACTIVE     LOW


//Codec reset
#define CODEC_RESET_PORT        STBC_PORT_NULL
#define CODEC_RESET_BIT         BIT2
#define CODEC_RESET_ACTIVE      LOW


// headphone detect (is done by amp)
#define HP_DET_PORT             STBC_PORT_B
#define HP_DET_BIT              BIT0
#define HP_DET_ACTIVE           HIGH
// headphone audio mute control (for de-pop circuit only, always high when monitor is on)
#define HP_MUTE_PORT            STBC_PORT_NULL
#define HP_MUTE_BIT             BIT7
#define HP_MUTE_ACTIVE          LOW
// headphone audio power control (no independent power control)
#define HP_PWR_PORT             STBC_PORT_NULL
#define HP_PWR_BIT              BIT1
#define HP_PWR_ACTIVE           HIGH
////

// Type c VIA Pin define
//V103_CC_IND
#define TYPEC_CC_INDICATE_PORT        STBC_PORT_NULL
#define TYPEC_CC_INDICATE_BIT         BIT2
#define TYPEC_CC_INDICATE_ACTIVE      HIGH

////
#define USB_2L_4L_PORT              STBC_PORT_NULL
#define USB_2L_4L_BIT               BIT1
#define USB_2L_4L_ACTIVE            HIGH

#define USB_VBUS_INFORM_PORT        STBC_PORT_NULL
#define USB_VBUS_INFORM_BIT         BIT3
#define USB_VBUS_INFORM_ACTIVE      HIGH
////

//USB Conrol
//USB Conrol
// Type B cable detect
#define USB_DET_PORT            STBC_PORT_C
#define USB_DET_BIT             BIT0
#define USB_DET_ACTIVE          LOW

// Type C cable detect
#define USBCG1_DET_PORT         STBC_PORT_C
#define USBCG1_DET_BIT          BIT2
#define USBCG1_DET_ACTIVE       LOW

#define USB_POWER_PORT          STBC_PORT_F
#define USB_POWER_BIT           BIT7
#define USB_POWER_ACTIVE        HIGH

#define USB_MODE_SEL_PORT   STBC_PORT_NULL
#define USB_MODE_SEL_BIT    BIT3
#define USB_MODE_SEL_ACTIVE HIGH

////
#define VL103_POWER_PORT        STBC_PORT_NULL
#define VL103_POWER_BIT         BIT1
#define VL103_POWER_ACTIVE      HIGH
////

//V103_SCL
#define TYPEC_GPIO6_PORT        STBC_PORT_NULL
#define TYPEC_GPIO6_BIT         BIT7
#define TYPEC_GPIO6_ACTIVE      HIGH

//V103_PIN_ASSIGN1
#define TYPEC_GPIO9_PORT        STBC_PORT_NULL
#define TYPEC_GPIO9_BIT         BIT3
#define TYPEC_GPIO9_ACTIVE      HIGH

//V103_PIN_ASSIGN2
#define TYPEC_GPIO2_PORT        STBC_PORT_NULL
#define TYPEC_GPIO2_BIT         BIT2
#define TYPEC_GPIO2_ACTIVE      HIGH

//V103_PIN_ASSIGN3
#define TYPEC_GPIO3_PORT        STBC_PORT_NULL
#define TYPEC_GPIO3_BIT         BIT1
#define TYPEC_GPIO3_ACTIVE      HIGH

//V103 IRQ
#define TYPEC_GPIO11_PORT       STBC_PORT_NULL
#define TYPEC_GPIO11_BIT        BIT0
#define TYPEC_GPIO11_ACTIVE     HIGH

#define TYPEC_POWER_PORT        STBC_PORT_NULL
#define TYPEC_POWER_BIT         BIT2
#define TYPEC_POWER_ACTIVE      HIGH

////
//V103_RESERVED1 for informing pin E or not, high means pin E
#define TYPEC_PIN_E_PORT        STBC_PORT_NULL
#define TYPEC_PIN_E_BIT         BIT5
#define TYPEC_PIN_E_ACTIVE      HIGH

// HIGH: address A0, LOW: Address A2
#define HDMI2_EDID_EEPROM_ADDR_SEL_PORT     STBC_PORT_NULL
#define HDMI2_EDID_EEPROM_ADDR_SEL_BIT      BIT0
#define HDMI2_EDID_EEPROM_ADDR_SEL_ACTIVE   HIGH

#define HDMI3_EDID_EEPROM_ADDR_SEL_PORT     STBC_PORT_NULL
#define HDMI3_EDID_EEPROM_ADDR_SEL_BIT      BIT1
#define HDMI3_EDID_EEPROM_ADDR_SEL_ACTIVE   HIGH
////

//#define USB_5V_G1_PORT          MCU_PORT_K
//#define USB_5V_G1_BIT           BIT2
//#define USB_5V_G1_ACTIVE        HIGH

//#define USB_12V_QC_PORT         MCU_PORT_K
//#define USB_12V_QC_BIT          BIT3
//#define USB_12V_QC_ACTIVE       HIGH

#define NUVOTON_POWER_PORT      STBC_PORT_NULL
#define NUVOTON_POWER_BIT       BIT2
#define NUVOTON_POWER_ACTIVE    HIGH

#define USB_SCALAR_ALERT_PORT   STBC_PORT_NULL
#define USB_SCALAR_ALERT_BIT    BIT7
#define USB_SCALAR_ALERT_ACTIVE HIGH



#define USB_VBUSDET_1_PORT   STBC_PORT_NULL
#define USB_VBUSDET_1_BIT    BIT0
#define USB_VBUSDET_1_ACTIVE HIGH

//DPTX swap
// Enable Configure :
//      TWO TCON :
//          EDP_PORT_SEL : 0 , EDP0_EN : TRUE , EDP1_EN : TRUE , EDP2_EN : FALSE , EDP3_EN : FALSE
//          EDP_PORT_SEL : 1 , EDP0_EN : FALSE , EDP1_EN : TRUE , EDP2_EN : TRUE , EDP3_EN : FALSE
//      TWO TCON + Repeat :
//          EDP_PORT_SEL : 0 , EDP0_EN : TRUE, EDP1_EN : TRUE , EDP2_EN : TRUE , EDP3_EN : TRUE
//      FOUR TCON :
//          EDP_PORT_SEL : X , EDP0_EN : TRUE, EDP1_EN : TRUE , EDP2_EN : TRUE , EDP3_EN : TRUE
// Lane Swap Configure :
//      0x00 : 0 1 2 3
//      0x40 : 2 3 0 1
//      0x80 : 1 0 3 2
//      0xC0 : 3 2 1 0
#define EDP0_PN_SWAP            0
#define EDP0_LANE_SWAP          0x00//0x00, 0x40, 0x80, 0xC0
#define EDP0_LANE0_SWING_OFFSET	0x00
#define EDP0_LANE0_PREM_OFFSET	0x00
#define EDP0_LANE1_SWING_OFFSET	0x00
#define EDP0_LANE1_PREM_OFFSET	0x00
#define EDP0_LANE2_SWING_OFFSET	0x00
#define EDP0_LANE2_PREM_OFFSET	0x00
#define EDP0_LANE3_SWING_OFFSET	0x00
#define EDP0_LANE3_PREM_OFFSET	0x00
#define EDP0_EN                 FALSE

#define EDP1_PN_SWAP            0
#define EDP1_LANE_SWAP          0x00//0x00, 0x40, 0x80, 0xC0
#define EDP1_LANE0_SWING_OFFSET	0x00
#define EDP1_LANE0_PREM_OFFSET	0x00
#define EDP1_LANE1_SWING_OFFSET	0x00
#define EDP1_LANE1_PREM_OFFSET	0x00
#define EDP1_LANE2_SWING_OFFSET	0x00
#define EDP1_LANE2_PREM_OFFSET	0x00
#define EDP1_LANE3_SWING_OFFSET	0x00
#define EDP1_LANE3_PREM_OFFSET	0x00
#define EDP1_EN                 FALSE

#define EDP2_PN_SWAP            0
#define EDP2_LANE_SWAP          0x00//0x00, 0x40, 0x80, 0xC0
#define EDP2_LANE0_SWING_OFFSET	0x00
#define EDP2_LANE0_PREM_OFFSET	0x00
#define EDP2_LANE1_SWING_OFFSET	0x00
#define EDP2_LANE1_PREM_OFFSET	0x00
#define EDP2_LANE2_SWING_OFFSET	0x00
#define EDP2_LANE2_PREM_OFFSET	0x00
#define EDP2_LANE3_SWING_OFFSET	0x00
#define EDP2_LANE3_PREM_OFFSET	0x00
#define EDP2_EN                 FALSE//TRUE

#define EDP3_PN_SWAP            0
#define EDP3_LANE_SWAP          0xC0//0x00, 0x40, 0x80, 0xC0
#define EDP3_LANE0_SWING_OFFSET	0x00
#define EDP3_LANE0_PREM_OFFSET	0x00
#define EDP3_LANE1_SWING_OFFSET	0x00
#define EDP3_LANE1_PREM_OFFSET	0x00
#define EDP3_LANE2_SWING_OFFSET	0x00
#define EDP3_LANE2_PREM_OFFSET	0x00
#define EDP3_LANE3_SWING_OFFSET	0x00
#define EDP3_LANE3_PREM_OFFSET	0x00
#define EDP3_EN                 FALSE//TRUE
#define DAISY_PN_SWAP           0
#define DAISY_LANE_SWAP         0x00//0x00, 0x40, 0x80, 0xC0

#define EDP_DUAL_PORT_SWAP      OFF // Andy for edp panel swap
#define EDP_PORT_SEL            0 // 0 : AB , 1 : BC 

#if (EDP0_EN || EDP1_EN || EDP2_EN || EDP3_EN)
#define ENABLE_EDP ON
#else
#define ENABLE_EDP OFF
#endif

#define EDP_HPD_CH_SEL          0xE4
//[1:0] eDP ch0: 2'b00: ch0, 2'b01: ch1, 2'b10: ch2, 2'b11: ch3,
//[3:2] eDP ch1: 2'b00: ch0, 2'b01: ch1, 2'b10: ch2, 2'b11: ch3,
//[5:4] eDP ch2: 2'b00: ch0, 2'b01: ch1, 2'b10: ch2, 2'b11: ch3,
//[7:6] eDP ch3: 2'b00: ch0, 2'b01: ch1, 2'b10: ch2, 2'b11: ch3,
#define EDP_SSC_ON              TRUE //0.2%
#if DISP_PANEL == TPV_TPM340Y1_SNFU02_310F_3440X1440_VX1_8L ||DISP_PANEL == TPV_TPM340Y1_SNFU02_310J_3440X1440_VX1_8L || DISP_PANEL == TPV_TPM340Y1_SNFU03_510B_3440X1440_LVDS_4P 
#define EDP_HPD_IO_SEL          FALSE//for 300 series combo io select
#elif DISP_PANEL == TPV_TPM270WQ1_KCAD9BN_C1D_2560X1440_eDP_4P||  DISP_PANEL ==TPV_TPM340Y1_SG2H03_16AF_3440X1440_eDP_8P ||  DISP_PANEL ==TPV_TPM340Y1_VWBCF1K_T8P0A_TWP0A_3440X1440_eDP_8P
#define EDP_HPD_IO_SEL          FALSE//for 300 series combo io select
#else
#error "Add support panel to 715GE336 BoardCfg.h"
#endif

//#define DAISY_PN_SWAP           1
//#define DAISY_LANE_SWAP         0xC0//0x00, 0x40, 0x80, 0xC0

//LVDS swap
#define LVDS_AB_CD_SWAP         0//1

////add this to pass build
// Control 0x3B79[4:2], Port A/B/C/D swap, for 4 port configure only
//000 = ABCD ( 0,1,2,3 )
//001 = ACBD ( 0,2,1,3 )
//010 = DCBA ( 3,2,1,0 )
//011 = DBCA ( 3,1,2,0 )
//100 = CDAB ( 2,3,0,1 )
//101 = BDAC ( 1,3,0,2 )
//110 = BADC ( 1,0,3,2 )
//111 = CADB ( 2,0,3,1 )
#define PANEL_FOUR_PORT_SWAP    0 //Port A/B/C/D swap ( pixel swap )
////

//VX1 swap
#define VX1_PORT_SWAP           0//0,1,2
//2b00/11: Port_V0; Port_V1; Port_V2; Port_V3 (Normal)
//2b01: Port_V1; Port_V0; Port_V3; Port_V2
//2b10: Port_V3; Port_V2; Port_V1; Port_V0
#define VX1_LANE_SWAP           0//0x00 ~ 0xFF
//[7:6]=port V3, [5:4]=port V2, [3:2]=port V1, [1:0]=port V0
//2b00: 0123-4567 (Normal)
//2b01: 1032-5476
//2b10: 3210-7654
//2b11: 7654-3210
#define VX1_PN_SWAP             0xFF//0x00 ~ 0xFF
//0x7200[5] 1:Swap , (Index 0x72EE=0xFF to control all lanes,0x01=lane0~3, 0x02=lane4~7, 0x80=lane28~31)
#define VX1_PORT_2HPD			0 // 1
//PL5_lockn, PL4_htpdn for lane 0~15,  PN7_lockn, PN6_htpdn for lane 16~32

//USB TYPEC VBUS ADC
#define CC_VBUS_ADC             STBC_ADC_NULL
//USB TYPEC VBUS
#define USB_VBUS_PORT           STBC_PORT_NULL//STBC_PORT_K
#define USB_VBUS_BIT            BIT0
#define USB_VBUS_ACTIVE         HIGH
//USB TYPEC UD swap
#define USB_UDSWAP_PORT         STBC_PORT_NULL
#define USB_UDSWAP_BIT          BIT5
#define USB_UDSWAP_ACTIVE       LOW
//USB TYPEC VCONN1 control
#define USB_VCONN1_CTRL_PORT    STBC_PORT_NULL
#define USB_VCONN1_CTRL_BIT     BIT2
#define USB_VCONN1_CTRL_ACTIVE  HIGH
//USB TYPEC VCONN2 control
#define USB_VCONN2_CTRL_PORT    STBC_PORT_NULL
#define USB_VCONN2_CTRL_BIT     BIT3
#define USB_VCONN2_CTRL_ACTIVE  HIGH
//USB TYPEC VBUS 5V->9V
#define USB_9V_SEL_PORT	        STBC_PORT_NULL//STBC_PORT_A
#define USB_9V_SEL_BIT          BIT3
#define USB_9V_SEL_ACTIVE       HIGH
//USB TYPEC VBUS 5V->12V
#define USB_12V_SEL_PORT        STBC_PORT_NULL
#define USB_12V_SEL_BIT         BIT2
#define USB_12V_SEL_ACTIVE      HIGH
//USB TYPEC VBUS 5V->15V
#define USB_15V_SEL_PORT	    STBC_PORT_NULL
#define USB_15V_SEL_BIT         BIT1
#define USB_15V_SEL_ACTIVE      HIGH
//USB TYPEC VBUS 5V->20V
#define USB_20V_SEL_PORT	    STBC_PORT_NULL
#define USB_20V_SEL_BIT         BIT0
#define USB_20V_SEL_ACTIVE      HIGH
//USB TYPEC DL switch
#define USB_DL_SW_PORT          STBC_PORT_NULL//STBC_PORT_K
#define USB_DL_SW_BIT           BIT1
#define USB_DL_SW_ACTIVE        HIGH

#define USB_VCONN_CC1_PORT      STBC_PORT_NULL
#define USB_VCONN_CC1_BIT       BIT3
#define USB_VCONN_CC1_ACTIVE    LOW

#define USB_VCONN_CC2_PORT      STBC_PORT_NULL
#define USB_VCONN_CC2_BIT       BIT2
#define USB_VCONN_CC2_ACTIVE    LOW

#define USB_VBUS_DET_PORT       STBC_PORT_NULL//STBC_PORT_B
#define USB_VBUS_DET_BIT        BIT0
#define USB_VBUS_DET_ACTIVE     HIGH

#define USB_AUXPNSWAPEN		FALSE
#define USB_PINASSIGN1_PORT	    STBC_PORT_NULL
#define USB_PINASSIGN1_PIN		BIT0
#define USB_PINASSIGN2_PORT	    STBC_PORT_NULL
#define USB_PINASSIGN2_PIN		BIT0
#define USB_PINASSIGNC_VAL		0x00	// USB_PINASSIGN1_PORT : LOW , USB_PINASSIGN2_PORT : LOW
#define USB_PINASSIGND_VAL		0x02	// USB_PINASSIGN1_PORT : LOW , USB_PINASSIGN2_PORT : HIGH
#define USB_PINASSIGNE_VAL      0x01	// USB_PINASSIGN1_PORT : HIGH  , USB_PINASSIGN2_PORT : LOW
#define USB_PLUGTYPE_DET_PORT	STBC_PORT_NULL
#define USB_PLUGTYPE_DET_BIT	BIT0
#define USB_PLUGTYPE_DET_ACTIVE HIGH		// Nornal Plug

//Panel power extra delay (This is an extra delay according to the PCB)
#if (DISP_PANEL == TPV_TPM340Y1_SNFU03_510B_3440X1440_LVDS_4P)
#define PANEL_POWER_DELAY       0//200  EDP delay to training
#else
#define PANEL_POWER_DELAY       200//200  EDP delay to training
#endif

//CEC Channel
#define HDMI_CEC_CHANNEL        0   // PC0:CEC0; PC3:CEC1

//LED green control
#define LED_GREEN_PORT          STBC_PORT_E
#define LED_GREEN_BIT           BIT3
#define LED_GREEN_ACTIVE        LOW
//LED red control
#define LED_RED_PORT            STBC_PORT_E
#define LED_RED_BIT             BIT2
#define LED_RED_ACTIVE          LOW

//LED BAR control
#define LED_BAR_PORT            STBC_PORT_NULL
#define LED_BAR_BIT             BIT1
#define LED_BAR_ACTIVE          HIGH

//ANC control
#define ANC_PORT                STBC_PORT_NULL
#define ANC_BIT                 BIT1
#define ANC_ACTIVE              LOW

////
#define SENSOR_POWER_PORT       STBC_PORT_NULL
#define SENSOR_POWER_BIT        BIT0
#define SENSOR_POWER_ACTIVE     HIGH
////

// DP cable power control
#define DP0_PS_CTRL_PORT		STBC_PORT_NULL
#define DP0_PS_CTRL_BIT         BIT7
#define DP0_PS_CTRL_ACTIVE      HIGH

////
// RogerKao breathing LED
#define BREATHING_LED_GREEN_PWM_PORT        PWM_D
#define BREATHING_LED_GREEN_STB_PWM_PORT    STBC_PWMD
#define BREATHING_LED_GREEN_PWM_OUT_PIN     PWMD_PIN_PE3
#define BREATHING_LED_GREEN_PWM_POL         LOW
#define BREATHING_LED_GREEN_PWM_GPIO_PORT   STBC_PORT_E
#define BREATHING_LED_GREEN_PWM_GPIO_PIN    BIT3

#define BREATHING_LED_RED_PWM_PORT          PWM_C
#define BREATHING_LED_RED_STB_PWM_PORT      STBC_PWMC
#define BREATHING_LED_RED_PWM_OUT_PIN       PWMC_PIN_PE2
#define BREATHING_LED_RED_PWM_POL           LOW
#define BREATHING_LED_RED_PWM_GPIO_PORT     STBC_PORT_E
#define BREATHING_LED_RED_PWM_GPIO_PIN      BIT2
////

// PWM power down config, if PWM is used for LED indicator, don't power down
#define PWMA_DPMS_POWERDOWN     TRUE
#define PWMB_DPMS_POWERDOWN     TRUE
#define PWMC_DPMS_POWERDOWN     FALSE
#define PWMD_DPMS_POWERDOWN     FALSE
#define PWME_DPMS_POWERDOWN     TRUE
#define PWMF_DPMS_POWERDOWN     TRUE

#define PWMA_DCOFF_POWERDOWN    TRUE
#define PWMB_DCOFF_POWERDOWN    TRUE
#define PWMC_DCOFF_POWERDOWN    TRUE
#define PWMD_DCOFF_POWERDOWN    TRUE
#define PWME_DCOFF_POWERDOWN    TRUE
#define PWMF_DCOFF_POWERDOWN    TRUE

#define FLASH_SIZE              8388608    // 4MB

/*******************************************************************************
               Ambient light LED
*******************************************************************************/
#define AMBIENT_LED_R_PWM_PORT         PWM_NULL
#define AMBIENT_LED_R_PWM_POL          HIGH
#define AMBIENT_LED_R_PWM_OUTPUT_PIN   PWM_PIN_NULL

#define AMBIENT_LED_G_PWM_PORT         PWM_NULL
#define AMBIENT_LED_G_PWM_POL          HIGH
#define AMBIENT_LED_G_PWM_OUTPUT_PIN   PWM_PIN_NULL

#define AMBIENT_LED_B_PWM_PORT         PWM_NULL
#define AMBIENT_LED_B_PWM_POL          HIGH
#define AMBIENT_LED_B_PWM_OUTPUT_PIN   PWM_PIN_NULL

/*******************************************************************************
               HDCP-related and digital(HDMI) interface Setting
*******************************************************************************/
//HDCP MUX
#define DIGITAL_INPUT0_HDCP_MUX 0 //TMDS PHY1
#define DIGITAL_INPUT1_HDCP_MUX 1 //TMDS PHY2
#define DIGITAL_INPUT2_HDCP_MUX 2 //TMDS PHY3
#define DIGITAL_INPUT3_HDCP_MUX 3 //TMDS PHY3

/*******************************************************************************
                           Keypad interface setting
*******************************************************************************/
// Specific IR port of IR Key
#define IR_PORT                 STBC_INTE_NULL
// Specific AD port of AD key
#define KEY_GROUP1_ADC          STBC_ADC_2
#define KEY_GROUP2_ADC          STBC_ADC_3

// Specific IO port of IO key
#define IOBTN_1_PORT            STBC_PORT_D
#define IOBTN_1_BIT             BIT0
#define IOBTN_1_ACTIVE          LOW
#define IOBTN_2_PORT            STBC_PORT_NULL
#define IOBTN_2_BIT             BIT1
#define IOBTN_2_ACTIVE          LOW
#define IOBTN_3_PORT            STBC_PORT_NULL
#define IOBTN_3_BIT             BIT2
#define IOBTN_3_ACTIVE          LOW
#define IOBTN_4_PORT            STBC_PORT_NULL
#define IOBTN_4_BIT             BIT3
#define IOBTN_4_ACTIVE          LOW
#define IOBTN_5_PORT            STBC_PORT_NULL
#define IOBTN_5_BIT             BIT0
#define IOBTN_5_ACTIVE          LOW
#define IOBTN_6_PORT            STBC_PORT_NULL
#define IOBTN_6_BIT             BIT1
#define IOBTN_6_ACTIVE          LOW
#define IOBTN_7_PORT            STBC_PORT_NULL
#define IOBTN_7_BIT             BIT2
#define IOBTN_7_ACTIVE          LOW
#define IOBTN_8_PORT            STBC_PORT_NULL
#define IOBTN_8_BIT             BIT3
#define IOBTN_8_ACTIVE          LOW

/*******************************************************************************
                               Audio Out Define
*******************************************************************************/
#define I2S_IN                  OFF
#define I2S_A_OUT               OFF
#define I2S_B_OUT               OFF
#define SPDIF0_IN               OFF
#define SPDIF1_IN               OFF
#define SPDIF0_OUT              OFF
#define SPDIF1_OUT              OFF
#define I2S_OUT_FORMAT      _Audio_I2S_OUT_32bit
#define I2S_OUT_MODE        _Audio_I2S_MODE_Philips////

/*******************************************************************************
               Peripherals
*******************************************************************************/
#define AD9884_SDA_PORT          STBC_PORT_NULL
#define AD9884_SDA_BIT           BIT0
#define AD9884_SCL_PORT          STBC_PORT_NULL
#define AD9884_SCL_BIT           BIT1
#define AD9884_WP_PORT           STBC_PORT_NULL
#define AD9884_WP_BIT            BIT0
#define AD9884_WP_ACTIVE         HIGH
#define AD9884_SW_I2C            ON
#define AD9884_P3_USE            OFF
#define AD9884_SLAVE             0x98
#define AD9884_ADDR_LEN          1


#if TPV_EDP_PANEL_POWER_SEQUENCE == ON
#define EDP_TEST_PORT            STBC_PORT_E
#define EDP_TEST_BIT             BIT1
#define EDP_TEST_ACTIVE          HIGH
#warning "No other peripheral pin choice, use EE_WP but need to undef EEPORM1_WP_PORT"
#undef EEPORM1_WP_PORT
#define EEPORM1_WP_PORT         STBC_PORT_NULL
#endif

#define I2CBUS_Num              0
#define I2CBUS_1_SDA_PORT       STBC_PORT_NULL
#define I2CBUS_1_SDA_BIT        BIT7
#define I2CBUS_1_SCL_PORT       STBC_PORT_NULL
#define I2CBUS_1_SCL_BIT        BIT6
#define I2CBUS_1_SW_I2C         ON
#define I2CBUS_1_P3_USE         OFF
#define I2CBUS_1_HW_IDX         STBC_DDC_NULL

#define I2CBUS_2_SDA_PORT       STBC_PORT_NULL
#define I2CBUS_2_SDA_BIT        BIT1
#define I2CBUS_2_SCL_PORT       STBC_PORT_NULL
#define I2CBUS_2_SCL_BIT        BIT0
#define I2CBUS_2_SW_I2C         ON
#define I2CBUS_2_P3_USE         OFF
#define I2CBUS_2_HW_IDX         STBC_DDC_NULL

#define I2CBUS_3_SDA_PORT       STBC_PORT_NULL
#define I2CBUS_3_SDA_BIT        BIT1
#define I2CBUS_3_SCL_PORT       STBC_PORT_NULL
#define I2CBUS_3_SCL_BIT        BIT0
#define I2CBUS_3_SW_I2C         ON
#define I2CBUS_3_P3_USE         OFF
#define I2CBUS_3_HW_IDX         STBC_DDC_NULL

#define I2CBUS_4_SDA_PORT       STBC_PORT_NULL
#define I2CBUS_4_SDA_BIT        BIT0
#define I2CBUS_4_SCL_PORT       STBC_PORT_NULL
#define I2CBUS_4_SCL_BIT        BIT1
#define I2CBUS_4_SW_I2C         ON
#define I2CBUS_4_P3_USE         OFF
#define I2CBUS_4_HW_IDX         STBC_DDC_NULL

#define I2CBUS_5_SDA_PORT       STBC_PORT_NULL
#define I2CBUS_5_SDA_BIT        BIT0
#define I2CBUS_5_SCL_PORT       STBC_PORT_NULL
#define I2CBUS_5_SCL_BIT        BIT1
#define I2CBUS_5_SW_I2C         ON
#define I2CBUS_5_P3_USE         OFF
#define I2CBUS_5_HW_IDX         STBC_DDC_NULL

#define I2CBUS_6_SDA_PORT       STBC_PORT_NULL
#define I2CBUS_6_SDA_BIT        BIT0
#define I2CBUS_6_SCL_PORT       STBC_PORT_NULL
#define I2CBUS_6_SCL_BIT        BIT1
#define I2CBUS_6_SW_I2C         ON
#define I2CBUS_6_P3_USE         OFF
#define I2CBUS_6_HW_IDX         STBC_DDC_NULL

#define I2CBUS_7_SDA_PORT       STBC_PORT_NULL
#define I2CBUS_7_SDA_BIT        BIT0
#define I2CBUS_7_SCL_PORT       STBC_PORT_NULL
#define I2CBUS_7_SCL_BIT        BIT1
#define I2CBUS_7_SW_I2C         ON
#define I2CBUS_7_P3_USE         OFF
#define I2CBUS_7_HW_IDX         STBC_DDC_NULL

#define I2CBUS_8_SDA_PORT       STBC_PORT_NULL
#define I2CBUS_8_SDA_BIT        BIT0
#define I2CBUS_8_SCL_PORT       STBC_PORT_NULL
#define I2CBUS_8_SCL_BIT        BIT1
#define I2CBUS_8_SW_I2C         ON
#define I2CBUS_8_P3_USE         OFF
#define I2CBUS_8_HW_IDX         STBC_DDC_NULL

/*******************************************************************************
               FPGA Setting
*******************************************************************************/
#define FPGA_SDA_PORT          STBC_PORT_NULL
#define FPGA_SDA_BIT           BIT0
#define FPGA_SCL_PORT          STBC_PORT_NULL
#define FPGA_SCL_BIT           BIT1

#define FPGA_SDA_PORT2          STBC_PORT_NULL
#define FPGA_SDA_BIT2           BIT2
#define FPGA_SCL_PORT2          STBC_PORT_NULL
#define FPGA_SCL_BIT2           BIT3

/*******************************************************************************
               DDR
*******************************************************************************/
#define DDR_NUM  1

/*******************************************************************************
               Power Mos
*******************************************************************************/
#define PW_MOS1_OFF_PORT       STBC_PORT_A // PD_CTRL2 for 3V3 cut power
#define PW_MOS1_OFF_BIT        BIT2
#define PW_MOS1_OFF_ACT        FALSE
#define PW_MOS1_OFF_TIME       0 //unit 10ms
#define PW_MOS2_OFF_PORT       STBC_PORT_F // 1.5V
#define PW_MOS2_OFF_BIT        BIT0
#define PW_MOS2_OFF_ACT        FALSE
#define PW_MOS2_OFF_TIME       2 //unit 10ms
#define PW_MOS3_OFF_PORT       STBC_PORT_D // PD_CTRL1 for 0.9V cut power
#define PW_MOS3_OFF_BIT        BIT1
#define PW_MOS3_OFF_ACT        FALSE
#define PW_MOS3_OFF_TIME       0 //unit 10ms
#define PW_MOS4_OFF_PORT       STBC_PORT_NULL
#define PW_MOS4_OFF_BIT        BIT0
#define PW_MOS4_OFF_ACT        TRUE
#define PW_MOS4_OFF_TIME       1 //unit 10ms

#define PW_MOS1_ON_PORT        STBC_PORT_D
#define PW_MOS1_ON_BIT         BIT1
#define PW_MOS1_ON_ACT         TRUE
#define PW_MOS1_ON_TIME        1 //unit 10ms
#define PW_MOS2_ON_PORT        STBC_PORT_F
#define PW_MOS2_ON_BIT         BIT0
#define PW_MOS2_ON_ACT         TRUE
#define PW_MOS2_ON_TIME        0 //unit 10ms
#define PW_MOS3_ON_PORT        STBC_PORT_A
#define PW_MOS3_ON_BIT         BIT2
#define PW_MOS3_ON_ACT         TRUE
#define PW_MOS3_ON_TIME        0 //unit 10ms
#define PW_MOS4_ON_PORT        STBC_PORT_NULL
#define PW_MOS4_ON_BIT         BIT0
#define PW_MOS4_ON_ACT        TRUE
#define PW_MOS4_ON_TIME        1 //unit 10ms


/*******************************************************************************
               Verify
*******************************************************************************/
#if (I2CBUS_Num == 0) && \
     ((I2CBUS_1_SDA_PORT != STBC_PORT_NULL) || (I2CBUS_1_SCL_PORT != STBC_PORT_NULL) || \
      (I2CBUS_2_SDA_PORT != STBC_PORT_NULL) || (I2CBUS_2_SCL_PORT != STBC_PORT_NULL) || \
      (I2CBUS_3_SDA_PORT != STBC_PORT_NULL) || (I2CBUS_3_SCL_PORT != STBC_PORT_NULL) || \
      (I2CBUS_4_SDA_PORT != STBC_PORT_NULL) || (I2CBUS_4_SCL_PORT != STBC_PORT_NULL) || \
      (I2CBUS_5_SDA_PORT != STBC_PORT_NULL) || (I2CBUS_5_SCL_PORT != STBC_PORT_NULL) || \
      (I2CBUS_6_SDA_PORT != STBC_PORT_NULL) || (I2CBUS_6_SCL_PORT != STBC_PORT_NULL) || \
      (I2CBUS_7_SDA_PORT != STBC_PORT_NULL) || (I2CBUS_7_SCL_PORT != STBC_PORT_NULL) || \
      (I2CBUS_8_SDA_PORT != STBC_PORT_NULL) || (I2CBUS_8_SCL_PORT != STBC_PORT_NULL) \
      )
#warning "I2CBUS_Num is 0 but port configures are not NULL!!"
#endif
#if (I2CBUS_Num > 0) && ((I2CBUS_1_SDA_PORT == STBC_PORT_NULL) || (I2CBUS_1_SCL_PORT == STBC_PORT_NULL))
#warning "I2CBUS_Num is larger than 0 but PORT 1 is NULL!!!"
#endif
#if (I2CBUS_Num > 1) && ((I2CBUS_2_SDA_PORT == STBC_PORT_NULL) || (I2CBUS_2_SCL_PORT == STBC_PORT_NULL))
#warning "I2CBUS_Num is larger than 1 but PORT 2 is NULL!!!"
#endif
#if (I2CBUS_Num > 2) && ((I2CBUS_3_SDA_PORT == STBC_PORT_NULL) || (I2CBUS_3_SCL_PORT == STBC_PORT_NULL))
#warning "I2CBUS_Num is larger than 2 but PORT 3 is NULL!!!"
#endif
#if (I2CBUS_Num > 3) && ((I2CBUS_4_SDA_PORT == STBC_PORT_NULL) || (I2CBUS_4_SCL_PORT == STBC_PORT_NULL))
#warning "I2CBUS_Num is larger than 3 but PORT 4 is NULL!!!"
#endif
#if (I2CBUS_Num > 4) && ((I2CBUS_5_SDA_PORT == STBC_PORT_NULL) || (I2CBUS_5_SCL_PORT == STBC_PORT_NULL))
#warning "I2CBUS_Num is larger than 4 but PORT 5 is NULL!!!"
#endif
#if (I2CBUS_Num > 5) && ((I2CBUS_6_SDA_PORT == STBC_PORT_NULL) || (I2CBUS_6_SCL_PORT == STBC_PORT_NULL))
#warning "I2CBUS_Num is larger than 5 but PORT 6 is NULL!!!"
#endif
#if (I2CBUS_Num > 6) && ((I2CBUS_7_SDA_PORT == STBC_PORT_NULL) || (I2CBUS_7_SCL_PORT == STBC_PORT_NULL))
#warning "I2CBUS_Num is larger than 6 but PORT 7 is NULL!!!"
#endif
#if (I2CBUS_Num > 7) && ((I2CBUS_8_SDA_PORT == STBC_PORT_NULL) || (I2CBUS_8_SCL_PORT == STBC_PORT_NULL))
#warning "I2CBUS_Num is larger than 0 but PORT 8 is NULL!!!"
#endif


/*******************************************************************************
               LGD_OLED_PANEL_IO
*******************************************************************************/
//EVDD control
#define LGDOLED_EVDD_PORT               STBC_PORT_NULL
#define LGDOLED_EVDD_BIT                BIT7
#define LGDOLED_EVDD_ACTIVE             HIGH

//OFF-RS & JB
#define LGDOLED_OFFRS_JB_DONE_PORT      STBC_PORT_NULL
#define LGDOLED_OFFRS_JB_DONE_BIT       BIT0
#define LGDOLED_OFFRS_JB_DONE_ACTIVE    HIGH

//QSM_EN
#define LGDOLED_QSM_EN_PORT             STBC_PORT_NULL
#define LGDOLED_QSM_EN_BIT              BIT4
#define LGDOLED_QSM_EN_ACTIVE           HIGH

//OLED_ERROR
#define LGDOLED_ERROR_PORT              STBC_PORT_NULL
#define LGDOLED_ERROR_BIT               BIT2
#define LGDOLED_ERROR_ACTIVE            HIGH

//FOR SS OLED Panel VDD Sequence
#define SSOLED_AC_POWER_DET_PORT        STBC_PORT_NULL
#define SSOLED_AC_POWER_DET_BIT         BIT6
#define SSOLED_AC_POWER_DET_ACTIVE      LOW

#define SSOLED_AC_DET_PORT              STBC_PORT_NULL
#define SSOLED_AC_DET_BIT               BIT3
#define SSOLED_AC_DET_ACTIVE            HIGH

#define SSOLED_VDD_DET_PORT             STBC_PORT_NULL
#define SSOLED_VDD_DET_BIT              BIT7
#define SSOLED_VDD_DET_ACTIVE           HIGH

#define SSOLED_SENSING_DONE_PORT        STBC_PORT_NULL
#define SSOLED_SENSING_DONE_BIT         BIT5
#define SSOLED_SENSING_DONE_ACTIVE      HIGH

#define SSOLED_ERR_DET_PORT             STBC_PORT_NULL
#define SSOLED_ERR_DET_BIT              BIT6
#define SSOLED_ERR_DET_ACTIVE           HIGH

#endif /* BOARDCFG_H_ */

