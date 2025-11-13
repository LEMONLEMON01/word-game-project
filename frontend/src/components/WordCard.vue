<template>
  <div 
    class="word-card grid-item"
    :class="{
      'selected': selected,
      'scramble-animation': scrambleAnimation
    }"
    @click="$emit('click', word)"
  >
    {{ word }}
  </div>
</template>

<script setup lang="ts">
interface Props {
  word: string
  selected?: boolean
  scrambleAnimation?: boolean
}

interface Emits {
  (e: 'click', word: string): void
}

defineProps<Props>()
defineEmits<Emits>()
</script>

<style scoped>
.word-card {
  padding: 20px 10px;
  text-align: center;
  background: #d3fbe3;
  border: 2px solid #c3ebd3;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  user-select: none;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1em;
}

.word-card:hover {
  background: #a1eec0;
  border-color: #91dea0;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.word-card.selected {
  background: #88c8a1;
  border-color: #78b891;
  color: white;
  transform: scale(1.05);
}

.scramble-animation {
  animation: scramble 0.3s ease-in-out;
}

@keyframes scramble {
  0% { transform: translateX(0) rotate(0deg); }
  25% { transform: translateX(-5px) rotate(-2deg); }
  50% { transform: translateX(5px) rotate(2deg); }
  75% { transform: translateX(-3px) rotate(-1deg); }
  100% { transform: translateX(0) rotate(0deg); }
}

@media (max-width: 768px) {
  .word-card {
    padding: 15px 8px;
    font-size: 0.9em;
  }
}
</style>