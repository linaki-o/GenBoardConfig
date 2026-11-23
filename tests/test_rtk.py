"""RTK 档案（引脚复用表）单测。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genboardconfig.domain.models import CheckStatus, ExpectedAttribute  # noqa: E402
from genboardconfig.domain.profiles import Profile  # noqa: E402
from genboardconfig.domain.rtk import RtkEngine, app_function, norm_text  # noqa: E402
from genboardconfig.infra.cconfig.editor import TextEdit, apply_edits  # noqa: E402
from genboardconfig.infra.cconfig.rtk_pinshare import RtkPinshareParser  # noqa: E402

PROFILE_PATH = Path(__file__).resolve().parents[1] / "config" / "profiles" / "rtk.yaml"

SAMPLE = """//---------------------------------------------------------------------------
// Function : HDMI2_HPD
// Pinshare : 0x1000
// MCU Ctrl : 0xFE00 at _PIN_C1_MCU_REG
//---------------------------------------------------------------------------
#define _PIN_C1                  (_PIN_C1_GPO_OD)

typedef enum
{
    _PIN_C1_GPI = 0x00,
    _PIN_C1_GPO_PP = 0x01,
    _PIN_C1_GPO_OD = 0x02,
    _PIN_C1_TTL_DVS = 0x03,
    _PIN_C1_NC = _PIN_C1_GPO_PP,
} EnumPinshareInfoPINC1;

//---------------------------------------------------------------------------
// Function : HDMI2_DET
//---------------------------------------------------------------------------
#define _PIN_E4                  (_PIN_E4_GPI)

typedef enum
{
    _PIN_E4_GPI = 0x00,
    _PIN_E4_GPO_PP = 0x01,
    _PIN_E4_GPO_OD = 0x02,
    _PIN_E4_HDMI_CAB_DET4 = 0x03,
    _PIN_E4_NC = _PIN_E4_GPO_PP,
} EnumPinshareInfoPINE4;

//---------------------------------------------------------------------------
// Function : DP1_HOT_PLUG
//---------------------------------------------------------------------------
#define _PIN_D10                 (_PIN_D10_GPO_PP)

typedef enum
{
    _PIN_D10_GPI = 0x00,
    _PIN_D10_GPO_PP = 0x01,
    _PIN_D10_GPO_OD = 0x02,
    _PIN_D10_NC = _PIN_D10_GPO_PP,
} EnumPinshareInfoPIND10;

//---------------------------------------------------------------------------
// Function : AUX1_CHP
//---------------------------------------------------------------------------
#define _PIN_E9                  (_PIN_E9_DPRX_AUX_P_1)

