<template>
  <div class="min-h-screen flex flex-col bg-bg-main text-text-primary">
    <AppHeader
      :user="currentUser"
      @login="showAuthModal('login')"
      @register="showAuthModal('register')"
      @logout="handleLogout"
      @open-history="handleOpenHistory"
    />
    <main class="flex-1">
      <HistoryPage
        v-if="currentPage === 'history'"
        :items="historyItems"
        :loading="historyLoading"
        :loadingMore="historyLoadingMore"
        :hasMore="historyHasMore"
        :error="historyError"
        @back-home="setCurrentPage('home')"
        @load-more="loadHistory()"
        @reparse="handleReparseFromHistory"
      />
      <template v-else>
        <HeroSection
          @parse="handleParse"
          :loading="loading"
          :compact="!!videoData"
          :showSlogan="!videoData || demoMode"
        />
        <!-- 视频信息 + AI 总结：左右双栏同屏布局 -->
        <section v-if="videoData" class="py-5 sm:py-8 bg-bg-main border-y border-border-light">
          <div class="max-w-7xl mx-auto px-4 sm:px-6">
            <div class="flex flex-col lg:flex-row gap-5 lg:gap-6">
              <!-- 左栏：视频信息 -->
              <div class="w-full lg:w-2/5 lg:flex-shrink-0">
                <VideoResult
                  :video="videoData"
                  :downloading="downloading"
                  :summarizing="summarizing"
                  @download="handleDownload"
                  @summarize="handleSummarize"
                />
              </div>
              <!-- 右栏：AI 总结 -->
              <div class="w-full lg:w-3/5 min-w-0">
                <VideoSummary
                  :videoUrl="currentUrl"
                  :videoTitle="videoData.title"
                  :user="currentUser"
                  :key="summaryKey"
                  @loading-change="handleSummarizeLoadingChange"
                  @need-login="showAuthModal('login')"
                />
              </div>
            </div>
          </div>
        </section>
        <FeatureSection />
        <HowToSection />
        <ComparisonSection />
      </template>
    </main>
    <AppFooter />

    <AuthModal
      :visible="authModalVisible"
      :initialMode="authModalMode"
      @close="authModalVisible = false"
      @success="handleAuthSuccess"
    />
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import HeroSection from './components/HeroSection.vue'
import VideoResult from './components/VideoResult.vue'
import VideoSummary from './components/VideoSummary.vue'
import HistoryPage from './components/HistoryPage.vue'
import FeatureSection from './components/FeatureSection.vue'
import HowToSection from './components/HowToSection.vue'
import ComparisonSection from './components/ComparisonSection.vue'
import AppFooter from './components/AppFooter.vue'
import AuthModal from './components/AuthModal.vue'
import { fetchHistory } from './api/history.js'
import { parseVideo, downloadViaServer } from './api/video.js'
import { getSavedUser, fetchMe, logout as logoutApi, isLoggedIn } from './api/auth.js'

const demoMode = ref(false)
let enterCount = 0
let enterTimer = null

function onKeyDown(e) {
  if (e.key === 'Enter' && !e.target.matches('input, textarea, [contenteditable]')) {
    enterCount++
    clearTimeout(enterTimer)
    if (enterCount >= 3) {
      demoMode.value = !demoMode.value
      enterCount = 0
    } else {
      enterTimer = setTimeout(() => { enterCount = 0 }, 800)
    }
  }
}

onMounted(() => {
  document.addEventListener('keydown', onKeyDown)
  currentPage.value = getPageFromUrl()
  if (currentPage.value === 'history' && !isLoggedIn()) {
    pendingPage.value = 'history'
    currentPage.value = 'home'
    syncPageQuery('home')
    showAuthModal('login')
  }
  restoreUser()
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKeyDown)
})

// ===== 用户状态管理 =====
const currentUser = ref(null)
const authModalVisible = ref(false)
const authModalMode = ref('login')
const pendingPage = ref(null)

function showAuthModal(mode = 'login') {
  authModalMode.value = mode
  authModalVisible.value = true
}

function handleAuthSuccess(user) {
  currentUser.value = user
  authModalVisible.value = false
  if (pendingPage.value === 'history') {
    pendingPage.value = null
    handleOpenHistory()
  }
}

function handleLogout() {
  logoutApi()
  currentUser.value = null
  pendingPage.value = null
  resetHistoryState()
  if (currentPage.value === 'history') {
    setCurrentPage('home')
  }
}

