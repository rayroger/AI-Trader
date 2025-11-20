# GitHub Actions Quick Reference

Quick commands and examples for using AI-Trader with GitHub Actions.

## 🎯 Quick Setup (5 Minutes)

```bash
# 1. Add secrets to GitHub repository:
Settings → Secrets → New repository secret

Required:
- OPENAI_API_KEY
- ALPHAADVANTAGE_API_KEY  
- JINA_API_KEY

# 2. Navigate to Actions tab

# 3. Select "AI-Trader Automated Trading"

# 4. Click "Run workflow" and configure
```

## 📝 Common Configurations

### US Stock Trading (Default)

```yaml
config_file: configs/default_config.json
market_type: us
commit_results: false
analyze_with_ai: false
```

### A-Share Trading

```yaml
config_file: configs/default_astock_config.json
market_type: cn
commit_results: true
analyze_with_ai: true
```

**Note**: Requires `TUSHARE_TOKEN` secret for A-share data

### Cryptocurrency Trading

```yaml
config_file: configs/default_crypto_config.json
market_type: crypto
commit_results: false
analyze_with_ai: false
```

### Quick Demo Test

```yaml
config_file: configs/github_actions_demo.json
market_type: us
commit_results: false
analyze_with_ai: false
```

**Use this for testing!** Short date range, single model, quick execution.

## 🔧 Common Tasks

### Download Trading Results

1. Go to workflow run page
2. Scroll to "Artifacts" section
3. Download `ai-trader-results-{number}.zip`
4. Extract and review files

### View Committed Results

```bash
# Clone repository
git clone https://github.com/your-username/AI-Trader.git
cd AI-Trader

# List result branches
git branch -r | grep results/

# Checkout specific date
git checkout results/2025-01-20

# View results
cat data/agent_data/*/metrics/performance_metrics.jsonl
```

### Analyze Results Locally

```bash
# Download artifacts and extract
unzip ai-trader-results-123.zip

# Run analysis script
export OPENAI_API_KEY="your-key"
python scripts/analyze_results.py \
  --config configs/default_config.json \
  --output my_analysis.md
```

## 📊 Understanding Outputs

### Artifact Files

```
artifacts/
├── agent_data/              # Trading results
│   └── {model-name}/
│       ├── position/        # Portfolio positions over time
│       ├── log/            # Detailed trading logs
│       └── metrics/        # Performance metrics
├── trading_run.log         # Main execution log
├── mcp_services.log        # MCP services log
└── summary.md             # Run summary
```

### Key Metrics

From `performance_metrics.jsonl`:

- **Sharpe Ratio**: Risk-adjusted return (higher is better)
- **Max Drawdown**: Largest peak-to-trough decline (lower is better)
- **Cumulative Return**: Total return over period
- **Win Rate**: Percentage of profitable days
- **Volatility**: Return variability (lower is better)

## 🔄 Scheduling Options

Edit `.github/workflows/ai-trader-run.yml`:

### Daily Trading (Weekdays)

```yaml
schedule:
  - cron: '0 9 * * 1-5'  # 9 AM UTC, Mon-Fri
```

### Weekly Trading

```yaml
schedule:
  - cron: '0 8 * * 1'  # 8 AM UTC every Monday
```

### Multiple Times Per Day

```yaml
schedule:
  - cron: '0 9,17 * * *'  # 9 AM and 5 PM UTC daily
```

**Remember**: Uncomment the `schedule:` section in the workflow file!

## 🐛 Troubleshooting

### Workflow Fails Immediately

```bash
# Check secrets are set:
Settings → Secrets → Actions

# Verify all required secrets exist
```

### MCP Services Fail to Start

```bash
# Check workflow logs for:
❌ MCP services failed to start

# Usually caused by:
- Invalid API keys
- API rate limits
- Service port conflicts
```

### No Trading Data Generated

```bash
# Verify date range in config:
{
  "date_range": {
    "init_date": "2025-01-01",  # Must be past date
    "end_date": "2025-01-20"     # Must be past date
  }
}

# Future dates won't have data!
```

