<template>
  <section id="how-to-use" class="bg-bg-main py-16 sm:py-20" aria-labelledby="howto-heading">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="mb-10 max-w-3xl">
        <p class="text-sm font-semibold text-primary">Workflow</p>
        <h2 id="howto-heading" class="mt-2 text-2xl font-semibold tracking-tight text-text-primary sm:text-3xl">
          三步完成视频处理
        </h2>
        <p class="mt-3 text-sm leading-7 text-text-secondary">
          不需要安装桌面软件，也不需要在一堆弹窗里找下载入口。
        </p>
      </div>

      <div class="grid gap-4 lg:grid-cols-3">
        <article
          v-for="step in steps"
          :key="step.number"
          class="relative rounded-lg border border-border bg-surface p-5 shadow-sm"
        >
          <div class="mb-5 flex items-center justify-between">
            <span class="font-mono text-sm font-semibold text-primary">0{{ step.number }}</span>
            <svg class="h-5 w-5 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="step.icon" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-text-primary">{{ step.title }}</h3>
          <p class="mt-3 text-sm leading-7 text-text-secondary">{{ step.desc }}</p>
        </article>
      </div>

      <div class="mt-6 rounded-lg border border-border-light bg-surface-muted px-4 py-3 text-sm text-text-secondary">
        手机和桌面浏览器都可以直接使用。更新于 2026 年 3 月。
      </div>
    </div>
  </section>
</template>

<script setup>
const steps = [
  {
    number: 1,
    title: '复制视频链接',
    desc: '从原平台复制分享链接或地址栏 URL，YouTube、Bilibili、抖音等都可以。',
    icon: 'M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z',
  },
  {
    number: 2,
    title: '粘贴并解析',
    desc: 'Agent_video 自动识别平台、标题、封面和可用格式，把可操作项集中展示。',
    icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
  },
  {
    number: 3,
    title: '下载或总结',
    desc: '选择格式下载，也可以继续生成摘要、字幕、思维导图，并围绕视频提问。',
    icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4',
  },
]
</script>
