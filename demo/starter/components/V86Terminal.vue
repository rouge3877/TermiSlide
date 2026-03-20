<script setup lang="ts">
import type { Ref } from 'vue'
import { computed, inject, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import {
  getOrCreateTerminal,
  initV86,
  mountTerminalTo,
  switchEnv,
  useV86,
} from '../setup/v86'

const props = defineProps<{
  env?: string
}>()

const terminalRef = ref<HTMLElement | null>(null)
let resizeObserver: ResizeObserver | null = null

const slidevPage = inject<Ref<number>>('$$slidev-page')

const route = useRoute()
const currentSlideNo = computed(() => {
  const path = route.path
  if (path === '/' || path === '') return 1
  const num = Number.parseInt(path.replace('/', ''), 10)
  return Number.isNaN(num) ? 1 : num
})

const isActive = computed(() => {
  return slidevPage?.value === currentSlideNo.value
})

const { booted, ready, switching } = useV86()

const showLoading = computed(() => {
  return !booted.value || !ready.value || switching.value
})

const loadingText = computed(() => {
  if (!booted.value) return 'Booting Linux kernel…'
  if (!ready.value) return 'Setting up environment…'
  return 'Switching environment…'
})

onMounted(async () => {
  await initV86()

  const { fitAddon } = getOrCreateTerminal()

  resizeObserver = new ResizeObserver(() => {
    if (isActive.value) fitAddon.fit()
  })
  if (terminalRef.value) {
    resizeObserver.observe(terminalRef.value)
  }

  watch(isActive, (active) => {
    if (active && terminalRef.value) {
      const termEl = terminalRef.value.querySelector('.v86-term-inner') as HTMLElement
      if (termEl) mountTerminalTo(termEl)

      if (props.env) {
        // switchEnv is debounced internally — safe to call rapidly
        switchEnv(props.env)
      }
    }
  }, { immediate: true })
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  resizeObserver = null
})
</script>

<template>
  <div ref="terminalRef" class="v86-terminal">
    <Transition name="fade">
      <div v-if="showLoading" class="v86-loading">
        <div class="v86-loading-content">
          <div class="v86-spinner" />
          <span>{{ loadingText }}</span>
        </div>
      </div>
    </Transition>
    <div class="v86-term-inner" />
  </div>
</template>

<style scoped>
.v86-terminal {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
}

.v86-term-inner {
  width: 100%;
  height: 100%;
}

.v86-term-inner :deep(.xterm) {
  height: 100%;
  padding: 8px;
}

.v86-term-inner :deep(.xterm-viewport) {
  overflow-y: auto !important;
}

/* Loading overlay */
.v86-loading {
  position: absolute;
  inset: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1e1e2e;
}

.v86-loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: #6c7086;
  font-family: 'Menlo', 'Monaco', monospace;
  font-size: 14px;
}

.v86-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #313244;
  border-top-color: #89b4fa;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
