<template>
  <section id="features" class="bg-surface py-16 sm:py-20" aria-labelledby="features-heading">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="mb-10 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p class="text-sm font-semibold text-primary">Core Capabilities</p>
          <h2 id="features-heading" class="mt-2 text-2xl font-semibold tracking-tight text-text-primary sm:text-3xl">
            常用的视频处理能力，集中在一个工作台
          </h2>
        </div>
        <p class="max-w-xl text-sm leading-7 text-text-secondary">
          从链接解析到字幕、摘要和问答，界面只保留真正会影响操作效率的信息。
        </p>
      </div>

      <div class="grid grid-cols-1 gap-px overflow-hidden rounded-lg border border-border bg-border md:grid-cols-2 lg:grid-cols-5">
        <article
          v-for="feature in features"
          :key="feature.title"
          class="group bg-surface p-5 transition-colors hover:bg-surface-muted"
        >
          <div class="mb-6 flex h-10 w-10 items-center justify-center rounded-md border border-border-light bg-bg-main text-primary">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="feature.icon" />
            </svg>
          </div>
          <h3 class="text-base font-semibold text-text-primary">{{ feature.title }}</h3>
          <p class="mt-3 text-sm leading-7 text-text-secondary">{{ feature.desc }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
const features = [
  {
    title: '多平台解析',
    desc: '覆盖 YouTube、Bilibili、抖音、TikTok、X、Instagram 等主流视频平台。',
    icon: 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2h1m4-5h1a2 2 0 012 2v1a2 2 0 002 2h1.945M7.737 7.737A8.963 8.963 0 0112 6c1.58 0 3.06.408 4.345 1.124M12 3v3m0 12v3m7.071-16.071l-2.121 2.121M7.05 16.95l-2.121 2.121M21 12h-3M6 12H3m16.071 7.071l-2.121-2.121M7.05 7.05L4.929 4.929',
  },
  {
    title: '清晰度选择',
    desc: '解析后直接选择格式与清晰度，下载按钮和当前选择保持在同一区域。',
    icon: 'M4 6h16M4 12h16M4 18h16M8 6v12m8-12v12',
  },
  {
    title: '字幕提取',
    desc: '自动提取可用字幕，支持复制、查看和导出，方便二次整理。',
    icon: 'M7 8h10M7 12h6m-6 4h10M5 4h14a2 2 0 012 2v12a2 2 0 01-2 2H5a2 2 0 01-2-2V6a2 2 0 012-2z',
  },
  {
    title: 'AI 内容总结',
    desc: '生成摘要、要点和思维导图，长视频也能快速抓住结构。',
    icon: 'M9 12h6m-3-3v6m8-3a8 8 0 11-16 0 8 8 0 0116 0z',
  },
  {
    title: '围绕视频问答',
    desc: '基于字幕上下文继续追问，适合学习、复盘和内容提炼。',
    icon: 'M8 10h8M8 14h5m8-2a9 9 0 11-4.219-7.626L21 4l-1.374 4.219A8.963 8.963 0 0121 12z',
  },
]
</script>
