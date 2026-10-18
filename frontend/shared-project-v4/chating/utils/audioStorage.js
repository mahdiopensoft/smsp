/**
 * IndexedDB Binary Audio Storage
 * Manages client-side persistent storage of custom trimmed notification and ringtone Blobs.
 * This bypasses localStorage's strict 5MB limit.
 */

const DB_NAME = 'whatsapp_clone_audio_db'
const DB_VERSION = 1
const STORE_NAME = 'audio_tracks'

class AudioStorage {
  constructor () {
    this.db = null
  }

  _getDb () {
    if (this.db) return Promise.resolve(this.db)

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION)

      request.onupgradeneeded = e => {
        const db = e.target.result
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME)
        }
      }

      request.onsuccess = e => {
        this.db = e.target.result
        resolve(this.db)
      }

      request.onerror = e => {
        reject(e.target.error)
      }
    })
  }

  /**
   * Save a binary sound Blob under a specific key
   * @param {string} key - e.g. 'custom_message_sound' or 'custom_call_sound'
   * @param {Blob} blob - The binary audio Blob to save
   */
  async saveSound (key, blob) {
    try {
      const db = await this._getDb()
      return new Promise((resolve, reject) => {
        const transaction = db.transaction(STORE_NAME, 'readwrite')
        const store = transaction.objectStore(STORE_NAME)
        const request = store.put(blob, key)

        request.onsuccess = () => resolve(true)
        request.onerror = () => reject(request.error)
      })
    } catch (e) {
      console.error('AudioStorage: saveSound failed', e)
      return false
    }
  }

  /**
   * Retrieve a stored audio Blob
   * @param {string} key - e.g. 'custom_message_sound' or 'custom_call_sound'
   * @returns {Promise<Blob|null>} The binary audio Blob or null if not found
   */
  async getSound (key) {
    try {
      const db = await this._getDb()
      return new Promise((resolve, reject) => {
        const transaction = db.transaction(STORE_NAME, 'readonly')
        const store = transaction.objectStore(STORE_NAME)
        const request = store.get(key)

        request.onsuccess = () => resolve(request.result || null)
        request.onerror = () => reject(request.error)
      })
    } catch (e) {
      console.error('AudioStorage: getSound failed', e)
      return null
    }
  }

  /**
   * Delete a stored sound Blob
   * @param {string} key
   */
  async deleteSound (key) {
    try {
      const db = await this._getDb()
      return new Promise((resolve, reject) => {
        const transaction = db.transaction(STORE_NAME, 'readwrite')
        const store = transaction.objectStore(STORE_NAME)
        const request = store.delete(key)

        request.onsuccess = () => resolve(true)
        request.onerror = () => reject(request.error)
      })
    } catch (e) {
      console.error('AudioStorage: deleteSound failed', e)
      return false
    }
  }
}

export const audioStorage = new AudioStorage()
export default audioStorage
