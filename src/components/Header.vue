<script setup lang="ts">
import Searchbar from './Searchbar.vue';

defineProps(['onSearch'])
</script>

<template>
    <header>
        <img src="/wild-project-logo.png" alt="Wild project small logo">
        <Searchbar :onSearch="onSearch"/>
    </header>
</template>

<style scoped>
header {
    width: 100%;
    display: inline-flex;
    justify-content: center;
    gap: 2em;
    padding: 2em 0;
}

img {
    width: 50px;
    height: 50px;
}
</style>
