import pytest
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path
import tempfile

# 添加src目录到Python路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.main import app

client = TestClient(app)


def test_upload_and_list_workflow():
    """测试完整的上传和列表工作流"""

    # 1. 首先获取当前文档列表
    response = client.get("/documents")
    assert response.status_code == 200
    initial_count = len(response.json()["documents"])

    # 2. 创建一个测试文件
    test_content = b"This is a test document for integration testing."

    # 3. 上传文件
    response = client.post(
        "/upload",
        files={"file": ("integration_test.txt", test_content, "text/plain")}
    )
    assert response.status_code == 200
    upload_data = response.json()
    assert upload_data["filename"] == "integration_test.txt"
    assert upload_data["size"] == len(test_content)

    # 4. 验证文件出现在列表中
    response = client.get("/documents")
    assert response.status_code == 200
    documents = response.json()["documents"]
    assert len(documents) == initial_count + 1

    # 5. 确认新文件在列表中
    uploaded_file = next((doc for doc in documents if doc["name"] == "integration_test.txt"), None)
    assert uploaded_file is not None
    assert uploaded_file["size"] == len(test_content)


def test_multiple_file_uploads():
    """测试多个文件上传"""
    files_to_upload = [
        ("test1.txt", b"Content 1", "text/plain"),
        ("test2.txt", b"Content 2", "text/plain"),
    ]

    uploaded_files = []

    for filename, content, content_type in files_to_upload:
        response = client.post(
            "/upload",
            files={"file": (filename, content, content_type)}
        )
        assert response.status_code == 200
        uploaded_files.append(response.json())

    # 验证所有文件都上传成功
    assert len(uploaded_files) == 2
    for i, upload_result in enumerate(uploaded_files):
        expected_filename = f"test{i + 1}.txt"
        assert upload_result["filename"] == expected_filename


def test_api_endpoints_integration():
    """测试所有API端点的集成"""

    # 测试根端点
    response = client.get("/")
    assert response.status_code == 200

    # 测试健康检查
    response = client.get("/health")
    assert response.status_code == 200

    # 测试文档列表
    response = client.get("/documents")
    assert response.status_code == 200

    # 测试上传（使用小文件）
    response = client.post(
        "/upload",
        files={"file": ("api_test.txt", b"API integration test", "text/plain")}
    )
    assert response.status_code == 200