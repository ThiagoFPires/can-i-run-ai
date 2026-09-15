from typing import List, Optional
from .schemas import HardwareInfo, ModelInfo, EvaluationResult, QuantProfile

def evaluate_model(hardware: HardwareInfo, model: ModelInfo, preferred_quant: Optional[str] = None) -> EvaluationResult:
    # Selecionar quantização padrão ou solicitada
    quant_key = preferred_quant if (preferred_quant and preferred_quant in model.quant_profiles) else model.default_quant
    if quant_key not in model.quant_profiles:
        quant_key = list(model.quant_profiles.keys())[0]
    
    profile: QuantProfile = model.quant_profiles[quant_key]
    
    vram_needed = profile.min_vram_gb
    ram_needed = profile.min_ram_gb
    weight_size = profile.weight_size_gb

    # Analisar GPU principal
    gpu = hardware.primary_gpu
    has_cuda = bool(gpu and gpu.cuda_supported)
    vram_available = gpu.vram_total_gb if gpu else 0.0
    ram_total = hardware.ram_total_gb
    ram_free = hardware.ram_available_gb

    # Caso especial: Modelos de Geração de Imagem (SD, Flux) exigem GPU moderna
    if model.category == "image":
        if has_cuda and vram_available >= vram_needed:
            return EvaluationResult(
                model_id=model.id,
                model=model,
                status="gpu_perfect",
                status_label="Roda Perfeito (GPU Acelerada)",
                status_color="emerald",
                selected_quant=quant_key,
                vram_required_gb=vram_needed,
                ram_required_gb=ram_needed,
                execution_mode="GPU (VRAM Nativa)",
                estimated_speed="2 a 10 segundos por imagem",
                compatibility_score=95,
                notes="Totalmente compatível com a sua GPU dedicada via PyTorch/CUDA e ComfyUI.",
                upgrade_recommendation=None
            )
        elif has_cuda and vram_available >= (vram_needed * 0.7) and ram_total >= ram_needed:
            return EvaluationResult(
                model_id=model.id,
                model=model,
                status="warning_marginal",
                status_label="Roda com Offload (Médio)",
                status_color="amber",
                selected_quant=quant_key,
                vram_required_gb=vram_needed,
                ram_required_gb=ram_needed,
                execution_mode="GPU + RAM compartilhada",
                estimated_speed="15 a 45 segundos por imagem",
                compatibility_score=65,
                notes="Pode ser necessário usar argumentos de baixo VRAM (--medvram ou --lowvram) no gerador.",
                upgrade_recommendation="Uma GPU com mais VRAM (12GB+) aceleraria a geração significativamente."
            )
        else:
            return EvaluationResult(
                model_id=model.id,
                model=model,
                status="incompatible",
                status_label="Inviável sem GPU Moderna",
                status_color="rose",
                selected_quant=quant_key,
                vram_required_gb=vram_needed,
                ram_required_gb=ram_needed,
                execution_mode="Inviável",
                estimated_speed="10+ minutos por imagem (CPU inviável)",
                compatibility_score=10,
                notes="Geração de imagens moderna necessita de aceleração por hardware CUDA com pelo menos 4GB-8GB de VRAM.",
                upgrade_recommendation="Recomendado: Adicionar uma GPU NVIDIA GeForce RTX (RTX 3060 12GB ou RTX 4060 8GB)."
            )

    # Caso 1: Roda 100% na GPU dedicada com CUDA
    if has_cuda and vram_available >= vram_needed:
        speed = "40 a 90 tokens/s (Ultra fluido)" if "0.5B" in model.parameters or "1B" in model.parameters or "2B" in model.parameters else "25 a 45 tokens/s (Muito rápido)"
        return EvaluationResult(
            model_id=model.id,
            model=model,
            status="gpu_perfect",
            status_label="Roda Perfeito (GPU Acelerada)",
            status_color="emerald",
            selected_quant=quant_key,
            vram_required_gb=vram_needed,
            ram_required_gb=ram_needed,
            execution_mode="GPU (100% VRAM)",
            estimated_speed=speed,
            compatibility_score=98,
            notes="Modelo cabe por completo na memória de vídeo da sua GPU. Respostas instantâneas e sem uso de CPU.",
            upgrade_recommendation=None
        )

    # Caso 2: Híbrido GPU + CPU (Se tiver GPU CUDA com VRAM parcial e RAM suficiente)
    if has_cuda and vram_available >= 3.5 and ram_total >= ram_needed:
        return EvaluationResult(
            model_id=model.id,
            model=model,
            status="cpu_viable",
            status_label="Roda Híbrido (GPU + CPU)",
            status_color="emerald",
            selected_quant=quant_key,
            vram_required_gb=vram_needed,
            ram_required_gb=ram_needed,
            execution_mode="Híbrido (GPU + RAM)",
            estimated_speed="12 a 25 tokens/s",
            compatibility_score=80,
            notes="O Ollama ou llama.cpp descarregará as camadas principais na GPU e o restante na RAM com bom desempenho.",
            upgrade_recommendation=None
        )

    # Caso 3: Execução via CPU (RAM do sistema)
    # Modelos pequenos (<= 3.5B) ou áudio (Whisper) rodam com ótima performance na CPU
    is_small_model = any(tag in model.parameters.upper() for tag in ["0.5B", "1B", "1.5B", "1.7B", "2B", "2.6B", "3B", "3.2B", "39M", "74M", "244M"]) or model.category == "audio"

    # Se a RAM total suporta com folga
    if ram_total >= ram_needed + 1.5:
        if is_small_model:
            return EvaluationResult(
                model_id=model.id,
                model=model,
                status="cpu_viable",
                status_label="Roda Fluido na CPU",
                status_color="emerald",
                selected_quant=quant_key,
                vram_required_gb=vram_needed,
                ram_required_gb=ram_needed,
                execution_mode="CPU (Inferência em RAM)",
                estimated_speed="12 a 25 tokens/s (Rápido e leve)",
                compatibility_score=85,
                notes="Modelo otimizado de baixo consumo. Roda com muita fluidez na CPU usando quantização GGUF.",
                upgrade_recommendation=None
            )
        elif ram_total >= ram_needed + 3.0:
            # Modelo de 7B a 9B com bastante RAM (ex: 16GB+)
            return EvaluationResult(
                model_id=model.id,
                model=model,
                status="cpu_viable",
                status_label="Roda na CPU (Velocidade Moderada)",
                status_color="emerald",
                selected_quant=quant_key,
                vram_required_gb=vram_needed,
                ram_required_gb=ram_needed,
                execution_mode="CPU (Inferência em RAM)",
                estimated_speed="6 a 12 tokens/s (Leitura confortável)",
                compatibility_score=75,
                notes="Sua memória RAM é suficiente para manter o modelo e o sistema operacional estáveis.",
                upgrade_recommendation="Uma GPU dedicada de 8GB-12GB multiplicaria a velocidade por 4x."
            )
        else:
            # Modelo de 7B a 8B em máquina de 8GB (como a do usuário)
            return EvaluationResult(
                model_id=model.id,
                model=model,
                status="warning_marginal",
                status_label="Atenção (Memória no Limite)",
                status_color="amber",
                selected_quant=quant_key,
                vram_required_gb=vram_needed,
                ram_required_gb=ram_needed,
                execution_mode="CPU (Aperto de Memória)",
                estimated_speed="3 a 6 tokens/s (Risco de swap)",
                compatibility_score=50,
                notes="O modelo consome quase toda a RAM livre. Recomendado fechar o navegador e outros programas antes de rodar.",
                upgrade_recommendation="Fazer upgrade para 16GB de RAM trará muito mais estabilidade."
            )

    # Se a RAM total cobre apenas o peso do modelo mas fica apertado com o Windows
    elif ram_total >= weight_size + 1.2:
        return EvaluationResult(
            model_id=model.id,
            model=model,
            status="warning_marginal",
            status_label="Memória Limítrofe (Pode Travar)",
            status_color="orange",
            selected_quant=quant_key,
            vram_required_gb=vram_needed,
            ram_required_gb=ram_needed,
            execution_mode="CPU (Swap / Paginação)",
            estimated_speed="1 a 4 tokens/s (Lento)",
            compatibility_score=40,
            notes="A memória livre atual é pouca. O sistema poderá usar o arquivo de paginação (disco), causando lentidão.",
            upgrade_recommendation=f"Recomendado expandir para no mínimo {int(ram_needed + 4)}GB de RAM."
        )

    # Caso 4: Incompatível (Não cabe na memória)
    else:
        return EvaluationResult(
            model_id=model.id,
            model=model,
            status="incompatible",
            status_label="Incompatível (Memória Insuficiente)",
            status_color="rose",
            selected_quant=quant_key,
            vram_required_gb=vram_needed,
            ram_required_gb=ram_needed,
            execution_mode="Inviável",
            estimated_speed="0 tokens/s (Risco de Out Of Memory)",
            compatibility_score=10,
            notes=f"Requer pelo menos {ram_needed:.1f} GB de memória RAM livre. Sua máquina possui {ram_total:.1f} GB no total.",
            upgrade_recommendation=f"Necessário upgrade para pelo menos {max(16, int(ram_needed + 4))}GB de RAM ou GPU com {int(vram_needed)}GB de VRAM."
        )

def evaluate_all_models(hardware: HardwareInfo, catalog: List[ModelInfo]) -> List[EvaluationResult]:
    results = [evaluate_model(hardware, m) for m in catalog]
    # Ordenar: primeiro os que rodam perfeito ou viável, e por popularidade/score
    status_order = {"gpu_perfect": 0, "cpu_viable": 1, "warning_marginal": 2, "incompatible": 3}
    results.sort(key=lambda r: (status_order.get(r.status, 9), -r.compatibility_score, not r.model.popular))
    return results
