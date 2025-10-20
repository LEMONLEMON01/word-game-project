class ConnectionsGame {
    constructor() {
        this.selectedWords = [];
        this.mistakes = 0;
        this.maxMistakes = 4;
        this.gameId = document.querySelector('input[name="game_id"]')?.value || 'default';

        this.initializeEventListeners();
        this.updateGameStatus();
    }

    initializeEventListeners() {
        // Выбор слов
        document.querySelectorAll('.word-card').forEach(card => {
            card.addEventListener('click', () => this.toggleWord(card));
        });

        // Кнопки управления
        document.getElementById('submitBtn').addEventListener('click', () => this.submitSelection());
        document.getElementById('deselectBtn').addEventListener('click', () => this.deselectAll());
        document.getElementById('newGameBtn').addEventListener('click', () => this.newGame());
    }

    toggleWord(card) {
        if (card.classList.contains('used')) return;

        const word = card.dataset.word;

        if (this.selectedWords.includes(word)) {
            // Убираем из выбора
            this.selectedWords = this.selectedWords.filter(w => w !== word);
            card.classList.remove('selected');
        } else {
            // Добавляем в выбор
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
        submitBtn.textContent = `Проверить выбор (${this.selectedWords.length}/4)`;
    }

    async submitSelection() {
        if (this.selectedWords.length !== 4) return;

        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('game_id', this.gameId);
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
        this.showMessage(`Правильно! "${result.category_name}" - ${result.description}`, 'success');

        // Помечаем слова как использованные
        this.selectedWords.forEach(word => {
            const card = document.querySelector(`.word-card[data-word="${word}"]`);
            if (card) {
                card.classList.add('used');
                card.classList.remove('selected');
            }
        });

        // Добавляем найденную категорию
        this.addFoundCategory(result.category_name, this.selectedWords);

        // Проверяем завершение игры
        if (result.game_complete) {
            setTimeout(() => {
                this.showMessage('🎉 Поздравляем! Вы нашли все категории!', 'success');
            }, 1000);
        }

        this.updateGameStatus();
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
    }

    updateMistakesDisplay() {
        const mistakes = document.querySelectorAll('.mistake');
        mistakes.forEach((mistake, index) => {
            if (index < this.mistakes) {
                mistake.classList.add('used');
            }
        });
    }

    addFoundCategory(categoryName, words) {
        const colors = ['yellow', 'green', 'blue', 'purple'];
        const foundCategories = document.getElementById('foundCategories');

        const categoryDiv = document.createElement('div');
        categoryDiv.className = `category-group ${colors[foundCategories.children.length % colors.length]}`;
        categoryDiv.innerHTML = `
            <strong>${categoryName}</strong>: ${words.join(', ')}
        `;

        foundCategories.appendChild(categoryDiv);
    }

    deselectAll() {
        this.selectedWords = [];
        document.querySelectorAll('.word-card.selected').forEach(card => {
            card.classList.remove('selected');
        });
        this.updateSubmitButton();
    }

    async newGame() {
        try {
            const response = await fetch('/new_game', {
                method: 'POST'
            });

            const result = await response.json();

            // Обновляем игровое поле
            this.gameId = result.game_id;
            this.selectedWords = [];
            this.mistakes = 0;

            const wordsGrid = document.getElementById('wordsGrid');
            wordsGrid.innerHTML = '';

            result.words.forEach(word => {
                const card = document.createElement('div');
                card.className = 'word-card';
                card.dataset.word = word;
                card.textContent = word;
                card.addEventListener('click', () => this.toggleWord(card));
                wordsGrid.appendChild(card);
            });

            // Сбрасываем интерфейс
            document.getElementById('foundCategories').innerHTML = '';
            document.querySelectorAll('.mistake').forEach(mistake => {
                mistake.classList.remove('used');
            });
            this.updateSubmitButton();
            this.hideMessage();

        } catch (error) {
            this.showMessage('Ошибка при создании новой игры', 'error');
        }
    }

    async updateGameStatus() {
        try {
            const response = await fetch(`/game_status/${this.gameId}`);
            const status = await response.json();

            if (status.error) {
                console.error('Ошибка получения статуса:', status.error);
            }
        } catch (error) {
            console.error('Ошибка обновления статуса:', error);
        }
    }

    showMessage(text, type) {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
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

// Инициализация игры при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new ConnectionsGame();
});