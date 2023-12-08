<script setup lang="ts">
import LoadingSpinner from './LoadingSpinner.vue';
import ResultCard from './ResultCard.vue';
defineProps(['results', 'loading'])

</script>

<template>
  <LoadingSpinner v-if="loading"/>
  <section v-else>
    <div v-if="results.length === 0">
      <img src="/dog-burning.gif" alt="Not found results">
      <h2>No se ha encontrado nada :(</h2>
    </div>
    <div v-else class="result-card" v-for="result in results">
        <ResultCard :result="result" />
    </div>
  </section>
</template>

<style>
.result-card:not(:last-child) {
  margin-bottom: 2em;
}
</style>
