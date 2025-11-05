class ConnectionsGame {
    constructor() {
        this.selectedWords = [];
        this.mistakes = 0;
        this.maxMistakes = 4;
        this.foundCategories = [];
        this.wordPositions = new Map();
        this.currentWords = [];

        this.initializeEventListeners();
        this.loadGameState();
        this.initializeWordPositions();
        this.updateGameStatus();
    }

    initializeWordPositions() {
        const wordCards = document.querySelectorAll('.word-card');
        wordCards.forEach((card, index) => {
            this.wordPositions.set(card.dataset.word, index);
        });
    }

    initializeEventListeners() {
        document.querySelectorAll('.word-card').forEach(card => {
            card.addEventListener('click', () => this.toggleWord(card));
        });

        document.getElementById('submitBtn').addEventListener('click', () => this.submitSelection());
        document.getElementById('deselectBtn').addEventListener('click', () => this.deselectAll());
        document.getElementById('shuffleBtn').addEventListener('click', () => this.shuffleWords());
    }

    toggleWord(card) {
        if (card.classList.contains('used')) return;

        const word = card.dataset.word;

        if (this.selectedWords.includes(word)) {
            this.selectedWords = this.selectedWords.filter(w => w !== word);
            card.classList.remove('selected');
        } else {
            if (this.selectedWords.length < 4) {
                this.selectedWords.push(word);
                card.classList.add('selected');
            }
        }

        this.updateSubmitButton();
    }

    updateSubmitButton() {
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = this.selectedWords.length !== 4;
    }

    async submitSelection() {
        if (this.selectedWords.length !== 4) return;

        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('selected_words', JSON.stringify(this.selectedWords));

            const response = await fetch('/check_selection', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.valid) {
                this.handleSuccess(result);
            } else {
                this.handleMistake(result.message);
            }

        } catch (error) {
            this.showMessage('Ошибка соединения', 'error');
        }

        this.deselectAll();
    }

    handleSuccess(result) {
        this.showMessage(`Правильно! "${result.category_name}"`, 'success');
        this.foundCategories.push({
            name: result.category_name,
            words: [...this.selectedWords]
        });

        this.replaceWordsWithCategory(result.category_name, this.selectedWords);

        if (result.game_complete) {
            setTimeout(() => {
                this.showMessage('Поздравляем! Вы нашли все категории!', 'success');
            }, 1000);
        }

        this.updateGameStatus();
        this.saveGameState();
    }

    replaceWordsWithCategory(categoryName, words) {
        const combinedGrid = document.getElementById('combinedGrid');
        const gridItems = Array.from(combinedGrid.querySelectorAll('.grid-item'));
        const wordPositions = words.map(word => {
            const index = Array.from(gridItems).findIndex(item =>
                item.classList.contains('word-card') && item.dataset.word === word
            );
            return index;
        }).filter(index => index !== -1).sort((a, b) => a - b);

        if (wordPositions.length !== 4) return;
        const firstPosition = wordPositions[0];
        const rowStart = Math.floor(firstPosition / 4) * 4;

        const categoryBlock = document.createElement('div');
        categoryBlock.className = `category-block grid-item ${this.getCategoryColor(this.foundCategories.length - 1)}`;
        categoryBlock.innerHTML = `
            <div class="category-content">
                <strong>${categoryName}</strong>
                <div class="category-words">${words.join(', ')}</div>
            </div>
        `;

        wordPositions.sort((a, b) => b - a).forEach(position => {
            gridItems[position].remove();
        });

        const rowItems = Array.from(combinedGrid.querySelectorAll('.grid-item'));
        const insertPosition = rowStart;

        if (rowItems[insertPosition]) {
            combinedGrid.insertBefore(categoryBlock, rowItems[insertPosition]);
        } else {
            combinedGrid.appendChild(categoryBlock);
        }
        this.updateGridLayout();
    }

    updateGridLayout() {
        const combinedGrid = document.getElementById('combinedGrid');
        const allItems = Array.from(combinedGrid.querySelectorAll('.grid-item'));
        const categoryBlocks = allItems.filter(item => item.classList.contains('category-block'));
        const wordCards = allItems.filter(item => item.classList.contains('word-card'));
        combinedGrid.innerHTML = '';
        categoryBlocks.forEach(block => {
            combinedGrid.appendChild(block);
        });

        wordCards.forEach(card => {
            combinedGrid.appendChild(card);
        });
    }

    getCategoryColor(categoryIndex) {
        const colors = ['yellow', 'green', 'blue', 'purple'];
        return colors[categoryIndex % colors.length];
    }

    handleMistake(message) {
        this.mistakes++;
        this.updateMistakesDisplay();
        this.showMessage(message, 'error');

        if (this.mistakes >= this.maxMistakes) {
            setTimeout(() => {
                this.showMessage('Игра окончена! Слишком много ошибок.', 'error');
                this.endGame();
            }, 1000);
        }
        this.updateGameStatus();
        this.saveGameState();
    }

    updateMistakesDisplay() {
        const mistakes = document.querySelectorAll('.mistake');
        mistakes.forEach((mistake, index) => {
            if (index < this.mistakes) {
                mistake.classList.add('used');
            }
        });
    }

    shuffleWords() {
        const combinedGrid = document.getElementById('combinedGrid');
        const wordCards = Array.from(combinedGrid.querySelectorAll('.word-card:not(.used)'));
        wordCards.forEach(card => {
            card.remove();
        });

        for (let i = wordCards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [wordCards[i], wordCards[j]] = [wordCards[j], wordCards[i]];
        }

        wordCards.forEach(card => {
            combinedGrid.appendChild(card);
            card.classList.add('scramble-animation');
            setTimeout(() => {
                card.classList.remove('scramble-animation');
            }, 300);
        });
    }

    deselectAll() {
        this.selectedWords = [];
        document.querySelectorAll('.word-card.selected').forEach(card => {
            card.classList.remove('selected');
        });
        this.updateSubmitButton();
        this.saveGameState();
    }

    async updateGameStatus() {
        try {
            const response = await fetch(`/game_status`);
            const status = await response.json();

            if (status.error) {
                console.error('Ошибка получения статуса:', status.error);
            }

            this.foundCategories = status.found_categories || [];
            this.updateProgress();
        } catch (error) {
            console.error('Ошибка обновления статуса:', error);
        }
    }

    async newGame() {
        try {
            const response = await fetch('/new_game', {
                method: 'POST'
            });
            const result = await response.json();

            if (result.words) {
                this.resetGame();
                this.updateGameBoard(result.words);
                this.saveGameState();
                this.showMessage('Новая игра начата!', 'success');
            }
        } catch (error) {
            console.error('Error starting new game:', error);
            this.showMessage('Ошибка при запуске новой игры', 'error');
        }
    }

    initializeWordCardListeners() {
        document.querySelectorAll('.word-card').forEach(card => {
            card.addEventListener('click', () => this.toggleWord(card));
        });
    }

    saveGameState() {
        const gameState = {
            selectedWords: this.selectedWords,
            mistakes: this.mistakes,
            foundCategories: this.foundCategories,
            currentWords: this.currentWords,
            words: Array.from(document.querySelectorAll('.word-card')).map(card => card.dataset.word)
        };
        localStorage.setItem('connectionsGameState', JSON.stringify(gameState));
    }

    async loadGameState() {
        const saved = localStorage.getItem('connectionsGame');

        if (saved) {
            try {
                const state = JSON.parse(saved);

                const isExpired = Date.now() - state.timestamp > 24 * 60 * 60 * 1000;

                if (!isExpired && state.currentWords && state.currentWords.length === 16) {
                    this.selectedWords = state.selectedWords || [];
                    this.mistakes = state.mistakes || 0;
                    this.foundCategories = state.foundCategories || [];
                    this.currentWords = state.currentWords;

                    this.restoreVisualState();

                    console.log('Игра восстановлена из сохранения');
                    return;
                }
            } catch (e) {
                console.error('Error loading saved game:', e);
            }
        }
        await this.loadNewGame();
    }

    restoreVisualState() {
        this.updateMistakesDisplay();

        this.updateProgress();

        this.restoreFoundCategories();

        this.restoreSelectedWords();
    }

    restoreFoundCategories() {
        this.foundCategories.forEach((category, index) => {
            this.replaceWordsWithCategory(category.name, category.words);
        });
    }

    restoreSelectedWords() {
        this.selectedWords.forEach(word => {
            const card = document.querySelector(`.word-card[data-word="${word}"]`);
            if (card && !card.classList.contains('used')) {
                card.classList.add('selected');
            }
        });
        this.updateSubmitButton();
    }

    clearSavedGame() {
        localStorage.removeItem('connectionsGameState');
    }

    showMessage(text, type) {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';

        setTimeout(() => {
            this.hideMessage();
        }, 3000);
    }

    hideMessage() {
        const messageDiv = document.getElementById('message');
        messageDiv.style.display = 'none';
        messageDiv.className = 'message';
    }

    updateProgress() {
        const foundCount = document.getElementById('foundCount');
        if (foundCount) {
            foundCount.textContent = this.foundCategories.length;
        }
    }

    showMessage(text, type) {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';

        setTimeout(() => {
            this.hideMessage();
        }, 3000);
    }

    hideMessage() {
        document.getElementById('message').style.display = 'none';
    }

    endGame() {
        document.querySelectorAll('.word-card').forEach(card => {
            card.classList.add('used');
        });
        document.getElementById('submitBtn').disabled = true;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ConnectionsGame();
});