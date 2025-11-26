<template>
  <div class="app-container">
    <!-- Success/Error Popup Message (Top Notification) -->
    <div v-if="gameStore.showMessage && !gameStore.gameOver" class="notification-popup" :class="gameStore.messageClass">
      <div class="notification-content">
        <p>{{ gameStore.messageText }}</p>
        <button class="notification-close" @click="closePopup">×</button>
      </div>
    </div>

    <!-- Game Over Popup (Top Notification) -->
    <div v-if="gameStore.gameOver" class="notification-popup game-over-notification">
      <div class="notification-content">
        <p>Игра окончена! Слишком много ошибок. Попробуйте снова завтра!</p>
        <button class="notification-close" @click="closeGameOver">×</button>
      </div>
    </div>
    <!-- Unified Background -->
    <div class="background-ornament">
      <img 
        src="/public/imgg/background-ornament.svg" 
        alt="Background ornament" 
        @load="handleSvgLoad('background')"
        @error="handleSvgError('background')"
      />
    </div>
    <!-- Unified Background -->
    <div class="background-ornament2">
      <img 
        src="/public/imgg/background-ornament.svg" 
        alt="Background ornament" 
        @load="handleSvgLoad('background')"
        @error="handleSvgError('background')"
      />
    </div>
    <GameHeader :daily-display="gameStore.dailyDisplay" />
    
    <div class="game-screen">
        

    <div class="container">
        <!-- Show loading state -->
        <div v-if="gameStore.loading" class="loading">
          Загрузка игры...
        </div>
        
        <!-- Show game completion message when all words are found -->
        <div v-else-if="gameStore.words.length === 0 && gameStore.foundCategories.length === 4" class="game-complete">
          <div class="completion-message">
            🎉 Поздравляем! Вы нашли все категории!
          </div>
          
          <!-- Show all found categories when game is complete -->
          <div class="categories-complete">
            <CategoryBlock
              v-for="(category, index) in gameStore.foundCategories"
              :key="'category-' + index"
              :name="category.name"
              :words="category.words"
              :color="gameStore.getCategoryColor(index)"
            />
          </div>
        </div>
        
        <!-- Show error message if no words but game not completed -->
        <div v-else-if="gameStore.words.length === 0" class="no-words">
          Не удалось загрузить слова. Проверьте консоль для ошибок.
        </div>
        
        <!-- Show game content when loaded and words available -->
        <div v-else class="combined-grid">
          <!-- Category Blocks for found categories -->
          <CategoryBlock
            v-for="(category, index) in gameStore.foundCategories"
            :key="'category-' + index"
            :name="category.name"
            :words="category.words"
            :color="gameStore.getCategoryColor(index)"
          />
          
          <!-- Word Cards for remaining words -->
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
      
      <div class="game-info">
        <div class="mistakes">
          Осталось ошибок: 
          <span 
            v-for="n in 4" 
            :key="n"
            class="mistake"
            :class="{ 'used': (5 - n) <= gameStore.mistakes }"
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
    </div>

    <section class="section instructions-section">
      

      <div class="spellbee-container">
        <div class="text-center ">
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

      <!-- Corner SVGs -->
      <div class="corner corner-top-left">
        <img 
          src="/public/imgg/corner-top-left.svg" 
          alt="Decorative corner" 
          @load="handleSvgLoad('top-left')"
          @error="handleSvgError('top-left')"
        />
        
      </div>
      <div class="corner corner-top-right">
        <img 
          src="/public/imgg/corner-top-right.svg" 
          alt="Decorative corner" 
          @load="handleSvgLoad('top-right')"
          @error="handleSvgError('top-right')"
        />
      </div>
      <div class="corner corner-bottom-left">
        <img 
          src="/public/imgg/corner-bottom-left.svg" 
          alt="Decorative corner" 
          @load="handleSvgLoad('bottom-left')"
          @error="handleSvgError('bottom-left')"
        />
      </div>
      <div class="corner corner-bottom-right ">
        <img 
          src="/public/imgg/corner-bottom-right.svg" 
          alt="Decorative corner" 
          @load="handleSvgLoad('bottom-right')"
          @error="handleSvgError('bottom-right')"
        />
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
import { onMounted, ref } from 'vue'
import { useGameStore } from '../stores/gameStore'
import GameHeader from '../components/GameHeader.vue'
import WordCard from '../components/WordCard.vue'
import CategoryBlock from '../components/CategoryBlock.vue'
import GameControls from '../components/GameControls.vue'

