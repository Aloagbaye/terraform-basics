# ML Platform on GCP with Terraform

A complete, production-ready ML platform infrastructure on Google Cloud Platform (GCP) using Terraform. This project demonstrates event-driven MLOps with automated pipeline orchestration, model deployment, and monitoring.

## 🏗️ Architecture Overview

This project implements a full ML platform architecture with the following components:

```
┌──────────────┐
│ Data Sources │
└──────┬───────┘
       ↓
┌──────────────┐
│ Pub/Sub      │  ← Event-driven messaging
└──────┬───────┘
       ↓
┌──────────────┐
│ Cloud        │  ← Event routing & orchestration
│ Functions    │
└──────┬───────┘
       ↓
┌──────────────┐
│ Vertex AI    │  ← ML pipeline execution
│ Pipelines    │
└──────┬───────┘
       ↓
┌──────────────┐
│ Vertex AI    │  ← Model registry & serving
│ Endpoints    │
└──────────────┘
```

### Key Components

- **Infrastructure as Code (Terraform)**: All GCP resources defined and managed via Terraform
- **Pub/Sub**: Event-driven messaging for decoupled ML workflows
- **Cloud Functions**: Serverless orchestration layer for ML pipeline triggers
- **Vertex AI Pipelines**: Reproducible ML workflows with full lineage tracking
- **GCS Buckets**: Data and artifact storage
- **IAM**: Least-privilege service accounts and permissions

## ✨ Features

- ✅ **Infrastructure as Code**: Complete Terraform configuration for all GCP resources
- ✅ **Event-Driven MLOps**: Pub/Sub triggers ML pipelines automatically
- ✅ **Multi-Environment Support**: Separate dev/prod configurations
- ✅ **Programmatic Pipeline Execution**: Run pipelines via Python scripts or CLI
- ✅ **Automated IAM**: Service accounts with least-privilege permissions
- ✅ **Cloud Function Integration**: Serverless event handlers for ML workflows
- ✅ **Vertex AI Integration**: Full ML pipeline lifecycle management

## 📋 Prerequisites

Before you begin, ensure you have:

1. **GCP Account** with billing enabled
2. **GCP Project** with the following APIs enabled:
   - Cloud Functions API
   - Cloud Build API
   - Vertex AI API
   - Pub/Sub API
   - Cloud Storage API
3. **Terraform** >= 1.0 installed
4. **Python** >= 3.9 installed
5. **gcloud CLI** installed and authenticated
6. **gsutil** installed (comes with gcloud CLI)

### Authentication

```bash
# Authenticate with GCP
gcloud auth login
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd terraform-basics
```

### 2. Configure Variables

Copy the example tfvars file and update with your values:

```bash
cp terraform.tfvars.example terraform.tfvars
# Or use environment-specific files
cp envs/dev.tfvars.example envs/dev.tfvars
```

Edit `envs/dev.tfvars`:

```hcl
project_id              = "your-gcp-project-id"
region                  = "us-central1"
environment             = "dev"
service_account_name    = "dev-ml-sa"
pubsub_topic_name       = "ml-events"
pubsub_subscription_name = "ml-events-sub"
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Review and Apply

```bash
# Review what will be created
terraform plan -var-file="envs/dev.tfvars"

# Apply the configuration
terraform apply -var-file="envs/dev.tfvars"
```

### 5. Prepare ML Pipeline

```bash
# Install pipeline dependencies
cd pipelines/simple_pipeline
pip install -r requirements.txt

# Compile the pipeline
python compile.py
cd ../..
```

### 6. Upload Pipeline to GCS

```bash
python scripts/upload_pipeline.py \
  --bucket $(terraform output -raw bucket_name) \
  --pipeline pipelines/simple_pipeline/simple_pipeline.json
```

### 7. Deploy Cloud Function

```bash
# Create zip file for Cloud Function
cd functions/ml_event_handler
zip -r ../../ml-event-handler.zip .
cd ../..

# Upload to GCS
gsutil cp ml-event-handler.zip gs://$(terraform output -raw bucket_name)/

