import pytest
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.main import app

# 创建测试客户端
client = TestClient(app)

def test_read_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Document Analyzer API is running!"}

def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "document-analyzer"

def test_upload_endpoint_exists():
    """测试上传端点存在（不测试实际上传，因为需要文件）"""
    # 测试没有文件的情况
    response = client.post("/upload")
    # 应该返回422 (validation error) 而不是404
    assert response.status_code == 422

def test_list_documents():
    """测试文档列表端点"""
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert isinstance(data["documents"], list)

def test_invalid_endpoint():
    """测试不存在的端点"""
    response = client.get("/nonexistent")
    assert response.status_code == 404