<script setup lang="ts">
import { nextTick, ref } from 'vue'
import ResultsList from './components/ResultsList.vue'

interface Result {
  id: string
  videoURL: string
  timestamps: string[]
}

const searchUsed = ref(false)
const searchterm = ref('')
const loading = ref(false)
const results = ref<Result[]>([])

const videos: string[] = [
  "https://www.youtube.com/watch?v=39jH02oBXIE",
  "https://www.youtube.com/watch?v=LTUUF_x5Ceg",
  "https://www.youtube.com/watch?v=ggFSisWer2c",
  "https://www.youtube.com/watch?v=k1PvPo8Qa9g",
  "https://www.youtube.com/watch?v=1IL4LgKSUzk"
]

function onInput(e: Event) {
  searchterm.value = (e.target as HTMLInputElement).value;
}

function onSearch() {
  searchUsed.value = true
  loading.value = true

  nextTick(() => scrollToResultsSection())

  setTimeout(() => {
    results.value = generateResults()
    loading.value = false
  }, 2000)
}

function scrollToResultsSection() {
  const resultsSection = document.getElementById('results-section')
  if (resultsSection) {
    resultsSection.scrollIntoView({ behavior: 'smooth' });
  }
}

function onClearInput() {
  searchterm.value = '';
}

function generateResults() {
  const length: number = Math.floor(Math.random() * 6);
  let res: Result[] = []
  for (let i = 0; i < length; i++) {
    const nTimestamps = Math.floor(Math.random() * 4) + 1;

    res.push({
      id: videos[i].split('=')[1],
      videoURL: videos[i],
      timestamps: ["00:45", "10:15", "25:02"].slice(0, nTimestamps)
    })
  }

  return res
}
</script>

<template>
  <section id="landing-section">
    <div class="img-container">
      <img src="/wild-project-logo.png" class="logo" alt="Wild Project logo" />
      <img src="/Title.png" alt="Wild Project logo" />
    </div>

    <div class="searchbar-container">
      <svg focusable="false" fill="#d0d2d6">
        <path
          d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z">
        </path>
      </svg>
      <input :value="searchterm" @input="onInput" @keyup.enter="onSearch()">
      <svg class="clear-input-svg" focusable="false" fill="#70757a" v-if="searchterm !== ''" @click="onClearInput()">
        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z">
        </path>
      </svg>
    </div>

    <div class="buttons-container">
      <button @click="onSearch()" :disabled="searchterm === ''">Search</button>
      <button :disabled="searchterm === ''">I'm feeling lucky</button>
    </div>
  </section>

  <section id="results-section" v-if="searchUsed">
    <ResultsList :results="results" :loading="loading"></ResultsList>
  </section>
</template>

<style scoped>
#landing-section {
  justify-content: center;
  height: calc(100vh - 4rem);
}

.img-container {
  margin-bottom: 1.5em;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #FFB400);
}

.searchbar-container {
  display: flex;
  width: 100%;
  align-items: center;
  margin-bottom: 1.5em;
  padding: 10px;
  padding-right: 15px;
  border: 1px solid #dfe1e5;
  box-shadow: none;
  border-radius: 24px;
  gap: 0.5em;
}

.searchbar-container:focus-within,
.searchbar-container:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.searchbar-container svg {
  height: 20px;
  width: 20px;
  color: #f2f2f2
}

input {
  flex: 1;
  outline: none;
  border: none;
}

.clear-input-svg {
  cursor: pointer;
}

.buttons-container {
  display: flex;
  gap: 10px;
  justify-content: center;
}

#results-section {
  min-height: 100vh;
  padding-top: 2em;
}
</style>
