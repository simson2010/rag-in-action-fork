import unittest
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

def load_txt_document(file_path):
    """
    使用 TextLoader 加载 txt 文档。

    Args:
        file_path (str): txt 文件路径。

    Returns:
        list[Document]: 包含文档内容的 Document 对象列表。
    """
    loader = TextLoader(file_path)
    documents = loader.load()
    return documents

class TestDocumentLoading(unittest.TestCase):
    def test_load_txt_document(self):
        """
        测试 load_txt_document 函数是否能正确加载 txt 文档。
        """
        file_path = "90-文档-Data/黑悟空/黑悟空设定.txt" # 确保文件路径正确
        documents = load_txt_document(file_path)

        self.assertIsInstance(documents, list) # 检查返回结果是否为列表
        self.assertTrue(len(documents) > 0) # 检查是否加载到文档

        doc = documents[0]
        self.assertIsInstance(doc, Document) # 检查列表中的元素是否为 Document 对象
        self.assertIn("黑神话：悟空", doc.page_content) # 检查文档内容是否包含预期文本
        self.assertIn("火照黑云", doc.page_content)

if __name__ == '__main__':
    # 示例使用
    file_path = "90-文档-Data/黑悟空/黑悟空设定.txt"
    documents = load_txt_document(file_path)
    print("加载的文档:")
    print(documents)

    # 运行单元测试
    unittest.main(argv=['first-arg-is-ignored'], exit=False) # 在notebook中运行时需要这样写，避免sys.exit()