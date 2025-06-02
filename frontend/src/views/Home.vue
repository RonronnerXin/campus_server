<template>
    <Header />
    <main class="main-content">
      <Sidebar />
      <div class="content-area">
          <router-view />
      </div>
    </main>
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
  height: calc(100vh - 88px); /* Adjust for header height */
}

.content-area {
  width: 1000px;
}
.content-container {
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
  padding: 0 20px;
}


@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 16px;
  }
    .content-container {
    max-width: 100%;
    padding: 0 16px;
  }
}
</style>