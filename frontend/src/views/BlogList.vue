<template>
  <div class="blog-list">
    <div 
      v-for="blog in blogs" 
      :key="blog.id" 
      class="blog-item"
      @click="viewBlogDetail(blog.id)"
    >
      <!-- 博客内容... -->
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const viewBlogDetail = (id) => {
  router.push(`/blog/${id}`)
}
</script>

<style scoped>
.blog-item {
  cursor: pointer;
  /* ...其他样式... */
}

.blog-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}
</style>