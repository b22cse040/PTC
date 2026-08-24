### High Level Worfklow

```
User Query
    │
    ▼
ToolSearchModule.invoke()
    │
    ├── result.tools
    │      └── retrieved tool definitions
    │
    └── result.tools_callable
           └── name → Python callable
    │
    ▼
PTCModule.invoke()
    │
    ├── deepcopy(result.tools)
    ├── add allowed_callers
    ├── append code_execution tool
    ├── send to Claude
    │
    └── while TURNS_LEFT > 0
           ├── model response
           ├── code execution / direct tool calls
           ├── execute Python callable
           ├── append tool results
           └── continue
```

