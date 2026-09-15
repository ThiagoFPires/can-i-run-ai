import os
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List

from .schemas import HardwareInfo, ModelInfo, EvaluationResult, SimulationRequest, GPUInfo
from .hardware import get_system_hardware
from .models_db import get_catalog
from .evaluator import evaluate_all_models, evaluate_model

app = FastAPI(
    title="Can I Run AI? - Hardware Advisor",
    description="Sistema de Análise de Compatibilidade de Modelos de IA no Hardware do Usuário",
    version="1.0.0"
)

# Configuração de CORS para permitir acesso a partir do Vite (porta 5173 ou qualquer porta local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hardware", response_model=HardwareInfo)
def get_hardware():
    """Retorna as especificações de hardware reais do computador."""
    return get_system_hardware()

@app.get("/api/models", response_model=List[ModelInfo])
def list_models():
    """Retorna o catálogo de modelos disponíveis para análise."""
    return get_catalog()

@app.get("/api/evaluate")
def evaluate_current():
    """Avalia todos os modelos contra o hardware atual do computador."""
    hardware = get_system_hardware()
    catalog = get_catalog()
    results = evaluate_all_models(hardware, catalog)
    
    # Top 3 recomendações ideais para o PC atual
    top_picks = [r for r in results if r.status in ["gpu_perfect", "cpu_viable"]][:4]
    
    return {
        "hardware": hardware,
        "results": results,
        "top_picks": top_picks,
        "total_models": len(catalog),
        "compatible_count": len([r for r in results if r.status in ["gpu_perfect", "cpu_viable"]])
    }

@app.post("/api/simulate")
def simulate_hardware(req: SimulationRequest):
    """Simula uma configuração de hardware customizada (ex: upgrade de RAM ou GPU)."""
    current_hw = get_system_hardware()
    
    simulated_gpu = None
    if req.vram_total_gb > 0:
        simulated_gpu = GPUInfo(
            name=req.gpu_name or f"GPU Simulada {req.vram_total_gb}GB",
            vram_total_gb=req.vram_total_gb,
            vram_free_gb=req.vram_total_gb,
            vendor=req.gpu_vendor,
            cuda_supported=req.cuda_supported,
            driver_version="Simulado"
        )
    
    simulated_hw = HardwareInfo(
        cpu_name=current_hw.cpu_name,
        cpu_cores_physical=current_hw.cpu_cores_physical,
        cpu_cores_logical=current_hw.cpu_cores_logical,
        ram_total_gb=req.ram_total_gb,
        ram_available_gb=round(req.ram_total_gb * 0.8, 2),
        ram_used_gb=round(req.ram_total_gb * 0.2, 2),
        gpus=[simulated_gpu] if simulated_gpu else [],
        primary_gpu=simulated_gpu,
        os_name=current_hw.os_name,
        os_version=current_hw.os_version,
        disk_free_gb=current_hw.disk_free_gb,
        is_simulated=True
    )
    
    catalog = get_catalog()
    results = evaluate_all_models(simulated_hw, catalog)
    top_picks = [r for r in results if r.status in ["gpu_perfect", "cpu_viable"]][:4]
    
    return {
        "hardware": simulated_hw,
        "results": results,
        "top_picks": top_picks,
        "total_models": len(catalog),
        "compatible_count": len([r for r in results if r.status in ["gpu_perfect", "cpu_viable"]])
    }

# Servir o frontend compilado se existir
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(frontend_dist / "index.html")
