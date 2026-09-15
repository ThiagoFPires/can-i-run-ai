from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class GPUInfo(BaseModel):
    name: str
    vram_total_gb: float
    vram_free_gb: float
    vendor: str  # "nvidia", "amd", "intel", "apple", "other"
    cuda_supported: bool = False
    driver_version: Optional[str] = None

class HardwareInfo(BaseModel):
    cpu_name: str
    cpu_cores_physical: int
    cpu_cores_logical: int
    ram_total_gb: float
    ram_available_gb: float
    ram_used_gb: float
    gpus: List[GPUInfo] = []
    primary_gpu: Optional[GPUInfo] = None
    os_name: str
    os_version: str
    disk_free_gb: float
    is_simulated: bool = False

class QuantProfile(BaseModel):
    quant_name: str  # e.g., "Q4_K_M", "Q8_0", "FP16"
    weight_size_gb: float
    min_vram_gb: float
    min_ram_gb: float
    recommended_context: int = 4096

class ModelInfo(BaseModel):
    id: str
    name: str
    category: str  # "llm", "image", "audio", "vision", "reasoning", "code"
    creator: str
    parameters: str
    description: str
    popular: bool = False
    default_quant: str
    quant_profiles: Dict[str, QuantProfile]
    tags: List[str] = []
    ollama_model: Optional[str] = None
    recommended_runner: str = "Ollama / LM Studio"

class EvaluationResult(BaseModel):
    model_id: str
    model: ModelInfo
    status: str  # "gpu_perfect", "cpu_viable", "warning_marginal", "incompatible"
    status_label: str
    status_color: str  # "emerald", "amber", "orange", "rose"
    selected_quant: str
    vram_required_gb: float
    ram_required_gb: float
    execution_mode: str  # "GPU (Acelerado)", "CPU (Viável)", "CPU (Lento / Risco de Swap)", "Inviável"
    estimated_speed: str
    compatibility_score: int  # 0 to 100
    notes: str
    upgrade_recommendation: Optional[str] = None

class SimulationRequest(BaseModel):
    ram_total_gb: float
    gpu_name: Optional[str] = None
    vram_total_gb: float = 0.0
    gpu_vendor: str = "nvidia"
    cuda_supported: bool = True
