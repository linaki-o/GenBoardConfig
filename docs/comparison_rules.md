# 比对逻辑（基于真实样例反推 · v0.3 已按评审要求收敛）

> 依据：`samples/05_Hardware_Software_Interface(HSI)-AOC CU34B3E  715GF603-M0A-B02-0050  20260621.xlsx`
> 与 `samples/BoardCfg.h`（真实板级配置，**头文件**而非 .c）。

## 0. 核对范围（评审确认）

| 侧 | 范围 |
|---|---|
| **C 侧** | **只核对 `PORT_<X>_DEFAULT_{OUT,DIR,PP,PU}` 端口位表**（`BitsToByte` 逐位） |
| **Excel 侧** | **只核对「GPIO  TYPE(输入输出类别)」列为 `IN` / `OUT` 的行** |
| 引脚来源 | Excel 的「PIN Name」列（芯片引脚），**不再依赖配置里的信号宏组** |
| 信号宏组 | 仅作为「该引脚被哪些信号占用」的**上下文展示**，不参与判定 |

范围写在 `config/profiles/hsi.yaml` 中（`row_filter` / `bit_tables` / `attribute_source`），
新增板型只需新增 YAML。

---

## 1. 真实数据结构

### 1.1 Excel：`HSI` Sheet 是唯一的 GPIO 核对表

表头在**第 5 行**（1~4 行是标题与分区说明），列语义：

| 列 | 表头 | 含义 | 示例 |
|---|---|---|---|
| A | `PIN #` | 芯片封装脚位 | `C4` |
| B | `Chip Section` | 方向（本板填了 `Output`） | `Output` |
| C | **`PIN Name`** | **scaler 引脚（核对定位键）** | `PA2`、`PB6/DPRX1_HPD`、`PK1/PWMB` |
| D | `Description/ Function` | 引脚复用功能全集 | `PA2/ADC6/PWMC` |
| F | `Schematic Function` | 原理图网络名（仅作参考） | `+3V3C_EN`、`ON_BACKLIGHT` |
| G | **`GPIO  TYPE(输入输出类别)`** | **行过滤列 + 方向期望** | `IN` / `OUT`（**当前样例此列全空**） |
| H | **`Output PIN 设定类型`** | 推挽/开漏 | `Open Drain`、`Push pull` |
| I | **`Power On`** | 上电电平 | `High`/`Low` |
| J | `Power Saving` | 省电电平 | `High`/`Low` |
| K | `Power Off` | 关机电平 | `High`/`Low` |
| L/M | `F/W Check` / `EE Check` | 人工核对结论 | `PASS` |

其余 Sheet：`Rev History`、`Key Setting`、`Other Requirements`、`Sheet1~3` **不参与核对**。

### 1.2 `BoardCfg.h`：端口位表（核对目标）

```c
//Mcu I/O port default output         bit:   7     6     5     4     3     2     1     0
#define PORT_C_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH,  LOW,  LOW, HIGH)
//Mcu I/O port default direction    bit:    7    6    5    4    3    2    1    0
#define PORT_C_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, IN, OUT, OUT,  IN)
// Push-Pull : 1 / Open-Drain : 0
#define PORT_C_DEFAULT_PP      BitsToByte( LOW,  LOW,  LOW,  LOW, LOW, HIGH, HIGH,  LOW)
// Pull-Hight : 1 / Non-Pull-High : 0
#define PORT_C_DEFAULT_PU      BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
```

位序为 `bit7 … bit0`，即 `BitsToByte` 的**第 1 个参数是 bit7**。
每个位都是**独立的可改写落点**（精确到列区间），改一位不影响其它位与排版。

### 1.3 信号宏组（仅上下文）

```c
#define DIG1_HPD_PORT           STBC_PORT_B//DP_HPD
#define DIG1_HPD_BIT            BIT6
#define BKL_ADIM_OUTPUT_PIN     PWMB_PIN_PK1
```

用于回答「这个引脚被哪些信号占用」，不参与判定。

---

## 2. 比对规则（评审确认的最终映射）

记 Excel 引脚 `PC1` → (端口 C, 位 1)；`PORT_C_DEFAULT_OUT` 的第 2 个参数即 C1。

| 板级配置宏 | Excel 列 | 属性 | 归一化 | 判定 |
|---|---|---|---|---|
| `PORT_X_DEFAULT_DIR[bit]` | **G 列**「GPIO  TYPE(输入输出类别)」 | 方向 | IN↔IN、OUT↔Output/OUT | 值相等 |
| `PORT_X_DEFAULT_PP[bit]` | **H 列**「Output PIN 设定类型」 | 输出类型 | Push pull↔HIGH、Open Drain↔LOW | 值相等 |
| `PORT_X_DEFAULT_OUT[bit]` | **I 列**「Power On」 | 上电电平 | High↔HIGH、Low↔LOW | 值相等 |
| `PORT_X_DEFAULT_PU[bit]` | （Excel 无对应列） | 上拉 | — | **暂时忽略** |

> 口径：`PORT_X_DEFAULT_PP` 的位值 **1(HIGH)=推挽、0(LOW)=开漏**（与 `.h` 注释一致）。
> 位序为 `bit7…bit0`，即 `BitsToByte` 的**第 1 个参数是 bit7**。

