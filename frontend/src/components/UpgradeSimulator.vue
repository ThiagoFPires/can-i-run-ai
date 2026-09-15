<script setup>
import { ref } from 'vue'
import { X, Sliders, RotateCcw, ArrowRight } from 'lucide-vue-next'

const props = defineProps({
  isOpen: Boolean,
  currentHardware: Object
})

const emit = defineEmits(['close', 'simulate', 'reset'])

const ramTotal = ref(props.currentHardware?.ram_total_gb ? Math.round(props.currentHardware.ram_total_gb) : 8)
const vramTotal = ref(props.currentHardware?.primary_gpu?.vram_total_gb || 0)
const gpuName = ref(props.currentHardware?.primary_gpu?.name || 'NVIDIA RTX 3060')
const cudaSupported = ref(true)

const presets = [
  {
    name: 'Upgrade +8GB RAM (16GB Total)',
    desc: 'Sem trocar placa de vídeo',
    ram: 16,
    vram: 0,
    gpu: 'Placa Integrada / CPU',
    cuda: false
  },
  {
    name: 'Gamer de Entrada (RTX 3060 12GB)',
    desc: '16GB RAM + 12GB VRAM (Ideal para IA)',
    ram: 16,
    vram: 12,
    gpu: 'NVIDIA GeForce RTX 3060 12GB',
    cuda: true
  },
  {
    name: 'Workstation IA (RTX 4070 12GB)',
    desc: '32GB RAM + 12GB VRAM GDDR6X',
    ram: 32,
    vram: 12,
    gpu: 'NVIDIA GeForce RTX 4070 12GB',
    cuda: true
  },
  {
    name: 'Enthusiast Pro (RTX 4090 24GB)',
    desc: '64GB RAM + 24GB VRAM (Roda 70B e Flux)',
    ram: 64,
    vram: 24,
    gpu: 'NVIDIA GeForce RTX 4090 24GB',
    cuda: true
  }
]

const applyPreset = (preset) => {
  ramTotal.value = preset.ram
  vramTotal.value = preset.vram
  gpuName.value = preset.gpu
  cudaSupported.value = preset.cuda
}

const handleSimulate = () => {
  emit('simulate', {
    ram_total_gb: Number(ramTotal.value),
    vram_total_gb: Number(vramTotal.value),
    gpu_name: gpuName.value,
    gpu_vendor: gpuName.value.toLowerCase().includes('nvidia') ? 'nvidia' : 'amd',
    cuda_supported: cudaSupported.value
  })
  emit('close')
}

const handleReset = () => {
  emit('reset')
  emit('close')
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm">
    <div class="neutral-card border border-zinc-700 w-full max-w-xl rounded-3xl p-6 shadow-2xl relative">
      <!-- Close Button -->
      <button
        @click="emit('close')"
        class="absolute top-5 right-5 p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-800 transition"
      >
        <X class="w-5 h-5" />
      </button>

      <!-- Modal Header -->
      <div class="flex items-center gap-3 mb-6">
        <div class="p-2.5 rounded-xl bg-zinc-900 border border-zinc-700 text-white">
          <Sliders class="w-5 h-5" />
        </div>
        <div>
          <h2 class="text-xl font-bold text-white">Simulador de Upgrade de Hardware</h2>
          <p class="text-xs text-zinc-400">
            Descubra quais modelos serão desbloqueados se você adicionar mais RAM ou uma nova GPU.
          </p>
        </div>
      </div>

      <!-- Presets -->
      <div class="mb-6">
        <label class="text-xs font-bold uppercase tracking-wider text-zinc-400 block mb-2">
          Configurações Prontas
        </label>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <button
            v-for="p in presets"
            :key="p.name"
            @click="applyPreset(p)"
            class="text-left p-2.5 rounded-xl bg-zinc-900/90 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-600 transition group"
          >
            <div class="text-xs font-bold text-white group-hover:text-zinc-200">{{ p.name }}</div>
            <div class="text-[11px] text-zinc-500">{{ p.desc }}</div>
          </button>
        </div>
      </div>

      <!-- Custom Adjustments -->
      <div class="space-y-4 mb-6 p-4 rounded-2xl bg-zinc-900/90 border border-zinc-800">
        <!-- RAM Slider -->
        <div>
          <div class="flex justify-between items-center text-xs mb-1.5">
            <span class="font-medium text-zinc-300">Memória RAM do Sistema:</span>
            <span class="font-mono font-bold text-white text-sm">{{ ramTotal }} GB</span>
          </div>
          <input
            v-model="ramTotal"
            type="range"
            min="4"
            max="128"
            step="4"
            class="w-full accent-white cursor-pointer"
          />
          <div class="flex justify-between text-[10px] text-zinc-500 font-mono mt-1">
            <span>4 GB</span>
            <span>16 GB</span>
            <span>32 GB</span>
            <span>64 GB</span>
            <span>128 GB</span>
          </div>
        </div>

        <!-- VRAM Slider -->
        <div>
          <div class="flex justify-between items-center text-xs mb-1.5">
            <span class="font-medium text-zinc-300">Memória de Vídeo Dedicada (VRAM):</span>
            <span class="font-mono font-bold text-white text-sm">{{ vramTotal }} GB</span>
          </div>
          <input
            v-model="vramTotal"
            type="range"
            min="0"
            max="48"
            step="2"
            class="w-full accent-white cursor-pointer"
          />
          <div class="flex justify-between text-[10px] text-zinc-500 font-mono mt-1">
            <span>0 GB (CPU)</span>
            <span>8 GB</span>
            <span>12 GB</span>
            <span>16 GB</span>
            <span>24 GB</span>
            <span>48 GB</span>
          </div>
        </div>

        <!-- GPU Name & CUDA -->
        <div class="pt-2 flex flex-col sm:flex-row items-center gap-3">
          <input
            v-model="gpuName"
            type="text"
            placeholder="Nome da Placa (ex: RTX 3060)"
            class="flex-1 w-full bg-zinc-950 border border-zinc-700 rounded-xl px-3 py-2 text-xs text-white placeholder-zinc-500 outline-none focus:border-zinc-400"
          />

          <label class="flex items-center gap-2 text-xs text-zinc-300 cursor-pointer select-none shrink-0">
            <input
              v-model="cudaSupported"
              type="checkbox"
              class="w-4 h-4 rounded accent-white cursor-pointer"
            />
            <span>Aceleração CUDA</span>
          </label>
        </div>
      </div>

      <!-- Action Footer -->
      <div class="flex items-center justify-between gap-3 pt-2">
        <button
          @click="handleReset"
          class="flex items-center gap-1.5 px-4 py-2.5 text-xs font-semibold text-zinc-400 hover:text-white bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded-xl transition"
        >
          <RotateCcw class="w-3.5 h-3.5" />
          Restaurar PC Real
        </button>

        <button
          @click="handleSimulate"
          class="flex items-center gap-2 px-6 py-2.5 text-xs font-bold text-black bg-white hover:bg-zinc-200 rounded-xl shadow transition active:scale-95 ml-auto"
        >
          <span>Aplicar e Analisar</span>
          <ArrowRight class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>
