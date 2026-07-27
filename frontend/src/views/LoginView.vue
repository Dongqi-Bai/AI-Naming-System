<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowRight, Eye, EyeOff, LockKeyhole, Mail } from 'lucide-vue-next'

import AuthShell from '../components/AuthShell.vue'
import { apiRequest } from '../services/api'
import { saveSession } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const form = ref({ email: '', password: '' })
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function submitLogin() {
  error.value = ''
  loading.value = true
  try {
    const data = await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify(form.value),
    })
    saveSession(data)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/naming'
    await router.replace(redirect)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <AuthShell>
    <div class="auth-form-wrap">
      <div class="form-heading">
        <span class="heading-mark">归</span>
        <div>
          <h2>欢迎回来</h2>
          <p>登录后，继续你的名字灵感之旅</p>
        </div>
      </div>

      <form class="auth-form" @submit.prevent="submitLogin">
        <p v-if="route.query.registered" class="form-notice" role="status">
          注册成功，请使用新账号登录
        </p>

        <label class="field">
          <span>邮箱地址</span>
          <div class="input-wrap">
            <Mail :size="18" />
            <input
              v-model.trim="form.email"
              type="email"
              autocomplete="email"
              placeholder="请输入注册邮箱"
              required
            />
          </div>
        </label>

        <label class="field">
          <span>密码</span>
          <div class="input-wrap">
            <LockKeyhole :size="18" />
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              minlength="6"
              placeholder="请输入密码"
              required
            />
            <button
              class="icon-button"
              type="button"
              :aria-label="showPassword ? '隐藏密码' : '显示密码'"
              @click="showPassword = !showPassword"
            >
              <EyeOff v-if="showPassword" :size="18" />
              <Eye v-else :size="18" />
            </button>
          </div>
        </label>

        <p v-if="error" class="form-error" role="alert">{{ error }}</p>

        <button class="primary-button" type="submit" :disabled="loading">
          <span>{{ loading ? '正在登录…' : '登录' }}</span>
          <ArrowRight v-if="!loading" :size="18" />
        </button>
      </form>

      <p class="switch-entry">
        还没有账号？
        <RouterLink to="/register">立即注册</RouterLink>
      </p>
      <div class="trust-note"><span></span> 你的信息将被安全保护 <span></span></div>
    </div>
  </AuthShell>
</template>
