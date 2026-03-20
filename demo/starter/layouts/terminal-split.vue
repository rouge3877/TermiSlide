<!--
  Usage:

```md
---
layout: terminal-split
env: lab1
---

# Lab 1: Introduction

Instructions on the left, terminal on the right.
```

  Props:
  - env: Name of the virtual environment (defined in environments/ folder).
         The environment config specifies the working directory and init commands.

  See environments/ folder for how to define environments.
-->

<script setup lang="ts">
import V86Terminal from '../components/V86Terminal.vue'

const props = defineProps<{
  env?: string
}>()
</script>

<template>
  <div class="slidev-layout terminal-split grid grid-cols-2 h-full w-full">
    <div class="col-left overflow-auto p-8">
      <slot />
    </div>
    <div class="col-right h-full overflow-hidden border-l border-gray-700">
      <V86Terminal :env="props.env" />
    </div>
  </div>
</template>

<style scoped>
.terminal-split {
  background: #1a1a2e;
  color: #e0e0e0;
}

.col-left {
  background: #0f0f23;
}

.col-right {
  background: #1e1e2e;
}
</style>
