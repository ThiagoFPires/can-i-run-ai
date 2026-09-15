from typing import List, Dict
from .schemas import ModelInfo, QuantProfile

MODELS_CATALOG: List[ModelInfo] = [
    # ------------------ ULTRA-LEVES (0.5B - 3B) ------------------
    ModelInfo(
        id="qwen-2.5-0.5b",
        name="Qwen 2.5 0.5B",
        category="llm",
        creator="Alibaba Cloud",
        parameters="0.5B",
        description="LLM ultra-compacto com suporte a múltiplos idiomas e raciocínio básico. Roda até em celulares ou computadores muito antigos.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=0.4, min_vram_gb=1.0, min_ram_gb=1.5, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=0.6, min_vram_gb=1.2, min_ram_gb=2.0, recommended_context=4096),
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=1.0, min_vram_gb=1.8, min_ram_gb=2.5, recommended_context=4096)
        },
        tags=["Ultra-leve", "Multilíngue", "Rápido"],
        ollama_model="qwen2.5:0.5b",
        recommended_runner="Ollama / LM Studio"
    ),
    ModelInfo(
        id="llama-3.2-1b",
        name="Llama 3.2 1B",
        category="llm",
        creator="Meta",
        parameters="1B",
        description="Modelo de borda da Meta otimizado para tarefas leves, resumos, reescrita de textos e conversação rápida sem placa de vídeo.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=0.8, min_vram_gb=1.5, min_ram_gb=2.2, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=1.3, min_vram_gb=2.0, min_ram_gb=2.8, recommended_context=4096),
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=2.4, min_vram_gb=3.5, min_ram_gb=4.5, recommended_context=4096)
        },
        tags=["Meta", "Borda / Edge", "Baixo Consumo"],
        ollama_model="llama3.2:1b",
        recommended_runner="Ollama / LM Studio"
    ),
    ModelInfo(
        id="qwen-2.5-1.5b",
        name="Qwen 2.5 1.5B",
        category="llm",
        creator="Alibaba Cloud",
        parameters="1.5B",
        description="Equilíbrio fantástico entre tamanho ínfimo e inteligência. Supera muitos modelos antigos de 7B em lógica e formatação.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=1.1, min_vram_gb=1.8, min_ram_gb=2.5, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=1.8, min_vram_gb=2.5, min_ram_gb=3.5, recommended_context=4096),
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=3.2, min_vram_gb=4.5, min_ram_gb=5.5, recommended_context=4096)
        },
        tags=["Popular", "Raciocínio Leve", "Recomendado"],
        ollama_model="qwen2.5:1.5b",
        recommended_runner="Ollama / LM Studio"
    ),
    ModelInfo(
        id="smollm2-1.7b",
        name="SmolLM2 1.7B",
        category="llm",
        creator="Hugging Face",
        parameters="1.7B",
        description="Criado pela Hugging Face especificamente para rodar localmente no dispositivo com alta eficiência e dados de alta qualidade.",
        popular=False,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=1.2, min_vram_gb=2.0, min_ram_gb=2.8, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=1.9, min_vram_gb=2.8, min_ram_gb=3.8, recommended_context=4096)
        },
        tags=["HuggingFace", "Eficiente", "Open Source"],
        ollama_model="smollm2:1.7b",
        recommended_runner="Ollama / llama.cpp"
    ),
    ModelInfo(
        id="gemma-2-2b",
        name="Gemma 2 2B",
        category="llm",
        creator="Google DeepMind",
        parameters="2.6B",
        description="Arquitetura de ponta do Google DeepMind com destilação de conhecimento de modelos gigantes. Respostas refinadas e precisas.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=1.7, min_vram_gb=2.5, min_ram_gb=3.5, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=2.8, min_vram_gb=3.8, min_ram_gb=4.8, recommended_context=4096)
        },
        tags=["Google", "DeepMind", "Alta Qualidade"],
        ollama_model="gemma2:2b",
        recommended_runner="Ollama / LM Studio"
    ),
    ModelInfo(
        id="llama-3.2-3b",
        name="Llama 3.2 3B",
        category="llm",
        creator="Meta",
        parameters="3.2B",
        description="O modelo pequeno mais inteligente da Meta. Excelente para redação, auxílio em tarefas e extração de dados.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=2.0, min_vram_gb=3.0, min_ram_gb=4.0, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=3.4, min_vram_gb=4.5, min_ram_gb=5.5, recommended_context=4096)
        },
        tags=["Meta", "Muito Popular", "Equilibrado"],
        ollama_model="llama3.2:3b",
        recommended_runner="Ollama / LM Studio"
    ),

    # ------------------ MÉDIOS (7B - 9B) ------------------
    ModelInfo(
        id="deepseek-r1-distill-qwen-7b",
        name="DeepSeek-R1 Distill Qwen 7B",
        category="reasoning",
        creator="DeepSeek",
        parameters="7B",
        description="Modelo de raciocínio profundo (Chain-of-Thought) destilado do DeepSeek-R1. Excelente em matemática, lógica e programação.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=4.7, min_vram_gb=6.0, min_ram_gb=8.0, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=7.6, min_vram_gb=9.0, min_ram_gb=12.0, recommended_context=4096)
        },
        tags=["Raciocínio CoT", "DeepSeek", "Lógica / Math"],
        ollama_model="deepseek-r1:7b",
        recommended_runner="Ollama / LM Studio"
    ),
    ModelInfo(
        id="llama-3.1-8b",
        name="Llama 3.1 8B",
        category="llm",
        creator="Meta",
        parameters="8B",
        description="O padrão da indústria para modelos de 8 bilhões de parâmetros. Suporta 128k de contexto, fluente e versátil.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=4.9, min_vram_gb=6.5, min_ram_gb=8.5, recommended_context=8192),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=8.5, min_vram_gb=10.0, min_ram_gb=13.0, recommended_context=8192)
        },
        tags=["Meta", "Padrão da Indústria", "128k Contexto"],
        ollama_model="llama3.1:8b",
        recommended_runner="Ollama / LM Studio"
    ),
    ModelInfo(
        id="qwen-2.5-coder-7b",
        name="Qwen 2.5 Coder 7B",
        category="code",
        creator="Alibaba Cloud",
        parameters="7B",
        description="Especialista em programação, depuração de código e geração de testes em mais de 90 linguagens de programação.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=4.7, min_vram_gb=6.0, min_ram_gb=8.0, recommended_context=8192),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=7.6, min_vram_gb=9.0, min_ram_gb=12.0, recommended_context=8192)
        },
        tags=["Programação", "Código", "Python/JS/Rust"],
        ollama_model="qwen2.5-coder:7b",
        recommended_runner="Ollama / LM Studio / Continue.dev"
    ),
    ModelInfo(
        id="mistral-7b-instruct",
        name="Mistral 7B Instruct v0.3",
        category="llm",
        creator="Mistral AI",
        parameters="7.3B",
        description="Modelo europeu aclamado pelo seguimento de instruções concisas, suporte a function calling nativo e rapidez.",
        popular=False,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=4.4, min_vram_gb=5.8, min_ram_gb=7.5, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=7.7, min_vram_gb=9.0, min_ram_gb=11.5, recommended_context=4096)
        },
        tags=["Mistral", "Instruções", "Function Calling"],
        ollama_model="mistral:7b",
        recommended_runner="Ollama / LM Studio"
    ),

    # ------------------ INTERMEDIÁRIOS FORTES (14B) ------------------
    ModelInfo(
        id="deepseek-r1-distill-qwen-14b",
        name="DeepSeek-R1 Distill 14B",
        category="reasoning",
        creator="DeepSeek",
        parameters="14B",
        description="Raciocínio de altíssimo nível. Supera o GPT-4o em diversos benchmarks de matemática e raciocínio dedutivo complexo.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=9.0, min_vram_gb=11.5, min_ram_gb=14.0, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=15.0, min_vram_gb=18.0, min_ram_gb=22.0, recommended_context=4096)
        },
        tags=["Alta Precisão", "DeepSeek", "Top Raciocínio"],
        ollama_model="deepseek-r1:14b",
        recommended_runner="Ollama / LM Studio"
    ),
    ModelInfo(
        id="phi-4-14b",
        name="Phi-4 14B",
        category="reasoning",
        creator="Microsoft",
        parameters="14B",
        description="Modelo da Microsoft treinado com dados sintéticos rigorosos. Pontuações impressionantes em raciocínio científico e código.",
        popular=False,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=9.1, min_vram_gb=11.5, min_ram_gb=14.5, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=15.2, min_vram_gb=18.0, min_ram_gb=22.5, recommended_context=4096)
        },
        tags=["Microsoft", "Acadêmico", "Ciência & Lógica"],
        ollama_model="phi4:latest",
        recommended_runner="Ollama / LM Studio"
    ),

    # ------------------ GRANDES (32B - 70B) ------------------
    ModelInfo(
        id="qwen-2.5-32b",
        name="Qwen 2.5 32B",
        category="llm",
        creator="Alibaba Cloud",
        parameters="32B",
        description="Poder de nível quase frontier rodando localmente. Exige GPUs de 16GB-24GB ou workstations com 32GB+ de RAM.",
        popular=False,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=19.8, min_vram_gb=22.0, min_ram_gb=28.0, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=34.0, min_vram_gb=38.0, min_ram_gb=44.0, recommended_context=4096)
        },
        tags=["Alta Capacidade", "Heavy Duty", "Semi-Frontier"],
        ollama_model="qwen2.5:32b",
        recommended_runner="Ollama / LM Studio / vLLM"
    ),
    ModelInfo(
        id="llama-3.3-70b",
        name="Llama 3.3 70B",
        category="llm",
        creator="Meta",
        parameters="70B",
        description="O modelo de código aberto mais capaz da Meta. Nível similar a GPT-4, exige configurações profissionais de hardware.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=42.5, min_vram_gb=48.0, min_ram_gb=56.0, recommended_context=4096),
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=74.0, min_vram_gb=80.0, min_ram_gb=90.0, recommended_context=4096)
        },
        tags=["Meta Topo de Linha", "Frontier Local", "Extremo"],
        ollama_model="llama3.3:70b",
        recommended_runner="vLLM / llama.cpp / Multi-GPU"
    ),

    # ------------------ VISÃO & MULTIMODAL ------------------
    ModelInfo(
        id="moondream-2",
        name="Moondream 2",
        category="vision",
        creator="Vikhyat",
        parameters="1.8B",
        description="Modelo de visão computacional super rápido. Analisa fotos, descreve cenas e responde perguntas visuais em frações de segundo.",
        popular=True,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=1.2, min_vram_gb=2.0, min_ram_gb=3.0, recommended_context=2048),
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=3.5, min_vram_gb=4.5, min_ram_gb=5.5, recommended_context=2048)
        },
        tags=["Visão Ultra-Leve", "Fotos & OCR", "Tempo Real"],
        ollama_model="moondream:latest",
        recommended_runner="Ollama / Transformers"
    ),
    ModelInfo(
        id="minicpm-v-2.6",
        name="MiniCPM-V 2.6 (8B)",
        category="vision",
        creator="OpenBMB",
        parameters="8B",
        description="Excelente modelo multimodal para OCR denso, gráficos, leitura de recibos e até compreensão de trechos curtos de vídeo.",
        popular=False,
        default_quant="Q4_K_M",
        quant_profiles={
            "Q4_K_M": QuantProfile(quant_name="Q4_K_M", weight_size_gb=5.5, min_vram_gb=7.0, min_ram_gb=9.0, recommended_context=4096)
        },
        tags=["Visão Avançada", "OCR / Gráficos", "Vídeo"],
        ollama_model="minicpm-v:latest",
        recommended_runner="Ollama / llama.cpp"
    ),

    # ------------------ ÁUDIO / RECONHECIMENTO DE VOZ ------------------
    ModelInfo(
        id="whisper-tiny",
        name="Whisper Tiny",
        category="audio",
        creator="OpenAI",
        parameters="39M",
        description="Transcrição de fala em tempo real para múltiplos idiomas. Consumo quase nulo de memória.",
        popular=True,
        default_quant="FP16",
        quant_profiles={
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=0.1, min_vram_gb=0.4, min_ram_gb=0.8, recommended_context=1024)
        },
        tags=["Transcrição Voz", "Super Rápido", "OpenAI"],
        ollama_model=None,
        recommended_runner="faster-whisper / whisper.cpp"
    ),
    ModelInfo(
        id="whisper-small",
        name="Whisper Small",
        category="audio",
        creator="OpenAI",
        parameters="244M",
        description="Excelente acurácia em português e inglês para transcrição de áudio, entrevistas e legendas.",
        popular=True,
        default_quant="FP16",
        quant_profiles={
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=0.5, min_vram_gb=1.2, min_ram_gb=1.8, recommended_context=1024)
        },
        tags=["Transcrição Acurada", "Multilíngue", "OpenAI"],
        ollama_model=None,
        recommended_runner="faster-whisper / WhisperX"
    ),
    ModelInfo(
        id="whisper-large-v3-turbo",
        name="Whisper Large v3 Turbo",
        category="audio",
        creator="OpenAI",
        parameters="809M",
        description="Versão topo de linha otimizada do Whisper. Máxima acurácia na transcrição com pontuação e vocabulário técnico.",
        popular=True,
        default_quant="FP16",
        quant_profiles={
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=1.6, min_vram_gb=2.5, min_ram_gb=3.5, recommended_context=1024)
        },
        tags=["Topo de Linha Áudio", "Máxima Precisão", "OpenAI"],
        ollama_model=None,
        recommended_runner="faster-whisper / PyTorch"
    ),

    # ------------------ GERAÇÃO DE IMAGEM ------------------
    ModelInfo(
        id="stable-diffusion-1.5",
        name="Stable Diffusion 1.5",
        category="image",
        creator="Runway / Stability AI",
        parameters="1B",
        description="O clássico mais compatível para geração de imagens. Grande acervo de LoRAs e Checkpoints compatível com GPUs modestas.",
        popular=True,
        default_quant="FP16",
        quant_profiles={
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=2.1, min_vram_gb=4.0, min_ram_gb=8.0, recommended_context=1)
        },
        tags=["Geração de Imagens", "LoRA", "ComfyUI / WebUI"],
        ollama_model=None,
        recommended_runner="ComfyUI / Automatic1111 / Fooocus"
    ),
    ModelInfo(
        id="sdxl-turbo",
        name="SDXL Turbo",
        category="image",
        creator="Stability AI",
        parameters="3.5B",
        description="Geração de imagens em altíssima qualidade com apenas 1 a 4 passos de inferência. Quase instantâneo em GPUs RTX.",
        popular=False,
        default_quant="FP16",
        quant_profiles={
            "FP16": QuantProfile(quant_name="FP16", weight_size_gb=6.8, min_vram_gb=8.0, min_ram_gb=12.0, recommended_context=1)
        },
        tags=["1-Step Image", "Alta Resolução", "Stability AI"],
        ollama_model=None,
        recommended_runner="ComfyUI / Fooocus"
    ),
    ModelInfo(
        id="flux-1-schnell",
        name="Flux.1 Schnell (8-bit)",
        category="image",
        creator="Black Forest Labs",
        parameters="12B",
        description="O modelo de geração de imagem state-of-the-art dos mesmos criadores do Stable Diffusion original. Exige hardware robusto.",
        popular=True,
        default_quant="Q8_0",
        quant_profiles={
            "Q8_0": QuantProfile(quant_name="Q8_0", weight_size_gb=12.0, min_vram_gb=12.0, min_ram_gb=20.0, recommended_context=1)
        },
        tags=["Black Forest Labs", "Foto-realismo", "Ultra Qualidade"],
        ollama_model=None,
        recommended_runner="ComfyUI / Forge WebUI"
    )
]

def get_catalog() -> List[ModelInfo]:
    return MODELS_CATALOG
