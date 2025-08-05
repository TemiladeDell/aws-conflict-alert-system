**Conflict Zone Alert System (Terraform + AWS)**

The **Conflict Zone Alert System** is an automated cloud-based application that monitors global conflict data in real-time and sends email alerts when relevant conflict events are detected. It leverages **AWS Lambda**, **EventBridge**, **SNS**, and is fully provisioned using **Terraform**.

This project demonstrates how Infrastructure as Code (IaC), serverless computing, and third-party APIs can be combined to create real-world alerting systems suitable for use in journalism, humanitarian aid, and global security awareness.

---

**Features**

- **Automated Alerts**: Detects and sends email notifications for conflict-related events.
- **Serverless Architecture**: Powered by AWS Lambda for cost efficiency and scalability.
- **Scheduled Event Trigger**: Uses EventBridge to schedule periodic data fetching.
- **Clean Infrastructure as Code**: Entire infrastructure is defined and reproducible using Terraform.
- **Modular Design**: Easily extendable for SMS, Slack, or mobile push notifications.

---

**How It Works**

1. **EventBridge Scheduler** triggers a Lambda function at defined intervals.
2. The **Lambda function** queries an external conflict data API.
3. If relevant conflict data is found, it publishes a message to an **SNS topic**.
4. **SNS** sends an email notification to all subscribed users.

---

**Tech Stack**

- **AWS Lambda**
- **Amazon EventBridge**
- **Amazon SNS (Simple Notification Service)**
- **Terraform**
- **Python (Lambda Function)**
- **Public Conflict Data API**

---

**Project Structure**

conflict-zone-alert/
├── main.py # Lambda function to fetch and process conflict data
├── lambda.tf # Terraform config for Lambda
├── eventbridge.tf # Terraform config for EventBridge rule
├── sns.tf # Terraform config for SNS topic and subscription
├── iam.tf # IAM roles and policies for Lambda
├── provider.tf # AWS provider setup
├── main.tf # Terraform root config
├── .gitignore # Git ignore rules
└── README.md # This file



**Prerequisites**

Before running this project, ensure you have:

- [AWS CLI configured](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Terraform installed](https://developer.hashicorp.com/terraform/downloads)
- AWS account with appropriate permissions
- A verified email address for SNS subscription
- Your own conflict data API key (insert in `main.py`)


**Setup Instructions**

1. Clone the Repository

**bash**
git clone https://github.com/TemiladeDell/aws-conflict-alert-system.git
cd aws-conflict-alert-system
2. Update main.py
Insert your conflict data API key where required.

3. Initialize and Deploy Terraform
terraform init
terraform apply
Confirm the SNS email subscription manually after Terraform creates it (check your inbox).

Example Alert Email
Subject: Conflict Alert - Nigeria
Message: Protest reported in Lagos State. Monitor the situation closely.
Timestamp: 2025-08-05T12:45Z

**Future Improvements**
Add SMS or WhatsApp notifications via Twilio or AWS Pinpoint

Store conflict event logs in S3 or DynamoDB

Add a front-end dashboard using React or Svelte

Integrate Docker and Kubernetes for advanced deployments

**License**
This project is open-source and available under the MIT License.

**Author**
Temilade Dell
Cloud Enthusiast | Terraform Practitioner | AWS Learner
[LinkedIn](www.linkedin.com/in/temilade-akinyimika-dell001) | [Medium](https://medium.com/@temiladedell)
