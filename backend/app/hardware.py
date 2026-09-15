import os
import platform
import subprocess
import shutil
import json
import psutil
from typing import List, Optional
from .schemas import HardwareInfo, GPUInfo

def _get_cpu_name() -> str:
    try:
        if platform.system() == "Windows":
            # Usar WMI via powershell rápido
            cmd = 'powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-CimInstance Win32_Processor).Name"'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=4)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip().split("\n")[0].strip()
    except Exception:
        pass
    return platform.processor() or "Processador Desconhecido"

def _detect_gpus() -> List[GPUInfo]:
    gpus: List[GPUInfo] = []
    
    # 1. Tentar nvidia-smi para GPUs NVIDIA com drivers modernos
    try:
        smi_path = shutil.which("nvidia-smi")
        if smi_path:
            cmd = 'nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader,nounits'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3)
            if res.returncode == 0 and res.stdout.strip():
                for line in res.stdout.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 4:
                        name = parts[0]
                        total_mb = float(parts[1])
                        free_mb = float(parts[2])
                        driver = parts[3]
                        # Modern nvidia-smi usually implies CUDA support
                        gpus.append(GPUInfo(
                            name=name,
                            vram_total_gb=round(total_mb / 1024, 2),
                            vram_free_gb=round(free_mb / 1024, 2),
                            vendor="nvidia",
                            cuda_supported=True,
                            driver_version=driver
                        ))
                if gpus:
                    return gpus
    except Exception:
        pass

    # 2. No Windows, consultar Win32_VideoController via WMI / PowerShell
    if platform.system() == "Windows":
        try:
            ps_cmd = (
                'powershell -NoProfile -ExecutionPolicy Bypass -Command '
                '"Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion | ConvertTo-Json"'
            )
            res = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    name = item.get("Name", "")
                    # Ignorar adaptadores virtuais de desktop remoto ou basic display se houver GPU real
                    if not name or "Remote Display" in name or "RDP" in name:
                        continue
                    
                    adapter_ram = item.get("AdapterRAM") or 0
                    # No Windows, AdapterRAM é unsigned 32-bit (máx 4GB reportado) ou bytes
                    # Se for positivo e razoável:
                    vram_gb = round(max(0, adapter_ram) / (1024**3), 2)
                    
                    vendor = "other"
                    name_lower = name.lower()
                    if "nvidia" in name_lower or "geforce" in name_lower or "quadro" in name_lower or "rtx" in name_lower:
                        vendor = "nvidia"
                    elif "amd" in name_lower or "radeon" in name_lower:
                        vendor = "amd"
                    elif "intel" in name_lower or "arc" in name_lower:
                        vendor = "intel"
                    
                    # Checar se a GPU suporta CUDA moderno (Ollama/PyTorch modernos exigem Compute Capability >= 5.0, ex: série GTX 900, 1000, RTX 20/30/40)
                    cuda_supported = False
                    if vendor == "nvidia":
                        # GPUs antigas como GeForce 210, 8400 GS, GT 610/710 não rodam CUDA moderno
                        legacy_keywords = ["geforce 2", "geforce 8", "geforce 9", "gt 2", "gt 4", "gt 6", "gt 7", "g210", "gt 210", "210"]
                        is_legacy = any(k in name_lower for k in legacy_keywords)
                        # Se tiver pelo menos 4GB e for GTX ou RTX moderna
                        if not is_legacy and ("gtx" in name_lower or "rtx" in name_lower or "tesla" in name_lower or "quadro" in name_lower or "a10" in name_lower or "t4" in name_lower):
                            cuda_supported = True
                        elif vram_gb >= 3.5 and not is_legacy:
                            cuda_supported = True

                    driver = item.get("DriverVersion", "Desconhecido")
                    
                    gpus.append(GPUInfo(
                        name=name,
                        vram_total_gb=vram_gb,
                        vram_free_gb=vram_gb,  # estimativa baseada no total
                        vendor=vendor,
                        cuda_supported=cuda_supported,
                        driver_version=str(driver)
                    ))
        except Exception:
            pass

    return gpus

def get_system_hardware() -> HardwareInfo:
    # Memória RAM
    vm = psutil.virtual_memory()
    ram_total_gb = round(vm.total / (1024**3), 2)
    ram_available_gb = round(vm.available / (1024**3), 2)
    ram_used_gb = round(vm.used / (1024**3), 2)

    # CPU
    cpu_cores_physical = psutil.cpu_count(logical=False) or 2
    cpu_cores_logical = psutil.cpu_count(logical=True) or 4
    cpu_name = _get_cpu_name()

    # GPU
    gpus = _detect_gpus()
    # Escolher GPU primária com mais VRAM ou com CUDA
    primary_gpu = None
    if gpus:
        # Priorizar GPUs com CUDA e depois maior VRAM
        sorted_gpus = sorted(gpus, key=lambda g: (1 if g.cuda_supported else 0, g.vram_total_gb), reverse=True)
        primary_gpu = sorted_gpus[0]

    # Espaço em disco (drive do SO ou atual)
    disk_path = "C:\\" if os.name == "nt" else "/"
    try:
        disk_usage = shutil.disk_usage(disk_path)
        disk_free_gb = round(disk_usage.free / (1024**3), 2)
    except Exception:
        disk_free_gb = 50.0

    return HardwareInfo(
        cpu_name=cpu_name,
        cpu_cores_physical=cpu_cores_physical,
        cpu_cores_logical=cpu_cores_logical,
        ram_total_gb=ram_total_gb,
        ram_available_gb=ram_available_gb,
        ram_used_gb=ram_used_gb,
        gpus=gpus,
        primary_gpu=primary_gpu,
        os_name=platform.system(),
        os_version=f"{platform.release()} ({platform.version()})",
        disk_free_gb=disk_free_gb,
        is_simulated=False
    )
