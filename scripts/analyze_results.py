#!/usr/bin/env python3
"""
AI Agent Analysis Script for Trading Results

This script analyzes trading results and generates insights using an AI agent.
It can be run standalone or as part of GitHub Actions workflow.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


def load_latest_metrics(config_file: str) -> List[Dict]:
    """
    Load latest performance metrics for all enabled models
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        List of metric dictionaries
    """
    results = []
    
    # Read configuration
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Determine log path
    log_path = config.get('log_config', {}).get('log_path', './data/agent_data')
    if log_path.startswith('./data/'):
        log_path = log_path[7:]
    
    base_dir = Path(__file__).resolve().parents[1]
    
    # Get metrics for each enabled model
    for model in config.get('models', []):
        if not model.get('enabled', True):
            continue
            
        signature = model.get('signature')
        if not signature:
            continue
        
        metrics_file = base_dir / 'data' / log_path / signature / 'metrics' / 'performance_metrics.jsonl'
        
        if metrics_file.exists():
            # Read last line (latest metrics)
            with open(metrics_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    latest_metric = json.loads(lines[-1])
                    results.append(latest_metric)
    
    return results


def generate_analysis_prompt(metrics: List[Dict]) -> str:
    """
    Generate analysis prompt for AI agent
    
    Args:
        metrics: List of performance metrics
        
    Returns:
        Formatted prompt string
    """
    prompt = """Analyze the following AI trading results and provide comprehensive insights:

## Trading Results Data

"""
    
    for metric in metrics:
        model_name = metric.get('model_name', 'Unknown')
        period = metric.get('analysis_period', {})
        perf = metric.get('performance_metrics', {})
        portfolio = metric.get('portfolio_summary', {})
        
        prompt += f"""
### Model: {model_name}

**Analysis Period**: {period.get('start_date')} to {period.get('end_date')} ({period.get('total_trading_days')} days)

**Performance Metrics**:
- Sharpe Ratio: {perf.get('sharpe_ratio', 0):.4f}
- Cumulative Return: {perf.get('cumulative_return', 0):.2%}
- Annualized Return: {perf.get('annualized_return', 0):.2%}
- Maximum Drawdown: {perf.get('max_drawdown', 0):.2%}
- Volatility: {perf.get('volatility', 0):.2%}
- Win Rate: {perf.get('win_rate', 0):.2%}
- Profit/Loss Ratio: {perf.get('profit_loss_ratio', 0):.4f}

**Portfolio Summary**:
- Initial Value: ${portfolio.get('initial_value', 0):,.2f}
- Final Value: ${portfolio.get('final_value', 0):,.2f}
- Value Change: ${portfolio.get('value_change', 0):,.2f} ({portfolio.get('value_change_percent', 0):.2%})

---
"""
    
    prompt += """

## Analysis Requirements

Please provide a comprehensive analysis covering:

1. **Overall Performance Summary**
   - Compare performance across all models
   - Identify best and worst performers
   - Highlight key trends

2. **Risk-Adjusted Returns**
   - Evaluate Sharpe ratios
   - Analyze risk vs. return tradeoffs
   - Comment on volatility patterns

3. **Drawdown Analysis**
   - Review maximum drawdown periods
   - Assess recovery capabilities
   - Identify risk management effectiveness

4. **Trading Behavior**
   - Analyze win rates and profit/loss ratios
   - Evaluate trading consistency
   - Comment on decision quality

5. **Recommendations**
   - Suggest improvements for underperforming models
   - Identify best practices from top performers
   - Recommend strategy adjustments

6. **Risk Assessment**
   - Identify potential risks
   - Evaluate portfolio diversification
   - Suggest risk mitigation strategies

Please format your analysis in clear sections with actionable insights.
"""
    
    return prompt


def analyze_with_openai(prompt: str, api_key: str, base_url: Optional[str] = None) -> str:
    """
    Generate analysis using OpenAI API
    
    Args:
        prompt: Analysis prompt
        api_key: OpenAI API key
        base_url: Optional custom base URL
        
    Returns:
        Analysis text
    """
    try:
        from openai import OpenAI
        
        client_kwargs = {'api_key': api_key}
        if base_url:
            client_kwargs['base_url'] = base_url
        
        client = OpenAI(**client_kwargs)
        
        response = client.chat.completions.create(
            model='gpt-4',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are an expert financial analyst specializing in algorithmic trading and AI-driven investment strategies. Provide detailed, actionable insights based on quantitative metrics.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        return "Error: openai package not installed. Run: pip install openai"
    except Exception as e:
        return f"Error generating analysis: {str(e)}"


def save_analysis(analysis: str, output_file: str = 'ai_analysis.md') -> None:
    """
    Save analysis to markdown file
    
    Args:
        analysis: Analysis text
        output_file: Output file path
    """
    with open(output_file, 'w') as f:
        f.write('# AI Trading Performance Analysis\n\n')
        f.write(f'*Generated on: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*\n\n')
        f.write(analysis)
    
    print(f"✅ Analysis saved to: {output_file}")


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze AI trading results with AI agent')
    parser.add_argument(
        '--config',
        default='configs/default_config.json',
        help='Configuration file path (default: configs/default_config.json)'
    )
    parser.add_argument(
        '--output',
        default='ai_analysis.md',
        help='Output file path (default: ai_analysis.md)'
    )
    parser.add_argument(
        '--api-key',
        default=None,
        help='OpenAI API key (default: read from OPENAI_API_KEY env var)'
    )
    parser.add_argument(
        '--base-url',
        default=None,
        help='OpenAI API base URL (default: read from OPENAI_API_BASE env var)'
    )
    
    args = parser.parse_args()
    
    # Get API credentials
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    base_url = args.base_url or os.getenv('OPENAI_API_BASE')
    
    if not api_key:
        print("❌ Error: OpenAI API key not provided")
        print("   Set OPENAI_API_KEY environment variable or use --api-key argument")
        sys.exit(1)
    
    print(f"📊 Loading metrics from config: {args.config}")
    
    # Load metrics
    try:
        metrics = load_latest_metrics(args.config)
    except Exception as e:
        print(f"❌ Error loading metrics: {e}")
        sys.exit(1)
    
    if not metrics:
        print("⚠️  No metrics found. Run trading agent first.")
        sys.exit(1)
    
    print(f"✅ Loaded metrics for {len(metrics)} model(s)")
    
    # Generate prompt
    print("🔧 Generating analysis prompt...")
    prompt = generate_analysis_prompt(metrics)
    
    # Generate analysis
    print("🧠 Analyzing results with AI agent...")
    analysis = analyze_with_openai(prompt, api_key, base_url)
    
    # Save results
    save_analysis(analysis, args.output)
    
    # Print analysis
    print("\n" + "="*60)
    print(analysis)
    print("="*60)
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