async function restoreUser() {
  if (!isLoggedIn()) return
  const saved = getSavedUser()
  if (saved) currentUser.value = saved
  try {
    currentUser.value = await fetchMe()
    if (currentPage.value === 'history') {
      await loadHistory({ reset: true })
    }
  } catch {
    const shouldReopenHistory = currentPage.value === 'history'
    handleLogout()
    if (shouldReopenHistory) {
      pendingPage.value = 'history'
      showAuthModal('login')
    }
  }
}

// ===== 历史记录 =====
const currentPage = ref('home')
const historyItems = ref([])
const historyLoading = ref(false)
const historyLoadingMore = ref(false)
const historyHasMore = ref(false)
const historyError = ref('')
const HISTORY_PAGE_LIMIT = 20

function getPageFromUrl() {
  const params = new URLSearchParams(window.location.search)
  return params.get('page') === 'history' ? 'history' : 'home'
}

function syncPageQuery(page) {
  const params = new URLSearchParams(window.location.search)
  if (page === 'history') {
    params.set('page', 'history')
  } else {
    params.delete('page')
  }
  const search = params.toString()
  window.history.replaceState({}, '', `${window.location.pathname}${search ? `?${search}` : ''}`)
}

function setCurrentPage(page) {
  currentPage.value = page
  syncPageQuery(page)
}

function resetHistoryState() {
  historyItems.value = []
  historyLoading.value = false
  historyLoadingMore.value = false
  historyHasMore.value = false
  historyError.value = ''
}

async function loadHistory({ reset = false } = {}) {
  if (!isLoggedIn()) return
  const offset = reset ? 0 : historyItems.value.length

  if (reset) {
    historyLoading.value = true
    historyError.value = ''
  } else {
    if (!historyHasMore.value && historyItems.value.length > 0) return
    historyLoadingMore.value = true
  }

  try {
    const res = await fetchHistory({ offset, limit: HISTORY_PAGE_LIMIT })
    if (res.success) {
      historyItems.value = reset ? res.data.items : [...historyItems.value, ...res.data.items]
      historyHasMore.value = res.data.has_more
      historyError.value = ''
    } else {
      historyError.value = '历史记录加载失败，请稍后重试'
    }
  } catch (err) {
    if (err.response?.status === 401) {
      handleLogout()
      pendingPage.value = 'history'
      showAuthModal('login')
      return
    }
    historyError.value = '历史记录加载失败，请稍后重试'
    if (reset) historyItems.value = []
  } finally {
    historyLoading.value = false
    historyLoadingMore.value = false
  }
}

async function handleOpenHistory() {
  if (!isLoggedIn()) {
    pendingPage.value = 'history'
    showAuthModal('login')
    return
  }
  setCurrentPage('history')
  await loadHistory({ reset: true })
}

// ===== 视频功能 =====
const loading = ref(false)
const downloading = ref(false)
const videoData = ref(null)
const currentUrl = ref('')
const summaryKey = ref(0)
const summarizing = ref(false)

function handleSummarize() {
  summaryKey.value++
}

function handleSummarizeLoadingChange(isLoading) {
  summarizing.value = isLoading
}

async function handleParse(url) {
  loading.value = true
  videoData.value = null
  currentUrl.value = url
  try {
    const res = await parseVideo(url)
    if (res.success) {
      videoData.value = res.data
      summaryKey.value++
    } else {
      alert('解析失败：' + (res.error || '未知错误'))
    }
  } catch (err) {
    const msg = err.response?.data?.detail?.error || err.response?.data?.detail || err.message
    alert('解析失败：' + msg)
  } finally {
    loading.value = false
  }
}

function handleReparseFromHistory(url) {
  setCurrentPage('home')
  handleParse(url)
}

async function handleDownload(formatId) {
  downloading.value = true
  try {
    const response = await downloadViaServer(currentUrl.value, formatId)
    const contentDisposition = response.headers['content-disposition']
    let filename = 'video.mp4'
    if (contentDisposition) {
      const match = contentDisposition.match(/filename\*?=(?:UTF-8'')?([^;\n]+)/i)
      if (match) filename = decodeURIComponent(match[1].replace(/"/g, ''))
    }
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    alert('下载失败：' + (err.message || '请稍后重试'))
  } finally {
    downloading.value = false
  }
}
</script>

<style>
@keyframes toast-in {
  from { opacity: 0; transform: translate(-50%, -10px); }
  to { opacity: 1; transform: translate(-50%, 0); }
}
.animate-toast-in {
  animation: toast-in 0.3s ease-out;
}
</style>
