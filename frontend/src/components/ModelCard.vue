<script setup>
import { ref, computed } from 'vue'
import { Check, Terminal, Cpu, Layers, Lightbulb } from 'lucide-vue-next'

const props = defineProps({
  result: {
    type: Object,
    required: true
  },
  systemHardware: {
    type: Object,
    required: true
  }
})

const selectedQuant = ref(props.result.selected_quant)
const copied = ref(false)

const currentProfile = computed(() => {
  return props.result.model.quant_profiles[selectedQuant.value] || props.result.model.quant_profiles[props.result.model.default_quant]
})

// Recalcular status dinamicamente se o usuário alternar a quantização
const dynamicStatus = computed(() => {
  const profile = currentProfile.value
  if (!profile) return props.result

  const vramNeeded = profile.min_vram_gb
  const ramNeeded = profile.min_ram_gb
  const gpu = props.systemHardware?.primary_gpu
  const hasCuda = Boolean(gpu && gpu.cuda_supported)
  const vramAvail = gpu ? gpu.vram_total_gb : 0
  const ramTotal = props.systemHardware ? props.systemHardware.ram_total_gb : 8

  if (props.result.model.category === 'image') {
    if (hasCuda && vramAvail >= vramNeeded) {
      return {
        status: 'gpu_perfect',
        status_label: 'Roda Perfeito (GPU)',
        status_color: 'emerald',
        isCompatible: true,
        execution_mode: 'GPU (VRAM Nativa)',
        speed: '2 a 10s / imagem'
      }
    } else if (hasCuda && vramAvail >= (vramNeeded * 0.7) && ramTotal >= ramNeeded) {
      return {
        status: 'warning_marginal',
        status_label: 'Roda com Offload',
        status_color: 'amber',
        isCompatible: true,
        execution_mode: 'GPU + RAM compartilhada',
        speed: '15 a 45s / imagem'
      }
    } else {
      return {
        status: 'incompatible',
        status_label: 'Inviável sem GPU',
        status_color: 'rose',
        isCompatible: false,
        execution_mode: 'Inviável',
        speed: '0 img/s'
      }
    }
  }

  if (hasCuda && vramAvail >= vramNeeded) {
    return {
      status: 'gpu_perfect',
      status_label: 'Roda Perfeito (GPU)',
      status_color: 'emerald',
      isCompatible: true,
      execution_mode: 'GPU (100% VRAM)',
      speed: '30 a 80+ tokens/s'
    }
  }

  if (hasCuda && vramAvail >= 3.5 && ramTotal >= ramNeeded) {
    return {
      status: 'cpu_viable',
      status_label: 'Roda Híbrido (GPU+RAM)',
      status_color: 'emerald',
      isCompatible: true,
      execution_mode: 'Híbrido (GPU + RAM)',
      speed: '12 a 25 tokens/s'
    }
  }

  // CPU
  const isSmall = ['0.5B', '1B', '1.5B', '1.7B', '2B', '2.6B', '3B', '3.2B', '39M', '74M', '244M'].some(s => props.result.model.parameters.includes(s)) || props.result.model.category === 'audio'
  if (ramTotal >= ramNeeded + 1.5) {
    return {
      status: 'cpu_viable',
      status_label: isSmall ? 'Roda Fluido na CPU' : 'Roda na CPU (Moderado)',
      status_color: 'emerald',
      isCompatible: true,
      execution_mode: 'CPU (Inferência em RAM)',
      speed: isSmall ? '12 a 25 tokens/s' : '6 a 12 tokens/s'
    }
  } else if (ramTotal >= profile.weight_size_gb + 1.2) {
    return {
      status: 'warning_marginal',
      status_label: 'Atenção (RAM no Limite)',
      status_color: 'amber',
      isCompatible: true,
      execution_mode: 'CPU (Risco de Swap)',
      speed: '2 a 5 tokens/s'
    }
  } else {
    return {
      status: 'incompatible',
      status_label: 'Incompatível (Falta de RAM)',
      status_color: 'rose',
      isCompatible: false,
      execution_mode: 'Inviável',
      speed: '0 tokens/s'
    }
  }
})