const gameStore = useGameStore()

// Track SVG loading state for each corner
const svgLoaded = ref({
  background: false,
  topLeft: false,
  topRight: false,
  bottomLeft: false,
  bottomRight: false
})

const handleSvgLoad = (type: string) => {
  console.log(`✅ SVG loaded: ${type}`)
  svgLoaded.value[type as keyof typeof svgLoaded.value] = true
}

const handleSvgError = (type: string) => {
  console.error(`❌ SVG failed to load: ${type}`)
  svgLoaded.value[type as keyof typeof svgLoaded.value] = false
}

const closePopup = () => {
  gameStore.showMessage = false
}

const closeGameOver = () => {
  // Game over popup can't be closed for now
}

onMounted(() => {
  console.log('🎮 GameView mounted, initializing game...')
  gameStore.initializeGame().then(() => {
    console.log('✅ Game initialization complete')
    console.log('📝 Words after init:', gameStore.words)
    console.log('🏆 Game status:', gameStore.gameStatus)
    console.log('🎯 Found categories:', gameStore.foundCategories.length)
    console.log('❌ Game over:', gameStore.gameOver)
  }).catch(error => {
    console.error('❌ Game initialization failed:', error)
  })
})
</script>

<style scoped>
.app-container {
  position: relative;
  min-height: 100vh;
}

/* Updated Notification Popup Styles - Smaller and Rounded */
.notification-popup {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 12px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  animation: slideDown 0.3s ease;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  border: 2px solid transparent;
}

.notification-popup.success {
  border-color: #28a745;
  background: #f8fff9;
}

.notification-popup.error {
  border-color: #dc3545;
  background: #fff8f8;
}

.game-over-notification {
  border-color: #dc3545;
  background: #fff8f8;
}

.notification-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.notification-content p {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  line-height: 1.4;
  flex: 1;
}

.notification-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #666;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
  flex-shrink: 0;
}

.notification-close:hover {
  background: #f5f5f5;
}

@keyframes slideDown {
  from { 
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to { 
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Game Screen with Background */
.game-screen {
  width: 45%;
  margin: auto;
  position: relative;
  min-height: 500px;
}

.background-ornament {
  position: absolute;
  top: 4%;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  width: 100%;
  height: 2%;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
}
.background-ornament2 {
  position: absolute;
  top: 22%;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  width: 100%;
  height: 2%;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: scaleY(-1);
}

/* Instructions Section with Corners */
.instructions-section {
  position: relative;
  background: #f8f9fa;
  border-radius: 12px;
  margin-top: 50px;
  padding: 60px 30px;
  overflow: hidden;
}

.corner {
  position: absolute;
  width: 25%;
  height: 25%;
  pointer-events: none;
  z-index: 1;
}

.corner img,
.corner .fallback-svg {
  width: 100%;
  height: 100%;
  opacity: 0.8;
  object-fit: contain;
}

.corner-top-left {
  top: 0;
  left: 0;
}

.corner-top-right {
  top: 0;
  right: 0;
}

.corner-bottom-left {
  bottom: 0;
  left: 0;
}

.corner-bottom-right {
  bottom: 0;
  right: 0;
}
.spellbee-container {
  z-index: 1;
}

/* Mistakes - Right to Left counting */
.mistakes {
  display: flex;
  align-items: center;
  gap: 5px;
}

.mistake {
  color: gray;
  font-size: 1.5em;
  transition: all 0.3s ease;
}

.mistake.used {
  opacity: 0.3;
}

/* Rest of your existing styles */
.combined-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 10px;
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

.game-complete {
  text-align: center;
}

.completion-message {
  font-size: 24px;
  font-weight: bold;
  color: #2e7d32;
  margin-bottom: 30px;
  padding: 20px;
  background: #e8f5e9;
  border-radius: 8px;
}

.categories-complete {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 600px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .combined-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .game-screen {
    width: 90%;
  }
  
  .categories-complete {
    max-width: 100%;
  }
  
  
  .instructions-section {
    padding: 40px 20px;
  }
  
  .notification-popup {
    max-width: 350px;
    padding: 10px 16px;
  }
  
  .notification-content p {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .notification-popup {
    max-width: 300px;
    top: 10px;
  }
}
</style>