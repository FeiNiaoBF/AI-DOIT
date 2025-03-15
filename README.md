## 项目任务

本项目是开发一个 AI 应用，用于分析 *Reddit* 中的讨论内容，提取趋势和关键观点。用户可以通过在前端界面来自定义分析范围，包括但不限于：

1. 选择不同的 Reddit 版块（subreddits）
2. 时间范围（如过去一天、一周或自定义日期）。
3. 关键字（如 `AI` 等）

项目技术栈为前端使用 `React`，后端使用 `Python Flask`，数据库使用 `SQLite`(不一定使用)，开发时间为 3 周左右。

## 项目架构

前端：使用 React Nextjs 开发一个网页，支持用户通过对话式界面与 AI 交互，并调整任务配置（例如关键词或分析方法）。
后端：使用 Python Flask 实现 API，执行定时任务，获取数据，调用 AI 模型（例如 OpenAI API, DeepSeek API等）进行分析和总结，并返回结果。

## 项目核心点

1. 降低信息获取成本：无需人工浏览海量帖子，AI自动总结
2. 灵活可控：用户可自定义分析范围（**版块**、**时间**、**关键词**）
3. 交互式界面：用户可通过对话式界面与 AI 交互
4. 任务调度：定时任务获取数据，调用 AI 模型进行分析

## 项目开发步骤

1. 项目架构设计
2. API 接口设计
3. 后端逻辑实现
4. 前端界面设计
5. 前后端对接
6. 测试和部署

## 项目开发相关文档

[flask](https://flask.palletsprojects.com/en/stable/)
[AI SDK](https://sdk.vercel.ai/)
[Reddit API](https://developers.reddit.com/docs/)
