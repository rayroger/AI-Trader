# GitHub Actions Guide for AI-Trader

This guide explains how to use GitHub Actions to automate AI-Trader runs, store results, and invoke AI agents for analysis.

## 🚀 Quick Start

### 1. Setup Repository Secrets

Before running the workflow, configure these secrets in your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets:

| Secret Name | Description | Required |
|------------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI models | ✅ Yes |
| `ALPHAADVANTAGE_API_KEY` | Alpha Vantage API key for market data | ✅ Yes |
| `JINA_API_KEY` | Jina AI API key for search | ✅ Yes |
| `OPENAI_API_BASE` | Custom OpenAI API base URL | ⚠️ Optional |
| `TUSHARE_TOKEN` | Tushare token for A-share data | ⚠️ Optional (for A-shares) |

### 2. Run Your First Workflow

1. Navigate to the **Actions** tab in your repository
2. Select **AI-Trader Automated Trading** workflow
3. Click **Run workflow** button
4. Configure options:
   - **config_file**: `configs/default_config.json` (or your custom config)
   - **market_type**: `us` (or `cn` for A-shares, `crypto` for cryptocurrencies)
   - **commit_results**: `false` (set to `true` to commit results)
   - **analyze_with_ai**: `false` (set to `true` for AI analysis)
5. Click **Run workflow**

### 3. Monitor Progress

- Watch the workflow progress in real-time
- Check logs for each step
- Review any errors or warnings

### 4. Download Results

After the workflow completes:
1. Scroll down to **Artifacts** section
2. Download `ai-trader-results-{run-number}.zip`
3. Extract and review:
   - Trading logs
   - Position data
   - Performance metrics
   - AI analysis (if enabled)

## 📋 Workflow Features

### Automated Market Data Preparation

The workflow automatically:
- Fetches latest market data based on selected market type
- Merges data into unified JSONL format
- Validates data quality

### MCP Service Management

- Starts MCP services in background
- Monitors service health
- Gracefully stops services after trading
- Captures service logs for debugging

### Trading Execution

- Runs AI trading agents with specified configuration
- Captures all trading decisions and logs
- Handles errors and retries
- Calculates performance metrics

### Result Storage Options

#### Option 1: Artifacts (Default)
- Results uploaded as workflow artifacts
- Available for download for 30 days
- Includes logs, positions, and metrics
- Does not modify repository

#### Option 2: Git Commits
- Results committed to dedicated branch
- Branch named `results/YYYY-MM-DD`
- Enables version control of results
- Allows historical comparison

### AI-Powered Analysis

When enabled, the workflow:
- Loads latest performance metrics
- Generates comprehensive analysis prompt
- Invokes OpenAI GPT-4 for insights
- Saves analysis as markdown report

## 🔧 Configuration Options

### Using Custom Configurations

Create custom config files in `configs/` directory:

```json
{
  "agent_type": "BaseAgent",
  "market": "us",
  "date_range": {
    "init_date": "2025-01-01",
    "end_date": "2025-01-31"
  },
  "models": [
    {
      "name": "my-model",
      "basemodel": "openai/gpt-4",
      "signature": "my-model-v1",
      "enabled": true
    }
  ],
  "agent_config": {
    "max_steps": 30,
    "initial_cash": 10000.0
  }
}
```

Then run workflow with:
```
config_file: configs/my-custom-config.json
```

### Market Types

#### US Stocks (`us`)
- Trades NASDAQ 100 stocks
- Uses Alpha Vantage data
- Initial capital: $10,000

#### A-Shares (`cn`)
- Trades SSE 50 stocks
- Uses Tushare data
- Initial capital: ¥100,000
- Requires `TUSHARE_TOKEN` secret

#### Cryptocurrencies (`crypto`)
- Trades BITWISE10 cryptocurrencies
- Uses Alpha Vantage crypto data
- Initial capital: 50,000 USDT

## 📊 Understanding Results

### Artifact Structure

