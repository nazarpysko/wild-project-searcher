import { reactive } from 'vue'

export const store = reactive({
    searchterm: '',
    setSearchterm(newSearchterm: string) {
        this.searchterm = newSearchterm
    },

    isLoading: false,
    setLoading(loading: boolean) { this.isLoading = loading },
    results: <any>[],
    setResults(newResults: any[]) {
        this.results = newResults
        this.setLoading(false)
    }
})
