<script setup>
import { Feather, Quote } from 'lucide-vue-next'

import AppLogo from './AppLogo.vue'
</script>

<template>
  <main class="auth-shell">
    <section class="auth-story">
      <AppLogo light />
      <div class="story-copy">
        <p class="eyebrow"><Feather :size="15" /> 以字为舟，寄意一生</p>
        <h1>好名字，<br />是人生的第一句诗。</h1>
        <p class="story-intro">
          从千年典籍与东方意象中，寻找音韵、字义与期许恰好相遇的名字。
        </p>
      </div>
      <blockquote>
        <Quote :size="20" aria-hidden="true" />
        <p>名正则言顺，言顺则事成。</p>
        <cite>—《论语·子路》</cite>
      </blockquote>
      <div class="landscape" aria-hidden="true">
        <span class="sun"></span>
        <span class="mountain mountain--back"></span>
        <span class="mountain mountain--front"></span>
      </div>
    </section>
    <section class="auth-content">
      <div class="mobile-logo"><AppLogo /></div>
      <slot />
      <p class="auth-footer">字里 AI 起名 · 愿每一个名字都有美好来处</p>
    </section>
  </main>
</template>

<style scoped>
.auth-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(410px, 44%) 1fr;
}

.auth-story {
  position: relative;
  isolation: isolate;
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  padding: 48px 9%;
  color: #fff;
  background:
    radial-gradient(circle at 82% 14%, rgba(212, 185, 131, 0.14), transparent 28%),
    linear-gradient(145deg, #173c34, #0f2c27 64%, #0d2521);
}

.auth-story::after {
  position: absolute;
  inset: 0;
  z-index: -3;
  background-image: radial-gradient(rgba(255, 255, 255, 0.14) 0.7px, transparent 0.7px);
  background-size: 7px 7px;
  content: '';
  opacity: 0.13;
}

.story-copy {
  margin-top: auto;
  margin-bottom: auto;
  padding: 54px 0 30px;
}

.eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
  color: #d9c59a;
  font-size: 13px;
  letter-spacing: 0.22em;
}

h1 {
  margin: 0;
  font-family: 'STKaiti', 'KaiTi', serif;
  font-size: clamp(42px, 4.1vw, 66px);
  font-weight: 400;
  line-height: 1.32;
  letter-spacing: 0.06em;
}

.story-intro {
  max-width: 450px;
  margin: 28px 0 0;
  color: rgba(255, 255, 255, 0.66);
  font-size: 15px;
  line-height: 2;
  letter-spacing: 0.07em;
}

blockquote {
  position: relative;
  z-index: 2;
  margin: 0;
  padding: 18px 20px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
}

blockquote svg {
  color: #d9c59a;
}

blockquote p {
  margin: 5px 0 8px;
  font-family: 'STKaiti', 'KaiTi', serif;
  font-size: 17px;
  letter-spacing: 0.12em;
}

blockquote cite {
  color: rgba(255, 255, 255, 0.48);
  font-size: 11px;
  font-style: normal;
}

.landscape span {
  position: absolute;
  z-index: -2;
  display: block;
}

.sun {
  top: 19%;
  right: 15%;
  width: 86px;
  height: 86px;
  border-radius: 50%;
  background: rgba(205, 171, 107, 0.13);
  box-shadow: 0 0 80px rgba(205, 171, 107, 0.09);
}

.mountain {
  right: -10%;
  bottom: 7%;
  width: 75%;
  height: 38%;
  border-radius: 100% 0 0;
  transform: rotate(-9deg) skewX(-24deg);
}

.mountain--back {
  background: rgba(255, 255, 255, 0.025);
}

.mountain--front {
  right: -28%;
  bottom: -7%;
  height: 46%;
  background: rgba(255, 255, 255, 0.035);
}

.auth-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 54px clamp(28px, 7vw, 110px);
  background: var(--paper);
}

.mobile-logo {
  display: none;
}

.auth-footer {
  position: absolute;
  right: 5%;
  bottom: 24px;
  margin: 0;
  color: var(--muted-light);
  font-size: 11px;
  letter-spacing: 0.08em;
}

@media (max-width: 860px) {
  .auth-shell {
    display: block;
  }

  .auth-story {
    display: none;
  }

  .auth-content {
    position: relative;
    min-height: 100vh;
    align-items: flex-start;
    padding-top: 34px;
  }

  .mobile-logo {
    position: absolute;
    top: 28px;
    left: 28px;
    display: block;
  }
}
</style>
