<template>
  <router-view />
</template>

<script>
export default {
  methods: {
    handleSelect(path) {
      this.$router.push(path)
    }
  }
}
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  height: 100%;  /* 添加这行 */
  width: 100%;   /* 添加这行 */
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #fafbfc;
  color: #1a1a1a;
  line-height: 1.6;
}

#app {
  min-height: 100vh;  /* 使用视口高度 */
  width: 100%;      /* 确保宽度100% */
  margin: 0;        /* 移除外边距 */
  padding: 0;       /* 移除内边距 */
}
</style>