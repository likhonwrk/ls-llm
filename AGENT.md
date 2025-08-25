# AGENTS.md

**Repository**: `ls-llm`  
**Last Updated**: 2025-08-26  
**Version**: 1.0.0

---

## 📋 Overview

This document describes all AI agents, tools, and automation components in this repository. It serves as the single source of truth for understanding, using, and extending the agents in this codebase.

**For AI Assistants (Jules, Claude, etc.)**: This file provides structured information about available agents, their interfaces, and usage patterns to enable effective code assistance and automation.

---

## 🤖 Active Agents

### LS-Agent (Primary LLM Interface)

**Status**: ✅ Production Ready  
**Type**: Interactive AI Assistant  
**Runtime**: Python 3.8+

#### Description
LS-Agent is the core conversational AI agent that provides local LLM inference capabilities. Designed for resource-constrained environments like Termux and lightweight Linux systems, it enables AI-powered interactions without requiring cloud services or high-end hardware.

#### Capabilities
- **Conversational AI**: Multi-turn dialogues with context retention
- **Text Generation**: Creative writing, summaries, explanations
- **Code Assistance**: Programming help, code generation, debugging
- **Local Inference**: Runs entirely offline with quantized models
- **Memory Management**: Efficient handling of limited system resources
- **Plugin Architecture**: Extensible through the `plugins/` system

#### Interface

**Command Line**:
```bash
python main.py [OPTIONS] [COMMAND]
```

**Required Parameters**:
- `--model <path>` : Path to model file (supports GGUF, GGML formats)
- `--prompt <text>` : Input query or conversation starter

**Optional Parameters**:
- `--temperature <float>` : Response randomness (0.0-2.0, default: 0.7)
- `--max_tokens <int>` : Maximum response length (default: 512)
- `--context_length <int>` : Context window size (default: 2048)
- `--threads <int>` : CPU threads to use (default: auto-detect)
- `--memory_limit <int>` : RAM limit in MB (default: 4096)
- `--stream` : Enable streaming output
- `--save_session <path>` : Save conversation to file
- `--load_session <path>` : Resume from saved session

**Interactive Mode**:
```bash
python main.py --model ./models/llama-7b.gguf --interactive
```

#### Input Formats
- **Plain Text**: Direct string input via `--prompt`
- **File Input**: `--prompt @filename.txt` reads from file
- **Stdin**: `echo "query" | python main.py --model path`
- **JSON API**: POST requests to `/api/v1/generate` when `--api` flag is used

#### Output Formats
- **Console**: Default formatted text output
- **JSON**: `--output json` for structured responses
- **Stream**: `--stream` for token-by-token output
- **File**: `--output_file <path>` to save responses

#### Usage Examples

**Basic Query**:
```bash
python main.py --model ./models/llama-7b.gguf --prompt "Explain quantum computing"
```

**Creative Writing**:
```bash
python main.py --model ./models/creative-7b.gguf \
  --prompt "Write a sci-fi story about AI" \
  --temperature 0.9 \
  --max_tokens 1000
```

**Code Generation**:
```bash
python main.py --model ./models/code-7b.gguf \
  --prompt "Create a Python function to parse JSON" \
  --temperature 0.2
```

**Interactive Session**:
```bash
python main.py --model ./models/llama-7b.gguf --interactive --save_session my_chat.json
```

**API Server Mode**:
```bash
python main.py --model ./models/llama-7b.gguf --api --host 0.0.0.0 --port 8080
```

#### Configuration
- **Config File**: `config/agent_config.yaml`
- **Model Registry**: `models/model_registry.json`
- **Plugin Settings**: `plugins/plugin_config.yaml`

#### Error Handling
- Returns exit code 0 on success
- Returns exit code 1 on model loading errors
- Returns exit code 2 on input validation errors
- Logs errors to `logs/agent.log` when `--verbose` flag is used

---

### Model-Manager (Model Lifecycle Tool)

**Status**: ✅ Production Ready  
**Type**: Utility Agent  
**Runtime**: Python 3.8+

#### Description
Automated model management system for downloading, validating, optimizing, and maintaining LLM models in the repository.

#### Capabilities
- **Model Discovery**: Search and index available models
- **Download Management**: Resume-capable downloads with verification
- **Format Conversion**: Convert between GGUF, GGML, and other formats
- **Quantization**: Reduce model size for resource-constrained environments
- **Validation**: Verify model integrity and compatibility
- **Cleanup**: Remove unused or corrupted models

#### Interface
```bash
python tools/model_manager.py [COMMAND] [OPTIONS]
```

**Commands**:
- `list` : Show available models
- `download <model_id>` : Download specified model
- `convert <input> <output> --format <fmt>` : Convert model format
- `quantize <model> --bits <4|8>` : Quantize model
- `validate <model>` : Check model integrity
- `cleanup` : Remove unused models

