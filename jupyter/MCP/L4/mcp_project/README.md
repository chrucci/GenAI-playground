
## How to run the MCP Server
- `cd` into `jupyter/MCP/L4/mcp_project/`
  - You should see `research_server.py` which was created in the L4 jupyter notebook.
- Create virtual env using `uv`
  - `uv init`
  - `uv venv`
  - `source .venv/bin/activate`
- add necessary libraries to venv
  - `uv add mcp arxiv`
- run the MCP server within the "Inspector" to see what it's doing
  - `npx @modelcontextprotocol/inspector uv run research_server.py`
- Launch the inspector page at `http://localhost:6274/`