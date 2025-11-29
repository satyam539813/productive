<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <div v-for="(field, key) in formFields" :key="key" 
           class="relative group"
           :class="{ 'md:col-span-2': key === 'focus_level' }">
        <label class="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1.5 ml-1">{{ field.label }}</label>
        <div class="relative transition-all duration-300 transform group-hover:-translate-y-0.5">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400 group-focus-within:text-indigo-500 transition-colors duration-200">
            <component :is="field.icon" class="w-5 h-5" />
          </div>
          <input
            v-model.number="form[key]"
            :type="field.type"
            :step="field.step"
            :placeholder="field.placeholder"
            required
            class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 dark:border-white/10 bg-white/50 dark:bg-black/20 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200 outline-none backdrop-blur-sm shadow-sm hover:shadow-md"
          />
        </div>
      </div>
    </div>

    <ShimmerButton type="submit" :disabled="loading" class="w-full font-medium text-lg py-4 shadow-lg shadow-indigo-500/20">
      <span v-if="loading" class="flex items-center gap-2">
        <Loader2 class="w-5 h-5 animate-spin" /> Processing...
      </span>
      <span v-else class="flex items-center gap-2">
        <Sparkles class="w-5 h-5" /> Predict Productivity
      </span>
    </ShimmerButton>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import ShimmerButton from './ui/ShimmerButton.vue';
import { Clock, Moon, CheckCircle2, Coffee, Zap, Sparkles, Loader2 } from 'lucide-vue-next';

defineProps<{
  loading: boolean;
}>();

const emit = defineEmits<{
  (e: 'submit', data: any): void;
}>();

const form = reactive<any>({
  hours_worked: '',
  sleep_hours: '',
  tasks_completed: '',
  breaks_taken: '',
  focus_level: ''
});

const formFields = {
  hours_worked: { label: 'Hours Worked', type: 'number', step: '0.1', placeholder: 'e.g. 8.5', icon: Clock },
  sleep_hours: { label: 'Sleep Hours', type: 'number', step: '0.1', placeholder: 'e.g. 7.0', icon: Moon },
  tasks_completed: { label: 'Tasks Completed', type: 'number', step: '1', placeholder: 'e.g. 10', icon: CheckCircle2 },
  breaks_taken: { label: 'Breaks Taken', type: 'number', step: '1', placeholder: 'e.g. 2', icon: Coffee },
  focus_level: { label: 'Focus Level (0-10)', type: 'number', step: '0.1', placeholder: 'e.g. 8', icon: Zap }
};

const submitForm = () => {
  emit('submit', { ...form });
};
</script>
