# PanCancer 初稿科研绘图代码

本仓库整理 **2026-11-20 story v2 初稿**的完整绘图代码，覆盖 **7 幅主图、12 幅补图**。所有绘图脚本与当时冻结交付包逐字节一致；代码 SHA256 见 [CODE_PROVENANCE.tsv](docs/CODE_PROVENANCE.tsv)。

[English README](README.md) · [全部图号映射](docs/FIGURES.md) · [外部输入要求](docs/INPUTS.md)

## 包含哪些代码

- `scripts/plotting/run_all_figures.py`：一条命令运行三个分支，组装19幅稿件图并记录57个输出文件的SHA256。
- `render_R4_portable.py`：统一UMAP、注释dotplot、模块网络、空间转录组及成像邻域等。
- `render_composition_and_LN.py`：历史组成、来源情境、淋巴结组织和分子测量图件。
- `render_story_panels.py`：免疫状态组合、临床关联及癌种情境图件。
- `verify_plot_inputs.py`：核对输入大小、SHA256及路径范围。
- `scripts/manuscript/`：英文正文、中文全译的DOCX构建和补充图PDF组装。

这是初稿冻结快照。后续UMAP直接标签修改以及Claude重绘稿是其他版本，没有替换进本快照。初稿的全部19幅图均由这三个绘图分支覆盖，不需要另找旧图PNG来拼装。

## 安装和运行

绘图原运行环境为Python 3.10.19，依赖见 `requirements-plotting.txt`；文档原运行环境为Python 3.12。若希望使用一个环境同时绘图和构建稿件，可采用Python 3.12：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

文档依赖保留原始Pillow 13.0.0版本，使用Python 3.12，不要将此文档依赖直接装进原Python 3.10绘图环境。

准备与初稿匹配的私有绘图输入包，把 `PLOT_PACKAGE` 指向其 `plotting/` 目录，即包含 `input_manifest.json` 和 `inputs/` 的目录：

```bash
export PLOT_PACKAGE=/absolute/path/to/private/review_package/plotting
export FIGURE_OUTPUT=/absolute/path/to/new_output_directory

python scripts/plotting/verify_plot_inputs.py --package-root "$PLOT_PACKAGE"
python scripts/plotting/run_all_figures.py \
  --package-root "$PLOT_PACKAGE" \
  --output "$FIGURE_OUTPUT"
```

输出目录必须不存在，以保留历史产物。`figures/` 中的稿件图号才是最终19图；`intermediate/` 保留各分支原图号和额外中间图。单分支执行、稿件构建、输出结构和校验说明见[英文README](README.md)。

## 数据和复现范围

公开仓库提供七个代码脚本、依赖、图号映射和输入格式文档；原始表达矩阵、科学结果表、展示数组、稿件正文、W/H权重和凭据不在仓库。私有配套包包含96个绘图输入，需与此初稿版本对应。

这些代码复用冻结坐标、marker统计和效应估计来重绘，不重新进行整合、注释、NMF、通讯检验或临床建模。图源精确相对路径见 [FIGURE_INPUT_MAP.tsv](docs/FIGURE_INPUT_MAP.tsv)。

UMAP、临床关联、蛋白相对状态、推断空间丰度和通讯表达分别保留其测量定义与原统计家族。文件哈希核对保障传输和输入完整性，不替代生物学验证。不同操作系统和字体可能使输出文件字节不同。

项目方法和脱敏运行轨迹保存在 [Pancancer_log](https://github.com/XX-114514/Pancancer_log)。仓库当前未选定软件许可证。
