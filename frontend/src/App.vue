<script setup>
import { ref, computed, onMounted } from 'vue'
import HardwareHeader from './components/HardwareHeader.vue'
import HardwareGauges from './components/HardwareGauges.vue'
import TopPicks from './components/TopPicks.vue'
import FilterBar from './components/FilterBar.vue'
import ModelCard from './components/ModelCard.vue'
import UpgradeSimulator from './components/UpgradeSimulator.vue'
import { AlertCircle, RefreshCw, Layers } from 'lucide-vue-next'

const hardware = ref(null)
const results = ref([])
const topPicks = ref([])
const totalModels = ref(0)
const compatibleCount = ref(0)
const loading = ref(true)
const error = ref(null)

const isSimulatorOpen = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedStatus = ref('all')

const API_BASE = 'http://127.0.0.1:8000'

const fetchEvaluation = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`${API_BASE}/api/evaluate`)
    if (!res.ok) throw new Error('Falha ao conectar ao servidor de diagnóstico.')
    const data = await res.json()
    hardware.value = data.hardware
    results.value = data.results
    topPicks.value = data.top_picks
    totalModels.value = data.total_models
    compatibleCount.value = data.compatible_count
  } catch (err) {
    console.error(err)
    error.value = 'Não foi possível se comunicar com o backend Python em ' + API_BASE + '. Verifique se o servidor está rodando.'
  } finally {
    loading.value = false
  }
}

const handleSimulate = async (simParams) => {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`${API_BASE}/api/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(simParams)
    })
    if (!res.ok) throw new Error('Erro ao processar simulação.')
    const data = await res.json()
    hardware.value = data.hardware
    results.value = data.results
    topPicks.value = data.top_picks
    totalModels.value = data.total_models
    compatibleCount.value = data.compatible_count
  } catch (err) {
    console.error(err)
    error.value = 'Falha ao executar a simulação de hardware.'
  } finally {
    loading.value = false
  }
}

const filteredResults = computed(() => {
  return results.value.filter(item => {
    // Busca textual
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase()
      const matchName = item.model.name.toLowerCase().includes(q)
      const matchCreator = item.model.creator.toLowerCase().includes(q)
      const matchParam = item.model.parameters.toLowerCase().includes(q)
      const matchTags = item.model.tags.some(t => t.toLowerCase().includes(q))
      if (!matchName && !matchCreator && !matchParam && !matchTags) return false
    }

    // Filtro de categoria
    if (selectedCategory.value !== 'all') {
      if (item.model.category !== selectedCategory.value) return false
    }

    // Filtro de status
    if (selectedStatus.value === 'compatible') {
      if (item.status !== 'gpu_perfect' && item.status !== 'cpu_viable') return false
    } else if (selectedStatus.value === 'warning') {
      if (item.status !== 'warning_marginal') return false
    } else if (selectedStatus.value === 'incompatible') {
      if (item.status !== 'incompatible') return false
    }

    return true
  })
})

onMounted(() => {
  fetchEvaluation()
})
</script>

<template>
  <div class="min-h-screen pb-16 bg-[#09090b] text-zinc-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
      <!-- Hardware Header -->
      <HardwareHeader
        :hardware="hardware || {}"
        :loading="loading"
        @open-simulator="isSimulatorOpen = true"
        @reset-hardware="fetchEvaluation"
        @refresh="fetchEvaluation"
      />

      <!-- Error State -->
      <div
        v-if="error"
        class="mb-8 p-4 rounded-2xl bg-zinc-900 border border-zinc-700 text-zinc-300 flex items-center justify-between gap-4"
      >
        <div class="flex items-center gap-3 text-sm">
          <AlertCircle class="w-5 h-5 text-zinc-400 shrink-0" />
          <span>{{ error }}</span>
        </div>
        <button
          @click="fetchEvaluation"
          class="px-3.5 py-1.5 rounded-lg bg-white text-black text-xs font-semibold shrink-0 hover:bg-zinc-200 transition"
        >
          Tentar Novamente
        </button>
      </div>

      <!-- Hardware Gauges & Metrics -->
      <HardwareGauges v-if="hardware" :hardware="hardware" />

      <!-- Top Picks (Highlighted recommendations) -->
      <TopPicks v-if="!loading && topPicks.length > 0" :picks="topPicks" />

      <!-- Filters & Search -->
      <FilterBar
        v-model:searchQuery="searchQuery"
        v-model:selectedCategory="selectedCategory"
        v-model:selectedStatus="selectedStatus"
        :totalCount="results.length"
        :filteredCount="filteredResults.length"
      />

      <!-- Loading State -->
      <div v-if="loading" class="py-20 flex flex-col items-center justify-center text-zinc-400">
        <RefreshCw class="w-6 h-6 animate-spin text-zinc-300 mb-3" />
        <p class="text-xs font-medium">Diagnosticando especificações do hardware...</p>
      </div>

      <!-- Grid of Models -->
      <div v-else-if="filteredResults.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <ModelCard
          v-for="res in filteredResults"
          :key="res.model_id"
          :result="res"
          :systemHardware="hardware"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="py-16 text-center neutral-card rounded-2xl p-8 border border-zinc-800">
        <Layers class="w-10 h-10 text-zinc-600 mx-auto mb-3" />
        <h3 class="text-base font-bold text-white mb-1">Nenhum modelo encontrado</h3>
        <p class="text-xs text-zinc-400 max-w-sm mx-auto mb-4">
          Nenhum modelo corresponde aos filtros ou busca selecionada. Tente limpar os filtros.
        </p>
        <button
          @click="searchQuery = ''; selectedCategory = 'all'; selectedStatus = 'all'"
          class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold rounded-xl transition"
        >
          Limpar Filtros
        </button>
      </div>
    </div>

    <!-- Upgrade Simulator Modal -->
    <UpgradeSimulator
      :isOpen="isSimulatorOpen"
      :currentHardware="hardware"
      @close="isSimulatorOpen = false"
      @simulate="handleSimulate"
      @reset="fetchEvaluation"
    />
  </div>
</template>
