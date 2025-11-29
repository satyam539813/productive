<template>
  <div v-if="result" class="mt-8 fade-in">
    <MagicCard class="w-full shadow-2xl border border-white/10 overflow-hidden" gradientColor="#6366f133">
      <div class="p-6 md:p-8 space-y-6">
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-indigo-500/10 rounded-lg">
            <Bot class="w-6 h-6 text-indigo-500" />
          </div>
          <h2 class="font-bold text-2xl text-gray-900 dark:text-white">AI Analysis</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-white/50 dark:bg-white/5 rounded-xl p-4 border border-gray-100 dark:border-white/5">
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Prediction</p>
            <p class="text-xl font-semibold text-indigo-600 dark:text-indigo-400">{{ result.prediction }} Productivity</p>
          </div>
          <div class="bg-white/50 dark:bg-white/5 rounded-xl p-4 border border-gray-100 dark:border-white/5">
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Recommendation</p>
            <p class="text-lg font-medium text-gray-800 dark:text-gray-200">{{ result.recommendation }}</p>
          </div>
        </div>

        <div class="bg-indigo-50/50 dark:bg-indigo-900/20 rounded-xl p-5 border border-indigo-100 dark:border-indigo-500/20">
          <div class="flex gap-2 mb-2">
            <Sparkles class="w-4 h-4 text-indigo-500 mt-0.5" />
            <p class="text-sm font-medium text-indigo-600 dark:text-indigo-300">AI Insights</p>
          </div>
          <p class="text-gray-700 dark:text-gray-300 leading-relaxed">{{ result.ai_text }}</p>
        </div>
      </div>
    </MagicCard>
  </div>
</template>

<script setup lang="ts">
import MagicCard from './ui/MagicCard.vue';
import { Bot, Sparkles } from 'lucide-vue-next';

defineProps<{
  result: {
    prediction: string;
    recommendation: string;
    ai_text: string;
  } | null;
}>();
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); filter: blur(10px); }
  to { opacity: 1; transform: translateY(0); filter: blur(0); }
}
</style>