# Redeploy (if needed)
terraform apply -var-file="envs/dev.tfvars"
```

## 📁 Project Structure

```
terraform-basics/
├── envs/                          # Environment-specific configurations
│   ├── dev.tfvars                 # Development environment
│   └── prod.tfvars                # Production environment
├── functions/                      # Cloud Functions source code
│   └── ml_event_handler/
│       ├── main.py                # Event handler function
│       └── requirements.txt       # Python dependencies
├── pipelines/                     # Vertex AI Pipelines
│   └── simple_pipeline/
│       ├── pipeline.py            # Pipeline definition
│       ├── compile.py             # Compilation script
│       ├── requirements.txt       # Pipeline dependencies
│       └── simple_pipeline.json   # Compiled pipeline
├── scripts/                       # Utility scripts
│   ├── run_pipeline.py            # Part C: Programmatic execution
│   ├── upload_pipeline.py         # Upload pipeline to GCS
│   └── test_pubsub_event.py       # Test Pub/Sub events
├── cloud_function.tf              # Cloud Function resource
├── iam.tf                         # IAM roles and permissions
├── main.tf                        # Storage bucket resources
├── outputs.tf                     # Terraform outputs
├── providers.tf                   # Provider configuration
├── pubsub.tf                      # Pub/Sub topics and subscriptions
├── variables.tf                   # Variable definitions
├── vertex_ai.tf                   # Vertex AI service enablement
├── PIPELINE_GUIDE.md              # Detailed pipeline documentation
└── README.md                      # This file
```

## 🔧 Configuration

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `project_id` | GCP Project ID | `my-project-123` |
| `region` | GCP region | `us-central1` |
| `environment` | Environment name | `dev` or `prod` |
| `service_account_name` | Service account ID | `dev-ml-sa` |
| `pubsub_topic_name` | Pub/Sub topic base name | `ml-events` |
| `pubsub_subscription_name` | Pub/Sub subscription base name | `ml-events-sub` |

### Terraform Outputs

After applying, you can access outputs:

```bash
# Get bucket name
terraform output bucket_name

# Get service account email
terraform output service_account_email

# Get Pub/Sub topic
terraform output pubsub_topic

# Get pipeline root
terraform output pipeline_root
```

## 📖 Usage Guide

### Part A: Infrastructure Setup

Deploy all infrastructure resources:

```bash
terraform apply -var-file="envs/dev.tfvars"
```

This creates:
- GCS bucket for data and artifacts
- Pub/Sub topic and subscription
- Service accounts with IAM permissions
- Cloud Function (2nd gen)
- Required GCP APIs

### Part B: ML Pipeline Development

1. **Develop your pipeline** in `pipelines/simple_pipeline/pipeline.py`
2. **Compile the pipeline**:
   ```bash
   cd pipelines/simple_pipeline
   python compile.py
   ```
3. **Upload to GCS**:
   ```bash
   python scripts/upload_pipeline.py \
     --bucket YOUR_BUCKET \
     --pipeline pipelines/simple_pipeline/simple_pipeline.json
   ```

### Part C: Programmatic Pipeline Execution

Run pipelines programmatically from Python or CLI:

```bash
python scripts/run_pipeline.py \
  --project-id $(terraform output -raw project_id) \
  --bucket $(terraform output -raw bucket_name) \
  --service-account $(terraform output -raw service_account_email) \
  --event-type new_data_arrived
```

Or in Python:

```python
from scripts.run_pipeline import run_pipeline

job = run_pipeline(
    project_id="your-project",
    region="us-central1",
    bucket_name="your-bucket",
    pipeline_json_path="pipelines/simple_pipeline/simple_pipeline.json",
    service_account_email="your-sa@project.iam.gserviceaccount.com",
    event_type="retrain_model"
)
```

### Part D: Event-Driven Pipeline Triggers

Send Pub/Sub events to trigger pipelines automatically:

```bash
python scripts/test_pubsub_event.py \
  --project-id $(terraform output -raw project_id) \
  --topic ml-events-dev \
  --event-type new_data_arrived
```

**Supported Event Types:**
- `new_data_arrived` - Trigger data validation pipeline
- `retrain_model` - Trigger model retraining
- `deploy_model` - Trigger model deployment
- `manual_run` - Manual pipeline execution

The Cloud Function automatically:
1. Receives the Pub/Sub event
2. Parses the event type
3. Submits the appropriate Vertex AI Pipeline job
4. Logs the job ID and status

## 🧪 Testing

### Test Infrastructure

```bash
# Validate Terraform configuration
terraform validate

