<template>
  <section
    class="relative overflow-hidden bg-bg-main border-b border-border-light transition-all"
    :class="
      compact ? 'pt-6 pb-5 sm:pt-8 sm:pb-7' : 'pt-12 pb-12 sm:pt-18 sm:pb-16'
    "
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div
        class="grid gap-8 lg:grid-cols-[minmax(0,1.1fr)_minmax(320px,0.9fr)] lg:items-center"
      >
        <div>
          <template v-if="showSlogan">
            <div
              class="inline-flex items-center gap-2 rounded-md border border-border bg-surface px-3 py-1.5 text-xs font-medium text-text-secondary shadow-sm"
              :class="compact ? 'mb-3' : 'mb-5'"
            >
              <span class="h-2 w-2 rounded-full bg-success"></span>
              Agent_video · 1800+ 平台解析
            </div>

            <h1
              :class="
                compact
                  ? 'text-2xl sm:text-4xl mb-3'
                  : 'text-4xl sm:text-6xl mb-5'
              "
              class="max-w-4xl font-semibold text-text-primary leading-[1.04] tracking-tight"
            >
              Agent_video，一键处理视频
            </h1>
            <p
              :class="
                compact
                  ? 'mb-5 text-sm sm:text-base'
                  : 'mb-7 text-base sm:text-lg'
              "
              class="max-w-2xl text-text-secondary leading-8"
            >
              粘贴视频链接，Agent_video
              会解析清晰度、生成字幕摘要、整理思维导图，并支持围绕视频继续提问。
            </p>
          </template>

          <div class="max-w-3xl">
            <form
              @submit.prevent="onSubmit"
              class="flex flex-col gap-3 rounded-lg border border-border bg-surface p-2 shadow-[0_18px_45px_rgba(16,32,29,0.08)] sm:flex-row sm:items-center"
              role="search"
              aria-label="视频链接解析"
            >
              <div class="relative flex-1">
                <label for="video-url-input" class="sr-only"
                  >粘贴视频链接进行解析下载</label
                >
                <svg
                  class="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-text-muted"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                  />
                </svg>
                <input
                  id="video-url-input"
                  v-model="url"
                  type="url"
                  :placeholder="placeholder"
                  class="h-13 w-full rounded-md border border-transparent bg-surface-muted pl-12 pr-4 text-base text-text-primary placeholder:text-text-muted transition-all focus:border-primary focus:bg-surface focus:outline-none focus:ring-3 focus:ring-primary/15 disabled:opacity-70"
                  :disabled="loading"
                  autocomplete="url"
                />
              </div>
              <button
                type="submit"
                :disabled="loading || !url.trim()"
                class="inline-flex h-13 items-center justify-center gap-2 rounded-md bg-primary px-6 text-base font-semibold text-white shadow-sm transition-all hover:bg-primary-dark disabled:cursor-not-allowed disabled:opacity-50 sm:min-w-[8.75rem]"
              >
                <svg
                  v-if="loading"
                  class="h-5 w-5 animate-spin"
                  fill="none"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                <svg
                  v-else
                  class="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                  />
                </svg>
                {{ loading ? "解析中" : "开始解析" }}
              </button>
            </form>

            <div
              v-if="showSlogan"
              class="mt-4 flex flex-wrap items-center gap-2 text-xs text-text-muted"
            >
              <span class="mr-1">示例链接</span>
              <button
                v-for="example in examples"
                :key="example.label"
                type="button"
                @click="url = example.url"
                class="rounded-md border border-border-light bg-surface px-3 py-1.5 text-text-secondary transition-colors hover:border-primary hover:text-primary"
              >
                {{ example.label }}
              </button>
            </div>
          </div>
        </div>

        <div
          v-if="showSlogan && !compact"
          class="hidden lg:block"
          aria-hidden="true"
        >
          <div
            class="rounded-lg border border-border bg-surface shadow-[0_18px_45px_rgba(16,32,29,0.08)]"
          >
            <div
              class="flex items-center justify-between border-b border-border-light px-4 py-3"
            >
              <div class="flex items-center gap-2">
                <span class="h-2.5 w-2.5 rounded-full bg-error/70"></span>
                <span class="h-2.5 w-2.5 rounded-full bg-warning/70"></span>
                <span class="h-2.5 w-2.5 rounded-full bg-success/70"></span>
              </div>
              <span class="text-xs font-medium text-text-muted"
                >Agent_video workspace</span
              >
            </div>
            <div class="p-4">
              <div
                class="aspect-video overflow-hidden rounded-md bg-ink text-primary-light"
              >
                <div class="flex h-full">
                  <div
                    class="relative flex min-w-0 flex-1 flex-col justify-between p-4"
                  >
                    <div class="flex items-center justify-between">
                      <span class="rounded-md bg-white/10 px-2.5 py-1 text-xs"
                        >4K MP4</span
                      >
                      <span class="rounded-md bg-white/10 px-2.5 py-1 text-xs"
                        >AI Summary</span
                      >
                    </div>
                    <div
                      class="absolute left-1/2 top-1/2 grid h-14 w-14 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full bg-white/15 shadow-[0_0_0_10px_rgba(255,255,255,0.06)]"
                    >
                      <svg
                        class="ml-0.5 h-6 w-6 text-primary-light"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        aria-hidden="true"
                      >
                        <path d="M6.5 4.75v10.5L15 10 6.5 4.75z" />
                      </svg>
                    </div>
                    <div>
                      <div class="mb-3 flex items-center gap-2">
                        <div
                          class="h-1.5 flex-1 overflow-hidden rounded-full bg-white/15"
                        >
                          <div
                            class="h-full w-[68%] rounded-full bg-primary-light"
                          ></div>
                        </div>
                        <span class="text-[10px] text-primary-light/75"
                          >08:42</span
                        >
                      </div>
                      <div class="grid grid-cols-5 gap-1.5">
                        <span
                          v-for="bar in waveformBars"
                          :key="bar"
                          class="rounded-full bg-primary-light/35"
                          :style="{ height: `${bar}px` }"
                        ></span>
                      </div>
                    </div>
                  </div>
                  <div
                    class="hidden w-32 border-l border-white/10 bg-white/[0.04] p-3 sm:block"
                  >
                    <div
                      class="mb-3 text-[11px] font-semibold text-primary-light"
                    >
                      Agent 视频工作台
                    </div>
                    <div class="space-y-2">
                      <div class="rounded-md bg-white/10 p-2">
                        <div class="text-[10px] text-primary-light/60">
                          内容章节
                        </div>
                        <div
                          class="mt-1 h-1.5 rounded-full bg-primary-light/70"
                        ></div>
                        <div
                          class="mt-1.5 h-1.5 w-2/3 rounded-full bg-primary-light/35"
                        ></div>
                      </div>
                      <div class="rounded-md bg-white/10 p-2">
                        <div class="text-[10px] text-primary-light/60">
                          关键片段
                        </div>
                        <div class="mt-1 flex gap-1">
                          <span class="h-5 flex-1 rounded bg-accent/80"></span>
                          <span class="h-5 flex-1 rounded bg-success/80"></span>
                          <span class="h-5 flex-1 rounded bg-primary/80"></span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="mt-4 grid grid-cols-3 gap-3">
                <div
                  v-for="metric in metrics"
                  :key="metric.label"
                  class="rounded-md border border-border-light bg-surface-muted p-3"
                >
                  <div class="text-lg font-semibold text-text-primary">
                    {{ metric.value }}
                  </div>
                  <div class="mt-1 text-xs text-text-muted">
                    {{ metric.label }}
                  </div>
                </div>
              </div>
              <div
                class="mt-4 space-y-2 rounded-md border border-border-light bg-surface-muted p-3"
              >
                <div
                  class="flex items-center gap-2 text-xs font-medium text-text-secondary"
                >
                  <svg
                    class="h-4 w-4 text-primary"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 17v-2a4 4 0 014-4h6m0 0l-3-3m3 3l-3 3M5 5h8a2 2 0 012 2v1M5 5a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-1"
                    />
                  </svg>
                  自动整理视频内容
                </div>
                <div class="h-2 rounded-full bg-border-light"></div>
                <div class="h-2 w-4/5 rounded-full bg-border-light"></div>
                <div class="h-2 w-2/3 rounded-full bg-border-light"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  loading: Boolean,
  compact: Boolean,
  showSlogan: { type: Boolean, default: true },
});
const emit = defineEmits(["parse"]);

const url = ref("");
const placeholder = "粘贴视频链接，例如 https://www.youtube.com/watch?v=...";

const examples = [
  { label: "YouTube", url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ" },
  { label: "Bilibili", url: "https://www.bilibili.com/video/BV1GJ411x7h7" },
  { label: "Twitter / X", url: "https://x.com/elonmusk/status/1234567890" },
];

const metrics = [
  { value: "1800+", label: "支持平台" },
  { value: "4K", label: "最高画质" },
  { value: "AI", label: "摘要问答" },
];

const waveformBars = [16, 24, 18, 30, 20];

function normalizeUrl(raw) {
  let u = raw;
  if (u.includes("bilibili.com") && !u.includes("www.bilibili.com")) {
    u = u.replace("bilibili.com", "www.bilibili.com");
  }
  return u;
}

function onSubmit() {
  const trimmed = url.value.trim();
  if (trimmed) {
    emit("parse", normalizeUrl(trimmed));
  }
}
</script>