const copyOllama = () => {
  if (!props.result.model.ollama_model) return
  const cmd = `ollama run ${props.result.model.ollama_model}`
  navigator.clipboard.writeText(cmd)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>

<template>
  <div
    class="neutral-card neutral-card-hover rounded-2xl p-5 flex flex-col justify-between"
    :class="{ 'opacity-70 hover:opacity-100': !dynamicStatus.isCompatible }"
  >
    <!-- Top Header of Card -->
    <div>
      <div class="flex items-start justify-between gap-3 mb-3">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="text-[11px] font-bold uppercase tracking-wider text-zinc-400">
              {{ result.model.creator }}
            </span>
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-zinc-900 border border-zinc-800 text-zinc-300">
              {{ result.model.parameters }}
            </span>
          </div>
          <h3 class="text-base font-bold text-white tracking-tight">
            {{ result.model.name }}
          </h3>
        </div>

        <!-- Status Badge Estilo Dashboard (Verde, Amarelo, Vermelho) -->
        <div
          class="px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 shrink-0 border"
          :class="{
            'bg-emerald-500/10 text-emerald-400 border-emerald-500/30': dynamicStatus.status_color === 'emerald',
            'bg-amber-500/10 text-amber-300 border-amber-500/30': dynamicStatus.status_color === 'amber',
            'bg-rose-500/10 text-rose-400 border-rose-500/30': dynamicStatus.status_color === 'rose',
          }"
        >
          <span
            class="w-1.5 h-1.5 rounded-full"
            :class="{
              'bg-emerald-400 animate-pulse': dynamicStatus.status_color === 'emerald',
              'bg-amber-400': dynamicStatus.status_color === 'amber',
              'bg-rose-400': dynamicStatus.status_color === 'rose',
            }"
          ></span>
          {{ dynamicStatus.status_label }}
        </div>
      </div>

      <!-- Description -->
      <p class="text-xs text-zinc-400 leading-relaxed mb-4">
        {{ result.model.description }}
      </p>

      <!-- Execution Mode & Speed Pill -->
      <div class="grid grid-cols-2 gap-2 mb-4 p-2.5 rounded-xl bg-zinc-900/90 border border-zinc-800 text-xs">
        <div>
          <span class="text-[11px] text-zinc-500 block">Modo:</span>
          <span class="font-medium text-zinc-200 flex items-center gap-1 truncate">
            <Cpu class="w-3.5 h-3.5 text-zinc-400 shrink-0" />
            {{ dynamicStatus.execution_mode }}
          </span>
        </div>
        <div>
          <span class="text-[11px] text-zinc-500 block">Velocidade:</span>
          <span
            class="font-semibold truncate font-mono"
            :class="dynamicStatus.status_color === 'emerald' ? 'text-emerald-400' : dynamicStatus.status_color === 'amber' ? 'text-amber-300' : 'text-rose-400'"
          >
            {{ dynamicStatus.speed }}
          </span>
        </div>
      </div>

      <!-- Quantization Selector & Memory Requirements -->
      <div class="mb-4">
        <div class="flex items-center justify-between text-xs mb-2">
          <span class="text-zinc-400 font-medium flex items-center gap-1">
            <Layers class="w-3.5 h-3.5 text-zinc-500" />
            Quantização:
          </span>
          <!-- Select Quantization -->
          <div class="flex items-center gap-1">
            <button
              v-for="qKey in Object.keys(result.model.quant_profiles)"
              :key="qKey"
              @click="selectedQuant = qKey"
              class="px-2 py-0.5 rounded text-[11px] font-mono transition border"
              :class="selectedQuant === qKey
                ? 'bg-white text-black border-white font-bold'
                : 'bg-zinc-900 text-zinc-400 border-zinc-800 hover:text-white'"
            >
              {{ qKey }}
            </button>
          </div>
        </div>

        <!-- Memory Breakdown -->
        <div class="space-y-1.5 pt-1 text-[11px] text-zinc-400">
          <div class="flex justify-between">
            <span>Tamanho dos Pesos:</span>
            <span class="font-mono text-zinc-200">{{ currentProfile?.weight_size_gb }} GB</span>
          </div>
          <div class="flex justify-between">
            <span>VRAM Mínima:</span>
            <span class="font-mono text-zinc-200">{{ currentProfile?.min_vram_gb }} GB</span>
          </div>
          <div class="flex justify-between">
            <span>RAM Mínima:</span>
            <span class="font-mono text-zinc-200">{{ currentProfile?.min_ram_gb }} GB</span>
          </div>
        </div>
      </div>

      <!-- Notes / Upgrade hint -->
      <div
        v-if="result.upgrade_recommendation && dynamicStatus.status !== 'gpu_perfect'"
        class="mb-4 p-2.5 rounded-xl bg-zinc-900/90 border border-zinc-800 text-[11px] text-zinc-300"
      >
        <div class="flex items-start gap-1.5">
          <Lightbulb class="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
          <span>{{ result.upgrade_recommendation }}</span>
        </div>
      </div>
    </div>

    <!-- Bottom Actions: Ollama copy or Runner -->
    <div class="pt-3 border-t border-zinc-800">
      <div v-if="result.model.ollama_model" class="flex items-center gap-2">
        <div class="flex-1 bg-zinc-950 border border-zinc-800 rounded-xl px-3 py-2 text-xs font-mono text-zinc-300 truncate">
          ollama run {{ result.model.ollama_model }}
        </div>
        <button
          @click="copyOllama"
          class="px-3.5 py-2 rounded-xl bg-white hover:bg-zinc-200 text-black font-semibold text-xs flex items-center gap-1.5 transition active:scale-95 shrink-0 shadow-sm"
        >
          <Check v-if="copied" class="w-3.5 h-3.5 text-emerald-600" />
          <Terminal v-else class="w-3.5 h-3.5" />
          <span>{{ copied ? 'Copiado' : 'Copiar' }}</span>
        </button>
      </div>

      <div v-else class="flex items-center justify-between text-xs py-1">
        <span class="text-zinc-500">Executar via:</span>
        <span class="font-medium text-zinc-300 font-mono">{{ result.model.recommended_runner }}</span>
      </div>
    </div>
  </div>
</template>
