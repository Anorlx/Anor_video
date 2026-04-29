<template>
  <section class="min-h-full bg-gradient-to-b from-primary-light/40 via-white to-white py-8 sm:py-10">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
          <button
            type="button"
            class="inline-flex items-center gap-2 text-sm text-text-secondary hover:text-primary transition-colors cursor-pointer"
            @click="$emit('back-home')"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            返回首页
          </button>
          <h1 class="mt-3 text-3xl sm:text-4xl font-bold text-text-primary tracking-tight">历史记录</h1>
          <p class="mt-2 text-sm sm:text-base text-text-secondary">
            查看最近解析过的视频，随时回到首页再次处理。
          </p>
        </div>
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/80 border border-border-light text-sm text-text-secondary shadow-sm">
          <span class="w-2 h-2 rounded-full bg-success"></span>
          最近解析优先展示
        </div>
      </div>

      <div v-if="loading" class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div
          v-for="placeholder in 3"
          :key="placeholder"
          class="rounded-3xl border border-border-light bg-white/90 p-5 shadow-sm animate-pulse"
        >
          <div class="aspect-video rounded-2xl bg-gray-100"></div>
          <div class="mt-4 h-5 rounded bg-gray-100"></div>
          <div class="mt-3 h-4 w-2/3 rounded bg-gray-100"></div>
          <div class="mt-6 h-10 rounded-full bg-gray-100"></div>
        </div>
      </div>

      <div v-else-if="error" class="rounded-3xl border border-red-100 bg-red-50 px-6 py-8 text-center shadow-sm">
        <p class="text-lg font-semibold text-red-700">历史记录加载失败</p>
        <p class="mt-2 text-sm text-red-600">{{ error }}</p>
      </div>

      <div v-else-if="!items.length" class="rounded-3xl border border-border-light bg-white/90 px-6 py-12 text-center shadow-sm">
        <div class="mx-auto w-16 h-16 rounded-2xl bg-primary-light text-primary flex items-center justify-center">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 6v6l4 2m5-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="mt-5 text-2xl font-semibold text-text-primary">你还没有解析记录</h2>
        <p class="mt-2 text-sm sm:text-base text-text-secondary">先去解析一个视频，之后就能在这里快速回看。</p>
        <button
          type="button"
          class="mt-6 inline-flex items-center justify-center h-11 px-6 rounded-full bg-primary text-white font-medium hover:bg-primary-dark transition-colors cursor-pointer"
          @click="$emit('back-home')"
        >
          去首页解析
        </button>
      </div>

      <div v-else>
        <div class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="item in items"
            :key="item.id"
            class="rounded-3xl border border-border-light bg-white/95 overflow-hidden shadow-sm hover:shadow-md transition-shadow"
          >
            <div class="relative aspect-video bg-gray-100">
              <img
                v-if="item.thumbnail"
                :src="thumbnailUrl(item.thumbnail)"
                :alt="item.title"
                class="w-full h-full object-cover"
                @error="hideBrokenImage"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-text-muted">
                <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="absolute inset-x-0 bottom-0 flex items-center justify-between px-4 py-3 bg-gradient-to-t from-black/65 to-transparent text-white">
                <span class="text-xs font-medium uppercase tracking-[0.18em]">{{ formatPlatform(item.platform) }}</span>
                <span v-if="item.duration_string" class="text-xs font-medium bg-black/30 px-2.5 py-1 rounded-full">
                  {{ item.duration_string }}
                </span>
              </div>
            </div>

            <div class="p-5">
              <h2 class="text-lg font-semibold text-text-primary leading-snug line-clamp-2 min-h-[3.5rem]">
                {{ item.title || '未命名视频' }}
              </h2>
              <div class="mt-3 flex flex-wrap items-center gap-3 text-sm text-text-secondary">
                <span v-if="item.uploader" class="inline-flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  {{ item.uploader }}
                </span>
                <span class="inline-flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ formatParsedAt(item.parsed_at) }}
                </span>
              </div>
              <p class="mt-3 text-sm text-text-muted break-all line-clamp-2">{{ item.source_url }}</p>

              <div class="mt-5 flex flex-wrap gap-3">
                <button
                  type="button"
                  class="flex-1 min-w-[9rem] inline-flex items-center justify-center gap-2 h-11 px-5 rounded-full bg-primary text-white font-medium hover:bg-primary-dark transition-colors cursor-pointer"
                  :data-testid="`reparse-history-${item.id}`"
                  @click="$emit('reparse', item.source_url)"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  再次解析
                </button>
                <button
                  type="button"
                  class="inline-flex items-center justify-center gap-2 h-11 px-5 rounded-full border border-border-light text-text-primary hover:border-primary hover:text-primary transition-colors cursor-pointer"
                  :data-testid="`copy-history-${item.id}`"
                  @click="copyLink(item)"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 10h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  {{ copiedId === item.id ? '已复制链接' : '复制链接' }}
                </button>
              </div>
            </div>
          </article>
        </div>

        <div v-if="hasMore" class="mt-8 flex justify-center">
          <button
            type="button"
            class="inline-flex items-center justify-center gap-2 h-11 px-6 rounded-full border border-border-light bg-white text-text-primary hover:border-primary hover:text-primary transition-colors disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
            data-testid="load-more-history"
            :disabled="loadingMore"
            @click="$emit('load-more')"
          >
            <svg v-if="loadingMore" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24" aria-hidden="true">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            {{ loadingMore ? '加载中...' : '加载更多' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onBeforeUnmount, ref } from 'vue'

defineProps({
  items: { type: Array, default: () => [] },
  loading: Boolean,
  loadingMore: Boolean,
  hasMore: Boolean,
  error: { type: String, default: '' },
})

defineEmits(['back-home', 'load-more', 'reparse'])

const copiedId = ref(null)
let copiedTimer = null

function hideBrokenImage(event) {
  event.target.style.display = 'none'
}

function thumbnailUrl(url) {
  if (!url) return ''
  return '/api/proxy/thumbnail?url=' + encodeURIComponent(url)
}

function formatPlatform(platform) {
  if (!platform) return 'VIDEO'
  return String(platform).replace(/_/g, ' ').trim()
}

function formatParsedAt(value) {
  if (!value) return '刚刚解析'
  const parsedAt = new Date(value)
  if (Number.isNaN(parsedAt.getTime())) return '刚刚解析'
  const date = `${parsedAt.getFullYear()}-${String(parsedAt.getMonth() + 1).padStart(2, '0')}-${String(parsedAt.getDate()).padStart(2, '0')}`
  const time = `${String(parsedAt.getHours()).padStart(2, '0')}:${String(parsedAt.getMinutes()).padStart(2, '0')}`
  return `${date} ${time}`
}

async function copyLink(item) {
  if (!item?.source_url) return

  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(item.source_url)
    } else {
      const textarea = document.createElement('textarea')
      textarea.value = item.source_url
      textarea.setAttribute('readonly', 'true')
      textarea.style.position = 'absolute'
      textarea.style.left = '-9999px'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }

    copiedId.value = item.id
    clearTimeout(copiedTimer)
    copiedTimer = window.setTimeout(() => {
      copiedId.value = null
    }, 2000)
  } catch {
    copiedId.value = null
  }
}

onBeforeUnmount(() => {
  clearTimeout(copiedTimer)
})
</script>