```
artifacts/
├── agent_data/              # US stocks results
│   └── {model-signature}/
│       ├── position/
│       │   └── position.jsonl
│       ├── log/
│       │   └── {date}/
│       │       └── log.jsonl
│       └── metrics/
│           └── performance_metrics.jsonl
├── agent_data_astock/       # A-shares results
├── agent_data_crypto/       # Crypto results
├── trading_run.log          # Trading execution log
├── mcp_services.log         # MCP services log
├── ai_analysis.md           # AI analysis (if enabled)
└── summary.md               # Run summary
```

### Performance Metrics

Each `performance_metrics.jsonl` contains:

```json
{
  "id": 0,
  "timestamp": "2025-01-20T10:00:00",
  "model_name": "claude-3.7-sonnet",
  "analysis_period": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-20",
    "total_trading_days": 15
  },
  "performance_metrics": {
    "sharpe_ratio": 1.2345,
    "max_drawdown": 0.1234,
    "cumulative_return": 0.0567,
    "annualized_return": 0.1234,
    "volatility": 0.0789,
    "win_rate": 0.6000,
    "profit_loss_ratio": 1.5678
  },
  "portfolio_summary": {
    "initial_value": 10000.00,
    "final_value": 10567.00,
    "value_change": 567.00,
    "value_change_percent": 0.0567
  }
}
```

## 🤖 Using AI Analysis

### Enable AI Analysis

Set `analyze_with_ai: true` when running workflow.

### What AI Analysis Provides

1. **Performance Summary**: Overview of all models
2. **Risk Assessment**: Analysis of risk metrics
3. **Comparative Analysis**: Model comparison
4. **Recommendations**: Actionable insights
5. **Strategy Insights**: Trading pattern analysis

### Example AI Analysis Output

```markdown
# AI Trading Performance Analysis

## Overall Performance Summary

The analysis covers 3 models over 15 trading days...

## Risk-Adjusted Returns

Model A shows the highest Sharpe ratio of 1.45...

## Recommendations

1. Consider reducing position sizes for Model B...
2. Model C shows consistent alpha generation...
```

## 🔄 Scheduled Runs

### Enable Scheduled Trading

Edit `.github/workflows/ai-trader-run.yml`:

```yaml
on:
  workflow_dispatch:
    # ... existing inputs ...
  
  schedule:
    - cron: '0 9 * * 1-5'  # 9 AM UTC, Monday-Friday
```

### Common Cron Schedules

```yaml
# Every day at 9 AM UTC
- cron: '0 9 * * *'

# Weekdays only at 9 AM UTC
- cron: '0 9 * * 1-5'

# Every Monday at 8 AM UTC
- cron: '0 8 * * 1'

# Twice daily (9 AM and 5 PM UTC)
- cron: '0 9,17 * * *'
```

**Note**: Scheduled workflows use default configuration. For custom configs, use manual triggers.

## 💾 Committing Results to Repository

### Why Commit Results?

- Version control of trading history
- Track performance over time
- Compare strategies across dates
- Enable collaborative analysis

### How It Works

1. Set `commit_results: true`
2. Workflow creates branch `results/YYYY-MM-DD`
3. Commits all result files
4. Pushes to repository

### Accessing Committed Results

```bash
# List result branches
git branch -r | grep results/

# Checkout specific results
git checkout results/2025-01-20

# View results
cat data/agent_data/claude-3.7-sonnet/metrics/performance_metrics.jsonl
```

## 🛠️ Local Testing

### Test Workflow Steps Locally

Before running in GitHub Actions, test locally:

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 2. Prepare data
cd data
python get_interdaily_price.py
python merge_jsonl.py
cd ..

# 3. Start MCP services
cd agent_tools
python start_mcp_services.py &
cd ..

# 4. Run trading
python main.py configs/default_config.json

# 5. Analyze results (optional)
python scripts/analyze_results.py --config configs/default_config.json
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Workflow Fails at "Start MCP Services"

**Symptoms**: MCP services fail to start or crash

**Solutions**:
- Verify all API keys are set in secrets
- Check API key validity and quotas
- Review `mcp_services.log` in artifacts

#### 2. No Market Data Available

**Symptoms**: Trading fails with "No price data found"

