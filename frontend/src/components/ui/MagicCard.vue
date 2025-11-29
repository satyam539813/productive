<template>
  <div
    :class="cn(
      'group relative flex h-full w-full flex-col overflow-hidden rounded-xl border bg-card text-card-foreground shadow',
      props.class,
    )"
  >
    <div class="relative z-10 flex flex-col h-full p-6">
      <slot />
    </div>
    <div
      class="pointer-events-none absolute -inset-px opacity-0 transition duration-300 group-hover:opacity-100"
      :style="{
        background: `radial-gradient(${gradientSize}px circle at ${mouseX}px ${mouseY}px, ${gradientColor}, transparent 100%)`,
      }"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { cn } from "../../lib/utils";

interface MagicCardProps {
  class?: string;
  gradientSize?: number;
  gradientColor?: string;
}

const props = withDefaults(defineProps<MagicCardProps>(), {
  class: "",
  gradientSize: 200,
  gradientColor: "#262626",
});

const mouseX = ref(0);
const mouseY = ref(0);

const handleMouseMove = (e: MouseEvent) => {
  const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
  mouseX.value = e.clientX - rect.left;
  mouseY.value = e.clientY - rect.top;
};

onMounted(() => {
  document.addEventListener("mousemove", handleMouseMove);
});

onUnmounted(() => {
  document.removeEventListener("mousemove", handleMouseMove);
});
</script>
