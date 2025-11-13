import axios from 'axios'
import type { CheckSelectionResponse, DailyInfo } from '../types/game'

// Use relative URL for production - will work with the same domain
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
    console.log('🚀 Fetching game from:', `${API_BASE_URL}/game`)
    try {
      const response = await api.get('/game')
      console.log('✅ Game data received:', response.data)
      return response.data
    } catch (error) {
      console.error('❌ Failed to fetch game:', error)
      throw error
    }
  },

  async checkSelection(selectedWords: string[]): Promise<CheckSelectionResponse> {
    console.log('📤 Submitting selection:', selectedWords)
    try {
      const response = await api.post('/check_selection', selectedWords)
      console.log('✅ Selection response:', response.data)
      return response.data
    } catch (error: any) {
      console.error('❌ Selection error details:', error)
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