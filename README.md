# AI-Quant — A股量化策略研究

A股量化策略研究项目，聚焦个股行情可视化与策略回测分析。

## 目录结构

```
量化策略/
├── README.md                        项目说明文档
├── .gitignore
├── data/                            原始数据（CSV / JSON）
│   └── 601226_consolidated.csv      华电科工 估值指标汇总数据
├── notebooks/                       Jupyter Notebook 交互式分析
│   └── 601226_dashboard.ipynb       华电科工行情面板生成
├── scripts/                         独立 Python 脚本
│   └── generate_dashboard.py        HTML 面板生成脚本
└── output/                          生成的 HTML 面板等输出产物
    └── 601226_dashboard.html        华电科工行情面板
```

### 目录职责

| 目录 | 职责 | 说明 |
|------|------|------|
| `data/` | 数据层 | 存放原始数据和预处理数据，只读，不存放代码 |
| `notebooks/` | 分析层 | Jupyter Notebook，用于交互式探索和可视化 |
| `scripts/` | 脚本层 | 可独立运行的 Python 脚本，路径以项目根目录为基准 |
| `output/` | 产出层 | 脚本/Notebook 生成的 HTML 报告、图表等产物 |

## 当前分析标的

### 华电科工 (601226.SH)

- **数据区间**: 2025-07-01 ~ 2026-07-03，共 245 个交易日
- **数据来源**: Tushare 日线行情 + CSV 汇总估值指标
- **CSV 字段**: `trade_date, close, pe, pe_ttm, pb, ps, ps_ttm, dv_ratio, dv_ttm, turnover_rate, volume_ratio, total_share, float_share, free_share, total_mv, circ_mv`

#### 行情面板包含

| 模块 | 内容 |
|------|------|
| K线图 | 蜡烛图 + MA5/MA10/MA20/MA60 四条均线，支持缩放拖拽 |
| 成交量 | 柱状图，与K线联动缩放，涨红跌绿（中国A股惯例） |
| 估值指标 | PE(TTM)、PB、换手率、总市值 四张子图 |
| 统计卡片 | 期间累计涨跌幅、最高/最低价及日期、日均成交量、最新估值 |

#### 关键数据

- 期间累计涨幅 **+7.19%**（6.12 → 6.56）
- 最高价 **12.73 元**（2026-02-04）
- 最低价 **6.06 元**（2025-07-01）
- 2026年1-2月曾经历大幅拉升（1月26日涨停 10.05%，2月4日涨停 10.03%），随后持续回调

## 使用方法

### 方式一：运行 Notebook（推荐）

```bash
cd notebooks
jupyter notebook 601226_dashboard.ipynb
```

逐 Cell 执行即可在 `output/` 目录下生成 HTML 面板。

### 方式二：运行脚本

```bash
python scripts/generate_dashboard.py
```

脚本会自动定位项目根目录下的 `data/` 和 `output/`，无需额外配置。

## 技术栈

- **数据获取**: Tushare Pro API（日线 OHLC + 估值指标）
- **可视化**: ECharts 5.5（K线图、成交量、折线图、柱状图）
- **运行环境**: Python 3.13+
- **图表配色**: 涨红跌绿（中国A股惯例）

## 约定

- 所有路径以项目根目录为基准，`scripts/` 中使用 `os.path` 自动定位
- `notebooks/` 中使用 `../data/` 和 `../output/` 相对路径
- 原始数据放入 `data/`，生成产物放入 `output/`，不混放
