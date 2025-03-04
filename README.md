# 远程控制面板

这是一个由DeepSeek生成的基于 Flask 的远程控制面板，允许用户通过网页界面执行系统命令、管理文件以及查看系统信息。该面板支持 Windows 系统，并提供了简单的文件浏览和系统控制功能。

## 功能特性

- **系统控制**：通过命令行执行系统命令，支持安全模式。
- **文件管理**：浏览本地文件系统，支持驱动器、文件夹和文件的查看。
- **系统设置**：查看本机信息，包括 IP 地址、CPU 信息、磁盘信息和显卡信息。
- **关闭面板**：提供关闭面板的功能。
- **更新面板**：提供更新面板的功能（模拟）。

## 安装与运行

### 依赖安装

在运行之前，请确保已安装以下 Python 库：

```bash
pip install flask psutil GPUtil
```
运行应用
克隆或下载项目代码。

在项目目录下运行以下命令启动应用：

```bash
python app.py
```
打开浏览器，访问 http://<你的IP地址>:80 即可使用控制面板。

文件结构
app.py：主程序文件，包含 Flask 应用的路由和逻辑。

control.html：系统控制页面的 HTML 模板。

files.html：文件管理页面的 HTML 模板。

settings.html：系统设置页面的 HTML 模板。

README.md：项目说明文件。

使用说明
系统控制
在系统控制页面，用户可以输入命令并执行。支持安全模式，开启安全模式后，命令将直接执行而不显示回显。

文件管理
在文件管理页面，用户可以浏览本地文件系统。点击驱动器或文件夹可以进入相应的目录，点击文件则无法操作。

系统设置
在系统设置页面，用户可以查看本机的 IP 地址、CPU 信息、磁盘信息和显卡信息。此外，还可以关闭面板或模拟更新面板。

注意事项
该面板仅适用于 Windows 系统。

由于涉及系统命令的执行，请谨慎操作，避免执行危险命令。

文件管理功能仅支持浏览，不支持文件上传、下载或删除。

许可证
本项目采用 GNU Affero General Public License (AGPL) 许可证。详情请参阅 LICENSE 文件。

贡献
欢迎提交 Issue 和 Pull Request 来帮助改进该项目。
