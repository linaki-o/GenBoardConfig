# RTK 系列核对规则（初稿 · 待确认）

> 依据样例：`samples/RTK/Hardware_Software_Interface_PHL 27M2N5500X_20250611.XLSX`
> 与 `samples/RTK/TPV_21_715GF225_2H1DP_EDP_PINSHARE.h`
> 状态：**初稿，等评审确认后再实现**（当前代码只实现了 NTK 规则）

---

## 0. 结论先行：RTK 与 NTK 不是同一套机制

| | **NTK（Novatek）** | **RTK（Realtek RL6829）** |
|---|---|---|
| 配置文件 | `BoardCfg.h` | `*_PINSHARE.h`（引脚复用表） |
| 配置载体 | 端口位表 `PORT_X_DEFAULT_OUT/DIR/PP` | 每 pad 一个 pinshare 区块：`#define _PIN_<PAD> (_PIN_<PAD>_<FUNC>)` |
| 核对粒度 | 端口 × 位（一位一属性） | 引脚（pad）× **复用功能**（一个功能名） |
| Excel 侧对应 | G/H/I 三列 ↔ 三张位表 | **C 列((App) 功能) + G 列(类别) + H 列(开漏/推挽)** ↔ 一行 `#define` |
| 上电电平 | 位表 `OUT` 有编码 → **可核对** | 本文件**无**编码（在 MCU 控制寄存器里）→ **不可核对** |
| 现成实现 | ✅ `domain/hsi.py` | ❌ 需新增引擎 |

**核心差异**：NTK 核的是「某个位上的电平/方向/开漏」，RTK 核的是「某个引脚被复用成了哪个功能、是什么电气属性」。

---

## 1. RTK 配置文件结构（158 个引脚区块）

```c
//---------------------------------------------------------------------------
// Function : HDMI2_HPD          ← 原理图网络名（对应 Excel F 列「Schematic Function」）
// Pinshare : 0x1000
// MCU Ctrl : 0xFE00 at _PIN_C1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C1                  (_PIN_C1_GPO_OD)      ← ★ 实际生效的复用功能

typedef enum
{
    _PIN_C1_GPI   = 0x00,       ← 通用输入
    _PIN_C1_GPO_PP = 0x01,      ← 通用推挽输出
    _PIN_C1_GPO_OD = 0x02,      ← 通用开漏输出
    _PIN_C1_TTL_DVS = 0x03,     ← 专用功能
    _PIN_C1_TCON11  = 0x04,
    _PIN_C1_TEST4B_OUT0..6,
    _PIN_C1_NC = _PIN_C1_GPO_PP,
} EnumPinshareInfoPINC1;
```

统计：**158 个引脚区块**（各有 `// Function :` 注释）/ **79 处引脚 `#define`**（其中 42 处选中 `NC` 即未使用）/ 另有 85 处 `_OFF_REGION`（未使用区定义）。

---

## 2. 三层核对规则

### L0 行筛选

- 只处理 **HSI Sheet** 中 **G 列「GPIO  TYPE(输入输出类别)」非空且非 `NA`** 的行 → **58 行**参与
  （`OUT` 30 / `IN` 16 / `SCL` 5 / `SDA` 5 / `ADC` 2）；其余 69 行跳过
- E 列「GPIO Init」**全表为空**，暂不参与

### L1 电气属性层（确定性，脚本判定）

把 `.h` 中 `#define` 选中的功能归为三类：

| 类别 | 成员 | 电气含义 |
|---|---|---|
| 通用输入 | `GPI` | 输入 |
| 通用输出 | `GPO_PP` / `GPO_OD` | 推挽输出 / 开漏输出 |
| 专用功能 | 其它（`DDCSCL_4`、`IICSCL_0_2`、`PWM_OUT`、`DPRX_AUX_P_1`…） | 由功能本身决定 |

判定表：

| `.h` 选中 | Excel G 列 | Excel H 列 | 结论 |
|---|---|---|---|
| `GPI` | `IN` | （空） | 一致 |
| `GPI` | `OUT` | 任意 | **不一致**：期望输出 |
| `GPO_PP` | `OUT` | `Push-Pull Output` | 一致 |
| `GPO_PP` | `OUT` | `Open-Drain Output` | **不一致**：期望开漏 |
| `GPO_OD` | `OUT` | `Open-Drain Output` | 一致 |
| `GPO_OD` | `OUT` | `Push-Pull Output` | **不一致**：期望推挽 |
| `GPO_*` | `IN` | — | **不一致**：方向反了 |
| 专用功能 | 与该功能类别相符（如 `SCL`↔`*SCL*`、`SDA`↔`*SDA*`） | — | 一致（需功能→类别映射表） |
| 专用功能 | 类别无法判定 | — | **歧义** → 交大模型 |

