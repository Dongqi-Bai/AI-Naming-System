<script setup>
defineProps({
  light: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <div class="brand" :class="{ 'brand--light': light }">
    <span class="brand__seal" aria-hidden="true">字</span>
    <span class="brand__text">
      <strong>字里</strong>
      <small>AI NAMING</small>
    </span>
  </div>
</template>

<style scoped>
.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  color: var(--ink);
}

.brand__seal {
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border-radius: 14px 6px 14px 6px;
  color: #fff;
  background: var(--vermilion);
  font-family: 'STKaiti', 'KaiTi', serif;
  font-size: 24px;
  box-shadow: 0 8px 20px rgba(167, 69, 55, 0.22);
}

.brand__text {
  display: grid;
  line-height: 1;
}

.brand__text strong {
  font-family: 'STKaiti', 'KaiTi', serif;
  font-size: 22px;
  letter-spacing: 0.18em;
}

.brand__text small {
  margin-top: 6px;
  color: var(--muted);
  font-size: 8px;
  letter-spacing: 0.24em;
}

.brand--light {
  color: #fff;
}

.brand--light .brand__text small {
  color: rgba(255, 255, 255, 0.62);
}
</style>
