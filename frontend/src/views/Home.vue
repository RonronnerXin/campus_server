<template>
  <div id="app">
    <Header />
    <main class="main-content">
      <Sidebar />
      <div class="content-area">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import Header from '../components/Header.vue'
import Sidebar from '../components/Sidebar.vue'
</script>

<style>
#app {
  min-height: 100vh;
}

.main-content {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.content-area {
  width: 100%;
}

@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 16px;
  }
}
</style>