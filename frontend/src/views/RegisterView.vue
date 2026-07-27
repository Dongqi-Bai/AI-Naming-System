<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowRight,
  BadgeCheck,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  UserRound,
} from 'lucide-vue-next'

import AuthShell from '../components/AuthShell.vue'
import { apiRequest } from '../services/api'

const router = useRouter()
const form = ref({
  username: '',
  email: '',
  code: '',
  password: '',
  confirm_password: '',
})
const showPassword = ref(false)
const loading = ref(false)
const sendingCode = ref(false)
const cooldown = ref(0)
const error = ref('')
const notice = ref('')
let timer

const codeButtonText = computed(() => {
  if (sendingCode.value) return '发送中…'
  if (cooldown.value) return `${cooldown.value}s 后重试`
  return '获取验证码'
})

function startCooldown() {
  cooldown.value = 60
  timer = window.setInterval(() => {
    cooldown.value -= 1
    if (cooldown.value <= 0) window.clearInterval(timer)
  }, 1000)
}

async function sendCode() {
  if (!form.value.email) {
    error.value = '请先填写邮箱地址'
    return
  }
  error.value = ''
  notice.value = ''
  sendingCode.value = true
  try {
    const data = await apiRequest(`/auth/code?email=${encodeURIComponent(form.value.email)}`, {
      method: 'POST',
    })
    notice.value = data.message
    startCooldown()
  } catch (err) {
    error.value = err.message
  } finally {
    sendingCode.value = false
  }
}

async function submitRegister() {
  error.value = ''
  notice.value = ''
  if (form.value.password !== form.value.confirm_password) {
    error.value = '两次输入的密码不一致'
    return
  }
  loading.value = true
  try {
    await apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(form.value),
    })
    await router.push({ name: 'login', query: { registered: '1' } })
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onBeforeUnmount(() => window.clearInterval(timer))
</script>

<template>
  <AuthShell>
    <div class="auth-form-wrap auth-form-wrap--register">
      <div class="form-heading">
        <span class="heading-mark">启</span>
        <div>
          <h2>创建账号</h2>
          <p>一段关于名字与期待的旅程，从这里开始</p>
        </div>
      </div>

      <form class="auth-form auth-form--compact" @submit.prevent="submitRegister">
        <label class="field">
          <span>昵称</span>
          <div class="input-wrap">
            <UserRound :size="18" />
            <input
              v-model.trim="form.username"
              autocomplete="nickname"
              minlength="2"
              maxlength="20"
              placeholder="怎么称呼你"
              required
            />
          </div>
        </label>

        <label class="field">
          <span>邮箱地址</span>
          <div class="input-wrap">
            <Mail :size="18" />
            <input
              v-model.trim="form.email"
              type="email"
              autocomplete="email"
              placeholder="用于接收验证码"
              required
            />
          </div>
        </label>

        <label class="field">
          <span>邮箱验证码</span>
          <div class="code-row">
            <div class="input-wrap">
              <BadgeCheck :size="18" />
              <input
                v-model.trim="form.code"
                inputmode="numeric"
                maxlength="4"
                pattern="\d{4}"
                placeholder="4 位验证码"
                required
              />
            </div>
            <button
              class="code-button"
              type="button"
              :disabled="sendingCode || cooldown > 0"
              @click="sendCode"
            >
              {{ codeButtonText }}
            </button>
          </div>
        </label>

        <div class="field-grid">
          <label class="field">
            <span>设置密码</span>
            <div class="input-wrap">
              <LockKeyhole :size="18" />
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="new-password"
                minlength="6"
                placeholder="至少 6 位"
                required
              />
            </div>
          </label>
          <label class="field">
            <span>确认密码</span>
            <div class="input-wrap">
              <LockKeyhole :size="18" />
              <input
                v-model="form.confirm_password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="new-password"
                minlength="6"
                placeholder="再次输入"
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
        </div>

        <p v-if="error" class="form-error" role="alert">{{ error }}</p>
        <p v-if="notice" class="form-notice" role="status">{{ notice }}</p>

        <button class="primary-button" type="submit" :disabled="loading">
          <span>{{ loading ? '正在创建…' : '注册并开启旅程' }}</span>
          <ArrowRight v-if="!loading" :size="18" />
        </button>
      </form>

      <p class="switch-entry">
        已有账号？
        <RouterLink to="/login">返回登录</RouterLink>
      </p>
    </div>
  </AuthShell>
</template>
