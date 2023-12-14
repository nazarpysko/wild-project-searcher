<script setup lang="ts">
import Searchbar from './Searchbar.vue';
import { useRouter } from 'vue-router'
import { store } from '../store';
const router = useRouter()

function handleSearch() {
    store.search()
    router.push('/search')
}
</script>

<template>
    <header>
        <router-link to="/"><img class="logo" src="/wild-project-logo.png" alt="Wild project small logo"></router-link>
        <Searchbar :handleSearch="handleSearch"/>
    </header>
</template>

<style scoped>
header {
    position: sticky;
    top: 0;
    width: 100%;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    gap: 2em;
    padding: 2em 0 1em 0;
    background-color: white;
    z-index: 10;
}

img {
    width: 50px;
    height: 50px;
}
</style>
