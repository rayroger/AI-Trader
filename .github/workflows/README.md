# GitHub Actions Workflows for AI-Trader

This directory contains GitHub Actions workflows that enable automated trading runs in CI/CD.

## Available Workflows

### 🤖 AI-Trader Automated Trading (`ai-trader-run.yml`)

Runs the AI-Trader system automatically with configurable options for storing results and AI-powered analysis.

#### Features

- ✅ **Automated Trading Execution**: Runs AI trading agents on schedule or manually
- 📦 **Artifact Storage**: Stores trading logs, positions, and performance metrics as artifacts
- 💾 **Git Commit Option**: Optionally commits results to a dedicated branch
- 🧠 **AI Analysis**: Optional AI-powered analysis of trading results
- 🔧 **Configurable Markets**: Supports US stocks, A-shares, and cryptocurrencies

#### Manual Trigger

You can manually trigger the workflow from the GitHub Actions tab with these inputs:

- **config_file**: Path to configuration file (default: `configs/default_config.json`)
- **market_type**: Market to trade (`us`, `cn`, or `crypto`)
- **commit_results**: Whether to commit results to repository (`true`/`false`)
- **analyze_with_ai**: Whether to analyze results with AI (`true`/`false`)

#### Schedule (Optional)

The workflow can be configured to run on a schedule by uncommenting the `schedule` section:

```yaml
schedule:
  - cron: '0 9 * * 1-5'  # 9 AM UTC, Monday to Friday
```

## Setup Instructions

### 1. Configure Repository Secrets

Add the following secrets to your repository (Settings → Secrets and variables → Actions):

Required secrets:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ALPHAADVANTAGE_API_KEY`: Alpha Vantage API key for market data
- `JINA_API_KEY`: Jina AI API key for search functionality

Optional secrets:
- `OPENAI_API_BASE`: Custom OpenAI API base URL (if using proxy)
- `TUSHARE_TOKEN`: Tushare token for A-share data (if trading A-shares)

### 2. Enable GitHub Actions

1. Go to your repository's "Actions" tab
2. Enable workflows if they're disabled
3. You should see "AI-Trader Automated Trading" workflow

### 3. Run the Workflow

#### Option A: Manual Run
1. Go to Actions tab
2. Select "AI-Trader Automated Trading" workflow
3. Click "Run workflow"
4. Configure options:
   - Choose config file
   - Select market type
   - Enable/disable result commits
   - Enable/disable AI analysis
5. Click "Run workflow"

#### Option B: Scheduled Run
1. Edit `.github/workflows/ai-trader-run.yml`
2. Uncomment the `schedule` section
3. Adjust the cron schedule as needed
4. Commit and push changes

## Workflow Steps

1. **Environment Setup**
   - Checkout code
   - Setup Python 3.10
   - Install dependencies
   - Configure environment variables

2. **Data Preparation**
   - Fetch market data based on selected market type
   - Merge data into unified format

3. **Trading Execution**
   - Start MCP services in background
   - Run AI trading agent with specified configuration
   - Calculate performance metrics

4. **Optional AI Analysis**
   - Analyze results with AI agent
   - Generate insights and recommendations

5. **Results Storage**
   - Upload artifacts (logs, positions, metrics)
   - Optionally commit results to repository branch

## Artifacts

After each run, the following artifacts are uploaded:

- **Trading Logs**: Detailed logs of trading decisions
- **Position Data**: Portfolio positions over time
- **Performance Metrics**: Calculated performance statistics
- **AI Analysis** (if enabled): AI-generated analysis report
- **Run Summary**: Summary of the workflow run

Artifacts are retained for 30 days and can be downloaded from the workflow run page.

## Result Commits

When `commit_results` is enabled, results are committed to a branch named:
```
results/YYYY-MM-DD
```

This allows you to:
- Track results over time
- Compare performance across different dates
- Review historical trading decisions

## Examples

### Example 1: Run US Stock Trading

```yaml
config_file: configs/default_config.json
market_type: us
commit_results: false
analyze_with_ai: false
```

### Example 2: Run A-Share Trading with AI Analysis

```yaml
config_file: configs/default_astock_config.json
market_type: cn
commit_results: true
analyze_with_ai: true
```

### Example 3: Run Crypto Trading and Store Results

```yaml
config_file: configs/default_crypto_config.json
market_type: crypto
commit_results: true
analyze_with_ai: false
```

## Troubleshooting

### Workflow Fails at "Start MCP Services"

- Check that all required API keys are configured in secrets
- Verify environment variables are set correctly
- Review MCP services logs in artifacts

### No Data Available

- Ensure API keys are valid and have quota
- Check that market data fetch scripts are working
- Verify date ranges in configuration are valid

### AI Analysis Fails

- Verify OPENAI_API_KEY is set
- Check that metrics were calculated successfully
- Review AI analysis error logs in workflow output

## Best Practices

1. **Test Locally First**: Test configurations locally before running in Actions
2. **Use Smaller Date Ranges**: Start with small date ranges to test workflow
3. **Monitor API Usage**: Be aware of API rate limits and quotas
4. **Review Artifacts**: Always review artifacts after runs
5. **Secure Secrets**: Never commit API keys to repository

## Advanced Configuration

### Custom Workflow

You can create your own workflow based on `ai-trader-run.yml`:

1. Copy the workflow file
2. Modify steps as needed
3. Adjust inputs and secrets
4. Test with manual trigger first

### Integration with Other Tools

The workflow can be extended to:
- Send notifications (Slack, Discord, Email)
- Upload results to cloud storage (S3, GCS)
- Trigger other workflows
- Generate visual reports

## Support

For issues or questions:
- Check workflow logs in Actions tab
- Review artifacts for detailed logs
- Open an issue on GitHub
- Consult the main README.md

## License

This workflow configuration is part of the AI-Trader project and follows the same MIT license.
