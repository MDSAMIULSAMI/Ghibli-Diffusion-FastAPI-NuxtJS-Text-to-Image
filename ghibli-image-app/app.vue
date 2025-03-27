<script setup>
const prompt = ref('')
const imageUrl = ref('')
const loading = ref(false)
const progress = ref(0)
const estimatedTime = ref('')

const generateImage = async () => {
  loading.value = true
  progress.value = 0
  estimatedTime.value = 'Estimating...'

  try {
    const response = await fetch('http://127.0.0.1:8000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: prompt.value }),
    })

    const data = await response.json()
    imageUrl.value = data.image_url

    let simulatedProgress = 0
    const progressInterval = setInterval(() => {
      simulatedProgress += 10
      progress.value = simulatedProgress
      if (simulatedProgress >= 100) {
        clearInterval(progressInterval)
        estimatedTime.value = 'Completed'
      } else {
        estimatedTime.value = `Estimated time: ${simulatedProgress}%`
      }
    }, 300)
  } catch (error) {
    console.error(error)
    loading.value = false
  }
}

const downloadImage = () => {
  const link = document.createElement('a')
  link.href = imageUrl.value
  link.download = 'generated-image.png'
  link.click()
}
</script>

<template>
  <div class="app-container">
    <div class="card">
      <h1 class="title">Ghibli Image Generator</h1>
      <input v-model="prompt" class="input-field" placeholder="Enter prompt" />
      <button @click="generateImage" class="generate-btn" :disabled="loading.value">
        <span v-if="loading.value">Generating...</span>
        <span v-else>Generate</span>
      </button>

      <div v-if="loading.value" class="spinner-container">
        <div class="spinner"></div>
        <p class="estimated-time">{{ estimatedTime }}</p>
      </div>

      <div v-if="imageUrl" class="image-container">
        <img :src="imageUrl" alt="Generated Image" class="generated-image" />
        <button @click="downloadImage" class="download-btn">Download Image</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
}

.card {
  background: #2a2a3d;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.4);
  max-width: 500px;
  width: 100%;
  text-align: center;
  backdrop-filter: blur(10px);
}

.title {
  font-size: 2.2rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 20px;
}

.input-field {
  width: 100%;
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #e1e1e1;
  font-size: 1rem;
  margin-bottom: 20px;
  transition: background-color 0.3s ease;
}

.input-field:focus {
  background: rgba(255, 255, 255, 0.2);
  border-color: #ff4081;
  outline: none;
}

.generate-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #ff4081, #ff80ab);
  border: none;
  border-radius: 8px;
  color: #ffffff;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.generate-btn:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.generate-btn:hover {
  background: linear-gradient(135deg, #ff80ab, #ff4081);
}

.spinner-container {
  margin-top: 20px;
  text-align: center;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #ff4081;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.estimated-time {
  color: #fff;
  font-size: 1rem;
}

.image-container {
  margin-top: 20px;
}

.generated-image {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  margin-top: 10px;
}

.download-btn {
  margin-top: 20px;
  padding: 12px;
  background: #4caf50;
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.download-btn:hover {
  background: #45a049;
}

@media (max-width: 768px) {
  .card {
    padding: 30px;
  }

  .title {
    font-size: 1.8rem;
  }

  .input-field {
    font-size: 0.9rem;
  }

  .generate-btn {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .card {
    padding: 20px;
  }

  .title {
    font-size: 1.5rem;
  }

  .input-field {
    font-size: 0.85rem;
  }

  .generate-btn {
    font-size: 1rem;
  }
}
</style>