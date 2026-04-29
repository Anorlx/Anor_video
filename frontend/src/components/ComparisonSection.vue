<template>
  <section id="comparison" class="bg-surface py-16 sm:py-20" aria-labelledby="comparison-heading">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="mb-10 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p class="text-sm font-semibold text-primary">Comparison</p>
          <h2 id="comparison-heading" class="mt-2 text-2xl font-semibold tracking-tight text-text-primary sm:text-3xl">
            和常见下载方式相比
          </h2>
        </div>
        <p class="max-w-xl text-sm leading-7 text-text-secondary">
          重点不是堆功能，而是把下载、字幕和 AI 理解放在同一条工作流里。
        </p>
      </div>

      <div class="overflow-x-auto rounded-lg border border-border shadow-sm">
        <table class="w-full min-w-[760px] text-sm">
          <thead>
            <tr class="bg-bg-main text-text-primary">
              <th class="px-5 py-4 text-left font-semibold">能力</th>
              <th class="px-5 py-4 text-left font-semibold text-primary">Agent_video</th>
              <th class="px-5 py-4 text-left font-semibold">普通网页工具</th>
              <th class="px-5 py-4 text-left font-semibold">桌面软件</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border-light bg-surface">
            <tr v-for="row in rows" :key="row.feature" class="hover:bg-surface-muted">
              <td class="px-5 py-4 font-medium text-text-primary">{{ row.feature }}</td>
              <td class="px-5 py-4 text-text-primary">
                <span v-if="row.saveany === true" class="inline-flex items-center gap-1.5 font-medium text-primary">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  支持
                </span>
                <span v-else-if="row.saveany === false" class="inline-flex items-center gap-1.5 text-text-muted">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  不支持
                </span>
                <span v-else>{{ row.saveany }}</span>
              </td>
              <td class="px-5 py-4 text-text-secondary">
                <span v-if="row.online === true" class="inline-flex items-center gap-1.5 text-success">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  支持
                </span>
                <span v-else-if="row.online === false" class="inline-flex items-center gap-1.5 text-text-muted">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  不支持
                </span>
                <span v-else>{{ row.online }}</span>
              </td>
              <td class="px-5 py-4 text-text-secondary">
                <span v-if="row.desktop === true" class="inline-flex items-center gap-1.5 text-success">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  支持
                </span>
                <span v-else-if="row.desktop === false" class="inline-flex items-center gap-1.5 text-text-muted">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  不支持
                </span>
                <span v-else>{{ row.desktop }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
const rows = [
  { feature: '支持平台数量', saveany: '1800+', online: '10-50', desktop: '100-500' },
  { feature: 'AI 视频总结', saveany: true, online: false, desktop: false },
  { feature: '思维导图生成', saveany: true, online: false, desktop: false },
  { feature: '字幕下载', saveany: 'SRT / VTT / TXT', online: '部分支持', desktop: '部分支持' },
  { feature: '抖音无水印下载', saveany: true, online: '部分支持', desktop: '通常需登录' },
  { feature: '最高画质', saveany: '4K', online: '720p-1080p', desktop: '4K' },
  { feature: '无需安装', saveany: true, online: true, desktop: false },
  { feature: '手机浏览器可用', saveany: true, online: '部分支持', desktop: false },
  { feature: '费用', saveany: '免费下载', online: '免费/付费', desktop: '付费为主' },
]

</script>
