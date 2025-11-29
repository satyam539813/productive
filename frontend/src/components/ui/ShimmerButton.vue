<template>
  <button
    :class="cn(
      'group relative z-0 flex cursor-pointer items-center justify-center overflow-hidden whitespace-nowrap border border-white/10 px-6 py-3 text-white [background:var(--bg)] [border-radius:var(--radius)]',
      'transform-gpu transition-transform duration-300 ease-in-out active:translate-y-[1px]',
      props.class,
    )"
    :style="{
      '--spread': '90deg',
      '--shimmer-color': shimmerColor,
      '--radius': borderRadius,
      '--speed': shimmerDuration,
      '--cut': shimmerSize,
      '--bg': background,
    }"
  >
    <div
      :class="cn(
        '-z-30 blur-[2px]',
        'absolute inset-0 overflow-visible [container-type:size]',
      )"
    >
      <div
        class="absolute inset-0 h-[100cqh] animate-shimmer-slide [aspect-ratio:1] [border-radius:0] [mask:none]"
      >
        <div
          class="absolute -inset-full w-auto rotate-0 animate-spin-around [background:conic-gradient(from_calc(270deg-(var(--spread)*0.5)),transparent_0,var(--shimmer-color)_var(--spread),transparent_var(--spread))] [translate:0_0]"
        />
      </div>
    </div>
    
    <div class="relative z-10">
      <slot />
    </div>

    <div
      :class="cn(
        'absolute [background:var(--bg)] [border-radius:var(--radius)] [inset:var(--cut)]',
      )"
    />
  </button>
</template>

<script setup lang="ts">
import { cn } from "../../lib/utils";

interface ShimmerButtonProps {
  shimmerColor?: string;
  shimmerSize?: string;
  borderRadius?: string;
  shimmerDuration?: string;
  background?: string;
  class?: string;
}

const props = withDefaults(defineProps<ShimmerButtonProps>(), {
  shimmerColor: "#ffffff",
  shimmerSize: "0.05em",
  borderRadius: "100px",
  shimmerDuration: "3s",
  background: "rgba(0, 0, 0, 1)",
  class: "",
});
</script>

<style scoped>
@keyframes shimmer-slide {
  to {
    transform: translate(calc(100cqw - 100%), 0);
  }
}

@keyframes spin-around {
  0% {
    transform: translateZ(0) rotate(0);
  }
  15%,
  35% {
    transform: translateZ(0) rotate(90deg);
  }
  65%,
  85% {
    transform: translateZ(0) rotate(270deg);
  }
  100% {
    transform: translateZ(0) rotate(360deg);
  }
}

.animate-shimmer-slide {
  animation: shimmer-slide var(--speed) ease-in-out infinite alternate;
}

.animate-spin-around {
  animation: spin-around calc(var(--speed) * 2) infinite linear;
}
</style>