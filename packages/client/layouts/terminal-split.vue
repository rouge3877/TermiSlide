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
    <div class="col-left w-1/2 h-full overflow-auto p-8">
      <slot />
    </div>
    <div class="col-right w-1/2 h-full p-4 flex flex-col">
      <WebTerminal :env-name="props.env" :ws-url="props.wsUrl" class="flex-1" />
    </div>
  </div>
</template>

<style scoped>
.terminal-split {
  gap: 0;
}

.col-left {
  border-right: 1px solid rgba(125, 125, 125, 0.2);
}
</style>
