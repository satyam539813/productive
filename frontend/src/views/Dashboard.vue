<template>
  <AuroraBackground>
    <div class="relative z-10 w-full max-w-7xl p-4 md:p-8 lg:p-12 mx-auto">
      <div class="bg-white/80 dark:bg-black/40 backdrop-blur-3xl shadow-2xl rounded-[2.5rem] p-6 md:p-12 w-full border border-white/20 dark:border-white/5 fade-in">
        
        <div class="text-center mb-12 space-y-4">
          <div class="inline-flex items-center justify-center p-3 bg-indigo-500/10 rounded-2xl mb-4 ring-1 ring-indigo-500/20">
            <BrainCircuit class="w-10 h-10 text-indigo-500" />
          </div>
          <h1 class="text-5xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 via-emerald-500 to-teal-500 tracking-tight pb-2">
            AI Productivity Assistant
          </h1>
          <p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Optimize your workflow with AI-powered insights and predictive analytics.
          </p>
        </div>

        <!-- Date Range Filter -->
        <div class="flex flex-wrap justify-center gap-4 mb-12">
          <div class="flex items-center gap-2 bg-white/50 dark:bg-white/5 px-4 py-2 rounded-xl border border-gray-200 dark:border-white/10">
            <Calendar class="w-5 h-5 text-gray-500" />
            <input type="date" v-model="startDate" class="bg-transparent outline-none text-gray-700 dark:text-gray-300" />
            <span class="text-gray-400">to</span>
            <input type="date" v-model="endDate" class="bg-transparent outline-none text-gray-700 dark:text-gray-300" />
          </div>
          <div v-if="overallProductivity" class="flex items-center gap-2 bg-indigo-500/10 px-4 py-2 rounded-xl border border-indigo-500/20">
            <span class="text-indigo-600 dark:text-indigo-400 font-medium">Overall Productivity: {{ overallProductivity }}</span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
          <!-- Left Column: Form & Result -->
          <div class="lg:col-span-5 space-y-8">
            <div class="bg-white/50 dark:bg-white/5 rounded-3xl p-6 md:p-8 border border-gray-100 dark:border-white/5 shadow-sm">
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
                <Activity class="w-5 h-5 text-indigo-500" /> Input Metrics
              </h3>
              <ProductivityForm @submit="handlePrediction" :loading="loading" />
            </div>
            <ProductivityResult :result="result" />
            <RoadmapGenerator />
          </div>

          <!-- Right Column: Charts -->
          <div class="lg:col-span-7 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-white/50 dark:bg-white/5 rounded-3xl p-6 border border-gray-100 dark:border-white/5 shadow-sm hover:bg-white/60 dark:hover:bg-white/10 transition-colors duration-300">
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Trend Analysis</h3>
                <TrendChart :history="filteredHistory" />
              </div>
              <div class="bg-white/50 dark:bg-white/5 rounded-3xl p-6 border border-gray-100 dark:border-white/5 shadow-sm hover:bg-white/60 dark:hover:bg-white/10 transition-colors duration-300">
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Category Breakdown</h3>
                <BreakdownChart :history="filteredHistory" />
              </div>
            </div>
            <div class="bg-white/50 dark:bg-white/5 rounded-3xl p-6 border border-gray-100 dark:border-white/5 shadow-sm">
               <WeeklySummary />
            </div>
          </div>
        </div>
      </div>
    </div>
  </AuroraBackground>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import ProductivityForm from '../components/ProductivityForm.vue';
import ProductivityResult from '../components/ProductivityResult.vue';
import TrendChart from '../components/TrendChart.vue';
import BreakdownChart from '../components/BreakdownChart.vue';
import WeeklySummary from '../components/WeeklySummary.vue';
import RoadmapGenerator from '../components/RoadmapGenerator.vue';
import AuroraBackground from '../components/ui/AuroraBackground.vue';
import { BrainCircuit, Activity, Calendar } from 'lucide-vue-next';

const loading = ref(false);
const result = ref(null);
const history = ref<{ time: string; score: number; date?: string }[]>([]);
const startDate = ref('');
const endDate = ref('');

// Load data from localStorage
const loadStoredData = () => {
  try {
    const stored = JSON.parse(localStorage.getItem("productivityData") || "[]");
    if (Array.isArray(stored)) {
      history.value = stored;
    }
  } catch (e) {
    console.error("Failed to parse history:", e);
    localStorage.removeItem("productivityData");
  }
};

const filteredHistory = computed(() => {
  if (!startDate.value && !endDate.value) return history.value;
  
  const start = startDate.value ? new Date(startDate.value) : new Date(0);
  const end = endDate.value ? new Date(endDate.value) : new Date();
  // Set end date to end of day
  end.setHours(23, 59, 59, 999);

  return history.value.filter(item => {
    // If item has no date property (legacy data), assume it's today or keep it
    if (!item.date) return true; 
    const itemDate = new Date(item.date);
    return itemDate >= start && itemDate <= end;
  });
});

const overallProductivity = computed(() => {
  if (filteredHistory.value.length === 0) return null;
  const total = filteredHistory.value.reduce((sum, item) => sum + item.score, 0);
  const avg = total / filteredHistory.value.length;
  if (avg >= 1.5) return "High 🚀";
  if (avg >= 0.5) return "Medium ⚖️";
  return "Low ⚠️";
});

const handlePrediction = async (formData: any) => {
  loading.value = true;
  try {
    const response = await axios.post('http://localhost:8000/predict', formData);
    result.value = response.data;

    // Update localStorage
    const prediction = response.data.prediction;
    const map: Record<string, number> = { "Low": 0, "Medium": 1, "High": 2 };
    const score = map[prediction];
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const dateString = now.toISOString().split('T')[0];

    const newHistory = [...history.value, { time: timeString, score, date: dateString }];
    // Keep last 50 items for history, but charts might show fewer
    if (newHistory.length > 50) newHistory.shift();
    
    history.value = newHistory;
    localStorage.setItem("productivityData", JSON.stringify(history.value));

  } catch (error) {
    console.error("Prediction error:", error);
    alert("Error getting prediction.");
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadStoredData();
});
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.8s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
