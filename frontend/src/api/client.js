import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const api = {
  // Health check
  checkHealth: () => apiClient.get('/health'),

  // Job operations
  uploadJob: (file, roleTitle) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('role_title', roleTitle)
    return apiClient.post('/jobs/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // Candidate operations
  uploadCandidates: (files) => {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    return apiClient.post('/candidates/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // Evaluation operations
  evaluateCandidates: (jobId, candidateIds = null) => 
    apiClient.post('/evaluate', { job_id: jobId, candidate_ids: candidateIds }),

  getRankings: (jobId) => apiClient.get(`/rankings/${jobId}`),

  overrideScore: (evaluationId, reviewer, newScore, reason) =>
    apiClient.post('/override', {
      evaluation_id: evaluationId,
      reviewer,
      new_score: newScore,
      reason
    })
}

export default api