### AI Analysis Fails

```bash
# Check:
1. OPENAI_API_KEY is set
2. API has sufficient quota
3. Metrics were calculated successfully

# View logs in workflow run
```

## 💡 Tips & Tricks

### Test Before Scheduling

1. Run manually with demo config first
2. Verify artifacts are correct
3. Check all steps complete successfully
4. Then enable scheduling

### Monitor API Usage

- Alpha Vantage: 25 requests/day (free tier)
- OpenAI: Check usage dashboard
- Consider upgrading for scheduled runs

### Optimize for Costs

```json
{
  "agent_config": {
    "max_steps": 10,  // Reduce from 30
    "initial_cash": 5000.0  // Use smaller portfolio
  }
}
```

### Keep Results Organized

Enable `commit_results: true` to maintain history:

```bash
# Results automatically organized by date
results/2025-01-20
results/2025-01-21
results/2025-01-22
```

## 📚 Learn More

- **[Complete Guide](GITHUB_ACTIONS_GUIDE.md)**: Detailed documentation
- **[Testing Guide](TESTING_GUIDE.md)**: Local testing instructions
- **[Main README](../README.md)**: Project overview
- **[Config Guide](CONFIG_GUIDE.md)**: Configuration options

## 🆘 Getting Help

1. Check [workflow logs](https://github.com/your-repo/actions)
2. Review [troubleshooting guide](GITHUB_ACTIONS_GUIDE.md#troubleshooting)
3. Search [existing issues](https://github.com/HKUDS/AI-Trader/issues)
4. Open new issue with details

## 📋 Checklist for First Run

- [ ] Secrets configured (OPENAI_API_KEY, ALPHAADVANTAGE_API_KEY, JINA_API_KEY)
- [ ] Demo config tested locally (optional but recommended)
- [ ] Workflow file syntax validated
- [ ] Manual workflow trigger successful
- [ ] Artifacts downloaded and reviewed
- [ ] Results meet expectations
- [ ] Ready for scheduled runs (optional)

## 🎓 Advanced Examples

### Custom Model Comparison

Create `configs/model_comparison.json`:

```json
{
  "models": [
    {"name": "gpt-4", "enabled": true, ...},
    {"name": "claude-3", "enabled": true, ...},
    {"name": "gemini", "enabled": true, ...}
  ]
}
```

Run with:
```yaml
config_file: configs/model_comparison.json
analyze_with_ai: true
```

### A/B Testing Strategy

Run same period with different configs:

```bash
# Monday: Strategy A
config_file: configs/strategy_a.json

# Tuesday: Strategy B  
config_file: configs/strategy_b.json

# Compare results in artifacts
```

### Multi-Market Portfolio

Run sequentially for different markets:

```yaml
# Workflow 1: US stocks
- market_type: us
  config_file: configs/us_config.json

# Workflow 2: Crypto
- market_type: crypto
  config_file: configs/crypto_config.json
```

## 🔐 Security Best Practices

1. **Never commit secrets** to repository
2. **Use GitHub secrets** for all API keys
3. **Rotate keys regularly** (every 90 days)
4. **Limit workflow permissions** if possible
5. **Review workflow logs** for exposed data

## ⏱️ Performance Optimization

### Faster Runs

```json
{
  "date_range": {
    "init_date": "2025-01-01",
    "end_date": "2025-01-05"  // Shorter range
  },
  "agent_config": {
    "max_steps": 10  // Fewer steps
  }
}
```

### Parallel Jobs

Split into multiple workflows:

```yaml
# .github/workflows/us-trading.yml
# .github/workflows/crypto-trading.yml
# .github/workflows/astock-trading.yml
```

## 📈 Success Metrics

Track these over time:

1. **Workflow Success Rate**: % of successful runs
2. **Execution Time**: Time per run (aim: < 30 min)
3. **Trading Performance**: Sharpe ratio, returns
4. **API Costs**: Monthly API usage costs
5. **Data Quality**: % of successful data fetches

---

**Ready to trade? Go to Actions tab and start your first run! 🚀**
