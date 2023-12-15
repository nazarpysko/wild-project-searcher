export interface Transcription {
    text: string
    timestamp: number
}

export interface Result {
    id: string
    videoURL: string
    transcriptions: Transcription[]
}

export type Results = Result[]