### L2 功能名层（确定性 + 大模型）

| 情形 | 处理 |
|---|---|
| `.h` 选中**通用 GPIO**，Excel C 列 (App) 是**专用功能名**（如 `HDMI_HPD_4`） | **视为一致**（实现方式不同，电气属性一致即可），备注「以通用 GPIO 实现」 |
| `.h` 选中**专用功能**，与 Excel (App) 名归一化后相同 | 一致 |
| `.h` 选中**专用功能**，与 Excel (App) 名不同 | **歧义** → 交大模型判定是否等效（例：`AUX1_CHP` 期望 `SBU2_1`，`.h` 用 `DPRX_AUX_P_1`） |

### L3 存在性层

| 情形 | 结论 |
|---|---|
| `.h` 中**没有**该网络名的 Function 区块 | **缺失 / 待确认**（23 行，见 §5 讨论） |
| `.h` 中该 pad 存在但选中 `NC` | 未使用 |
| `.h` 中该 pad 存在且已选中功能 | 进入 L1/L2 |

### L4 Excel 侧噪声过滤（建议）

23 行「缺失」里有明显不是 GPIO 的行（SPI/ADC/AUDIO/LVDS/复位/按键）与 Excel 模板占位符
（`AJ19_FUNCTION` 等）。建议在 L0 阶段先剔除：

- 网络名含 `FUNCTION` 或以 `_FUNCTION` 结尾 → **模板占位符，忽略**
- 网络名带后缀 `(SPI)` / `(KEY ADC)` / `( Headphone out )` 等 → **专用功能域，不在本文件核对**

---

## 3. 归一化与匹配规则

| 对象 | 规则 |
|---|---|
| 网络名匹配 | 去括号说明（`CLK (SPI)`→`CLK`）、去分隔符、转大写后比较 |
| 功能名提取 | Excel C 列按 `/` 拆分，取带 `(App)` 的那项（无则取第一项）；`.h` 侧去掉 `_PIN_<PAD>_` 前缀 |
| 类型词表 | `GPI`=输入；`GPO_PP`=推挽输出；`GPO_OD`=开漏输出；`*SCL*`=SCL 类；`*SDA*`=SDA 类；`PWM*`=PWM 输出；`ADC*`=模拟输入 |
| 值映射 | G 列：`IN`→输入、`OUT`→输出、`SCL`→SCL 类、`SDA`→SDA 类、`ADC`→ADC 类；H 列：`Open-Drain Output`→开漏、`Push-Pull Output`→推挽（注意比 NTK 的 `Open Drain`/`Push pull` 多连字符） |

---

## 4. 实测量化（58 行参与核对）

| 结论 | 数量 | 样例 |
|---|---|---|
| 一致（通用 GPIO 实现，电气符合） | **14** | `HDMI2_HPD` 期望 HDMI_HPD_4，`.h` 用 `GPO_OD` |
| 一致（专用功能且功能名一致） | **10** | `HDMI_2_DDCCK` ↔ `DDCSCL_4` |
| **不一致（方向/类型）** | **5** | `LEDA`/`LEDG` 期望输出但 `.h` 选中 `GPI` |
| **不一致（开漏/推挽）** | **4** | `DP1_HOT_PLUG` 期望开漏但 `.h` 是 `GPO_PP` |
| 歧义（需语义判定） | **2** | `AUX1_CHP` 期望 `SBU2_1` vs `.h` `DPRX_AUX_P_1` |
| 缺失 / 待确认 | **23** | 见下 |

**明确不一致清单（可直接脚本判定）**

| 行 | 网络名 | G | H | `.h` 实际 | pad |
|---|---|---|---|---|---|
| 23 | DP1_HOT_PLUG | OUT | Open-Drain Output | `GPO_PP` | D10 |
| 73 | LEDA | OUT | Open-Drain Output | `GPI` | B3 |
| 77 | LEDG | OUT | Open-Drain Output | `GPI` | H4 |
| 80 | USB_ON | OUT | Open-Drain Output | `GPO_PP` | F2 |
| 87 | PANEL_SCL | SCL | — | `GPO_OD` | F4 |
| 88 | PANEL_SDA | SDA | — | `GPO_OD` | G1 |
| 98 | USB_DET | OUT | Push-Pull Output | `GPI` | AH1 |
| 104 | DDR_PW_EN | OUT | Push-Pull Output | `GPO_OD` | B4 |
| 113 | power | IN | Open-Drain Output | `GPI` | AB6 |

