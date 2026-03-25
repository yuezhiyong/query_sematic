大语言模型的应用远不止聊天机器人和文本生成。利用嵌入（Embeddings），我们还可以构建搜索应用。嵌入是数据的数值化表示，也称为向量，可用于数据的语义搜索。

在本课中，你将为我们教育初创公司构建一个搜索应用。我们的初创公司是一家非营利组织，为发展中国家的学生提供免费教育。我们拥有大量 YouTube 视频，学生可以通过这些视频学习人工智能知识。我们希望构建一个搜索应用，让学生能够通过输入问题来搜索相关的 YouTube 视频。
学习
例如，学生可能会输入“什么是 Jupyter Notebooks？”或“什么是 Azure ML”，搜索应用会返回与问题相关的 YouTube 视频列表，更进一步，搜索应用还能返回视频中答案所在位置的具体链接。



本节课将涵盖以下内容：

语义搜索与关键词搜索的对比

什么是文本嵌入（Text Embeddings）

创建文本嵌入索引

搜索文本嵌入索引


完成本课程后，你将能够：

区分语义搜索与关键词搜索的不同

解释什么是文本嵌入（Text Embeddings）

使用嵌入创建一个用于搜索数据的应用程序


为什么要构建搜索应用？

构建一个搜索应用将帮助你理解如何使用嵌入来搜索数据。你还将学习如何构建一个可供学生快速查找信息的搜索应用。

本课程包含一个嵌入索引，该索引基于微软 AI Show YouTube 频道的视频转录文本构建。AI Show 是一个教授人工智能和机器学习知识的 YouTube 频道。该嵌入索引包含了截至 2023 年 10 月每个 YouTube 视频转录文本的嵌入。你将使用这个嵌入索引为我们的初创公司构建一个搜索应用。该搜索应用会返回一个指向视频中答案所在位置的链接。这对于学生快速找到所需信息来说是一种极好的方式。

以下是一个语义查询的示例，问题是“能否在 Azure ML 中使用 RStudio？”。查看 YouTube 链接，你会发现链接中包含一个时间戳，可以直接定位到视频中答案所在的位置。





什么是语义搜索？

现在你可能会想，什么是语义搜索？语义搜索是一种利用查询中词语的语义或含义来返回相关结果的搜索技术。

这里有一个语义搜索的例子。假设你想买一辆车，你可能会搜索“my dream car”。语义搜索能够理解你并非真的在做关于车的梦，而是在寻找你理想中的车。语义搜索理解你的意图，并返回相关的结果。

与之相对的是关键词搜索，它会字面地去搜索“关于车的梦”，通常会返回不相关的结果。



什么是文本嵌入？

文本嵌入是自然语言处理中使用的一种文本表示技术。文本嵌入是文本的语义数值化表示。嵌入用于以机器易于理解的方式来表示数据。有许多模型可用于构建文本嵌入，在本课中，我们将重点介绍如何使用 OpenAI 嵌入模型生成嵌入。

以下是一个示例，假设某个 AI Show YouTube 频道剧集的转录文本中有这样一句话：

“今天我们将来学习 Azure 机器学习。”

我们将这段文本传递给 OpenAI 嵌入 API，它会返回一个由 1536 个数字组成的嵌入，即一个向量。向量中的每个数字都代表了文本的不同方面的特征。为简洁起见，这里仅展示该向量的前 10 个数字：


[-0.006655829958617687, 0.0026128944009542465, 0.008792596869170666, -0.02446001023054123, -0.008540431968867779, 0.022071078419685364, -0.010703742504119873, 0.003311325330287218, -0.011632772162556648, -0.02187200076878071, ...]

嵌入索引是如何创建的？

本课程的嵌入索引是通过一系列 Python 脚本创建的。你可以在本课程的 scripts 文件夹中的 README 文件中找到这些脚本及相关说明。你无需运行这些脚本来完成本课程，因为嵌入索引已经为你准备好了。

这些脚本执行以下操作：

下载转录文本：下载 AI Show 播放列表中每个 YouTube 视频的转录文本。

提取演讲者姓名：使用 OpenAI 函数，尝试从 YouTube 转录文本的前 3 分钟中提取演讲者姓名。每个视频的演讲者姓名都存储在名为 embedding_index_3m.json 的嵌入索引中。

文本分块：将转录文本分成 3 分钟的文本片段。每个片段会包含与下一个片段约 20 个单词的重叠，以确保片段的嵌入不会被截断，并提供更好的搜索上下文。

