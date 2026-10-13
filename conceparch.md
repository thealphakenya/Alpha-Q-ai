[ Developer Input ]
        │
                ▼
                [ GitHub Copilot Chat ] (Consumes ~20% of your Copilot monthly limit)
                        │
                                ├─► Formulates high-level plan & passes structured payload to local agent
                                        │
                                                ▼
                                                [ Local Agent Extension / Bridge ] (OpenCode / Cline / Custom Script)
                                                        │
                                                                ▼
                                                                [ Local Ollama Instance in Codespace ] (Executes 400%+ work volume locally)
                                                                        ├─ Runs shell commands & file updates inside container
                                                                                ├─ Iterates through error-fix loops on local CPU/GPU
                                                                                        └─ Returns final diff/summary back to Copilot
                                                                                        