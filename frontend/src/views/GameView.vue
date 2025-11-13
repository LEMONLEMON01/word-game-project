<template>
  <div>
    <GameHeader :daily-display="gameStore.dailyDisplay" />
    
    <div class="container">
      <div class="game-screen">
        <!-- Show loading state -->
        <div v-if="gameStore.loading" class="loading">
          Загрузка игры...
        </div>
        
        <!-- Show message if no words -->
        <div v-else-if="gameStore.words.length === 0" class="no-words">
          Не удалось загрузить слова. Проверьте консоль для ошибок.
        </div>
        
        <!-- Show game content when loaded -->
        <div v-else>
          <!-- Found Categories Section - ABOVE the word grid -->
          <div v-if="gameStore.foundCategories.length > 0" class="found-categories-section">
            <h4>Найденные категории:</h4>
            <div class="found-categories-grid">
              <CategoryBlock
                v-for="(category, index) in gameStore.foundCategories"
                :key="'category-' + index"
                :name="category.name"
                :words="category.words"
                :color="gameStore.getCategoryColor(index)"
              />
            </div>
          </div>

          <!-- Word Cards Grid -->
          <div class="words-grid">
            <WordCard
              v-for="(word, index) in gameStore.words"
              :key="'word-' + index"
              :word="word"
              :selected="gameStore.selectedWords.includes(word)"
              :scramble-animation="gameStore.scrambleAnimation"
              @click="gameStore.toggleWord(word)"
            />
          </div>
        </div>
      </div>
      
      <div class="game-info">
        <div class="mistakes">
          Осталось ошибок: 
          <span 
            v-for="n in 4" 
            :key="n"
            class="mistake"
            :class="{ 'used': gameStore.mistakes >= n }"
          >●</span>
        </div>
      </div>
      
      <GameControls
        :can-submit="gameStore.selectedWords.length === 4 && !gameStore.gameOver"
        :game-over="gameStore.gameOver"
        @deselect-all="gameStore.deselectAll"
        @shuffle-words="gameStore.shuffleWords"
        @submit-guess="gameStore.submitGuess"
      />

      <MessageAlert
        :show="gameStore.showMessage"
        :text="gameStore.messageText"
        :type="gameStore.messageClass"
      />
    </div>

    <section class="section">
      <div class="spellbee-container">
        <div class="text-center">
          <h3 class="text-center">Как играть в ТылМус</h3>
          <ul class="list-unstyled">
            <li>
              <h4>Прочти слова</h4>
              <span>Первый шаг — внимательно прочитать и понять слова, представленные в игре "ТылМус". Не спешите, постарайтесь понять каждое слово и подумать, что оно означает в контексте головоломки.</span><br>
              <div class="image">
                <img class="adaptive-image" src="/img/step1.png" alt="Прочти слова" title="Прочти слова">
              </div>
            </li>
            <li>
              <h4>Найди общее</h4>
              <span>После того как вы прочитаете и поймёте слова, следующий шаг — найти общую тему, которая их связывает.</span><br>
              <div class="image">
                <img class="adaptive-image" src="/img/step2.png" alt="Найди общее" title="Найди общее">
              </div>
            </li>
            <li>
              <h4>Выбери и отправь свой ответ</h4>
              <span>Когда вы определите общую тему и найдёте четыре слова, подходящие под неё, пора сделать свой выбор.</span><br>
              <div class="image">
                <img class="adaptive-image" src="/img/step3.png" alt="Выбери и отправь свой ответ" title="Выбери и отправь свой ответ">
              </div>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <footer class="bg-light py-4 mt-5">
      <div class="container text-center">
        <p class="mb-0">@LemonLemon Ltd | ТылМус | Связать слова</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useGameStore } from '../stores/gameStore'
import GameHeader from '../components/GameHeader.vue'
import WordCard from '../components/WordCard.vue'
import CategoryBlock from '../components/CategoryBlock.vue'
import GameControls from '../components/GameControls.vue'
import MessageAlert from '../components/MessageAlert.vue'

const gameStore = useGameStore()

onMounted(() => {
  console.log('🎮 GameView mounted, initializing game...')
  gameStore.initializeGame().then(() => {
    console.log('✅ Game initialization complete')
    console.log('📝 Words after init:', gameStore.words)
  }).catch(error => {
    console.error('❌ Game initialization failed:', error)
  })
})
</script>

<style scoped>
.game-screen {
  width: 45%;
  margin: auto;
}

.found-categories-section {
  margin-bottom: 30px;
}

.found-categories-section h4 {
  text-align: center;
  margin-bottom: 15px;
  color: #333;
  font-weight: 600;
}

.found-categories-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.words-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
  min-height: 400px;
}

.grid-item {
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.game-info {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
}

.mistakes {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
}

.mistake {
  color: #28a745;
  font-size: 1.5em;
}

.mistake.used {
  color: #dc3545;
  opacity: 0.5;
}

.section {
  margin-top: 50px;
  padding: 30px 0;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #666;
}

.no-words {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #ff0000;
  background: #ffe6e6;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .words-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .game-screen {
    width: 90%;
  }
  
  .found-categories-grid {
    gap: 8px;
  }
}
</style>