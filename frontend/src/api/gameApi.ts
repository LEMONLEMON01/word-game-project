import axios from 'axios'
import type { CheckSelectionResponse, DailyInfo } from '../types/game'

// Use absolute path for production
const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

export const gameApi = {
  async getGame() {
    const response = await api.get('/game')
    return response.data
  },

  async checkSelection(selectedWords: string[]): Promise<CheckSelectionResponse> {
    const response = await api.post('/check_selection', selectedWords)
    return response.data
  },

  async getGameStatus() {
    const response = await api.get('/game_status')
    return response.data
  },

  async getDailyInfo(): Promise<DailyInfo> {
    const response = await api.get('/daily_info')
    return response.data
  }
}