<template>
  <div class="category-block" :class="color">
    <div class="category-content">
      <strong class="category-name">{{ name }}</strong>
      <div class="category-words">{{ words.join(', ') }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  name: string
  words: string[]
  color: string
}

defineProps<Props>()
</script>

<style scoped>
.category-block {
  padding: 15px 20px;
  border-radius: 8px;
  color: #333;
  font-weight: bold;
  text-align: center;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.5s ease-in;
  border: 2px solid transparent;
}

.category-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.category-name {
  font-size: 1.1em;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.category-words {
  font-size: 0.9em;
  opacity: 0.8;
  font-weight: normal;
}

.category-block.yellow { 
  background: #ffcc95; 
  border-color: #e6b885;
}
.category-block.green { 
  background: #aef8cb; 
  border-color: #9de6b8;
}
.category-block.blue { 
  background: #b6ceff; 
  border-color: #a4bde6;
}
.category-block.purple { 
  background: #E0ceff; 
  border-color: #cebce6;
}

@keyframes fadeIn {
  from { 
    opacity: 0; 
    transform: translateY(-10px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}
</style>