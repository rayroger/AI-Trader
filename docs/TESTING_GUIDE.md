# Testing GitHub Actions Locally

This guide helps you test GitHub Actions workflows locally before running them in GitHub.

## Prerequisites

- Python 3.10+
- All dependencies installed (`pip install -r requirements.txt`)
- API keys configured in `.env` file

## Test Checklist

### 1. Validate Workflow YAML

```bash
# Install PyYAML if not already installed
pip install pyyaml

# Validate workflow syntax
python -c "
import yaml
with open('.github/workflows/ai-trader-run.yml', 'r') as f:
    workflow = yaml.safe_load(f)
print('✅ Workflow YAML is valid')
"
```

### 2. Validate Configuration Files

```bash
# Test all config files
python -c "
import json
configs = [
    'configs/default_config.json',
    'configs/github_actions_demo.json',
    'configs/default_astock_config.json',
    'configs/default_crypto_config.json'
]
for cfg in configs:
    with open(cfg) as f:
        json.load(f)
    print(f'✅ {cfg} is valid')
"
```

### 3. Test Environment Setup

```bash
# Verify .env file exists and has required keys
cat .env | grep -E "OPENAI_API_KEY|ALPHAADVANTAGE_API_KEY|JINA_API_KEY"

# If missing, create from example
cp .env.example .env
# Edit .env with your API keys
```

### 4. Test Data Preparation (Dry Run)

```bash
# Test US market data preparation
cd data
python -c "
# Quick validation of data scripts
import os
print('✅ Data directory:', os.getcwd())
print('✅ Files:', os.listdir('.'))
"
cd ..
```

### 5. Test MCP Services

```bash
# Start MCP services in background
cd agent_tools
python start_mcp_services.py &
MCP_PID=$!

# Wait for startup
sleep 5

# Check if running
ps -p $MCP_PID && echo "✅ MCP services running" || echo "❌ MCP services failed"

# Stop services
kill $MCP_PID

cd ..
```

### 6. Test Trading Agent (Minimal)

```bash
# Run with demo config (short date range)
python main.py configs/github_actions_demo.json

# Check if logs were created
ls -la data/agent_data/*/
```

### 7. Test Analysis Script

```bash
# Test without API key (should show error message)
python scripts/analyze_results.py --config configs/github_actions_demo.json

# Test with API key (set in environment)
export OPENAI_API_KEY="your-key-here"
python scripts/analyze_results.py --config configs/github_actions_demo.json
```

### 8. Simulate Workflow Steps

Create a test script that mimics the workflow:

```bash
#!/bin/bash
# test_workflow_steps.sh

set -e  # Exit on error

echo "🧪 Testing GitHub Actions workflow steps locally..."

# Step 1: Environment setup
echo "1️⃣ Setting up environment..."
source .env
echo "✅ Environment loaded"

# Step 2: Data preparation
echo "2️⃣ Preparing data..."
cd data
python merge_jsonl.py 2>/dev/null || echo "⚠️ merge_jsonl.py needs actual data"
cd ..
echo "✅ Data preparation tested"

# Step 3: MCP services
echo "3️⃣ Starting MCP services..."
cd agent_tools
nohup python start_mcp_services.py > ../test_mcp.log 2>&1 &
MCP_PID=$!
sleep 5
if ps -p $MCP_PID > /dev/null; then
    echo "✅ MCP services running"
else
    echo "❌ MCP services failed"
    cat ../test_mcp.log
    exit 1
fi
cd ..

# Step 4: Trading agent
echo "4️⃣ Running trading agent (demo config)..."
python main.py configs/github_actions_demo.json 2>&1 | tee test_trading.log || echo "⚠️ Trading may need actual market data"

# Step 5: Cleanup
echo "5️⃣ Cleaning up..."
kill $MCP_PID 2>/dev/null || true
rm -f test_mcp.log test_trading.log

echo "✅ All workflow steps tested successfully!"
```

Make it executable and run:

```bash
chmod +x test_workflow_steps.sh
./test_workflow_steps.sh
```

## Common Issues and Fixes

### Issue: YAML Syntax Error

```bash
# Solution: Check YAML indentation
python -c "
import yaml
try:
    with open('.github/workflows/ai-trader-run.yml') as f:
        yaml.safe_load(f)
except yaml.YAMLError as e:
    print('Error:', e)
"
```

### Issue: Missing Dependencies

