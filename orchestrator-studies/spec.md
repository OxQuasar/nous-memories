

- Nous to be a combination:
     - OpenClaw's always on feature 
     - Precision and multi-agent arch of OpenClaw 
     - Golang implementation of Crush. 
- Nous to be primarily used for research and development of trading code strategies (golang). 


1. Always on (For Linux) 
- Gateway daemon service
- Telegram integration
- TUI (Look to Crush) 
- WebUI - Lower priority but scoped
- Cron jobs - ability to schedule jobs at regular intervals like openclaw

2. Memory
- Tiered memory system: 
- Per trading strategy memory - relevant memory files to each trading strategy to be integrated into strategy subfolders. Should remember what research has been done, what needs to be tried.
- Overall project memory - memory and project states to be stored in main repo memory folder. Overall state, research hypothesis, results, test data. 
- Overall system memory - more abstract and general system memory to be stored in nous system home directory. Session transcripts, general learnings, patterns.
- RAG retrival and indexing system - easy to search on keywords. implentation in: ~/code/gandiva-memory/rag/server.py
- Memory should be automatically consolidated at regular intervals (internal cron jobs). Consolidate older memories and flow them upwards from strategy -> project -> system

3. Models
- 1 Provider to start: Use Anthropic Claude Opus 4.6 for most tasks. Haiku for cron jobs and lower compute tasks. 
- Auth using Anthropic Pro/Max subscription (look at how openclaw does it) 

4. Context Compaction: Use context pruning logic found on the compact branch of ~/deps/moltbot - 1. OpenCode inspired pruner pruneToolOutputs -> 2. LLM summary (ignore the 
 
5. Sessions: 
- Can open new session, which is project scoped like OpenCode. When opening session, project level memory is loaded into session context. 

6. Multi-Agent Management: Apply techniques from OpenCode. 
- Agent relationships and interactions to be configurable. 
For example, a skill could specify: create 1 research agent and 1 review agent. Research agent will write report and review agent will give critique. Repeat with 2 iterations. 
Or: Create 10 coding agents and 2 review agents. After the 10 agents complete, the 2 review agents will review each code agent's work one at a time and prompt improvements. 
Or: Skill like Plan: 
- Allow the LLM to determine how many explore agents to create and write a plan for X. (Look into how OpenCode does this) 

7. Automation Mode
- In automation mode, an agent is created, the Manager, whose job it is to continue prompting sessions as necessary to complete a plan or assigned task. 
It is the stand in for the user for tasks marked for automation. 


Principles: 
1. Make debugging and updates easy. We maintain source code and will update as we want. 
2. Make logging and transparency easy. If say we want to look more into how the compactor and context works, make it so session context can be easily extracted and analyzed.
3. No need for extendable plugins or multi-os compatibility. We are using it for ourselves on linux platforms. We will change our source code directly to add new features. 
4. Keep archetecture clear and flows clear so that large scale changes can be possible. 