**Solutions**:
- Verify `ALPHAADVANTAGE_API_KEY` is valid
- Check API rate limits
- Ensure date range is valid (not future dates)

#### 3. AI Analysis Fails

**Symptoms**: AI analysis step fails or produces errors

**Solutions**:
- Verify `OPENAI_API_KEY` is set
- Check API quota and limits
- Ensure metrics were calculated successfully

#### 4. Artifacts Too Large

**Symptoms**: Artifact upload fails due to size

**Solutions**:
- Reduce date range in configuration
- Disable unnecessary logging
- Clean up old data files

### Debug Mode

Add this step to workflow for detailed debugging:

```yaml
- name: Debug Information
  run: |
    echo "Python version:"
    python --version
    echo "Installed packages:"
    pip list
    echo "Environment variables:"
    env | grep -v "KEY\|TOKEN\|SECRET"
    echo "Directory structure:"
    ls -la
```

## 📈 Best Practices

1. **Start Small**: Test with short date ranges first
2. **Monitor Costs**: Track API usage and costs
3. **Review Regularly**: Check artifacts and logs
4. **Use Version Control**: Commit important results
5. **Document Changes**: Note configuration changes
6. **Secure Secrets**: Rotate API keys periodically
7. **Test Locally**: Validate before running in Actions

## 🔐 Security Considerations

- Never commit API keys to repository
- Use GitHub secrets for all sensitive data
- Rotate secrets regularly
- Limit workflow permissions if possible
- Review audit logs periodically

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [AI-Trader Main README](../README.md)
- [Configuration Guide](../docs/CONFIG_GUIDE.md)
- [Workflow README](.github/workflows/README.md)

## 🆘 Getting Help

If you encounter issues:

1. Check workflow logs in Actions tab
2. Review artifacts for detailed logs
3. Search existing GitHub issues
4. Open a new issue with:
   - Workflow run link
   - Error messages
   - Configuration used
   - Expected vs actual behavior

## 📝 Example Workflows

### Example 1: Daily US Stock Trading

```yaml
# Run daily at 9 AM UTC
schedule:
  - cron: '0 9 * * 1-5'

# With these settings:
config_file: configs/default_config.json
market_type: us
commit_results: true
analyze_with_ai: true
```

### Example 2: Weekly A-Share Analysis

```yaml
# Run every Monday
schedule:
  - cron: '0 8 * * 1'

# With these settings:
config_file: configs/default_astock_config.json
market_type: cn
commit_results: true
analyze_with_ai: true
```

### Example 3: Crypto Trading with Hourly Checks

```yaml
# Run every 6 hours
schedule:
  - cron: '0 */6 * * *'

# With these settings:
config_file: configs/default_crypto_config.json
market_type: crypto
commit_results: false
analyze_with_ai: false
```

## 🎓 Advanced Usage

### Custom Analysis Scripts

Create custom analysis in `scripts/custom_analysis.py`:

```python
from tools.result_tools import calculate_all_metrics

# Load and analyze results
metrics = calculate_all_metrics('my-model', market='us')

# Custom analysis logic
# ...

# Save custom report
with open('custom_report.md', 'w') as f:
    f.write(report)
```

Add to workflow:

```yaml
- name: Custom Analysis
  run: python scripts/custom_analysis.py
```

### Integration with External Services

Add steps to send results to external services:

```yaml
- name: Upload to S3
  run: |
    aws s3 cp artifacts/ s3://my-bucket/results/ --recursive

- name: Send Notification
  run: |
    curl -X POST ${{ secrets.WEBHOOK_URL }} \
      -H "Content-Type: application/json" \
      -d '{"text": "AI-Trader run completed"}'
```

## 🔄 Continuous Improvement

Track and improve your trading strategies:

1. **Compare Metrics**: Review performance across runs
2. **Identify Patterns**: Analyze what works
3. **Adjust Configs**: Fine-tune parameters
4. **A/B Testing**: Run multiple configurations
5. **Iterate**: Continuously improve based on results

---

**Happy Automated Trading! 🚀**