#### Usage Examples
```bash
# List available models
python tools/model_manager.py list

# Download a model
python tools/model_manager.py download llama-7b-chat

# Convert and quantize
python tools/model_manager.py convert ./models/llama-7b.gguf ./models/llama-7b-q4.gguf --format q4_0

# Validate model
python tools/model_manager.py validate ./models/llama-7b.gguf
```

---

### Performance-Monitor (System Metrics Agent)

**Status**: 🚧 Beta  
**Type**: Background Monitoring  
**Runtime**: Python 3.8+

#### Description
Continuous monitoring agent that tracks system resources, model performance, and usage patterns to optimize agent operations.

#### Capabilities
- **Resource Tracking**: CPU, RAM, disk usage monitoring
- **Performance Metrics**: Inference speed, token throughput
- **Usage Analytics**: Model usage patterns and statistics
- **Alerting**: Warnings for resource constraints
- **Auto-Optimization**: Dynamic parameter adjustment

#### Interface
```bash
python tools/monitor.py [OPTIONS]
```

**Options**:
- `--daemon` : Run as background service
- `--interval <seconds>` : Monitoring frequency (default: 5)
- `--log_file <path>` : Custom log location
- `--alert_threshold <percent>` : Resource alert level (default: 85)

#### Usage Examples
```bash
# Start monitoring daemon
python tools/monitor.py --daemon --interval 10

# One-time system check
python tools/monitor.py --check

# Monitor with custom thresholds
python tools/monitor.py --daemon --alert_threshold 90
```

---

## 🧩 Plugin System

### Available Plugins

#### WebSearch Plugin
- **Purpose**: Enable agents to search the internet for current information
- **Status**: ✅ Ready
- **Config**: `plugins/websearch/config.yaml`

#### CodeRunner Plugin  
- **Purpose**: Execute generated code in sandboxed environments
- **Status**: 🚧 Development
- **Config**: `plugins/coderunner/config.yaml`

#### FileSystem Plugin
- **Purpose**: Safe file operations with permission controls
- **Status**: ✅ Ready
- **Config**: `plugins/filesystem/config.yaml`

### Plugin Development
See `plugins/README.md` for plugin development guidelines and API documentation.

---

## 🔧 Development Tools

### Test Suite Runner
```bash
python tests/run_tests.py [--agent <name>] [--coverage]
```

### Benchmarking Tool
```bash
python tools/benchmark.py --model <path> --dataset <path>
```

### Debug Console
```bash
python tools/debug_console.py --agent <name>
```

---

## 📚 API Reference

### REST API Endpoints (when `--api` flag is used)

**Base URL**: `http://localhost:8080/api/v1/`

#### Generate Text
```http
POST /generate
Content-Type: application/json

{
  "prompt": "Your query here",
  "temperature": 0.7,
  "max_tokens": 512,
  "stream": false
}
```

#### Model Info
```http
GET /model/info
```

#### Health Check
```http
GET /health
```

### Python API
```python
from ls_llm import LSAgent

agent = LSAgent(model_path="./models/llama-7b.gguf")
response = agent.generate("Explain machine learning")
print(response.text)
```

---

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download a Model**:
   ```bash
   python tools/model_manager.py download llama-7b-chat
   ```

3. **Start Interactive Session**:
   ```bash
   python main.py --model ./models/llama-7b-chat.gguf --interactive
   ```

---

## 🔍 Troubleshooting

### Common Issues

**Model Not Found**:
- Verify model path with `ls models/`
- Check `models/model_registry.json` for registered models

**Out of Memory**:
- Use `--memory_limit` to set RAM constraints
- Try quantized models (Q4, Q8 variants)
- Reduce `--context_length`

**Slow Performance**:
- Increase `--threads` up to CPU core count
- Use smaller models for faster inference
- Enable `--stream` for responsive output

**API Connection Issues**:
- Check firewall settings for specified port
- Verify `--host` and `--port` parameters
- Test with `curl http://localhost:8080/health`

---

## 📖 Documentation Links

- **API Documentation**: `docs/api.md`
- **Plugin Development**: `plugins/README.md`
- **Model Guide**: `docs/models.md`
- **Configuration Reference**: `docs/config.md`
- **Contributing Guidelines**: `CONTRIBUTING.md`

---

## 🏷️ Agent Metadata

```yaml
agents:
  ls-agent:
    version: "1.0.0"
    python_version: ">=3.8"
    dependencies: ["torch", "transformers", "llama-cpp-python"]
    platforms: ["linux", "termux", "macOS"]
    memory_min: "2GB"
    memory_recommended: "8GB"
    
  model-manager:
    version: "1.0.0"  
    python_version: ">=3.8"
    dependencies: ["requests", "tqdm", "huggingface_hub"]
    platforms: ["linux", "termux", "macOS", "windows"]
    
  performance-monitor:
    version: "0.9.0"
    python_version: ">=3.8"
    dependencies: ["psutil", "prometheus_client"]
    platforms: ["linux", "macOS"]
```

---

*This document is automatically validated against the actual codebase. Last validation: 2025-08-26*
