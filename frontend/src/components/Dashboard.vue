<template>
  <div class="bg-gray-50 min-h-screen flex flex-col items-center justify-center py-10">
    <div class="bg-white shadow-xl rounded-xl p-8 w-full max-w-md fade-in">
      <h1 class="text-2xl font-bold text-center text-indigo-600 mb-6">
        🧠 AI Productivity Assistant
      </h1>

      <ProductivityForm @submit="handlePredict" :loading="loading" />

      <ResultDisplay :result="result" />

      <TrendChart :history="history" />
      
      <WeeklySummary />

      <BreakdownChart :history="history" />
    </div>

    <footer class="mt-6 text-gray-400 text-sm text-center">
      ⚡ Powered by <a href="https://openrouter.ai/" target="_blank" class="text-indigo-500 hover:text-indigo-700">OpenRouter AI</a>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ProductivityForm from './ProductivityForm.vue';
import ResultDisplay from './ResultDisplay.vue';
import TrendChart from './TrendChart.vue';
import WeeklySummary from './WeeklySummary.vue';
import BreakdownChart from './BreakdownChart.vue';

const loading = ref(false);
const result = ref(null);
const history = ref([]);

const loadHistory = () => {
  const stored = localStorage.getItem('productivityData');
  if (stored) {
    try {
      const parsed = JSON.parse(stored);
      if (Array.isArray(parsed)) {
        history.value = parsed;
      }
    } catch (e) {
      console.error("Failed to parse history:", e);
      localStorage.removeItem('productivityData');
    }
  }
};

onMounted(() => {
  loadHistory();
});

const handlePredict = async (formData) => {
  loading.value = true;
  result.value = null;
  try {
    const response = await axios.post('http://127.0.0.1:8000/predict', formData);
    result.value = response.data;

    // Update history
    const prediction = result.value.prediction;
    const map = { "Low": 0, "Medium": 1, "High": 2 };
    const score = map[prediction];
    const now = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    history.value.push({ time: now, score });
    if (history.value.length > 10) history.value.shift();
    localStorage.setItem("productivityData", JSON.stringify(history.value));

  } catch (error) {
    console.error("Prediction error:", error);
    alert("Failed to get prediction. Ensure backend is running.");
  } finally {
    loading.value = false;
  }
};
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
