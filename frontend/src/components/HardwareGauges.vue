<script setup>
import { computed } from 'vue'
import { Cpu, HardDrive, MemoryStick, Monitor, Zap, ZapOff, CheckCircle2 } from 'lucide-vue-next'

const props = defineProps({
  hardware: {
    type: Object,
    required: true
  }
})

const ramPercent = computed(() => {
  if (!props.hardware?.ram_total_gb) return 0
  const used = props.hardware.ram_used_gb || (props.hardware.ram_total_gb - props.hardware.ram_available_gb)
  return Math.min(100, Math.round((used / props.hardware.ram_total_gb) * 100))
})

const hasCuda = computed(() => {
  return props.hardware?.primary_gpu?.cuda_supported === true
})
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    <!-- CPU Card -->
    <div class="neutral-card p-4 rounded-2xl">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-zinc-400">Processador</span>
        <div class="p-2 rounded-lg bg-zinc-800/80 text-zinc-300">
          <Cpu class="w-4 h-4" />
        </div>
      </div>
      <div class="text-base font-bold text-white truncate" :title="hardware?.cpu_name">
        {{ hardware?.cpu_name || 'Detectando...' }}
      </div>
      <div class="mt-2 flex items-center gap-2 text-xs text-zinc-400">
        <span class="px-2 py-0.5 rounded-md bg-zinc-900 border border-zinc-800 font-mono text-zinc-300">
          {{ hardware?.cpu_cores_physical || '-' }} Núcleos
        </span>
        <span class="px-2 py-0.5 rounded-md bg-zinc-900 border border-zinc-800 font-mono text-zinc-300">
          {{ hardware?.cpu_cores_logical || '-' }} Threads
        </span>
      </div>
    </div>

    <!-- RAM Card (Com barra colorida estilo Dashboard: Verde/Amarelo/Vermelho) -->
    <div class="neutral-card p-4 rounded-2xl">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-zinc-400">Memória RAM</span>
        <div class="p-2 rounded-lg bg-zinc-800/80 text-zinc-300">
          <MemoryStick class="w-4 h-4" />
        </div>
      </div>
      <div class="flex items-baseline gap-1.5">
        <span class="text-2xl font-bold text-white">{{ hardware?.ram_total_gb || 0 }}</span>
        <span class="text-sm font-medium text-zinc-400">GB Total</span>
        <span class="text-xs text-emerald-400 ml-auto font-mono font-medium">
          {{ hardware?.ram_available_gb || 0 }} GB Livre
        </span>
      </div>
      <!-- Progress Bar colorida conforme nível de uso -->
      <div class="mt-3 w-full bg-zinc-800 rounded-full h-1.5 overflow-hidden">
        <div
          class="h-full rounded-full transition-all duration-500"
          :class="ramPercent > 85 ? 'bg-rose-500' : ramPercent > 70 ? 'bg-amber-500' : 'bg-emerald-500'"
          :style="{ width: `${ramPercent}%` }"
        ></div>
      </div>
      <div class="mt-1.5 flex justify-between text-[11px] text-zinc-400">
        <span>Uso: {{ ramPercent }}%</span>
        <span>{{ hardware?.ram_used_gb || 0 }} GB Usado</span>
      </div>
    </div>

    <!-- GPU & VRAM Card -->
    <div class="neutral-card p-4 rounded-2xl">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-zinc-400">Placa de Vídeo</span>
        <div class="p-2 rounded-lg bg-zinc-800/80 text-zinc-300">
          <Monitor class="w-4 h-4" />
        </div>
      </div>
      <div class="text-base font-bold text-white truncate" :title="hardware?.primary_gpu?.name">
        {{ hardware?.primary_gpu?.name || 'Sem GPU Dedicada' }}
      </div>
      <div class="mt-2 flex items-center justify-between gap-2">
        <div class="flex items-center gap-1.5">
          <span class="text-lg font-bold text-white">{{ hardware?.primary_gpu?.vram_total_gb || 0 }}</span>
          <span class="text-xs font-medium text-zinc-400">GB VRAM</span>
        </div>
        <div>
          <!-- Status Verde para CUDA e Amarelo para CPU -->
          <span
            v-if="hasCuda"
            class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/25"
          >
            <Zap class="w-3 h-3 text-emerald-400" /> CUDA Ativo
          </span>
          <span
            v-else
            class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-amber-500/10 text-amber-300 border border-amber-500/25"
            title="Inferência será realizada via CPU"
          >
            <ZapOff class="w-3 h-3 text-amber-400" /> Modo CPU
          </span>
        </div>
      </div>
    </div>

    <!-- Storage Card -->
    <div class="neutral-card p-4 rounded-2xl">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-zinc-400">Disco Livre</span>
        <div class="p-2 rounded-lg bg-zinc-800/80 text-zinc-300">
          <HardDrive class="w-4 h-4" />
        </div>
      </div>
      <div class="flex items-baseline gap-1.5">
        <span class="text-2xl font-bold text-white">{{ hardware?.disk_free_gb || 0 }}</span>
        <span class="text-sm font-medium text-zinc-400">GB Livres</span>
      </div>
      <div class="mt-2 text-xs text-zinc-400 flex items-center gap-1.5">
        <CheckCircle2 class="w-3.5 h-3.5 text-emerald-400" />
        <span>Espaço para pesos GGUF</span>
      </div>
    </div>
  </div>
</template>