# Check plan
terraform plan -var-file="envs/dev.tfvars"
```

### Test Pipeline Compilation

```bash
cd pipelines/simple_pipeline
python compile.py
# Should create simple_pipeline.json
```

### Test Pub/Sub Event

```bash
python scripts/test_pubsub_event.py \
  --project-id YOUR_PROJECT \
  --topic ml-events-dev \
  --event-type new_data_arrived \
  --data '{"data_path": "gs://bucket/data.csv"}'
```

### Test Cloud Function

```bash
# Check function logs
gcloud functions logs read ml-event-handler-dev \
  --region us-central1 \
  --limit 50
```

### Test Pipeline Execution

```bash
# List pipeline jobs
gcloud ai pipeline-jobs list --region us-central1

# View specific job
gcloud ai pipeline-jobs describe JOB_ID --region us-central1
```

## 🔍 Monitoring

### View Cloud Function Logs

```bash
gcloud functions logs read ml-event-handler-dev \
  --region us-central1
```

### View Pipeline Runs

- **Console**: [Vertex AI Pipelines](https://console.cloud.google.com/vertex-ai/pipelines)
- **CLI**:
  ```bash
  gcloud ai pipeline-jobs list --region us-central1
  ```

### View Pub/Sub Messages

- **Console**: [Pub/Sub Topics](https://console.cloud.google.com/cloudpubsub)
- **CLI**:
  ```bash
  gcloud pubsub subscriptions pull ml-events-sub-dev --limit 10
  ```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Permission Denied Errors

**Problem**: Service account lacks required permissions

**Solution**: Verify IAM bindings:
```bash
gcloud projects get-iam-policy $(terraform output -raw project_id) \
  --flatten="bindings[].members" \
  --filter="bindings.members:*$(terraform output -raw service_account_email)"
```

#### 2. Pipeline Template Not Found

**Problem**: Pipeline JSON not uploaded to GCS

**Solution**:
```bash
python scripts/upload_pipeline.py \
  --bucket $(terraform output -raw bucket_name) \
  --pipeline pipelines/simple_pipeline/simple_pipeline.json
```

#### 3. Cloud Function Timeout

**Problem**: Function times out before completing

**Solution**: Increase timeout in `cloud_function.tf`:
```hcl
timeout_seconds = 300  # 5 minutes
```

#### 4. Module Not Found (kfp)

**Problem**: `ModuleNotFoundError: No module named 'kfp'`

**Solution**:
```bash
pip install kfp
```

#### 5. Terraform Apply Fails on Windows

**Problem**: `-var-file` syntax issues in PowerShell

**Solution**: Use quotes around the path:
```powershell
terraform apply -var-file="envs/dev.tfvars"
```

## 🔐 Security Best Practices

- ✅ **Least-Privilege IAM**: Service accounts only have required permissions
- ✅ **Environment Isolation**: Separate resources for dev/prod
- ✅ **No Hardcoded Secrets**: All sensitive data in variables
- ✅ **Service Account Keys**: Not used; leveraging Workload Identity
- ✅ **Bucket Access**: Uniform bucket-level access enabled

## 📚 Additional Documentation

- **[PIPELINE_GUIDE.md](PIPELINE_GUIDE.md)**: Complete guide for Parts C & D
- **[PARTS_C_D_SUMMARY.md](PARTS_C_D_SUMMARY.md)**: Quick reference for pipeline integration

## 🗑️ Cleanup

To destroy all resources:

```bash
terraform destroy -var-file="envs/dev.tfvars"
```

**Note**: This will delete all resources including:
- GCS buckets (if `force_destroy = true` in dev)
- Pub/Sub topics and subscriptions
- Cloud Functions
- Service accounts
- IAM bindings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [Terraform GCP Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Vertex AI Pipelines Documentation](https://cloud.google.com/vertex-ai/docs/pipelines)
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)

## 💡 Next Steps

- Add more complex ML pipelines (training, evaluation, deployment)
- Implement model monitoring and drift detection
- Add CI/CD integration (GitHub Actions workflow included)
- Set up alerting for pipeline failures
- Implement canary deployments for models

---

**Built with ❤️ using Terraform and GCP**
