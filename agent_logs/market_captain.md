

# Relevant Files

- Market Research Directory: memories/markets
- Henry Arch Doc: memories/arch/henry-arch
- Henry Strategy Doc: memories/arch/henry-strategy.md (Log and Update Trading Strategies Implementation Here)

# How to test a new strategy 

1. Create a new strategy file in Henry: callandor/strategy/strategies
2. Launch a Callandor simulator backtest 
    - go run . backtest-strategy -s [strategy_name] -p 1 -m 5 # first week (-p) of 5 months (-m)
        - Do not run more than 12 weeks (m * parallel_runs) at a time due to memory limits. 
    - go run . backtest-strategy -s [strategy_name]  --start 2025-10-01 --end 2025-10-30
        - Due to chunked loading can run --start to --end timeframes of arbitrary length. (But cannot exceed 5 parallel workers)
3. Add/Change logging capabilites to extract data from runs as needed

Refer to henry/CLAUDE.md for additional guidelines
Log strategy WIP status and new hypotheses into memories/arch/henry-strategy.md
Log detailed notes about strategy into memories/markets/[folder_for_strategy]

