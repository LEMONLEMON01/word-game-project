import axios from 'axios'
import type { CheckSelectionResponse, DailyInfo } from '../types/game'

// Use relative URL for production
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
    try {
      const response = await api.get('/game')
      return response.data
    } catch (error) {
      console.error('Failed to fetch game:', error)
      throw error
    }
  },

  async checkSelection(selectedWords: string[]): Promise<CheckSelectionResponse> {
    try {
      const response = await api.post('/check_selection', selectedWords)
      return response.data
    } catch (error: any) {
      console.error('Selection error:', error)
      throw error
    }
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