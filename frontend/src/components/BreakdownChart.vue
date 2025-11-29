<template>
  <div>
    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 pl-2">Productivity Breakdown</h3>
    <div class="h-64 w-full">
      <Bar v-if="chartData && chartData.labels.length > 0" :data="chartData" :options="chartOptions" />
      <div v-else class="h-full flex items-center justify-center text-gray-400 text-sm">No data available yet</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps<{
  history: { time: string; score: number }[];
}>();

const chartData = computed(() => {
  const counts = [0, 0, 0]; // Low, Medium, High
  if (!props.history || !Array.isArray(props.history)) {
    return { labels: ['Low', 'Medium', 'High'], datasets: [] };
  }
  props.history.forEach(h => {
    if (h.score >= 0 && h.score <= 2) {
      counts[h.score]++;
    }
  });

  return {
    labels: ['Low', 'Medium', 'High'],
    datasets: [
      {
        label: 'Count',
        data: counts,
        backgroundColor: ['#ef4444', '#facc15', '#22c55e'],
        borderRadius: 8,
        borderSkipped: false
      }
    ]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(0,0,0,0.8)',
      padding: 12,
      cornerRadius: 8,
      titleFont: { family: 'Outfit', size: 13 },
      bodyFont: { family: 'Outfit', size: 13 }
    }
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { font: { family: 'Outfit' }, color: '#9ca3af' }
    },
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(200,200,200,0.1)' },
      ticks: { font: { family: 'Outfit' }, color: '#9ca3af', stepSize: 1 }
    }
  }
};
</script>
