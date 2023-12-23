<script setup lang="ts">
import Header from '../components/Header.vue';
import ResultsList from '../components/ResultsList.vue';
import Footer from '../components/Footer.vue';
</script>

<template>
    <section id="results-section">
        <Header class="header"></Header>
        <ResultsList class="results-list"/>
        <Footer></Footer>
    </section>
</template>

<style scoped>
.header {
  top: 0;
}

#results-section {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
