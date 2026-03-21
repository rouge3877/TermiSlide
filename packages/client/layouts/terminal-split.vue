<!--
  Terminal Split Layout - Left: slide content, Right: interactive terminal

  Usage:

  ```md
  ---
  layout: terminal-split
  env: my-env
  ---

  # Slide Title

  Instructions on the left, terminal on the right.
  ```
-->

<script setup lang="ts">
import WebTerminal from '../builtin/WebTerminal.vue'

const props = withDefaults(defineProps<{
  env?: string
  wsUrl?: string
}>(), {
  env: 'default',
})
</script>

<template>
  <div class="slidev-layout terminal-split flex w-full h-full">
    <div class="col-left h-full overflow-auto p-6">
      <slot />
    </div>
    <div class="col-right h-full p-2 flex flex-col">
      <WebTerminal :env-name="props.env" :ws-url="props.wsUrl" class="flex-1" />
    </div>
  </div>
</template>

<style scoped>
.terminal-split {
  gap: 0;
}

.col-left {
  width: 42%;
  flex-shrink: 0;
  border-right: 1px solid rgba(125, 125, 125, 0.2);
  font-size: 0.85em;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}

.col-left::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

.col-right {
  width: 58%;
  flex-shrink: 0;
}
</style>
