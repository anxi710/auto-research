# 可迁移的科研工作流

[![版本 0.1.3](https://img.shields.io/badge/version-0.1.3-blue)](skills/research-workflow/SKILL.md)
[![许可证：MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![批量工具所需 Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](#环境要求)
[![zpm 1.3.1](https://img.shields.io/badge/zpm-1.3.1-blue)](skills/research-workflow/references/scripted-bulk-literature.md)
[![notebooklm-py 0.8.5](https://img.shields.io/badge/notebooklm--py-0.8.5-4285F4)](skills/research-workflow/references/scripted-bulk-literature.md)
[![rclone CLI](https://img.shields.io/badge/rclone-CLI-3F79AD)](skills/research-workflow/references/scripted-bulk-literature.md)

[English](README.md) | 简体中文

这套工具为 AI 助手提供统一的科研流程，涵盖学习、提问、实验、分析、写作和评审。
Harness 是运行助手及其工具的应用程序。
研究进展保存在文件中，因此更换 harness 后也能继续工作。

本项目的主要来源是 [Research-Starter-Kit](https://github.com/LAMDA-NeSy/Research-Starter-Kit)。
[来源说明](skills/research-workflow/references/sources.md)介绍了它的覆盖范围，以及 autoresearch、AI-Scientist、Hermes 和 Pi 等其他参考项目。
本工作流对计算类 AI 和机器学习研究提供了较详细的支持。
它不包含实验调度器或模型训练框架。

## 环境要求

使用工作流只需要一个能访问文件的 AI 助手。
Python 和工具徽章仅适用于可选的批量文献分析流程。

| 用途 | 所需工具 |
| --- | --- |
| 完整批量工具链 | Linux 或 macOS 上的 Python 3.11+。 |
| 文献库导出 | Zotero 和 zpm 1.3.1。 |
| 云端传输 | rclone 和 Google Drive 账号。 |
| 文献查询 | NotebookLM 访问权限和 notebooklm-py 0.8.5。 |

运行脚本本身支持 Python 3.9+，且只使用标准库。
外部工具有各自的依赖。
请按照[脚本流程指南](skills/research-workflow/references/scripted-bulk-literature.md#prepare-the-tools)单独安装这些工具。
本仓库不需要 `requirements.txt` 文件。

## 开始或继续研究

在你的 harness 中打开本仓库。
将下方占位内容替换为你的任务和目标研究仓库：

```text
阅读 skills/research-workflow/SKILL.md，并用它处理本次任务。
目标研究仓库是 <路径>。
我的研究主题或起始论文是 <主题或论文>。
我当前的任务是 <任务>。
使用 <语言> 编写研究记录。
在创建新记录之前，先阅读已有研究记录。
从当前任务所需的阶段开始。
```

对于新项目，助手会在目标仓库中创建 `research/STATE.md` 和 `research/BRIEF.md`。
对于已有项目，助手会保留现有记录结构，并先阅读已保存的证据。
对于独立任务，助手只创建所需的输出。

[阶段指南](skills/research-workflow/references/workflow.md)定义了研究循环：

```text
确定范围 -> 学习 -> 提出问题 -> 设计 -> 运行 -> 分析 -> 写作
```

评审可以在任何阶段进行。
新证据可以让研究回到先前的阶段。
失败的运行和负面结果会保留在项目历史中。

更换 harness 后，使用以下提示词：

```text
阅读 research-workflow skill 和 research/STATE.md。
阅读下一步操作所需的记录。
确认记录中的输出和运行中的任务仍然存在。
在已保存的约束范围内继续当前任务。
将结果和下一步操作保存到研究记录中。
```

每个 harness 提供自己的工具、凭据和权限。
关于入口文件、安装和可选的 skill 自动发现方式，请阅读 [harness 指南](docs/harnesses.md)。

## 选择本地偏好和可选流程

共享 skill 不包含个人默认设置。
你可以直接使用它，无需创建偏好文件。
如果需要保存可复用的选择，请使用[偏好指南](skills/research-workflow/references/preferences.md)及其[模板](skills/research-workflow/templates/PREFERENCES.md)。
[Zotero 与 Git 示例](skills/research-workflow/references/zotero-git-example.md)仅在你主动选择时适用。

对于几十篇或几百篇论文，请使用[批量文献分析流程](skills/research-workflow/references/bulk-literature.md)。
它介绍了一套可选的 Zotero、zpm、rclone、Google Drive 和 NotebookLM 方案。
[脚本流程指南](skills/research-workflow/references/scripted-bulk-literature.md)说明了安装、执行、恢复和输出检查方法。
其中的 NotebookLM 客户端 `notebooklm-py` 是第三方软件，使用未公开说明的接口。
生成的回答需要对照原论文检查，也不能证明已完整覆盖所有证据。

关于工作流想法或改进，请遵循[演化流程](skills/research-workflow/references/evolution.md)。
该流程区分提案、本地选择、项目约定和共享规则。
行为变更需要在限定范围内进行对照，并保存证据和恢复路径。
本工具包不提供后台工作进程，也不包含 Hermes 或 Pi 原生扩展。

## 开发与共享

修改前，请阅读[仓库结构](docs/architecture.md)和[贡献指南](CONTRIBUTING.md)。
[测试结果](tests/RESULTS.md)区分已观察到的行为和未经测试的声明。
工具包说明使用简明英语。
研究记录使用你指定的语言。

本工具包采用 [MIT 许可证](LICENSE)。
完整的 skill 包也包含一份[许可证副本](skills/research-workflow/LICENSE)。
外部工具和研究资料仍受各自的许可证与条款约束。
