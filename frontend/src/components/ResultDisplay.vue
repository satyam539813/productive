<template>
  <div v-if="result" class="mt-6 p-4 bg-gray-100 rounded fade-in">
    <h2 class="font-semibold text-lg mb-2 text-indigo-700">Result</h2>
    <p><strong>Predicted Productivity:</strong> {{ result.prediction }}</p>
    <p><strong>Recommendation:</strong> {{ result.recommendation }}</p>
    <p class="mt-2 text-sm text-gray-700">{{ result.ai_text }}</p>
  </div>
</template>

<script setup>
defineProps({
  result: Object
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
