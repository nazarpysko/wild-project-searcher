import axios from 'axios'

export async function fetchResults(searchterm: string) {
    const encodedParam = encodeURIComponent(searchterm)
    try {
        const response = await axios.get(`http://localhost:5000/api/search?query=${encodedParam}`)
        return response.data
    } catch (err) { console.error(err) }
}
