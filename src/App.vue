<script setup lang="ts">
import { nextTick, ref } from 'vue'

// Importing service
import { fetchResults } from './services'

// Importing store
import { store } from './store'

// Importing types
import { Results } from './types'

// Importing components
import ResultsList from './components/ResultsList.vue'
import Header from './components/Header.vue';
import Searchbar from './components/Searchbar.vue';

const searchUsed = ref(false)

async function onSearch() {
  searchUsed.value = true

  store.isLoading = true

  // Need to nextTick because results-section is not rendered yet to perform the scroll
  nextTick(() => scrollToResultsSection())

  const results: Results = (await fetchResults(store.searchterm)) as Results
  store.setResults(results)

}

function scrollToResultsSection() {
  const resultsSection = document.getElementById('results-section')
  if (resultsSection) {
    resultsSection.scrollIntoView({ behavior: 'smooth' });
  }
}
</script>

<template>
  <section id="landing-section">
    <div class="img-container">
      <img src="/wild-project-logo.png" class="logo" alt="Wild Project logo" />
      <img src="/Title.png" alt="Wild Project logo" />
    </div>

    <Searchbar class="landing-searchbar" :onSearch="onSearch"></Searchbar>

    <div class="buttons-container">
      <button @click="onSearch()" :disabled="store.searchterm === ''">Search</button>
      <button :disabled="store.searchterm === ''">I'm feeling lucky</button>
    </div>
  </section>

  <section id="results-section" v-if="searchUsed">
    <Header class="header" :onSearch="onSearch"></Header>
    <ResultsList :results="store.results" :loading="store.isLoading" />
  </section>
</template>

<style scoped>
#landing-section {
  justify-content: center;
  height: 100vh;
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

.landing-searchbar {
  width: 570px;
}

.buttons-container {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin: 1em;
}

#results-section {
  min-height: 100vh;
  width: 95%;
  margin: 0 2em;
  padding-bottom: 2em;
}
</style>