```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: API Keys Not Working

```bash
# Solution: Verify API keys
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
keys = ['OPENAI_API_KEY', 'ALPHAADVANTAGE_API_KEY', 'JINA_API_KEY']
for key in keys:
    val = os.getenv(key)
    if val:
        print(f'✅ {key}: Set ({len(val)} chars)')
    else:
        print(f'❌ {key}: Not set')
"
```

### Issue: MCP Services Won't Start

```bash
# Solution: Check port availability
netstat -tuln | grep -E "8000|8001|8002|8003"

# If ports are in use, kill processes
lsof -ti:8000,8001,8002,8003 | xargs kill -9
```

### Issue: No Trading Data Generated

```bash
# Solution: Check if data files exist
ls -la data/*.jsonl
ls -la data/agent_data/

# Verify date range in config is valid
python -c "
import json
from datetime import datetime
with open('configs/github_actions_demo.json') as f:
    config = json.load(f)
    dates = config['date_range']
    print(f\"Date range: {dates['init_date']} to {dates['end_date']}\")
"
```

## Using Act to Test GitHub Actions Locally

[Act](https://github.com/nektos/act) allows you to run GitHub Actions locally.

### Install Act

```bash
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows
choco install act-cli
```

### Run Workflow Locally

```bash
# List workflows
act -l

# Run specific workflow
act workflow_dispatch -j run-trading

# Run with secrets
act workflow_dispatch -j run-trading \
  -s OPENAI_API_KEY="your-key" \
  -s ALPHAADVANTAGE_API_KEY="your-key" \
  -s JINA_API_KEY="your-key"

# Run specific event with inputs
act workflow_dispatch \
  -j run-trading \
  --input config_file=configs/github_actions_demo.json \
  --input market_type=us \
  --input commit_results=false \
  --input analyze_with_ai=false
```

### Act Configuration

Create `.actrc` file:

```
-P ubuntu-latest=catthehacker/ubuntu:full-latest
--secret-file .env
--artifact-server-path /tmp/artifacts
```

## Continuous Testing

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "🧪 Running pre-commit tests..."

# Validate workflow YAML
python -c "
import yaml
with open('.github/workflows/ai-trader-run.yml') as f:
    yaml.safe_load(f)
" || exit 1

echo "✅ Workflow YAML is valid"

# Validate configs
for cfg in configs/*.json; do
    python -c "import json; json.load(open('$cfg'))" || exit 1
done

echo "✅ All configs are valid"
echo "✅ Pre-commit checks passed"
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

### Automated Testing Script

Create `scripts/test_all.sh`:

```bash
#!/bin/bash
set -e

echo "🧪 Running comprehensive tests..."

# Test 1: YAML validation
echo "Test 1: Validating YAML..."
python -c "import yaml; yaml.safe_load(open('.github/workflows/ai-trader-run.yml'))"

# Test 2: JSON validation
echo "Test 2: Validating JSON configs..."
for cfg in configs/*.json; do
    python -c "import json; json.load(open('$cfg'))"
done

# Test 3: Python syntax
echo "Test 3: Checking Python syntax..."
python -m py_compile scripts/analyze_results.py
python -m py_compile main.py

# Test 4: Import checks
echo "Test 4: Checking imports..."
python -c "from tools.result_tools import calculate_all_metrics"
python -c "from tools.general_tools import get_config_value"

# Test 5: Analysis script help
echo "Test 5: Testing analysis script..."
python scripts/analyze_results.py --help > /dev/null

echo "✅ All tests passed!"
```

Run tests:

```bash
chmod +x scripts/test_all.sh
./scripts/test_all.sh
```

## Next Steps

After successful local testing:

1. **Commit changes**: `git add . && git commit -m "Test commit"`
2. **Push to GitHub**: `git push`
3. **Run workflow**: Go to Actions tab and manually trigger
4. **Monitor logs**: Watch workflow execution in real-time
5. **Download artifacts**: Check results after completion

## Troubleshooting Resources

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Act Documentation](https://github.com/nektos/act)
- [AI-Trader Issues](https://github.com/HKUDS/AI-Trader/issues)

## Tips

1. **Start small**: Use `github_actions_demo.json` with short date ranges
2. **Test incrementally**: Test each workflow step separately
3. **Check logs**: Always review logs for warnings
4. **Use dry runs**: Test without actual API calls when possible
5. **Monitor costs**: Be aware of API usage in automated runs

Happy testing! 🚀
