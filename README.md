# Programmatic Tool Calling POC

This project is a proof of concept for combining semantic tool search with programmatic tool calling (PTC). Instead of sending the full tool catalog to the model, it finds tools relevant to a user's query and lets the model call them as needed. The sample asks for an Engineering workforce report using employee, attendance, benefits, and project data.

## Features

- Semantically retrieves relevant tool definitions using `sentence-transformers` and stores them in a local SQLite database (`tools.db`).
- Supports native Python tools and tools exposed through a local MCP server.
- Uses the PTC implementation configured in `PTC_POC.py` (currently OpenAI); an Anthropic implementation is also included in the source.
- Prints the generated response along with token usage, API call count, elapsed time, and messages.

## Run the project

The steps below use PowerShell on Windows. Run them from the project directory, the folder containing `PTC_POC.py` and `requirements.txt`.

1. Install Python and create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the project dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. Create a file named `.env` in the same directory as `PTC_POC.py`. Add your OpenAI API key:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key
   ```

   Do not include quotes or commit the real key. The entry point currently uses OpenAI and the model name configured in `PTC_POC.py`; your API account must have access to that model.

4. Run the POC:

   ```powershell
   python PTC_POC.py
   ```

On first run, the sentence-transformers embedding model may be downloaded, so internet access is required. The script creates or updates `tools.db`, starts the MCP server as a subprocess, retrieves tools for its sample query, and prints the result. To change the query or model, edit the corresponding values in `PTC_POC.py`.
