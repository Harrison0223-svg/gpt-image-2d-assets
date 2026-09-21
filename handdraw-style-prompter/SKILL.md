---
name: handdraw-style-prompter
description: 从 001–261 原图风格库、G01–G24 游戏风格配方、自定义参考或混合方向选择 2D 画风，生成提示词或图片；制作游戏资源时衔接 gpt-image-2d-assets 的统一生产与审核流程。
metadata:
  short-description: 261 原图风格与 24 游戏风格配方
---

# 可选风格库与提示词

保留原编号与图库，扩展可用于 2D 资产的画法。按用户的真实意图路由，不把所有请求默认缩成提示词。

## 入口

- 有编号与主题、没有生图意图：默认输出中文和英文提示。英文版应真正翻译主题与约束，不只是添加英文标签。
- 要浏览：原库打开 `gallery/index.html`，扩展打开 `gallery/extensions.html`。有有效编号时只查对应条目，不自动打开全库。若浏览工具策略阻止本地页，改为在对话中列出相关编号和文字特征；不绕过拒绝，不声称浏览页已打开。
- 自然语言找风格：`python scripts/style_catalog.py --search <关键词>`；查单项用 `--style 063` 或 `--style G03`。搜索无结果时根据现有条目语义给候选，不能虚构命中。
- 要生成插画/图片：内置 GPT Image 执行，按下述参考规则并实际看图审核。
- 要角色、图标、组件、场景、动作表或特效等资产：读取同级 `../gpt-image-2d-assets/SKILL.md`，由其完成本次生产，不在两个入口间重复路由或停在提示词。

## 风格到提示

原库 `references/styles.json` 保持为 001–261 权威索引；扩展 `references/game-styles.json` 使用 G 前缀，无样图项明确为文字配方。`scripts/style_catalog.py` 统一查询两者。允许自定义及混合，不要求用户只能选编号。

分离画法和示例内容：条目中的人物、道具、故事、背景与布局不自动进入提示。用户主题、画幅、文字及资源要求优先。提示包括风格编号/名称、适用视觉特征与主题；原作者名可保留为索引标签。`scripts/prompt_style.py` 是旧版编号文本拼接助手，不是完整翻译器或最终生产提示。

更多混合、游戏适配和风格锁定规则见同级 `../gpt-image-2d-assets/references/style-selection.md`；仅在这些任务需要时读取。

## 图像引用与审核

原库运行 `python scripts/resolve_reference.py --style <编号>`，默认图像后端 unknown。只有本次可证实的后端才传 `--model`；旧 `model_capabilities.json` 是历史建议，不保证当前激活效果。Astra 主模型不等于图像后端。

返回 reference-image 时先打开实际图片再按当前工具 schema 引用，读 [参考隔离](references/reference-image.md)。用户明确提供的风格参考优先于历史路由。G 系列没有既有图像时用文字特征，不传虚构参考路径。生成/修改只用内置 GPT Image，不使用外部生成器或代码替代美术。

主任务检查实际结果的主体与视觉语言，保留原图、提示、引用编号/作用、路径和审核结果；在已授权范围内修复具体缺陷并复核。不要固定只准一次修复，也不要无限重试。确认额度/权限问题时停止受影响调用并保留成功结果。未实际生图的配方不得标成验证通过。
