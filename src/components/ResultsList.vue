<script setup lang="ts">
import { Result } from '../types';
import { store } from '../store';
import LoadingSpinner from './LoadingSpinner.vue';
import ResultCard from './ResultCard.vue';

function getResultsCount() {
  return store.results.reduce((acc: number, res: Result) => acc + res.timestamps.length, 0)
}
</script>

<template>
  <div id="loading-container" v-if="store.isLoading">
    <LoadingSpinner />
    <p>Cargando</p>
  </div>
  <div v-else>
    <div v-if="store.results.length === 0">
      <img src="/dog-burning.gif" alt="Not found results">
      <h2>No se ha encontrado nada :(</h2>
    </div>
    <div v-else>
        <p id="result-performance">Se han obtenido {{ getResultsCount() }} resultados en {{ store.searchTime }} segundos</p>
        <ResultCard class="result-card" v-for="result in store.results" :result="result" />
    </div>
  </div>
</template>

<style scoped>
#loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5em;
}
.result-card:not(:last-child) {
  margin-bottom: 2em;
}

#result-performance {
  text-align: left;
  font-size: 14px;
  color: #7d7c7c;
  opacity: 0.7;
  font-weight: normal;
  border-bottom: 0.5px solid #7d7c7c;
  margin-top: 0;
}
</style>
