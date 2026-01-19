---
name: hcp-terraform
description: HCP Terraform (Terraform Cloud) workflow for remote plan and apply. Use when working with Terraform that runs in Terraform Cloud, not locally.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, WebFetch
---

# HCP Terraform (Terraform Cloud)

Workflow for Terraform projects that use HCP Terraform (formerly Terraform Cloud) for remote execution.

## Key Constraint

**You cannot apply locally.** All plans and applies run in HCP Terraform.

## Setup

### Authentication

```bash
# Login to Terraform Cloud
terraform login

# Credentials stored in ~/.terraform.d/credentials.tfrc.json
```

### Backend Configuration

```hcl
# backend.tf
terraform {
  cloud {
    organization = "your-org"

    workspaces {
      name = "your-workspace"
    }
  }
}
```

Or with tags for multiple workspaces:

```hcl
terraform {
  cloud {
    organization = "your-org"

    workspaces {
      tags = ["app:myapp"]
    }
  }
}
```

## Workflow

### 1. Initialize

```bash
terraform init
```

This connects to HCP Terraform and sets up remote state.

### 2. Plan (Remote)

```bash
terraform plan
```

The plan runs in HCP Terraform. Output is streamed to your terminal.

### 3. Apply (Remote)

```bash
terraform apply
```

**Note:** For workspaces with auto-apply disabled, you may need to approve in the UI.

### 4. Check Run Status

```bash
# Using the TFC API
TFC_TOKEN=$(jq -r '.credentials."app.terraform.io".token' ~/.terraform.d/credentials.tfrc.json)

curl -s \
  -H "Authorization: Bearer $TFC_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  "https://app.terraform.io/api/v2/organizations/YOUR_ORG/workspaces/YOUR_WORKSPACE" \
  | jq '.data.attributes | {auto_apply, latest_change: .["latest-change-at"], resources: .["resource-count"]}'
```

### Makefile Target (from ethertext)

```makefile
TFC_ORG := your_org
TFC_WORKSPACE := your_workspace
TFC_TOKEN_FILE := $(HOME)/.terraform.d/credentials.tfrc.json

tfc-status:
	@test -f $(TFC_TOKEN_FILE) || (echo "Error: No TFC credentials. Run 'terraform login' first." && exit 1)
	@TFC_TOKEN=$$(jq -r '.credentials."app.terraform.io".token' $(TFC_TOKEN_FILE)) && \
	RESPONSE=$$(curl -s -H "Authorization: Bearer $$TFC_TOKEN" -H "Content-Type: application/vnd.api+json" \
		"https://app.terraform.io/api/v2/organizations/$(TFC_ORG)/workspaces/$(TFC_WORKSPACE)") && \
	echo "$$RESPONSE" | jq -r '.data.attributes | "Workspace: $(TFC_WORKSPACE)\nAuto-apply: \(.["auto-apply"])\nLast change: \(.["latest-change-at"])\nResources: \(.["resource-count"])"'
	@echo "View runs: https://app.terraform.io/app/$(TFC_ORG)/workspaces/$(TFC_WORKSPACE)/runs"
```

## Variables

### Workspace Variables

Set in HCP Terraform UI or via API:

1. Go to Workspace → Variables
2. Add Terraform variables (for `.tf` files)
3. Add Environment variables (for providers, e.g., `AWS_ACCESS_KEY_ID`)

### Sensitive Variables

Mark sensitive variables in the UI. They won't be shown in logs.

### Variable Sets

For variables shared across workspaces:

1. Organization Settings → Variable Sets
2. Create set with common variables
3. Apply to workspaces by tag or name

## Common Patterns

### AWS Provider

```hcl
provider "aws" {
  region = var.aws_region

  # Credentials come from TFC environment variables:
  # AWS_ACCESS_KEY_ID
  # AWS_SECRET_ACCESS_KEY
}
```

### S3 Resources (ethertext pattern)

```hcl
resource "aws_s3_bucket" "website" {
  bucket = "myapp-website"
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
```

### CloudFront Distribution

```hcl
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.website.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.website.id}"
  }

  enabled             = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.website.id}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

## Troubleshooting

### Token Expired

```bash
# Re-authenticate
terraform login
```

### Workspace Not Found

```bash
# List workspaces
terraform workspace list

# Select workspace
terraform workspace select workspace-name
```

### Plan Pending Approval

Go to HCP Terraform UI → Workspace → Runs → Approve or discard.

### Locked State

If state is locked from a failed run:

1. Go to HCP Terraform UI
2. Workspace → Settings → Locking
3. Unlock (or wait for timeout)

## CLI Commands Reference

```bash
# Initialize (required first)
terraform init

# Format check
terraform fmt -check

# Validate configuration
terraform validate

# Plan (runs remotely)
terraform plan

# Apply (runs remotely)
terraform apply

# Show current state (fetches from remote)
terraform show

# Output values
terraform output

# Import existing resource
terraform import aws_s3_bucket.example bucket-name
```

## Best Practices

1. **Never hardcode secrets** - Use TFC variables
2. **Use workspaces per environment** - dev, staging, prod
3. **Enable Sentinel policies** - For compliance
4. **Review plans before apply** - Disable auto-apply for production
5. **Use run triggers** - Chain dependent workspaces
6. **Lock provider versions** - Prevent unexpected upgrades

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```
