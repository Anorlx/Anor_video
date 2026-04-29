<template>
  <footer class="bg-ink border-t border-ink py-8 text-primary-light">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <!-- 底部关键词友好描述 -->
      <div class="text-center mb-6">
        <p class="text-sm text-primary-light/75 leading-relaxed max-w-3xl mx-auto">
          <strong>Agent_video</strong> — AI 视频工作台，支持
          <a href="#features" class="text-primary-light hover:underline" title="YouTube视频下载">YouTube</a>、
          <a href="#features" class="text-primary-light hover:underline" title="Bilibili视频下载">Bilibili</a>、
          <a href="#features" class="text-primary-light hover:underline" title="抖音视频下载">抖音</a>、
          <a href="#features" class="text-primary-light hover:underline" title="TikTok视频下载">TikTok</a>
          等 1800+ 平台视频下载。提供
          <a href="#features" class="text-primary-light hover:underline" title="AI视频总结功能">AI 视频总结</a>、思维导图生成、字幕下载等智能功能。
        </p>
      </div>
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <a href="/" class="flex items-center gap-2" title="Agent_video 首页">
          <div class="w-7 h-7 rounded-md bg-primary-light/10 flex items-center justify-center">
            <svg class="w-4 h-4 text-primary-light" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <span class="text-sm font-medium text-primary-light">Agent_video</span>
        </a>
        <p class="text-xs text-primary-light/55 text-center leading-relaxed">
          本工具仅供学习交流使用，请尊重视频版权，勿用于商业用途。下载内容的版权归原作者所有。
        </p>
        <p class="text-xs text-primary-light/55">
          &copy; {{ new Date().getFullYear() }} Agent_video
        </p>
      </div>
    </div>
  </footer>
</template>
