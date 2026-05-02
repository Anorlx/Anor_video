<template>
  <header
    class="sticky top-0 z-50 bg-surface/90 backdrop-blur-xl border-b border-border-light"
  >
    <div
      class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between"
    >
      <a
        href="/"
        class="flex items-center gap-3 group"
        title="Agent_video - AI 视频工作台"
      >
        <div
          class="w-9 h-9 rounded-lg bg-ink flex items-center justify-center shadow-sm transition-transform group-hover:scale-[1.03]"
          role="img"
          aria-label="Agent_video Logo"
        >
          <svg
            class="w-5 h-5 text-primary-light"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <div class="leading-tight">
          <span
            class="block text-lg font-semibold text-text-primary tracking-tight"
            >Agent_video</span
          >
          <span class="hidden sm:block text-[11px] text-text-muted"
            >AI 视频工作台</span
          >
        </div>
      </a>
      <nav
        class="hidden md:flex items-center gap-1 text-sm text-text-secondary rounded-lg border border-border-light bg-surface-muted p-1"
        aria-label="主导航"
      >
        <a
          href="#features"
          class="px-3 py-1.5 rounded-md hover:bg-surface hover:text-primary transition-colors"
          title="查看Agent_video功能特性"
          >能力</a
        >
        <a
          href="#how-to-use"
          class="px-3 py-1.5 rounded-md hover:bg-surface hover:text-primary transition-colors"
          title="了解如何使用Agent_video处理视频"
          >流程</a
        >
        <a
          href="#comparison"
          class="px-3 py-1.5 rounded-md hover:bg-surface hover:text-primary transition-colors"
          title="Agent_video与其他工具对比"
          >对比</a
        >
      </nav>
      <div class="flex items-center gap-3">
        <!-- 未登录 -->
        <template v-if="!user">
          <button
            @click="$emit('login')"
            class="hidden sm:inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium text-text-secondary hover:text-primary hover:bg-primary-light/50 transition-colors cursor-pointer"
          >
            登录
          </button>
          <button
            @click="$emit('register')"
            class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium text-white bg-primary hover:bg-primary-dark transition-colors shadow-sm cursor-pointer"
          >
            免费注册
          </button>
        </template>

        <!-- 已登录 -->
        <template v-else>
          <!-- 用户下拉菜单 -->
          <div class="relative" ref="menuRef">
            <button
              @click="menuOpen = !menuOpen"
              class="flex items-center gap-2 px-2.5 py-2 rounded-lg hover:bg-primary-light/50 transition-colors cursor-pointer"
            >
              <div
                class="w-8 h-8 rounded-lg bg-ink flex items-center justify-center text-primary-light text-sm font-semibold"
              >
                {{ user.email[0].toUpperCase() }}
              </div>
              <svg
                class="w-4 h-4 text-text-muted transition-transform"
                :class="{ 'rotate-180': menuOpen }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            <div
              v-if="menuOpen"
              class="absolute right-0 top-full mt-2 w-56 bg-surface rounded-lg border border-border shadow-xl py-2 animate-menu-in"
            >
              <div class="px-4 py-2 border-b border-border">
                <p class="text-sm font-medium text-text-primary truncate">
                  {{ user.email }}
                </p>
                <p class="text-xs text-text-muted mt-0.5">已登录</p>
              </div>
              <button
                data-testid="open-history"
                @click="
                  menuOpen = false;
                  $emit('open-history');
                "
                class="w-full text-left px-4 py-2.5 text-sm text-text-secondary hover:bg-surface-muted transition-colors cursor-pointer flex items-center gap-2"
              >
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                历史记录
              </button>
              <button
                @click="
                  menuOpen = false;
                  $emit('logout');
                "
                class="w-full text-left px-4 py-2.5 text-sm text-text-secondary hover:bg-surface-muted transition-colors cursor-pointer flex items-center gap-2"
              >
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                  />
                </svg>
                退出登录
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

defineProps({
  user: { type: Object, default: null },
});

defineEmits(["login", "register", "logout", "open-history"]);

const menuOpen = ref(false);
const menuRef = ref(null);

function handleClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    menuOpen.value = false;
  }
}

onMounted(() => document.addEventListener("click", handleClickOutside));
onBeforeUnmount(() =>
  document.removeEventListener("click", handleClickOutside)
);
</script>

<style scoped>
@keyframes menu-in {
  from {
    opacity: 0;
    transform: translateY(-4px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
.animate-menu-in {
  animation: menu-in 0.15s ease-out;
}
</style>