typedef enum
{
    _PIN_E9_GPI = 0x00,
    _PIN_E9_GPO_PP = 0x01,
    _PIN_E9_DPRX_AUX_P_1 = 0x02,
    _PIN_E9_NC = _PIN_E9_GPO_PP,
} EnumPinshareInfoPINE9;
"""


def _profile() -> Profile:
    return Profile.load(PROFILE_PATH)


def _engine() -> RtkEngine:
    parser = RtkPinshareParser()
    result = parser.parse_text(SAMPLE)
    return RtkEngine(_profile(), result.entries)


def _req(
    net: str,
    gpio_type: str,
    io_type: str = "",
    pin_name: str = "",
    req_id: str = "R1",
):
    profile = _profile()
    attrs = [
        ExpectedAttribute(
            name="elec_type",
            label="方向/类别",
            source_field="gpio_type",
            value=gpio_type,
            normalized=profile.map_value("gpio_type", gpio_type),
            checkable=True,
            check="rtk_electrical",
        ),
        ExpectedAttribute(
            name="io_type",
            label="输出类型",
            source_field="io_type",
            value=io_type,
            normalized=profile.map_value("io_type", io_type),
            checkable=bool(io_type),
            check="rtk_electrical",
        ),
    ]
    from genboardconfig.domain.models import GPIORequirement

    return GPIORequirement(
        id=req_id, sheet="HSI", row_no=6, pin_name_raw=pin_name, net_name=net,
        config_key=net, attributes=attrs,
    )


# ----------------------------------------------------------------------
def test_norm_and_app_function():
    assert norm_text("CLK (SPI)") == "CLK"
    assert norm_text("EE_WP (H:ON)") == "EE_WP"
    assert app_function("HDMI_HPD_4(App) / HDMI_RX_HPD_4 / DVS") == "HDMI_HPD_4"
    assert app_function("SBU2_1 / SBU1_1") == "SBU2_1"


def test_parser_extracts_define_right_value_span():
    parser = RtkPinshareParser()
    result = parser.parse_text(SAMPLE)
    entry = next(e for e in result.entries if e.function == "HDMI2_HPD")
    assert entry.value_raw == "GPO_OD"
    assert entry.group == "C1"
    line = SAMPLE.split("\n")[entry.line - 1]
    assert line[entry.value_col : entry.value_col + entry.value_len] == "GPO_OD"
    assert entry.members


def test_generic_gpio_implementing_dedicated_function_is_match():
    engine = _engine()
    req = _req("HDMI2_HPD", "OUT", "Open-Drain Output", "HDMI_HPD_4(App) / DVS")
    result = engine.check([req])[0]
    assert result.status == CheckStatus.MATCH
    # 功能名属性：通用 GPIO 实现 → 一致但标注
    fn = result.attribute("function_name")
    assert fn is not None
    assert fn.status == CheckStatus.MATCH
    assert "通用 GPIO" in fn.notes


def test_direction_mismatch_is_detected_with_writeback():
    engine = _engine()
    req = _req("DP1_HOT_PLUG", "OUT", "Open-Drain Output", "DP_HPD1(App)")
    result = engine.check([req])[0]
    assert result.status == CheckStatus.MISMATCH
    change = result.proposed_change
    assert change.type.value == "set_macro"
    assert change.old_value == "GPO_PP"
    assert change.new_value == "GPO_OD"
    target = next(e for e in engine.entries if e.id == change.target)
    assert target.key == "DP1_HOT_PLUG"


def test_input_row_ignores_output_type_column():
    """方向为 IN 时，输出类型列不参与判定。"""
    engine = _engine()
    req = _req("HDMI2_DET", "IN", "Open-Drain Output", "HDMI_CAB_DET4(App)")
    result = engine.check([req])[0]
    assert result.status == CheckStatus.MATCH


def test_dedicated_function_name_differs_goes_ambiguous():
    engine = _engine()
    req = _req("AUX1_CHP", "IN", "", "SBU2_1(App) / SBU1_1")
    result = engine.check([req])[0]
    assert result.status == CheckStatus.AMBIGUOUS
    fn = result.attribute("function_name")
    assert fn.expected == "SBU2_1"
    assert fn.actual == "DPRX_AUX_P_1"


def test_missing_net_is_not_checked():
    engine = _engine()
    req = _req("NOT_IN_HEADER", "OUT", "Push-Pull Output", "X(App)")
    result = engine.check([req])[0]
    assert result.status == CheckStatus.NOT_APPLICABLE
    assert "未定义" in result.notes


def test_noise_net_is_skipped():
    engine = _engine()
    req = _req("CLK (SPI)", "OUT", "", "SPI_CLK(App)")
    result = engine.check([req])[0]
    assert result.status == CheckStatus.NOT_APPLICABLE
    assert "噪声" in result.notes


def test_writeback_changes_define_suffix_only():
    parser = RtkPinshareParser()
    result = parser.parse_text(SAMPLE)
    entry = next(e for e in result.entries if e.function == "DP1_HOT_PLUG")
    new_text = apply_edits(
        SAMPLE,
        [TextEdit(line=entry.line, col=entry.value_col, length=entry.value_len,
                  new_value="GPO_OD")],
    )
    assert "#define _PIN_D10                 (_PIN_D10_GPO_OD)" in new_text
    # 枚举成员（可选功能清单）保持不变
    assert "_PIN_D10_GPO_PP = 0x01," in new_text
    # 其它行不受影响
    assert "#define _PIN_C1                  (_PIN_C1_GPO_OD)" in new_text


# ---------------------------------------------------------------------------
# 新式 Realtek 宏名（_LQFP216_..._PIN_201）与条件编译分支
# ---------------------------------------------------------------------------

NEW_SAMPLE = """//---------------------------------------------------------------------------
// Function : EE_WP
// Pinshare : 0x1000
// MCU Ctrl : 0xFE00 at _LQFP216_3D_USB_DDRX1_LVDS_PIN_201_MCU_REG
//---------------------------------------------------------------------------
#define _LQFP216_3D_USB_DDRX1_LVDS_PIN_201                  (_LQFP216_3D_USB_DDRX1_LVDS_PIN_201_GPO_OD)

typedef enum
{
    _LQFP216_3D_USB_DDRX1_LVDS_PIN_201_GPI = 0x00,
    _LQFP216_3D_USB_DDRX1_LVDS_PIN_201_GPO_PP = 0x01,
    _LQFP216_3D_USB_DDRX1_LVDS_PIN_201_GPO_OD = 0x02,
    _LQFP216_3D_USB_DDRX1_LVDS_PIN_201_NC = _LQFP216_3D_USB_DDRX1_LVDS_PIN_201_GPO_PP,
} EnumPinshareInfoLQFP216_3D_USB_DDRx1_LVDS_PIN_201;

