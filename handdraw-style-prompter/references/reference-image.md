# Reference image isolation

Use this for any style-only image reference, including user-supplied references and resolver results. Inspect the actual local image before passing it to generation.

Use the relevant language block in the image-generation prompt (both are not required):

Chinese: `所附图片仅用于参考画风。只提取参考图的线条、笔触、媒介、材质、色彩倾向和整体视觉语言；不要使用、复制或延续其中的任何主体、人物、动物、服装、道具、动作、姿态、场景、背景、构图、布局、文字或故事。最终画面内容完全以用户提供的主题为准。`

English: `Use the attached image only as a style reference. Extract only linework, brushwork, medium, material texture, color tendencies, and overall visual language. Do not use, copy, or carry over any subject, person, animal, clothing, prop, action, pose, setting, background, composition, layout, text, or story from the reference image. The user's written theme is the sole source for the image content.`
