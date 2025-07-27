
# User Behavior & Risk Analytics Platform

This project builds a real-time analytics platform to monitor and assess user behavior for risk, ensuring platform integrity and enabling proactive mitigation.

## Overview
- Assigns risk scores to users based on behavioral patterns and anomalies.
- Uses Lambda functions and CloudWatch for real-time alerting.
- Loads data to Redshift to support downstream ML model training.

## Directory Structure
- `code/` : Scripts for Lambda functions, Redshift integration, and monitoring setup.
- `data/` : Sample dataset used for simulation and testing.
- `docs/` : Detailed explanation of the architecture and system design.

## Tech Stack
- AWS Lambda, Redshift, CloudWatch
- Python (boto3, pandas), SQL
