
## Technical Architecture

- **Lambda**: Executes Python code triggered by user activity stream.
- **CloudWatch**: Monitors risk scores and raises alerts above a defined threshold.
- **Redshift**: Stores event and risk score data for batch analytics and ML modeling.

### Flow:
1. User actions trigger events captured via Lambda.
2. Events are enriched with risk scores and logged to CloudWatch.
3. Events are loaded into Redshift for downstream use.
