"""
Multi-Strategy Algorithmic Trading Bot
=======================================
Entry point — run backtests, comparisons, live signals, and optimisation.

Usage:
    python main.py                        # runs default backtest (MA)
    python main.py --strategy rsi         # RSI mean reversion
    python main.py --strategy zipline     # Zipline-style momentum
    python main.py --compare              # compare all strategies
    python main.py --live                 # today's live signals
    python main.py --optimise rsi         # grid-search RSI params
    python main.py --ticker TCS.NS --strategy rsi
"""

import argparse
from bot.runner import run_backtest, compare_strategies, live_signal, optimise
from bot.config import DEFAULT_CONFIG


def parse_args():
    p = argparse.ArgumentParser(description="Algorithmic Trading Bot")
    p.add_argument("--strategy",  default="ma",
                   choices=["ma", "rsi", "zipline"],
                   help="Strategy to backtest (default: ma)")
    p.add_argument("--ticker",    default=DEFAULT_CONFIG["ticker"])
    p.add_argument("--start",     default=DEFAULT_CONFIG["start"])
    p.add_argument("--end",       default=DEFAULT_CONFIG["end"])
    p.add_argument("--cash",      default=DEFAULT_CONFIG["initial_cash"], type=float)
    p.add_argument("--compare",   action="store_true",
                   help="Run all strategies and print comparison table")
    p.add_argument("--live",      action="store_true",
                   help="Print today's live signal for all strategies")
    p.add_argument("--optimise",  metavar="STRATEGY",
                   help="Grid-search params for given strategy")
    return p.parse_args()


def main():
    args = parse_args()

    if args.live:
        live_signal(args.ticker)
        return

    if args.compare:
        compare_strategies(
            ticker       = args.ticker,
            start        = args.start,
            end          = args.end,
            initial_cash = args.cash,
        )
        return

    if args.optimise:
        optimise(args.optimise, args.ticker, args.start, args.end)
        return

    # Default: single strategy backtest
    strategy_defaults = {
        "ma":      dict(short_period=10, long_period=40, stop_pct=0.03, trail_pct=0.05),
        "rsi":     dict(rsi_period=14, oversold_level=30, overbought_level=70,
                        trend_filter=True, volume_filter=True, stop_pct=0.03, trail_pct=0.05),
        "zipline": dict(momentum_threshold=0.05, reversal_threshold=0.10,
                        rebalance_days=21, stop_pct=0.04, trail_pct=0.06),
    }
    run_backtest(
        strategy_name = args.strategy,
        ticker        = args.ticker,
        start         = args.start,
        end           = args.end,
        initial_cash  = args.cash,
        **strategy_defaults[args.strategy],
    )


if __name__ == "__main__":
    main()
