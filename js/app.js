const { createApp, ref, computed, onMounted } = Vue;

createApp({
    setup() {
        // Reactive state
        const words = ref([]);
        const selectedWords = ref([]);
        const foundCategories = ref([]);
        const mistakes = ref(0);
        const gameOver = ref(false);
        const scrambleAnimation = ref(false);
        const showMessage = ref(false);
        const messageText = ref('');
        const messageClass = ref('');
        const loading = ref(false);

        // Computed properties
        const gameStatus = computed(() => {
            if (gameOver.value) return 'game-over';
            if (foundCategories.value.length === 4) return 'won';
            return 'playing';
        });

        // Methods
        const initializeGame = async () => {
            loading.value = true;
            try {
                const response = await fetch('/api/game');
                const data = await response.json();
                
                words.value = data.words;
                resetGameState();
            } catch (error) {
                console.error('Error initializing game:', error);
                showMessage.value = true;
                messageText.value = 'Ошибка загрузки игры';
                messageClass.value = 'error';
            } finally {
                loading.value = false;
            }
        };

        const resetGameState = () => {
            selectedWords.value = [];
            foundCategories.value = [];
            mistakes.value = 0;
            gameOver.value = false;
            showMessage.value = false;
        };

        const toggleWord = (word) => {
            if (gameOver.value) return;
            
            const index = selectedWords.value.indexOf(word);
            if (index > -1) {
                selectedWords.value.splice(index, 1);
            } else if (selectedWords.value.length < 4) {
                selectedWords.value.push(word);
            }
        };

        const deselectAll = () => {
            selectedWords.value = [];
        };

        const shuffleWords = () => {
            scrambleAnimation.value = true;
            
            // Fisher-Yates shuffle
            const shuffled = [...words.value];
            for (let i = shuffled.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }
            words.value = shuffled;
            
            setTimeout(() => {
                scrambleAnimation.value = false;
            }, 300);
        };

        const submitGuess = async () => {
            if (selectedWords.value.length !== 4) return;
            
            loading.value = true;
            try {
                const response = await fetch('/api/check_selection', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        selected_words: selectedWords.value
                    })
                });

                const result = await response.json();

                if (result.valid) {
                    handleSuccess(result);
                } else {
                    handleMistake(result.message);
                }
            } catch (error) {
                showMessage.value = true;
                messageText.value = 'Ошибка соединения';
                messageClass.value = 'error';
            } finally {
                loading.value = false;
            }
        };

        const handleSuccess = (result) => {
            showMessage.value = true;
            messageText.value = `Правильно! "${result.category_name}"`;
            messageClass.value = 'success';

            // Add to found categories
            foundCategories.value.push({
                name: result.category_name,
                words: [...selectedWords.value]
            });

            // Remove words from the grid
            words.value = words.value.filter(word => !selectedWords.value.includes(word));
            selectedWords.value = [];

            if (result.game_complete) {
                gameOver.value = true;
                setTimeout(() => {
                    showMessage.value = true;
                    messageText.value = 'Поздравляем! Вы нашли все категории!';
                    messageClass.value = 'success';
                }, 1000);
            }

            setTimeout(() => {
                showMessage.value = false;
            }, 3000);
        };

        const handleMistake = (message) => {
            mistakes.value++;
            showMessage.value = true;
            messageText.value = message || 'Неправильно! Попробуйте еще раз.';
            messageClass.value = 'error';
            selectedWords.value = [];

            if (mistakes.value >= 4) {
                gameOver.value = true;
                setTimeout(() => {
                    showMessage.value = true;
                    messageText.value = 'Игра окончена! Слишком много ошибок.';
                    messageClass.value = 'error';
                }, 1000);
            }

            setTimeout(() => {
                showMessage.value = false;
            }, 3000);
        };

        const getCategoryColor = (index) => {
            const colors = ['yellow', 'green', 'blue', 'purple'];
            return colors[index % colors.length];
        };

        const newGame = async () => {
            try {
                const response = await fetch('/api/new_game', {
                    method: 'POST'
                });
                const data = await response.json();
                words.value = data.words;
                resetGameState();
            } catch (error) {
                console.error('Error starting new game:', error);
            }
        };

        // Lifecycle
        onMounted(() => {
            initializeGame();
        });

        return {
            words,
            selectedWords,
            foundCategories,
            mistakes,
            gameOver,
            scrambleAnimation,
            showMessage,
            messageText,
            messageClass,
            gameStatus,
            toggleWord,
            deselectAll,
            shuffleWords,
            submitGuess,
            getCategoryColor,
            newGame
        };
    }
}).mount('#app');