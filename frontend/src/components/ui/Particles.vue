<template>
  <div :id="id" :class="cn('relative w-full h-full overflow-hidden', $attrs.class as string)">
    <canvas ref="canvasRef" class="absolute inset-0 w-full h-full"></canvas>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from "vue";
import { cn } from "../../lib/utils";

const props = withDefaults(
  defineProps<{
    id?: string;
    color?: string;
    quantity?: number;
    staticity?: number;
    ease?: number;
    refresh?: boolean;
  }>(),
  {
    id: "particles",
    color: "#000000",
    quantity: 100,
    staticity: 50,
    ease: 50,
    refresh: false,
  },
);

const canvasRef = ref<HTMLCanvasElement | null>(null);
const canvasContainerRef = ref<HTMLDivElement | null>(null);
const context = ref<CanvasRenderingContext2D | null>(null);
const circles = ref<any[]>([]);
const mouse = ref<{ x: number; y: number }>({ x: 0, y: 0 });
const canvasSize = ref<{ w: number; h: number }>({ w: 0, h: 0 });
const dpr = typeof window !== "undefined" ? window.devicePixelRatio : 1;
const rafID = ref<number | null>(null);

const initCanvas = () => {
  resizeCanvas();
  drawParticles();
};

const resizeCanvas = () => {
  if (canvasContainerRef.value && canvasRef.value && context.value) {
    circles.value.length = 0;
    canvasSize.value.w = canvasContainerRef.value.offsetWidth;
    canvasSize.value.h = canvasContainerRef.value.offsetHeight;
    canvasRef.value.width = canvasSize.value.w * dpr;
    canvasRef.value.height = canvasSize.value.h * dpr;
    canvasRef.value.style.width = `${canvasSize.value.w}px`;
    canvasRef.value.style.height = `${canvasSize.value.h}px`;
    context.value.scale(dpr, dpr);
  }
};

const circleParams = (): any => {
  const x = Math.floor(Math.random() * canvasSize.value.w);
  const y = Math.floor(Math.random() * canvasSize.value.h);
  const translateX = 0;
  const translateY = 0;
  const pSize = Math.floor(Math.random() * 2) + 0.1;
  const alpha = 0;
  const targetAlpha = parseFloat((Math.random() * 0.6 + 0.1).toFixed(1));
  const dx = (Math.random() - 0.5) * 0.1;
  const dy = (Math.random() - 0.5) * 0.1;
  const magnetism = 0.1 + Math.random() * 4;
  return {
    x,
    y,
    translateX,
    translateY,
    size: pSize,
    alpha,
    targetAlpha,
    dx,
    dy,
    magnetism,
  };
};

const drawCircle = (circle: any, update = false) => {
  if (context.value) {
    const { x, y, translateX, translateY, size, alpha } = circle;
    context.value.translate(translateX, translateY);
    context.value.beginPath();
    context.value.arc(x, y, size, 0, 2 * Math.PI);
    context.value.fillStyle = `rgba(${hexToRgb(props.color).join(", ")}, ${alpha})`;
    context.value.fill();
    context.value.setTransform(dpr, 0, 0, dpr, 0, 0);

    if (!update) {
      circles.value.push(circle);
    }
  }
};

const clearContext = () => {
  if (context.value) {
    context.value.clearRect(0, 0, canvasSize.value.w, canvasSize.value.h);
  }
};

const drawParticles = () => {
  clearContext();
  const particleCount = props.quantity;
  for (let i = 0; i < particleCount; i++) {
    const circle = circleParams();
    drawCircle(circle);
  }
};

const remapValue = (
  value: number,
  start1: number,
  end1: number,
  start2: number,
  end2: number,
) => {
  const remapped =
    ((value - start1) * (end2 - start2)) / (end1 - start1) + start2;
  return remapped > 0 ? remapped : 0;
};

const animate = () => {
  clearContext();
  circles.value.forEach((circle: any, i: number) => {
    // Handle the alpha value
    const edge = [
      circle.x + circle.translateX - circle.size, // distance from left edge
      canvasSize.value.w - circle.x - circle.translateX - circle.size, // distance from right edge
      circle.y + circle.translateY - circle.size, // distance from top edge
      canvasSize.value.h - circle.y - circle.translateY - circle.size, // distance from bottom edge
    ];
    const closestEdge = edge.reduce((a, b) => Math.min(a, b));
    const remapClosestEdge = parseFloat(
      remapValue(closestEdge, 0, 20, 0, 1).toFixed(2),
    );
    if (remapClosestEdge > 1) {
      circle.alpha += 0.02;
      if (circle.alpha > circle.targetAlpha) {
        circle.alpha = circle.targetAlpha;
      }
    } else {
      circle.alpha = circle.targetAlpha * remapClosestEdge;
    }
    circle.x += circle.dx;
    circle.y += circle.dy;
    circle.translateX +=
      (mouse.value.x / (props.staticity / circle.magnetism) -
        circle.translateX) /
      props.ease;
    circle.translateY +=
      (mouse.value.y / (props.staticity / circle.magnetism) -
        circle.translateY) /
      props.ease;

    drawCircle(circle, true);

    // circle gets out of the canvas
    if (
      circle.x < -circle.size ||
      circle.x > canvasSize.value.w + circle.size ||
      circle.y < -circle.size ||
      circle.y > canvasSize.value.h + circle.size
    ) {
      // remove the circle from the array
      circles.value.splice(i, 1);
      // create a new circle
      const newCircle = circleParams();
      drawCircle(newCircle);
    }
  });
  rafID.value = window.requestAnimationFrame(animate);
};

const onMouseMove = (e: MouseEvent) => {
  const rect = canvasRef.value?.getBoundingClientRect();
  if (rect) {
    const x = e.clientX - rect.left - canvasSize.value.w / 2;
    const y = e.clientY - rect.top - canvasSize.value.h / 2;
    mouse.value.x = x;
    mouse.value.y = y;
  }
};

const hexToRgb = (hex: string) => {
  hex = hex.replace("#", "");
  const hexInt = parseInt(hex, 16);
  const r = (hexInt >> 16) & 255;
  const g = (hexInt >> 8) & 255;
  const b = hexInt & 255;
  return [r, g, b];
};

onMounted(() => {
  if (canvasRef.value) {
    context.value = canvasRef.value.getContext("2d");
  }
  initCanvas();
  animate();
  window.addEventListener("resize", initCanvas);
  window.addEventListener("mousemove", onMouseMove);
});

onUnmounted(() => {
  if (rafID.value) {
    window.cancelAnimationFrame(rafID.value);
  }
  window.removeEventListener("resize", initCanvas);
  window.removeEventListener("mousemove", onMouseMove);
});

watch(
  () => props.refresh,
  () => {
    initCanvas();
  },
);
</script>