不在核对范围：J 列「Power Saving」、K 列「Power Off」（板级端口位表中无对应编码）。

### 2.1 行过滤

只处理 **HSI Sheet** 中 `GPIO TYPE ∈ {IN, OUT}` 的行；其它 Sheet 一律不参与。

**主列 + 备用列（自动回退）**：

| 情形 | 行为 |
|---|---|
| G 列（GPIO TYPE）有 `IN`/`OUT` | 用 G 列过滤，并按 G 列判定「方向」 |
| G 列为空 / 无匹配 | **自动回退**到备用列 `Chip Section`（`Output`/`Input`），并按该列判定「方向」；报告与界面明确标注「回退」及实际使用的列 |

回退时提示：`* 「gpio_type」列无匹配行（该列取值：无），已自动改用备用列「chip_section」参与核对，共 14 行。`

> **当前样例的事实**：`GPIO  TYPE(输入输出类别)` 列（**G 列**）在本文件里 **G6:G23 全部为空**
> （openpyxl 两种读法 + raw XML 三重验证一致；全工作簿唯一的 `IN`/`OUT` 文本在 `Sheet1!C4='In'`、
> `Sheet1!C5='out'`，那是 I/O 类型图例表）。因此本文件实际走的是**回退分支**（用 Chip Section 过滤 14 行）。
> 若换成 G 列已填写的版本，工具会自动使用 G 列，无需任何配置改动。

也可在设置页手动指定过滤列（存 `config/settings.local.yaml`），或改 `config/profiles/hsi.yaml` 的
`row_filter.field / values / fallback`。

### 2.2 不适用（NA）占位值

Excel 中标注 `NA` / `N/A` / `-` / `NULL` 等占位值的单元格**不参与判定**，
但原文照常显示，结论标注「Excel 标注为 NA，不参与判定」（`excel.na_values` 可配置）。

### 2.3 冲突保护

同一 (位表, 端口, 位, 属性) 被多行要求、且期望值互相冲突时 → 该属性判为**歧义**且**不自动改写**，
交人工确认（例：两行都写 PC1，一行要求上电 High、一行要求 Low）。

### 2.4 差异判定状态

沿用六态：一致 / 不一致 / 缺失 / 歧义 / 不适用 / 未解析。行状态 = 可核对属性中最严重者
（不一致 > 缺失 > 歧义 > 未解析 > 不适用 > 一致）；不在核对范围的属性不参与行状态。

### 2.5 修改落点

| 差异 | 落点 | 编辑方式 |
|---|---|---|
| 方向 / 输出类型 / 上电电平不符 | `PORT_<X>_DEFAULT_{DIR,PP,OUT}` 的第 n 个 `BitsToByte` 实参 | **位内改写**（只替换该实参） |
| 引脚无法解析 | — | 不生成修改，判为未解析 |
| 冲突 | — | 不生成修改，判为歧义 |

---

## 3. 大模型在真实场景中的角色

范围收敛后，**绝大多数判定是确定性的**（引脚来自 Excel、位表是位表）。
大模型只处理规则判不了的部分：

1. **残余歧义项复核**：期望值无法用值映射判定（表里出现未登记的写法）、
   或同一单元格语义存疑时，把「期望值 + 目标位表原文 + 行号」交给模型判定，
   模型结论必须带证据且置信度 ≥ 0.7 才采纳，否则保持歧义。
2. **报告摘要**：对差异给出归因与修改建议的自然语言说明。

> 约束：模型结论必须带证据（宏名 + 行号 + 原文）；无证据或置信度不足 → 不采纳，保持歧义。

---

## 4. 实测结论

### 4.1 默认配置（过滤列 = `GPIO TYPE`）

参与核对 **0 行**（该列全空），工具给出明确诊断。

### 4.2 改用 `Chip Section` 过滤（14 行）

| 状态 | 数量 | 说明 |
|---|---|---|
| 一致 | 8 | 方向 / 输出类型 / 上电电平全部吻合 |
| 不一致 | 6 | **全部是上电电平**：PC1、PC2（期望 High 实际 Low）、PE2、PE3（期望 Low 实际 High）、PK1、PK2（期望 HIGH 实际 LOW） |

其中 PK1/PK2 是 PWM 输出（`BKL_ADIM` / `BKL_PDIM`），其电平由 PWM/PSM 块决定
（`BKL_ADIM_POL = HIGH`），端口位表的 `LOW` 是否等同需人工判断——按当前规则（只核对位表）判为不一致。

---

## 5. 待确认

1. `GPIO TYPE` 列在其它板型是否填写？若长期为空，是否改用 `Chip Section` 作为过滤列与方向来源？
2. PWM/PSM 型引脚（BL_ADIM / BL_PDIM）的上电电平，是否应改取宏组 `_POL` 而非端口位表？
3. `Power Saving` / `Power Off` 两列在固件中由谁实现，是否需要扩展核对到 `.c` 实现文件？
4. 是否需要**多文件**核对（`BoardCfg.h` + `ModelAppCfgList.h` + 实现文件）？
5. 条件编译宏（如 `TPV_EDP_PANEL_POWER_SEQUENCE`）是否需要接入实际编译命令行以确定生效分支？