生成摘要：将每个文本片段传递给 OpenAI Chat API，将文本摘要为 60 个单词。摘要也存储在嵌入索引 embedding_index_3m.json 中。

生成嵌入向量：最后，将片段文本传递给 OpenAI 嵌入 API。嵌入 API 返回一个包含 1536 个数字的向量，这些数字代表了该片段的语义含义。片段及其对应的 OpenAI 嵌入向量一同存储在嵌入索引 embedding_index_3m.json 中。

向量数据库

为简化课程，嵌入索引被存储在一个名为 embedding_index_3m.json 的 JSON 文件中，并加载到 Pandas DataFrame 中使用。然而，在生产环境中，嵌入索引通常会存储在向量数据库中，例如 Azure Cognitive Search、Redis、Pinecone、Weaviate 等，这里仅举几例。



理解余弦相似度

我们已经学习了文本嵌入，下一步是学习如何使用文本嵌入来搜索数据，特别是如何通过余弦相似度找到与给定查询最相似的嵌入。

什么是余弦相似度？
余弦相似度是衡量两个向量之间相似度的一种度量，你也会听到它被称为最近邻搜索。
要执行余弦相似度搜索，你需要：

1.使用 OpenAI 嵌入 API 将查询文本向量化。
2.计算查询向量与嵌入索引中每个向量之间的余弦相似度。
3.记住，嵌入索引为每个 YouTube 转录文本片段都有一个对应的向量
4.最后，按余弦相似度对结果进行排序，余弦相似度最高的文本片段与查询最相似

从数学角度来看，余弦相似度衡量的是在多维空间中投影的两个向量之间夹角的余弦值。这种度量方式很有优势，因为如果两个文档由于大小差异而在欧几里得距离上相距甚远，它们之间仍然可能具有较小的夹角，从而具有较高的余弦相似度。

关于余弦相似度公式的更多信息，请参阅余弦相似度相关文档。


构建你的第一个搜索应用

接下来，我们将学习如何使用嵌入构建一个搜索应用程序。该搜索应用将允许学生通过输入问题进行视频搜索。搜索应用会返回与问题相关的视频列表，并且还会提供指向视频中答案所在位置的具体链接。

该解决方案已在 Windows 11、macOS 和 Ubuntu 22.04 系统上使用 Python 3.10 或更高版本进行了构建和测试。你可以从 python.org 下载 Python。



作业 - 构建一个搜索应用，赋能学生

在本课程开始时，我们介绍了自己的初创公司。现在是时候让学生们能够为他们的评估构建一个搜索应用了。

在此作业中，你将创建用于构建搜索应用的 Azure OpenAI 服务。你需要创建一个 Azure OpenAI 服务资源。完成此作业需要 Azure 订阅。

1. 启动 Azure Cloud Shell
登录到 Azure 门户。
选择 Azure 门户右上角的 Cloud Shell 图标。
选择 Bash 作为环境类型。

2. 创建资源组

按照以下说明，我们使用位于“美国东部”地区、名为 semantic-video-search 的资源组。你可以更改资源组的名称，但如果更改资源的位置，请务必查看模型可用性表。

bash
az group create --name semantic-video-search --location eastus

3. 创建 Azure OpenAI 服务资源

在 Azure Cloud Shell 中运行以下命令来创建 Azure OpenAI 服务资源。

bash
az cognitiveservices account create --name semantic-video-openai --resource-group semantic-video-search \
    --location eastus --kind OpenAI --sku s0


4. 获取端点 URL 和密钥

在 Azure Cloud Shell 中运行以下命令，以获取 Azure OpenAI 服务资源的端点 URL 和密钥。

bash
# 获取端点 URL
az cognitiveservices account show --name semantic-video-openai \
   --resource-group semantic-video-search | jq -r .properties.endpoint

# 获取密钥
az cognitiveservices account keys list --name semantic-video-openai \
   --resource-group semantic-video-search | jq -r .key1


5. 部署 OpenAI 嵌入模型

在 Azure Cloud Shell 中运行以下命令，以部署 OpenAI 嵌入模型。

bash
az cognitiveservices account deployment create \
    --name semantic-video-openai \
    --resource-group semantic-video-search \
    --deployment-name text-embedding-ada-002 \
    --model-name text-embedding-ada-002 \
    --model-version "2" \
    --model-format OpenAI \
    --sku-capacity 100 --sku-name "Standard"




说明：由于国内个人用户无法正常在Azure OpenAI服务部署模型，这里根据DeepSeek建议完全采用开源的
向量存储库+DeepSeekAPI进行向量检索。