//---------------------------------------------------------------------------
// Function : PANEL_SCL
// Pinshare : 0x104D
//---------------------------------------------------------------------------
#if(_ACER_OSD_DFR_SUPPORT != _DFR_OFF)
#define _LQFP216_3D_USB_DDRX1_LVDS_PIN_114                  (_LQFP216_3D_USB_DDRX1_LVDS_PIN_114_GPO_OD)
#else
#define _LQFP216_3D_USB_DDRX1_LVDS_PIN_114                  (_LQFP216_3D_USB_DDRX1_LVDS_PIN_114_NC)
#endif

typedef enum
{
    _LQFP216_3D_USB_DDRX1_LVDS_PIN_114_GPI = 0x00,
    _LQFP216_3D_USB_DDRX1_LVDS_PIN_114_GPO_OD = 0x01,
    _LQFP216_3D_USB_DDRX1_LVDS_PIN_114_NC = _LQFP216_3D_USB_DDRX1_LVDS_PIN_114_GPO_OD,
} EnumPinshareInfoLQFP216_3D_USB_DDRx1_LVDS_PIN_114;

//---------------------------------------------------------------------------
// Function : NC
// Pinshare : 0x1036 at _OFF_Region
//---------------------------------------------------------------------------
#define _LQFP216_3D_USB_DDRX1_LVDS_PIN_48_OFF_REGION        (_LQFP216_3D_USB_DDRX1_LVDS_PIN_48_NC)
"""


def test_parser_handles_new_style_macro_names():
    """新版 Realtek 宏名（封装+引脚编号）也能解析出复用功能与落点。"""
    parser = RtkPinshareParser()
    result = parser.parse_text(NEW_SAMPLE)
    entry = next(e for e in result.entries if e.function == "EE_WP")
    assert entry.value_raw == "GPO_OD"
    assert entry.group == "201"          # 引脚标识取 _PIN_ 之后的编号
    assert entry.owner == "_LQFP216_3D_USB_DDRX1_LVDS_PIN_201"
    assert entry.members == ["GPI", "GPO_PP", "GPO_OD", "NC"]   # 成员为相对宏名的后缀


def test_parser_skips_off_region_defines():
    """`..._OFF_REGION (_..._NC)` 不是本宏的复用选择，应被跳过。"""
    parser = RtkPinshareParser()
    result = parser.parse_text(NEW_SAMPLE)
    assert not any(e.function == "NC" for e in result.entries)
    assert all(e.value_raw != "NC" or e.owner.endswith("_PIN_201") for e in result.entries)


def test_parser_prefers_unconditional_branch():
    """同一 pad 多分支条件编译时，优先取无条件分支，并记录所选分支条件。"""
    parser = RtkPinshareParser()
    result = parser.parse_text(NEW_SAMPLE)
    entry = next(e for e in result.entries if e.function == "PANEL_SCL")
    assert entry.value_raw == "GPO_OD"
    assert entry.condition == "#if _ACER_OSD_DFR_SUPPORT != _DFR_OFF"


def test_parser_warns_when_no_selection_found():
    """识别到区块但解析不出选择时必须给出警告，不能静默返回 0 条目。"""
    parser = RtkPinshareParser()
    text = (
        "//---------------------------------------------------------------------------\n"
        "// Function : EE_WP\n"
        "// Pinshare : 0x1000\n"
        "//---------------------------------------------------------------------------\n"
        "#define SOMETHING_ELSE          (OTHER_VALUE)\n"
    )
    result = parser.parse_text(text)
    assert result.entries == []
    assert result.warnings and "未能" in result.warnings[0]


def test_detect_series_recognizes_new_style_pinshare(tmp_path):
    """新式宏名的 PINSHARE 头文件必须被识别为 RTK，而不是 NTK。"""
    from genboardconfig.app.service_factory import detect_series

    path = tmp_path / "new_pinshare.h"
    path.write_text(NEW_SAMPLE, encoding="utf-8")
    assert detect_series(path) == "rtk"


def test_new_style_sample_matches_network_name():
    """新式头文件按网络名建立映射，可被 Excel 侧命中。"""
    parser = RtkPinshareParser()
    result = parser.parse_text(NEW_SAMPLE)
    engine = RtkEngine(_profile(), result.entries)
    assert "EE_WP" in engine.by_function
    assert engine.by_function["EE_WP"].value_raw == "GPO_OD"


def test_detect_series_on_real_samples():
    """系列判定必须准确：NTK 不得被 PINSHARE 特征误判为 RTK。"""
    from genboardconfig.app.service_factory import detect_series

    root = Path(__file__).resolve().parents[1] / "samples"
    ntk = root / "NTK" / "BoardCfg.h"
    if ntk.exists():
        # NTK 的 BoardCfg.h 里有 `#define AUDIO_OUT (LINE_OUT)` 这类普通宏，
        # 不能只靠 define 形态判定为 RTK
        assert detect_series(ntk) == "ntk"
    for folder in ("RTK", "RTK_NEW"):
        headers = list((root / folder).glob("*.h")) if (root / folder).exists() else []
        for header in headers:
            assert detect_series(header) == "rtk", header.name
