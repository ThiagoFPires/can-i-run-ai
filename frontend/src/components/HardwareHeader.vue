<script setup>
import { computed } from 'vue'
import { Cpu, RefreshCw, Sliders, AlertCircle, Terminal } from 'lucide-vue-next'

const props = defineProps({
  hardware: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['open-simulator', 'reset-hardware', 'refresh'])

const gpuName = computed(() => {
  if (!props.hardware?.primary_gpu) return 'Placa Integrada / Sem GPU Dedicada'
  return props.hardware.primary_gpu.name.trim()
})
</script>

<template>
  <header class="mb-8">
    <!-- Top Bar -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-zinc-800/80">
      <div>
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-zinc-900 border border-zinc-700 flex items-center justify-center text-white shadow-sm">
            <Terminal class="w-5 h-5" />
          </div>
          <div>
            <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-white">
              Can I Run AI?
            </h1>
            <p class="text-xs md:text-sm text-zinc-400">
              Diagnóstico de compatibilidade de modelos de Inteligência Artificial para o seu hardware
            </p>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2.5">
        <button
          v-if="hardware?.is_simulated"
          @click="emit('reset-hardware')"
          class="flex items-center gap-2 px-3.5 py-2 text-xs md:text-sm font-medium bg-zinc-900 hover:bg-zinc-800 text-zinc-300 hover:text-white border border-zinc-700 rounded-xl transition"
        >
          <RefreshCw class="w-3.5 h-3.5" />
          Restaurar PC Real
        </button>

        <button
          @click="emit('open-simulator')"
          class="flex items-center gap-2 px-4 py-2 text-xs md:text-sm font-semibold bg-white hover:bg-zinc-200 text-black rounded-xl shadow transition active:scale-95"
        >
          <Sliders class="w-4 h-4" />
          Simular Upgrades
        </button>

        <button
          @click="emit('refresh')"
          :disabled="loading"
          class="p-2.5 text-zinc-400 hover:text-white bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 rounded-xl transition"
          title="Recarregar Diagnóstico"
        >
          <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
        </button>
      </div>
    </div>

    <!-- Simulated Banner -->
    <div
      v-if="hardware?.is_simulated"
      class="mt-4 p-3.5 bg-zinc-900 border border-zinc-700 rounded-xl flex items-center justify-between gap-3 text-zinc-300 text-xs md:text-sm"
    >
      <div class="flex items-center gap-2">
        <AlertCircle class="w-4 h-4 text-white shrink-0" />
        <span>Você está visualizando em <strong>Modo Simulado</strong> (Especificações Virtuais).</span>
      </div>
      <button @click="emit('reset-hardware')" class="text-white underline hover:text-zinc-300 font-semibold shrink-0">
        Voltar ao PC real
      </button>
    </div>
  </header>
</template>
