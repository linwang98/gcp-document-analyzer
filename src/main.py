# CI/CD test
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Document Analyzer API", version="1.0.0")

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建本地存储目录
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Document Analyzer API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "document-analyzer"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    上传文档到本地存储
    """
    try:
        # 验证文件类型
        allowed_types = ["application/pdf", "text/plain", "image/jpeg", "image/png"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not supported"
            )

        # 读取文件内容
        content = await file.read()

        # 保存到本地
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        logger.info(f"File {file.filename} uploaded successfully")

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "size": len(content),
            "type": file.content_type,
            "local_path": str(file_path)
        }

    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/documents")
async def list_documents():
    """
    列出所有上传的文档
    """
    try:
        documents = []
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                documents.append({
                    "name": file_path.name,
                    "size": stat.st_size,
                    "created": stat.st_mtime,
                })

        return {"documents": documents}

    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
