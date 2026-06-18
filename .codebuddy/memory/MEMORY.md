# ZeroUI Project Memory

## 项目概况
- **路径**: `/Users/cangcang/Documents/code/ZeroUI-/`
- **类型**: Minecraft Java Edition 资源包
- **目标**: 用 Material Design 3 风格替换原版 Minecraft UI
- **MC 版本**: 1.21+ (pack_format 34)

## 技术方案
- 使用 Python PIL (Pillow) 程序化生成所有 GUI 纹理
- 生成脚本: `generate_textures.py`
- 包含完整的 MD3 颜色令牌系统 (Surface/Container/Primary/Secondary/Tertiary/Error)
- 支持 Dark Theme 暗色主题

## 包含内容 (36 个纹理)
- 18 种容器 GUI (背包、工作台、熔炉、箱子、酿造台等)
- HUD 元素 (生命值、饥饿值、护甲、经验条、快捷栏)
- 菜单系统 (选项背景、配方书、Toast、Boss 条)
- 创造模式标签页
- 旁观模式、辅助功能、流式指示器
- 标题画面

## 设计特点
- 多层 Surface 高度系统 (表面→容器→高→最高)
- 圆角卡片 (3-14px)
- GaussianBlur 高度阴影
- 完整 outline 系统 (variant + standard)
- 可自定义: 修改 MD3 字典后重新运行生成脚本
