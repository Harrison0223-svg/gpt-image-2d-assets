# 检查与合成工具

需要 Python 3 和 Pillow。优先使用已有运行环境；脚本不联网，不调用生成器。`--out` 必须是新目录或空目录，重跑用新版本目录，不覆盖原图。

## Alpha 测量与三底色预览

```powershell
python "<skill-dir>/scripts/asset_tools.py" inspect "<asset.png>" --out "<new-review-dir>"
```

输出 `measurements.json` 与 `backgrounds.png`。报告保留原始模式、Alpha分布、阈值包围盒和SHA256；RGB图转换用于测量不代表添加了有效透明。退出码0只代表检查完成，`content_state=fully_opaque/empty`可能正是待拒绝结果。主agent仍须打开实际预览。

预览按统一比例缩至最多900像素单边。检查原始像素可增大 `--max-side` 或直接打开有问题区域的原图，不拿缩略图证明复杂边缘全部干净。

## 明确裁框与时间的序列

创建项目内JSON，`source`相对JSON文件所在目录解析，也可用绝对路径。一个示例（坐标与时长需换成实际资产值）：

```json
{
  "canvas": [520, 444],
  "repeat": false,
  "preview_background": "#303840",
  "frames": [
    {"source": "sheet.png", "crop": [0, 0, 444, 444], "offset": [40, 0], "duration_ms": 120},
    {"source": "sheet.png", "crop": [444, 0, 887, 444], "offset": [40, 0], "duration_ms": 80}
  ]
}
```

```powershell
python "<skill-dir>/scripts/asset_tools.py" assemble "<sequence.json>" --out "<new-frames-dir>"
```

- `crop` 是原图矩形 `[left, top, right, bottom]`，右下不包含；省略则取整图。
- `offset` 是裁图左上放入共享画布的坐标；省略为`[0,0]`。不自动对齐人物。
- `duration_ms` 必填，GIF要求正的10ms倍数。不要静默舍入动作时长。
- `repeat` 默认false，单次播放；true为无限循环审核。循环审核不证明首尾连续。
- 每帧可附 `anchor`、`events`，脚本原样记录，解释由项目约定。

输出完整RGBA帧PNG、固定底色GIF及 `assembly.json`。先验证所有裁框、放置与时长，再写输出；越界或裁图放不下会报错，不静默截肢。脚本不自动推断网格，不清理透明、不缩放人物、不生成中间帧。

RGBA裁图像素原样复制；透明补边是技术组装。GIF只是预览，编码可能合并相同帧，报告保存实际帧数和总时长；PNG序列保持所有输入帧。

维护脚本时运行：

```powershell
python "<skill-dir>/scripts/test_asset_tools.py"
```

测试验证透明分类、精确裁切/补边、GIF时长、越界拒绝和非覆盖行为，不替代真实美术审查。