**23 行「缺失」的构成**（不能一律判为配置缺失）：

- 专用功能不在本文件：`CLK (SPI)` / `SDIN/SDOUT/CE (SPI)`、`XI`/`XO`、`KEY1/KEY2 (KEY ADC)`、`AUDIO_H_L/R`、`LD_CLK_A`/`LD_DI_A`/`LD_DO_A`/`LD_CS_A`/`LD_VSYNC_A`/`LD_HSYNC_A`
- 其它配置域：`RESETB`、`REXT`、`con_off`、`Dim-on`
- Excel 模板占位符：`AJ19_FUNCTION`、`AJ20_FUNCTION`、`AL30_FUNCTION`

---

## 5. 待确认问题（决定实现方式）

| # | 问题 | 我的建议 |
|---|---|---|
| Q1 | **行过滤范围**：只核对 G ∈ {IN, OUT}（46 行），还是含 SCL/SDA/ADC（58 行）？ | 含全部非空（58 行）；SCL/SDA 是 I2C 专用功能，可比 |
| Q2 | **「通用 GPIO 实现专用功能」算不算一致？**（14 行，占比最大） | **算一致**，但备注「以通用 GPIO 实现」；若你认为必须显式声明专用功能，改为「不一致」 |
| Q3 | **23 行「缺失」如何定性**？ | 三分：① 不在本文件（SPI/ADC/AUDIO/LVDS/复位/按键）→ 标「不在本文件·需人工确认」；② Excel 模板占位符 → 忽略；③ 其它 → 判「配置缺失」 |
| Q4 | **上电电平（I/J/K 列）** 在本文件无编码（MCU 控制寄存器里设置）→ 是否需要扩展核对到 MCU 初始化表？ | 本期不核对，标「不在核对范围」 |
| Q5 | 是否核对「Excel C 列候选功能集」与「`.h` 枚举成员集」的一致性（芯片手册 vs 头文件）？ | 本期不做（属另一类检查：芯片手册一致性） |
| Q6 | 功能名等效关系（如 `AUX1_CHP`↔`DPRX_AUX_P_1`）用**别名表**还是交模型？ | 别名表 + 模型兜底 |
| Q7 | **写回目标**确认：改 `#define _PIN_C1 (_PIN_C1_GPO_OD)` 的右值？ | 是（列偏移精确，与 NTK 同机制） |
| Q8 | 两套 Excel 的 HSI **表头几乎相同**，档案不能只按 Sheet 名选 | 档案匹配改为由 **C 侧文件特征**驱动：含 `PORT_X_DEFAULT_*` → NTK；含 `_PIN_<PAD> (...)` 区块 → RTK |

---

## 6. 实现计划（待 Q1~Q8 确认后）

1. **解析器** `infra/cconfig/rtk_pinshare.py`：解析 158 个区块 → `RtkPinBlock{function, pad, selected, members, define_line, define_col}`，保留 `#define` 右值的精确列区间（可写回）。
2. **档案** `config/profiles/rtk.yaml`：Sheet=HSI、列映射（G/H/C/F）、行过滤、值映射、功能类别词表、别名表。
3. **引擎** `domain/rtk.py`：L0 行筛选 → L1 电气属性 → L2 功能名（歧义交模型）→ L3 存在性 → 生成 `AttributeResult` 与 `ChangePlan`（复用现有模型与写回链路）。
4. **档案匹配**：`app/service_factory.py` 改为按 C 侧文件特征选择档案；`samples/` 下按 `NTK/`、`RTK/` 分目录不影响选择（样本目录仅用于演示）。
5. **UI**：并排对比视图复用（右侧表格换成 RTK 条目：功能区块、pad、选中功能、枚举成员）。
6. **测试**：`tests/test_rtk.py`（解析、区块匹配、L1/L2/L3 判定、写回落点）。

> 现有 NTK 链路与已写回的文件**不受影响**：新档案独立、引擎并列、UI 复用表格渲染。
