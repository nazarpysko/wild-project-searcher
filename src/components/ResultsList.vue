<script setup lang="ts">
import ResultCard from './ResultCard.vue';
defineProps(['results', 'loading'])

</script>

<template>
  <p v-if="loading">cargando...</p>
  <section v-else>
    <div class="result-card" v-for="result in results">
        <ResultCard :result="result" />
    </div>
  </section>
</template>

<style>
.result-card:not(:last-child) {
  margin-bottom: 2em;
}
</style>
