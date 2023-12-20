import axios from 'axios'

export async function fetchResults(searchterm: string) {
    try {
        const response = await axios.put('http://localhost:5000/api/search', `query=${searchterm}`)
        return response.data
    } catch (err) { console.error(err) }
}
