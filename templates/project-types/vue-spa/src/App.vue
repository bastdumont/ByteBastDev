<template>
  <div id="app" :class="{ dark: isDark }">
    <header class="app-header">
      <nav class="container mx-auto flex items-center justify-between p-4">
        <router-link to="/" class="text-2xl font-bold">
          {{project_name}}
        </router-link>

        <div class="flex items-center gap-4">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/about" class="nav-link">About</router-link>
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>

          <button
            @click="toggleDark"
            class="rounded-lg p-2 hover:bg-gray-200 dark:hover:bg-gray-700"
          >
            {{ isDark ? '🌙' : '☀️' }}
          </button>
        </div>
      </nav>
    </header>

    <main class="flex-1">
      <router-view />
    </main>

    <footer class="bg-gray-100 py-8 dark:bg-gray-800">
      <div class="container mx-auto text-center text-gray-600 dark:text-gray-400">
        <p>© 2025 {{project_name}}. Built with Vue 3 + Vite.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)
</script>

<style>
@import './assets/main.css';

#app {
  @apply min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition-colors;
}

.app-header {
  @apply bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700;
}

.nav-link {
  @apply px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors;
}

.nav-link.router-link-active {
  @apply bg-blue-500 text-white hover:bg-blue-600 dark:hover:bg-blue-600;
}
</style>
