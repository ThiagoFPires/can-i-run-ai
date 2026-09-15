<script setup>
import { Search } from 'lucide-vue-next'

defineProps({
  searchQuery: String,
  selectedCategory: String,
  selectedStatus: String,
  totalCount: Number,
  filteredCount: Number
})

const emit = defineEmits(['update:searchQuery', 'update:selectedCategory', 'update:selectedStatus'])

const categories = [
  { id: 'all', label: 'Todos os Modelos' },
  { id: 'llm', label: 'LLMs Conversacionais' },
  { id: 'reasoning', label: 'Raciocínio & Lógica' },
  { id: 'code', label: 'Programação' },
  { id: 'vision', label: 'Visão & OCR' },
  { id: 'audio', label: 'Áudio (Whisper)' },
  { id: 'image', label: 'Geração de Imagens' }
]

const statusFilters = [
  { id: 'all', label: 'Todos' },
  { id: 'compatible', label: 'Roda no PC' },
  { id: 'warning', label: 'Atenção / CPU' },
  { id: 'incompatible', label: 'Incompatível' }
]
</script>

<template>
  <div class="mb-6 space-y-3">
    <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
      <!-- Search Input -->
      <div class="relative flex-1">
        <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
        <input
          :value="searchQuery"
          @input="emit('update:searchQuery', $event.target.value)"
          type="text"
          placeholder="Buscar modelos (ex: Llama 3, DeepSeek, Whisper, Qwen, 8B)..."
          class="w-full bg-zinc-900 border border-zinc-800 focus:border-zinc-500 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition"
        />
      </div>

      <!-- Status Filter Buttons -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
        <button
          v-for="status in statusFilters"
          :key="status.id"
          @click="emit('update:selectedStatus', status.id)"
          class="px-3.5 py-2 text-xs font-semibold rounded-xl border transition whitespace-nowrap"
          :class="selectedStatus === status.id
            ? 'bg-white text-black border-white shadow-sm'
            : 'bg-zinc-900 text-zinc-400 border-zinc-800 hover:text-white hover:bg-zinc-800'"
        >
          {{ status.label }}
        </button>
      </div>
    </div>

    <!-- Category Pills -->
    <div class="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
      <button
        v-for="cat in categories"
        :key="cat.id"
        @click="emit('update:selectedCategory', cat.id)"
        class="px-3 py-1.5 rounded-lg border transition whitespace-nowrap font-medium"
        :class="selectedCategory === cat.id
          ? 'bg-zinc-800 text-white border-zinc-600'
          : 'bg-transparent text-zinc-400 border-transparent hover:bg-zinc-900 hover:text-zinc-200'"
      >
        {{ cat.label }}
      </button>

      <span class="ml-auto text-xs text-zinc-500 pl-3 shrink-0">
        Exibindo {{ filteredCount }} de {{ totalCount }} modelos
      </span>
    </div>
  </div>
</template>
