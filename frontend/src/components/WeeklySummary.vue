<template>
  <div class="mt-8 p-6 bg-white/50 dark:bg-black/30 rounded-2xl shadow-sm">
    <h3 class="text-lg font-semibold text-indigo-600 dark:text-indigo-400 text-center mb-4">🧾 Weekly AI Summary</h3>
    
    <ShimmerButton @click="generateSummary" :disabled="loading" class="w-full">
      <span v-if="loading">🔄 Generating summary...</span>
      <span v-else>Generate Weekly Summary</span>
    </ShimmerButton>

    <div v-if="summaryItems.length > 0" class="mt-6 space-y-3">
      <div v-for="(item, index) in summaryItems" :key="index" class="w-full animate-fade-in" :style="{ animationDelay: `${index * 100}ms` }">
        <div class="bg-white/80 dark:bg-white/10 backdrop-blur-sm p-4 rounded-xl border border-gray-100 dark:border-white/5 shadow-sm flex gap-3 items-start hover:bg-white/90 dark:hover:bg-white/15 transition-colors">
          <div class="p-2 bg-indigo-500/10 rounded-lg shrink-0">
            <Sparkles class="w-4 h-4 text-indigo-500" />
          </div>
          <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">{{ item }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import axios from 'axios';
import ShimmerButton from './ui/ShimmerButton.vue';
import { Sparkles } from 'lucide-vue-next';

const summary = ref('');
const loading = ref(false);

const summaryItems = computed(() => {
  if (!summary.value) return [];
  // Split by sentences but filter out empty strings
  const items = summary.value.split('. ').filter(s => s.trim().length > 0).map(s => s.endsWith('.') ? s : s + '.');
  return items.slice(0, 5);
});

const generateSummary = async () => {
  loading.value = true;
  try {
    const response = await axios.get('http://localhost:8000/weekly_summary');
    summary.value = response.data.summary;
  } catch (error) {
    console.error('Error fetching summary:', error);
    summary.value = "Error generating summary. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>
