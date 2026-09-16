<script setup>
import { ref } from 'vue'
import { Terminal, Check, Flame } from 'lucide-vue-next'

defineProps({
  picks: {
    type: Array,
    default: () => []
  }
})

const copiedId = ref(null)

const copyCommand = (cmd, id) => {
  if (!cmd) return
  navigator.clipboard.writeText(cmd)
  copiedId.value = id
  setTimeout(() => {
    copiedId.value = null
  }, 2000)
}
</script>

<template>
  <div v-if="picks.length > 0" class="mb-10">
    <div class="flex items-center gap-2 mb-4">
      <Flame class="w-4 h-4 text-amber-400" />
      <h2 class="text-base font-bold text-white tracking-wide uppercase">
        Recomendações Ideais para o seu PC
      </h2>
      <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 font-medium">
        Roda com Fluidez
      </span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="pick in picks"
        :key="pick.model_id"
        class="neutral-card neutral-card-hover p-4 rounded-2xl flex flex-col justify-between group"
      >
        <div>
          <div class="flex items-start justify-between gap-2 mb-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-zinc-400 bg-zinc-900 border border-zinc-800 px-2 py-0.5 rounded">
              {{ pick.model.creator }}
            </span>
            <span class="text-xs font-mono font-semibold text-zinc-300">
              {{ pick.model.parameters }}
            </span>
          </div>

          <h3 class="text-base font-bold text-white group-hover:text-zinc-200 transition">
            {{ pick.model.name }}
          </h3>

          <p class="mt-1.5 text-xs text-zinc-400 line-clamp-2 leading-relaxed">
            {{ pick.model.description }}
          </p>

          <div class="mt-3 py-1.5 px-2.5 rounded-lg bg-zinc-900/90 border border-zinc-800 flex items-center justify-between text-xs">
            <span class="text-zinc-500">Velocidade:</span>
            <span class="font-semibold text-emerald-400 font-mono">{{ pick.estimated_speed ? pick.estimated_speed.split('(')[0] : 'Rápido' }}</span>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-zinc-800/80">
          <div v-if="pick.model.ollama_model" class="flex items-center gap-1.5">
            <div class="flex-1 bg-zinc-950 border border-zinc-800 rounded-lg px-2.5 py-1.5 text-[11px] font-mono text-zinc-300 truncate">
              ollama run {{ pick.model.ollama_model }}
            </div>
            <button
              @click="copyCommand(`ollama run ${pick.model.ollama_model}`, pick.model_id)"
              class="p-2 rounded-lg bg-white hover:bg-zinc-200 text-black transition active:scale-95 shrink-0 shadow-sm"
              :title="copiedId === pick.model_id ? 'Copiado!' : 'Copiar comando Ollama'"
            >
              <Check v-if="copiedId === pick.model_id" class="w-3.5 h-3.5 text-emerald-600" />
              <Terminal v-else class="w-3.5 h-3.5" />
            </button>
          </div>
          <div v-else class="text-[11px] text-zinc-500 font-medium">
            Execução: <span class="text-zinc-300">{{ pick.model.recommended_runner }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
