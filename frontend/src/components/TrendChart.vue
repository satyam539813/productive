<template>
  <div>
    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 pl-2">Productivity Trend</h3>
    <div class="h-64 w-full">
      <Line v-if="chartData && chartData.labels.length > 0" :data="chartData" :options="chartOptions" />
      <div v-else class="h-full flex items-center justify-center text-gray-400 text-sm">No data available yet</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps<{
  history: { time: string; score: number }[];
}>();

const chartData = computed(() => {
  if (!props.history || !Array.isArray(props.history)) {
    return { labels: [], datasets: [] };
  }
  return {
    labels: props.history.map(h => h.time),
    datasets: [
      {
        label: 'Productivity Score',
        data: props.history.map(h => h.score),
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        borderColor: '#8b5cf6',
        backgroundColor: (context: any) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          gradient.addColorStop(0, 'rgba(139, 92, 246, 0.5)');
          gradient.addColorStop(1, 'rgba(139, 92, 246, 0)');
          return gradient;
        },
        pointRadius: 4,
        pointBackgroundColor: '#8b5cf6'
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
      displayColors: false,
      titleFont: { family: 'Outfit', size: 13 },
      bodyFont: { family: 'Outfit', size: 13 },
      callbacks: {
        label: (context: any) => {
          const val = context.raw;
          return ["Low", "Medium", "High"][val] || "";
        }
      }
    }
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { font: { family: 'Outfit' }, color: '#9ca3af' }
    },
    y: {
      min: 0,
      max: 2,
      grid: { color: 'rgba(200,200,200,0.1)' },
      ticks: {
        font: { family: 'Outfit' },
        color: '#9ca3af',
        stepSize: 1,
        callback: (v: string | number) => {
          const val = Number(v);
          return ["Low", "Medium", "High"][val] || "";
        }
      }
    }
  }
};
</script>
