<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const emit = defineEmits(['task-created'])

const activeTab = ref('text')
const textInput = ref('')
const uploadedFile = ref(null)
const terms = ref([])
const crawlInterval = ref(3)
const loading = ref(false)
const error = ref(null)

const parsedTerms = computed(() => {
  if (!textInput.value.trim()) return []
  return textInput.value
    .split('\n')
    .map(t => t.trim())
    .filter(t => t.length > 0)
})

const updateTermsFromText = () => {
  terms.value = [...new Set(parsedTerms.value)]
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  uploadedFile.value = file
  const reader = new FileReader()
  
  reader.onload = (e) => {
    const content = e.target.result
    const fileTerms = content
      .split('\n')
      .map(line => {
        // Handle CSV format (take first column)
        if (file.name.endsWith('.csv')) {
          return line.split(',')[0].trim()
        }
        return line.trim()
      })
      .filter(t => t.length > 0 && !t.toLowerCase().startsWith('term')) // Remove header
    
    terms.value = [...new Set(fileTerms)]
  }
  
  reader.readAsText(file)
}

const removeTerm = (index) => {
  terms.value.splice(index, 1)
}

const clearAll = () => {
  terms.value = []
  textInput.value = ''
  uploadedFile.value = null
  error.value = null
}

const createBatchTask = async () => {
  if (terms.value.length === 0) {
    error.value = "Please add at least one term"
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.post('http://localhost:8000/api/batch/create', {
      terms: terms.value,
      crawl_interval: crawlInterval.value
    })
    
    emit('task-created', response.data)
    clearAll()
  } catch (err) {
    error.value = err.response?.data?.detail || "Failed to create batch task"
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
      <h2 class="text-xl font-bold text-white">📝 Batch Import</h2>
      <p class="text-blue-100 text-sm mt-1">Import multiple terms at once</p>
    </div>
    
    <!-- Tab Navigation -->
    <div class="border-b border-gray-200 bg-gray-50">
      <div class="flex">
        <button
          @click="activeTab = 'text'"
          :class="[
            'flex-1 px-6 py-3 text-sm font-medium transition-colors',
            activeTab === 'text' 
              ? 'text-blue-600 border-b-2 border-blue-600 bg-white' 
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          ]"
        >
          Text Input
        </button>
        <button
          @click="activeTab = 'file'"
          :class="[
            'flex-1 px-6 py-3 text-sm font-medium transition-colors',
            activeTab === 'file' 
              ? 'text-blue-600 border-b-2 border-blue-600 bg-white' 
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          ]"
        >
          Upload File
        </button>
      </div>
    </div>
    
    <!-- Content Area -->
    <div class="p-6">
      <!-- Text Input Tab -->
      <div v-if="activeTab === 'text'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Enter terms (one per line)
          </label>
          <textarea
            v-model="textInput"
            @input="updateTermsFromText"
            rows="8"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition font-mono text-sm"
            placeholder="Inflation&#10;Gross Domestic Product&#10;Recession&#10;..."
          ></textarea>
        </div>
      </div>
      
      <!-- File Upload Tab -->
      <div v-if="activeTab === 'file'" class="space-y-4">
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition">
          <input
            type="file"
            @change="handleFileUpload"
            accept=".txt,.csv"
            class="hidden"
            id="file-upload"
          />
          <label for="file-upload" class="cursor-pointer">
            <div class="text-gray-400 mb-2">
              <svg class="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p class="text-sm text-gray-600">
              <span class="text-blue-600 font-medium">Click to upload</span> or drag and drop
            </p>
            <p class="text-xs text-gray-500 mt-1">TXT or CSV files only</p>
            <p v-if="uploadedFile" class="text-sm text-green-600 mt-2">
              ✓ {{ uploadedFile.name }}
            </p>
          </label>
        </div>
      </div>
      
      <!-- Error Message -->
      <div v-if="error" class="mt-4 rounded-md bg-red-50 p-4 border border-red-200">
        <p class="text-sm text-red-800">{{ error }}</p>
      </div>
      
      <!-- Terms Preview -->
      <div v-if="terms.length > 0" class="mt-6">
        <div class="flex justify-between items-center mb-3">
          <h3 class="text-sm font-medium text-gray-700">
            Terms Preview ({{ terms.length }})
          </h3>
          <button
            @click="clearAll"
            class="text-xs text-red-600 hover:text-red-700 font-medium"
          >
            Clear All
          </button>
        </div>
        
        <div class="max-h-60 overflow-y-auto border border-gray-200 rounded-lg p-3 bg-gray-50 custom-scrollbar">
          <div
            v-for="(term, index) in terms"
            :key="index"
            class="flex items-center justify-between py-2 px-3 mb-1 bg-white rounded border border-gray-100 hover:border-blue-200 transition group"
          >
            <div class="flex items-center gap-2">
              <span class="text-xs font-mono text-gray-400 w-8">{{ index + 1 }}.</span>
              <span class="text-sm text-gray-800">{{ term }}</span>
            </div>
            <button
              @click="removeTerm(index)"
              class="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 transition"
            >
              ×
            </button>
          </div>
        </div>
      </div>
      
      <!-- Settings -->
      <div v-if="terms.length > 0" class="mt-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Crawl Interval (seconds)
        </label>
        <input
          v-model.number="crawlInterval"
          type="number"
          min="1"
          max="10"
          class="w-32 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
        />
        <p class="text-xs text-gray-500 mt-1">
          Wait time between each Wikipedia request (prevents blocking)
        </p>
      </div>
      
      <!-- Action Button -->
      <div v-if="terms.length > 0" class="mt-6">
        <button
          @click="createBatchTask"
          :disabled="loading"
          class="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition shadow-md hover:shadow-lg"
        >
          <span v-if="loading">Creating Task...</span>
          <span v-else>Start Batch Crawl ({{ terms.length }} terms)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
