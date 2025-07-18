# 指定Terraform版本和provider
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

# 配置Google Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# 变量定义
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

# 创建存储桶
resource "google_storage_bucket" "document_storage" {
  name     = "${var.project_id}-documents"
  location = var.region
  
  # 防止意外删除
  lifecycle {
    prevent_destroy = true
  }
}

# 输出存储桶名称
output "bucket_name" {
  value = google_storage_bucket.document_storage.name
}