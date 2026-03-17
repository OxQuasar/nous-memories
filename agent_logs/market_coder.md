
# Relevant Files

- Market Research Directory: memories/markets
- Henry Arch Doc: memories/arch/henry-arch
- Henry Strategy Doc: memories/arch/henry-strategy.md (Overall strategy state tracking)


# How to test a strategy 

1. Create/modify strategy file in Henry: callandor/strategy/strategies
2. Launch a Callandor simulator backtest 
    - go run . backtest-strategy -s [strategy_name] -p 1 -m 5 # first week (-p) of 5 months (-m)
        - Do not run more than 8 weeks (m * parallel_runs) at a time due to memory limits. 
    - go run . backtest-strategy -s [strategy_name]  --start 2025-10-01 --end 2025-10-30
        - Due to chunked loading can run --start to --end timeframes of arbitrary length. (But cannot exceed 3 parallel workers)
3. Add/Change logging capabilites to extract data from runs as needed

Refer to henry/CLAUDE.md for additional guidance. 


# Python analysis

When doing python analysis: 
    - Use the python venv at /home/quasar/nous/.venv/
    - Write scripts and outputs to memories/markets/[subfolder if appropriate]

