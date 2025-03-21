## 为什么选择定时任务

定时任务是一种非常常见的业务场景，比如定时发送邮件、定时统计数据、定时清理数据等。
在实际开发中，我们可以使用定时任务来实现这些功能，但是定时任务的实现方式有很多种，在保证系统响应性的同时，实现了数据持续更新、复杂计算、资源优化等关键能力。
这种模式特别适合需要长期数据观察的AI分析类应用，既能满足用户即时交互需求，又能完成深度数据处理任务。

数据获取问题：如何有效地从Reddit获取相关数据
数据处理问题：如何结构化存储和处理获取的数据
AI分析问题：如何利用AI模型分析数据并提取有价值的信息
用户交互问题：如何让用户直观地设置参数和查看结果
系统架构问题：如何设计一个既能响应用户实时请求又能执行定时任务的系统

## Flask 的配置

[Automatically Load Environment Variables in Flask](https://prettyprinted.com/tutorials/automatically_load_environment_variables_in_flask/)

## 使用 `--app`

```shell
flask --app reddchat run
```

[Command Line Interface](https://flask.palletsprojects.com/en/stable/cli/#application-discovery)

## 使用SQlite

[sqlite3](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection)