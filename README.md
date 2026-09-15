# 🧠 Can I Run AI? — AI Hardware Advisor

Sistema inteligente em **Python (FastAPI)** e **Vue 3 (Vite + Tailwind CSS)** que analisa o hardware do seu computador (CPU, núcleos, RAM total/disponível, GPU dedicada, VRAM e aceleração CUDA) e calcula matematicamente quais modelos de Inteligência Artificial sua máquina consegue rodar, com qual velocidade e quais configurações ideais.

---

## ✨ Funcionalidades Principais

1. **Detecção Automática e Real do Hardware:**
   - Detecta o processador (núcleos físicos e lógicos).
   - Detecta memória RAM total, usada e disponível.
   - Detecta placa de vídeo (NVIDIA, AMD, Intel, Apple), quantidade de VRAM e suporte a aceleração por hardware CUDA.
   - Analisa espaço livre em disco para download dos pesos dos modelos.

2. **Cálculo Matemático de Memória:**
   - Calcula o tamanho dos pesos quantizados (Q4_K_M, Q8_0, FP16).
   - Calcula o overhead do KV Cache (janela de contexto) e runtime do sistema operacional.
   - Categoriza o resultado em 4 status visuais:
     - 🟢 **Roda Perfeito (GPU Acelerada):** Modelo cabe 100% na VRAM (velocidade máxima de 30 a 80+ tok/s).
     - 🟢/🟡 **Roda Fluido na CPU:** Modelos leves (0.5B a 3B) e Whisper rodando direto na RAM com resposta rápida.
     - 🟠 **Atenção (Memória no Limite):** Modelos que cabem no limite físico da RAM com risco de lentidão ou swap.
     - 🔴 **Incompatível:** Falta de memória que causaria Out of Memory (OOM) ou travamentos.

3. **Catálogo Rico de Modelos:**
   - **LLMs Leves:** Qwen 2.5 0.5B / 1.5B / 3B, Llama 3.2 1B / 3B, SmolLM2 1.7B, Gemma 2 2B.
   - **Modelos de Raciocínio & Código:** DeepSeek-R1 Distill 7B / 14B, Qwen 2.5 Coder 7B, Phi-4 14B.
   - **LLMs Médios & Grandes:** Llama 3.1 8B, Mistral 7B, Qwen 2.5 32B, Llama 3.3 70B.
   - **Visão & Multimodal:** Moondream 2, MiniCPM-V 2.6.
   - **Áudio & Transcrição:** Whisper Tiny, Small, Large-v3 Turbo.
   - **Geração de Imagens:** Stable Diffusion 1.5, SDXL Turbo, Flux.1 Schnell.

4. **Simulador de Upgrades Interativo:**
   - Experimente simular: *"E se eu adicionar +8GB de RAM ou comprar uma RTX 3060 de 12GB?"*.
   - Veja instantaneamente na tela os modelos sendo desbloqueados!

5. **Pronto para Uso (1-Click Copy):**
   - Botão para copiar comandos prontos do Ollama (ex: `ollama run qwen2.5:1.5b`) ou recomendações de executores (LM Studio, llama.cpp, ComfyUI).

---

## 🚀 Como Executar

### Opção 1: Inicialização com 1 Clique (Windows)
Basta dar um duplo clique no arquivo:
```cmd
start.bat
```
Ele abrirá automaticamente o backend Python e o frontend no navegador em `http://localhost:5173`.

---

### Opção 2: Execução Manual

#### 1. Backend (Python):
```cmd
cd backend
python -m pip install -r requirements.txt
python run.py
```
*O backend estará rodando em `http://127.0.0.1:8000` (documentação Swagger interativa em `/docs`).*

> **Nota:** Como o frontend já foi compilado para a pasta `frontend/dist`, você pode acessar a aplicação completa diretamente em `http://127.0.0.1:8000/` apenas iniciando o backend!

#### 2. Frontend (Modo Desenvolvimento com Hot-Reload):
```cmd
cd frontend
npm.cmd install
npm.cmd run dev
```
*O painel interativo abrirá em `http://localhost:5173`.*

---

## 📁 Estrutura de Pastas

```
ai-hardware-advisor/
├── backend/
│   ├── app/
│   │   ├── hardware.py       # Coleta de métricas reais da máquina
│   │   ├── models_db.py      # Catálogo de modelos e quantizações
│   │   ├── evaluator.py      # Motor de cálculo e diagnóstico
│   │   ├── schemas.py        # Modelos de dados Pydantic
│   │   └── main.py           # API FastAPI + Servidor SPA
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HardwareHeader.vue
│   │   │   ├── HardwareGauges.vue
│   │   │   ├── TopPicks.vue
│   │   │   ├── FilterBar.vue
│   │   │   ├── ModelCard.vue
│   │   │   └── UpgradeSimulator.vue
│   │   ├── App.vue
│   │   ├── style.css
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── start.bat
└── README.md
```
