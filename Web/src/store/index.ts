import { reactive } from 'vue'

import { fetchResults } from '../services'
import { Results } from '../types'

export const store = reactive({
    searchterm: '',
    setSearchterm(newSearchterm: string) {
        this.searchterm = newSearchterm
    },

    isLoading: false,
    setLoading(loading: boolean) { this.isLoading = loading },
    results: <Results>[],
    setResults(newResults: Results) {
        this.results = newResults
        this.setLoading(false)
    },
    searchTime: '',

    async search() {
        this.setLoading(true)
        const startTime = performance.now()
        const results: Results = (await fetchResults(store.searchterm)) as Results
        store.searchTime = ((performance.now() - startTime) / 1000).toFixed(2)
        this.setResults(results)
    }
})
