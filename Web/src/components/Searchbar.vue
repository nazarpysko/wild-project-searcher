<script setup lang="ts">
import { store } from '../store'

defineProps(['handleSearch'])

function onInput(e: Event) {
  const newSearchrterm = (e.target as HTMLInputElement).value
  store.setSearchterm(newSearchrterm)
}

function onClearInput() {
  store.setSearchterm('')
}
</script>

<template>
  <div class="searchbar-container">
    <svg focusable="false" fill="#d0d2d6">
      <path
        d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z">
      </path>
    </svg>
    <input autofocus :value="store.searchterm" @keyup.enter="handleSearch" @input="onInput">
    <svg class="clear-input-svg" focusable="false" fill="#70757a" v-if="store.searchterm !== ''" @click="onClearInput()">
      <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z">
      </path>
    </svg>
  </div>
</template>

<style scoped>
.searchbar-container {
  display: flex;
  width: 100%;
  height: min-content;
  align-items: center;
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
}

input {
  flex: 1;
  outline: none;
  border: none;
}

.clear-input-svg {
  cursor: pointer;
}
</style>
