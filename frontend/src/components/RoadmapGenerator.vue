<template>
  <div class="bg-white/50 dark:bg-white/5 rounded-3xl p-6 border border-gray-100 dark:border-white/5 shadow-sm">
    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center gap-2">
      <Map class="w-5 h-5 text-indigo-500" /> Learning Roadmap
    </h3>
    
    <div class="flex gap-3 mb-6">
      <input 
        v-model="topic" 
        @keyup.enter="generateRoadmap"
        placeholder="What do you want to learn? (e.g. Full Stack)" 
        class="flex-1 px-4 py-2 rounded-xl border border-gray-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500/50 outline-none transition-all"
      />
      <ShimmerButton @click="generateRoadmap" :disabled="loading || !topic" class="px-6">
        <span v-if="loading">Generating...</span>
        <span v-else>Generate</span>
      </ShimmerButton>
    </div>

    <div v-if="roadmapItems.length > 0" class="space-y-3">
      <div v-for="(step, index) in roadmapItems" :key="index" 
           class="animate-fade-in flex gap-3 items-start p-3 bg-white/60 dark:bg-white/5 rounded-xl border border-gray-100 dark:border-white/5"
           :style="{ animationDelay: `${index * 150}ms` }">
        <div class="flex items-center justify-center w-6 h-6 rounded-full bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 text-xs font-bold shrink-0 mt-0.5">
          {{ index + 1 }}
        </div>
        <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">{{ step }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import ShimmerButton from './ui/ShimmerButton.vue';
import { Map } from 'lucide-vue-next';

const topic = ref('');
const loading = ref(false);
const roadmapItems = ref<string[]>([]);

const generateRoadmap = async () => {
  if (!topic.value) return;
  
  loading.value = true;
  roadmapItems.value = []; // Clear previous
  
  try {
    const response = await axios.post('http://localhost:8000/generate_roadmap', { topic: topic.value });
    const rawRoadmap = response.data.roadmap;
    
    // Parse numbered list
    roadmapItems.value = rawRoadmap
      .split('\n')
      .filter((line: string) => line.trim().length > 0)
      .map((line: string) => line.replace(/^\d+\.\s*/, '').trim());
      
  } catch (error) {
    console.error("Error generating roadmap:", error);
    roadmapItems.value = ["Failed to generate roadmap. Please try again."];
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
  opacity: 0;
  transform: translateY(10px);
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
