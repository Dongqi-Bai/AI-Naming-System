<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  BookOpenText,
  ChevronDown,
  Feather,
  LogOut,
  RefreshCw,
  Sparkles,
  UserRound,
} from 'lucide-vue-next'

import AppLogo from '../components/AppLogo.vue'
import { apiRequest } from '../services/api'
import { authState, clearSession, refreshCurrentUser } from '../stores/auth'

const router = useRouter()
const form = ref({
  surname: '',
  gender: '不限',
  length: '不限',
  other: '',
  excludeText: '',
})
const results = ref([])
const loading = ref(false)
const error = ref('')
const hasGenerated = computed(() => results.value.length > 0)

async function verifySession() {
  try {
    await refreshCurrentUser()
  } catch (err) {
    if (err.status === 401) logout()
  }
}

function logout() {
  clearSession()
  router.replace('/login')
}

async function generateNames() {
  error.value = ''
  results.value = []
  loading.value = true
  const exclude = form.value.excludeText
    .split(/[,，、\s]+/)
    .map((item) => item.trim())
    .filter(Boolean)

  try {
    const data = await apiRequest('/name', {
      method: 'POST',
      body: JSON.stringify({
        surname: form.value.surname,
        gender: form.value.gender,
        length: form.value.length,
        other: form.value.other,
        exclude,
      }),
    })
    results.value = data.names
  } catch (err) {
    if (err.status === 401) {
      logout()
      return
    }
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(verifySession)
</script>

<template>
  <main class="naming-page">
    <header class="app-header">
      <AppLogo />
      <div class="header-actions">
        <div class="user-chip">
          <span class="user-avatar"><UserRound :size="15" /></span>
          <div>
            <strong>{{ authState.user?.username || '起名访客' }}</strong>
            <small>{{ authState.user?.email }}</small>
          </div>
        </div>
        <button class="logout-button" type="button" aria-label="退出登录" @click="logout">
          <LogOut :size="18" />
        </button>
      </div>
    </header>

    <section class="naming-hero">
      <div class="hero-ornament" aria-hidden="true">名</div>
      <p class="eyebrow"><Sparkles :size="15" /> AI × 中华典籍</p>
      <h1>为一生的期许，<em>寻一个好名字</em></h1>
      <p>告诉我们你的偏好，AI 将从音韵、字义与文化出处中，为你细细斟酌。</p>
    </section>

    <section class="naming-workspace" :class="{ 'has-results': hasGenerated }">
      <form class="naming-form panel" @submit.prevent="generateNames">
        <div class="panel-heading">
          <span><Feather :size="19" /></span>
          <div>
            <h2>起名信息</h2>
            <p>越具体的描述，越能贴近你的期待</p>
          </div>
        </div>

        <label class="field">
          <span>姓氏 <b>必填</b></span>
          <div class="surname-input">
            <input
              v-model.trim="form.surname"
              maxlength="4"
              placeholder="如：林"
              required
            />
            <small>氏</small>
          </div>
        </label>

        <fieldset class="field">
          <legend>性别偏好</legend>
          <div class="segmented">
            <label v-for="item in ['不限', '男', '女']" :key="item">
              <input v-model="form.gender" type="radio" :value="item" />
              <span>{{ item }}</span>
            </label>
          </div>
        </fieldset>

        <fieldset class="field">
          <legend>名字字数</legend>
          <div class="segmented">
            <label v-for="item in ['不限', '单字', '双字']" :key="item">
              <input v-model="form.length" type="radio" :value="item" />
              <span>{{ item }}</span>
            </label>
          </div>
        </fieldset>

        <label class="field">
          <span>更多期待 <i>选填</i></span>
          <textarea
            v-model.trim="form.other"
            maxlength="200"
            rows="4"
            placeholder="例如：希望名字清雅温润，带有山水意象…"
          ></textarea>
          <small class="character-count">{{ form.other.length }} / 200</small>
        </label>

        <label class="field">
          <span>避用字 <i>选填</i></span>
          <input
            v-model.trim="form.excludeText"
            placeholder="多个字请用逗号分隔"
          />
        </label>

        <p v-if="error" class="form-error" role="alert">{{ error }}</p>

        <button class="generate-button" type="submit" :disabled="loading">
          <RefreshCw v-if="loading" class="spin" :size="18" />
          <Sparkles v-else :size="18" />
          {{ loading ? '正在翻阅典籍，细细斟酌…' : hasGenerated ? '再寻一组好名字' : '开始寻名' }}
        </button>
        <p class="form-tip">每次将为你生成 6 个专属名字方案</p>
      </form>

      <section class="results-panel">
        <div v-if="loading" class="loading-state">
          <div class="ink-loader"><span>字</span></div>
          <h2>正在为你寻名</h2>
          <p>品音韵 · 查典故 · 悟寓意</p>
          <div class="loading-lines">
            <i></i><i></i><i></i>
          </div>
        </div>

        <div v-else-if="hasGenerated" class="results-content">
          <div class="results-heading">
            <div>
              <p class="eyebrow"><BookOpenText :size="15" /> 寻名结果</p>
              <h2>为你甄选的名字</h2>
            </div>
            <span>共 {{ results.length }} 个方案</span>
          </div>

          <div class="name-grid">
            <article v-for="(item, index) in results" :key="`${item.name}-${index}`" class="name-card">
              <span class="card-number">{{ String(index + 1).padStart(2, '0') }}</span>
              <h3>{{ item.name }}</h3>
              <div class="reference">
                <BookOpenText :size="15" />
                <p><span>出处</span>{{ item.reference }}</p>
              </div>
              <p class="moral">{{ item.moral }}</p>
            </article>
          </div>
        </div>

        <div v-else class="empty-state">
          <div class="empty-seal" aria-hidden="true">待<br />寻</div>
          <h2>你的好名字，会在这里出现</h2>
          <p>填写左侧信息，让我们从诗词典籍中<br />为你寻得一份独特的美好寓意。</p>
          <span class="empty-line"><i></i><ChevronDown :size="14" /><i></i></span>
          <small>一个名字 · 一份期许 · 一生相伴</small>
        </div>
      </section>
    </section>

    <footer class="app-footer">字里 AI 起名 · 取意经典，寄愿未来</footer>
  </main>
</template>
