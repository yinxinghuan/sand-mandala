# Technical

## 1. 技术栈

- 游戏：Sand Mandala
- 类型：casual
- 简述：Draw a kaleidoscopic sand mandala with 4/6/8/12-fold symmetry. Frame your work or long-press the center to dissolve it — the dissolution becomes the seed of the next one.
- 框架 / 语言 / 构建：TypeScript, Vite
- 渲染方式：Canvas/WebGL
- 依赖摘录：vite@^5.1.0
- 平台元信息：meta.title=Sand Mandala；cover_url=/poster.png；category=casual；uuid=4fad1cd0-4f60-4ba5-a14c-4853dd556cdc

## 2. 目录结构

- `index.html`：Vite/浏览器入口，挂载根节点和基础 meta。
- `vite.config.js`：配置构建、插件和相对路径 base。
- `package.json`：定义 npm 脚本、依赖和工程名称。
- `meta.json`：平台发布元信息，包含标题和封面。

关键源码模块：

- `src/`：源码目录。

## 3. 核心模块

- 状态管理与主循环：通过模块级状态、对象引用和 `requestAnimationFrame` 推进游戏帧。
- 渲染方式：Canvas/WebGL，样式由 CSS/Less 和组件结构共同完成。
- 碰撞 / 更新：未发现独立物理引擎，主要由用户操作和状态切换驱动。
- 音频：包含程序化音频或音频文件播放，按交互事件触发。
- 多语言：包含 i18n / locale 检测或 `t()` 文案函数。
- 存储：使用 localStorage、useGameSave 或 persist 保存分数、收藏、墙数据或本地状态。
- Aigram 运行时：接入 `@shared/runtime` 或平台桥接能力，用于用户、资料页、分享、通知或平台 API。
- 社交墙 / 归档：包含 wall、gallery、feed 或 archive 数据流与浏览界面。

## 4. 扩展点

- 改玩法参数：优先查找 `src/` 内大写常量、hooks、主组件顶部配置或关卡数组。
- 换素材：替换 `public/`、`src/img/` 或源码 import 的图片/音频文件，并保持相对路径。
- 调视觉：修改主样式文件中的颜色、间距、动画时长、网格尺寸和响应式规则。
- 改文案：修改 i18n 字典、组件内标题按钮文案，保持 zh/en 同步。
- 加平台能力：在已有 `@shared/runtime`、useGameSave、排行榜、墙或通知调用附近扩展，避免另起一套存储。
