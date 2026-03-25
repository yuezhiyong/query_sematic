通过本课程的学习，你已经了解到一些核心概念，比如提示，甚至还有一门被称为"提示工程"的完整学科。许多你可以交互的工具，如 ChatGPT、Office 365、Microsoft Power Platform 等，都支持你使用提示来完成各种任务。
要将这样的体验添加到应用程序中，你需要理解提示、补全等概念，并选择一个合适的库来使用。这正是你将在本章中学到的内容。

概述
在本章中，你将：

了解 OpenAI 库及其核心概念

使用 OpenAI 构建一个文本生成应用程序

理解如何运用提示、温度和词元等概念来构建文本生成应用


学习目标
完成本课后，你将能够：

解释什么是文本生成应用程序

使用 OpenAI 构建一个文本生成应用程序

配置应用程序以使用更多或更少的词元，并调整温度参数，从而获得多样化的输出。


什么是文本生成应用程序？

通常，当你构建应用程序时，它会具有某种类型的界面，例如：

基于命令的：控制台应用是典型的应用程序，你输入命令，它执行任务。例如，git 就是一个基于命令的应用程序。

用户界面：一些应用程序具有图形用户界面，你可以点击按钮、输入文本、选择选项等。




控制台和UI应用的局限性

与基于命令的应用程序（你输入命令）相比：

局限性：你不能随意输入任何命令，只能输入应用程序支持的那些命令。

语言特定：有些应用程序支持多种语言，但默认情况下应用程序是为特定语言构建的，即使你可以添加更多语言支持。

文本生成应用的优势

那么，文本生成应用有何不同？

在文本生成应用中，你拥有更大的灵活性，不局限于一组命令或特定的输入语言。相反，你可以使用自然语言与应用程序交互。另一个好处是，你已经在与一个经过海量信息训练的数据源进行交互，而传统应用可能受限于数据库中的内容。

我能用文本生成应用构建什么？

你可以构建很多东西，例如：




应用类型    说明
聊天机器人  回答关于公司、产品等主题问题的聊天机器人
辅助工具    LLM擅长文本摘要、从文本中获取洞察、生成简历等任务
代码助手    根据使用的语言模型，可以构建帮助你编写代码的代码助手，如GitHub Copilot或ChatGPT

    
如何开始？
你需要找到一种与LLM集成的方式，通常有以下两种方法：



方法    说明
使用 API    通过构建包含提示的 Web 请求，并返回生成的文本
使用库  库封装了 API 调用，使其更易于使用


库/SDK

有几个知名的库用于处理LLM，例如：

openai：这个库可以轻松连接你的模型并发送提示。

还有在更高层次上操作的库，例如：

LangChain：LangChain非常知名，支持Python。

Semantic Kernel：Semantic Kernel是微软开发的库，支持C#、Python和Java语言。




使用openai的第一个应用程序

让我们看看如何构建我们的第一个应用程序，需要哪些库，需要做哪些准备等等。

安装 openai

有很多库可用于与 OpenAI 或 Azure OpenAI 进行交互。也可以使用多种编程语言，如 C#、Python、JavaScript、Java 等。我们选择使用 openai Python 库，因此我们将使用 pip 来安装它。

bash
pip install openai
创建资源

你需要执行以下步骤：

在 Azure 上创建一个账户：https://azure.microsoft.com/free/。

获取 Azure OpenAI 的访问权限。访问 https://learn.microsoft.com/azure/ai-services/openai/overview#how-do-i-get-access-to-azure-openai 并申请访问权限。

[!NOTE]
在撰写本文时，你需要申请才能访问 Azure OpenAI。

安装 Python：https://www.python.org/

创建一个 Azure OpenAI 服务资源。有关如何创建资源，请参阅此指南。

找到 API 密钥和终结点

此时，你需要告诉你的 openai 库使用哪个 API 密钥。要找到你的 API 密钥，请转到你的 Azure OpenAI 资源的“密钥和终结点”部分，并复制“密钥 1”的值。



既然你已经复制了这些信息，让我们指示库来使用它。

注意

将你的 API 密钥与代码分离是值得的。你可以通过使用环境变量来实现这一点。

将环境变量 OPENAI_API_KEY 设置为你的 API 密钥。

bash
export OPENAI_API_KEY='sk-...'



Azure 配置设置

如果你使用的是 Azure OpenAI，以下是配置设置的方法：

python
openai.api_type = 'azure'
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_version = '2023-05-15'
openai.api_base = os.getenv("API_BASE")
上面我们设置了以下内容：

api_type 设置为 azure。这告诉库使用的是 Azure OpenAI，而不是 OpenAI。

api_key，这是在 Azure 门户中找到的 API 密钥。

api_version，这是你想要使用的 API 版本。在撰写本文时，最新版本是 2023-05-15。

api_base，这是 API 的端点。你可以在 Azure 门户中 API 密钥旁边找到它。

[!NOTE]
os.getenv 是一个读取环境变量的函数。你可以使用它来读取像 OPENAI_API_KEY 和 API_BASE 这样的环境变量。在终端中设置这些环境变量，或者使用像 dotenv 这样的库来设置。


生成文本
生成文本的方式是使用 Completion 类。以下是一个示例：

python
prompt = "补全以下内容：从前有一个"

completion = openai.Completion.create(model="davinci-002", prompt=prompt)
print(completion.choices[0].text)
在上述代码中，我们创建了一个补全对象，传入了我们想要使用的模型和提示。然后我们打印出生成的文本。




