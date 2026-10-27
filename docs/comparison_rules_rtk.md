# RTK 系列核对规则（已确认 · 已实现）

> 依据样例：`samples/RTK/Hardware_Software_Interface_PHL 27M2N5500X_20250611.XLSX`
> 与 `samples/RTK/TPV_21_715GF225_2H1DP_EDP_PINSHARE.h`
> 状态：**规则已评审确认并实现**（档案 `config/profiles/rtk.yaml`，引擎 `src/genboardconfig/domain/rtk.py`）

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

## 5. 评审确认结论（8 项已定）

| # | 问题 | 确认结论 | 实现落点 |
|---|---|---|---|
| Q1 | 行过滤范围 | **含全部**（G 列非空：IN/OUT/SCL/SDA/ADC → 58 行） | `row_filter.values` |
| Q2 | 通用 GPIO 实现专用功能 | **算一致但标注** | `RtkEngine._check_function_name`（备注「以通用 GPIO 实现」） |
| Q3 | 23 行「缺失」 | **不进行核对**（标为不适用） | `missing_action: skip` |
| Q4 | 上电电平 I/J/K 列 | **默认正确，当前不核对** | 档案中不列为核对属性 |
| Q5 | 候选功能集 vs 枚举成员集 | **不核对** | 枚举成员仅作上下文展示 |
| Q6 | 功能名等效关系 | **交模型**（置信度阈值 0.7） | `orchestrator.review_functions()` + `config/prompts/review_functions.md` |
| Q7 | 写回目标 | **改 `#define _PIN_C1 (_PIN_C1_GPO_OD)` 的右值** | `RtkPinshareParser` 记录后缀的精确列区间 |
| Q8 | 档案选择冲突 | **设置内增加 NTK/RTK 切换** | 设置页「项目系列」；自动模式按 C 侧文件特征识别 |

### 实现后的实测结果（58 行参与）

| 结论 | 数量 | 说明 |
|---|---|---|
| 一致 | **25** | 含 14 行「以通用 GPIO 实现专用功能」（已标注） |
| **不一致** | **6** | 全部可自动改写：DP1_HOT_PLUG、LEDA、LEDG、USB_ON、USB_DET、DDR_PW_EN |
| 歧义（需人工/模型） | **2** | AUX1_CHP、AUX1_CHN（模型置信度不足，保持歧义） |
| 不适用（不核对） | **25** | 23 行 `.h` 中无该网络名 + 2 行 Excel 噪声 |

写回与复检：6 项改动只替换 `#define` 右值的后缀（`_PIN_B3_GPI` → `_PIN_B3_GPO_OD`），
排版与对齐完全保留；复检结果 **修复 12 / 剩余 0 / 新增 0**（12 = 6 行 × 2 个属性）。

### 补充规则（实现时确定）

- **输出类型列只对输出类信号有效**：G 列非 OUT 时，H 列不参与判定（否则 `power` 行 G=IN/H=Open-Drain 会被误判）
- **I2C 期望开漏**：G 列为 `SCL`/`SDA` 时，期望 `.h` 选中 `GPO_OD`（推挽则判不一致）
- **专用功能 → 通用 GPIO 的改动不自动应用**：影响硬件行为，仅给人工建议（`type=none` + 原因）

---

## 6. 实现落点（已完成）

| 模块 | 位置 | 说明 |
|---|---|---|
| 档案 | `config/profiles/rtk.yaml` | Sheet=HSI、列映射、行过滤、值映射、类型词表、噪声规则 |
| 解析器 | `infra/cconfig/rtk_pinshare.py` | 解析 158 个引脚复用区块；`#define` 右值（后缀）精确列区间 |
| 引擎 | `domain/rtk.py` | L0 行筛选 / L1 电气属性 / L2 功能名 / L3 存在性 / L4 噪声 |
| 模型复核 | `infra/llm/orchestrator.py:review_functions()` + `config/prompts/review_functions.md` | 功能名等效关系 |
| 系列选择 | `app/service_factory.py:detect_series()` + 设置页「项目系列」 | 自动按 C 侧文件特征识别，或手动指定 |
| 复检 | `infra/validate/semantic.py`（按档案类型选引擎） | 写回后逐属性复检 |
| 测试 | `tests/test_rtk.py`（9 项） | 解析、落点、L1/L2/L3/L4 判定、写回 |
| 端到端 | `tools/smoke_rtk.py` | 真实样例核对 + 副本上写回 |
