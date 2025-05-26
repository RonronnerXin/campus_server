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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #fafbfc;
  color: #1a1a1a;
  line-height: 1.6;
}
</style>