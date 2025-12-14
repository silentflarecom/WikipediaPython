<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const emit = defineEmits(['view-task', 'close'])

const tasks = ref([])
const loading = ref(true)
const error = ref(null)
const deleteConfirm = ref(null)
const resetting = ref(false)
const resetConfirm = ref(false)
const statistics = ref(null)

const loadTasks = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get('http://localhost:8000/api/batch/tasks')
    tasks.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load tasks'
  } finally {
    loading.value = false
  }
}

const loadStatistics = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/corpus/statistics')
    statistics.value = response.data
  } catch (err) {
    console.error('Failed to load statistics:', err)
  }
}

const deleteTask = async (taskId) => {
  try {
    await axios.delete(`http://localhost:8000/api/batch/${taskId}`)
    deleteConfirm.value = null
    await loadTasks()
    await loadStatistics()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to delete task'
  }
}

const resetAllData = async () => {
  if (!resetConfirm.value) return
  
  resetting.value = true
  try {
    await axios.post('http://localhost:8000/api/system/reset?confirm=true')
    resetConfirm.value = false
    await loadTasks()
    await loadStatistics()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to reset database'
  } finally {
    resetting.value = false
  }
}

const downloadBackup = () => {
  window.open('http://localhost:8000/api/system/backup', '_blank')
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString()
}

const getStatusColor = (status) => {
  const colors = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'running': 'bg-blue-100 text-blue-800',
    'completed': 'bg-green-100 text-green-800',
    'failed': 'bg-red-100 text-red-800',
    'cancelled': 'bg-gray-100 text-gray-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

onMounted(() => {
  loadTasks()
  loadStatistics()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Statistics Panel -->
    <div v-if="statistics" class="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
      <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
        📊 Corpus Statistics
      </h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white/20 backdrop-blur rounded-lg p-4">
          <p class="text-sm text-white/80">Total Tasks</p>
          <p class="text-2xl font-bold">{{ statistics.total_tasks }}</p>
        </div>
        <div class="bg-white/20 backdrop-blur rounded-lg p-4">
          <p class="text-sm text-white/80">Completed Terms</p>
          <p class="text-2xl font-bold">{{ statistics.completed_terms }}</p>
        </div>
        <div class="bg-white/20 backdrop-blur rounded-lg p-4">
          <p class="text-sm text-white/80">Bilingual Pairs</p>
          <p class="text-2xl font-bold">{{ statistics.bilingual_pairs }}</p>
        </div>
        <div class="bg-white/20 backdrop-blur rounded-lg p-4">
          <p class="text-sm text-white/80">Database Size</p>
          <p class="text-2xl font-bold">{{ formatBytes(statistics.db_size_bytes) }}</p>
        </div>
      </div>
    </div>

    <!-- Task List -->
    <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      <div class="bg-gradient-to-r from-gray-700 to-gray-800 px-6 py-4 flex justify-between items-center">
        <div>
          <h2 class="text-xl font-bold text-white">📚 Task Manager</h2>
          <p class="text-gray-300 text-sm mt-1">Manage all batch crawling tasks</p>
        </div>
        <button
          @click="loadTasks"
          class="px-4 py-2 bg-white/20 text-white rounded-lg hover:bg-white/30 transition"
        >
          🔄 Refresh
        </button>
      </div>
      
      <!-- Loading -->
      <div v-if="loading" class="p-8 text-center">
        <div class="animate-spin inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
        <p class="mt-2 text-gray-500">Loading tasks...</p>
      </div>
      
      <!-- Error -->
      <div v-else-if="error" class="p-6 bg-red-50 border-b border-red-200">
        <p class="text-red-700">{{ error }}</p>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="tasks.length === 0" class="p-12 text-center">
        <div class="text-gray-400 text-6xl mb-4">📭</div>
        <p class="text-gray-500 text-lg">No tasks yet</p>
        <p class="text-gray-400 text-sm mt-1">Create a batch task to get started</p>
      </div>
      
      <!-- Task List -->
      <div v-else class="divide-y divide-gray-100">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="p-4 hover:bg-gray-50 transition"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center text-xl font-bold text-gray-600">
                #{{ task.id }}
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <span :class="['px-2 py-1 rounded-full text-xs font-medium', getStatusColor(task.status)]">
                    {{ task.status }}
                  </span>
                  <span class="text-sm text-gray-500">
                    {{ task.completed_terms }}/{{ task.total_terms }} terms
                  </span>
                </div>
                <p class="text-xs text-gray-400 mt-1">
                  Created: {{ formatDate(task.created_at) }}
                </p>
              </div>
            </div>
            
            <div class="flex items-center gap-2">
              <button
                @click="emit('view-task', task.id)"
                class="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition"
              >
                View
              </button>
              <button
                @click="deleteConfirm = task.id"
                class="px-3 py-1.5 bg-red-100 text-red-700 rounded-lg text-sm font-medium hover:bg-red-200 transition"
              >
                Delete
              </button>
            </div>
          </div>
          
          <!-- Progress bar -->
          <div class="mt-3 h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              class="h-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-300"
              :style="{ width: `${task.total_terms > 0 ? (task.completed_terms / task.total_terms * 100) : 0}%` }"
            ></div>
          </div>
          
          <!-- Delete Confirmation -->
          <div v-if="deleteConfirm === task.id" class="mt-3 p-3 bg-red-50 rounded-lg border border-red-200">
            <p class="text-sm text-red-700 mb-2">Are you sure you want to delete this task? This action cannot be undone.</p>
            <div class="flex gap-2">
              <button
                @click="deleteTask(task.id)"
                class="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
              >
                Yes, Delete
              </button>
              <button
                @click="deleteConfirm = null"
                class="px-3 py-1 bg-gray-200 text-gray-700 rounded text-sm hover:bg-gray-300"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Danger Zone -->
    <div class="bg-white rounded-xl shadow-lg border border-red-200 overflow-hidden">
      <div class="bg-red-600 px-6 py-4">
        <h2 class="text-lg font-bold text-white">⚠️ Danger Zone</h2>
      </div>
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <p class="font-medium text-gray-800">Backup Database</p>
            <p class="text-sm text-gray-500">Download the database file for safekeeping</p>
          </div>
          <button
            @click="downloadBackup"
            class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"
          >
            📥 Download Backup
          </button>
        </div>
        
        <hr class="my-4 border-gray-200" />
        
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium text-red-700">Reset All Data</p>
            <p class="text-sm text-gray-500">Delete all tasks, terms, and associations. This cannot be undone!</p>
          </div>
          <button
            @click="resetConfirm = true"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
          >
            🗑️ Reset Database
          </button>
        </div>
        
        <!-- Reset Confirmation Modal -->
        <div v-if="resetConfirm" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div class="bg-white rounded-xl shadow-2xl p-6 max-w-md mx-4">
            <h3 class="text-xl font-bold text-red-700 mb-2">⚠️ Confirm Database Reset</h3>
            <p class="text-gray-600 mb-4">
              This will permanently delete ALL data including:
            </p>
            <ul class="list-disc list-inside text-gray-600 mb-4 space-y-1">
              <li>All batch tasks</li>
              <li>All crawled terms</li>
              <li>All term associations</li>
              <li>All knowledge graph data</li>
            </ul>
            <p class="text-red-600 font-medium mb-4">
              This action CANNOT be undone!
            </p>
            <div class="flex gap-3">
              <button
                @click="resetAllData"
                :disabled="resetting"
                class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition"
              >
                {{ resetting ? 'Resetting...' : 'Yes, Reset Everything' }}
              </button>
              <button
                @click="resetConfirm = false"
                :disabled="resetting"
                class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
