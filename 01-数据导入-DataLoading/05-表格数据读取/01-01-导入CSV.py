from langchain_community.document_loaders import CSVLoader
# # 第 1 部分: 基本加载 CSV 文件并打印记录
file_path = "/home/ericpan/Geektime/rag-in-action-fork/90-文档-Data/黑悟空/黑神话悟空.csv"

# loader = CSVLoader(file_path=file_path)
# data = loader.load()
# print("示例 1: 基本加载 CSV 文件并打印前两条记录")
# for record in data[:2]:
#     print("="*60)
#     print(record)
# print("-" * 80)

# 第 2 部分: 跳过 CSV 文件的标题行并使用自定义列名
# loader = CSVLoader(
#     file_path=file_path,
#     csv_args={
#         "delimiter": ",",
#         "quotechar": '"',
#         "fieldnames": ["种类", "名称", "说明", "等级"],
#     },
# )
# data = loader.load()

# print("示例 2: 跳过标题行并使用自定义列名")
# for record in data[:2]:
#     print(type(record), "\n")
#     print(record , "="*60)
# print("-" * 80)


# # 第 3 部分: 指定 "Name" 列作为 source_column
# loader = CSVLoader(file_path=file_path, source_column="Name")
# data = loader.load()

# print("示例 3: 使用 'Name' 列作为主要内容来源")
# for record in data[:2]:
#     print(record)
# print("-" * 80)


# 第 4 部分: 使用 UnstructuredCSVLoader 加载 CSV 文件
# from langchain_community.document_loaders import UnstructuredCSVLoader
# loader = UnstructuredCSVLoader(file_path=file_path)
# data = loader.load()
# print("示例 4: 使用 UnstructuredCSVLoader 加载文件")
# print(data[0])
# print("-" * 80)

# Self Demo with DirectoryLoader and CSVLoader
from langchain_community.document_loaders import DirectoryLoader

directory_loader = DirectoryLoader(
    path='/home/ericpan/Geektime/rag-in-action-fork/90-文档-Data/黑悟空/',
    glob="*.csv",
    #loader_cls=CSVLoader,
    show_progress=True,
    use_multithreading=True
)
data = directory_loader.load()
print("示例 5: 使用 DirectoryLoader 加载目录中的所有 CSV 文件")
print(data[0])
print("-" * 80)
