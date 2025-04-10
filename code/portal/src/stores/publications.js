import { defineStore } from 'pinia'
import axios from 'axios'
import { API_URL } from '@/constants/constants'

/*const API_URL = import.meta.env.VITE_API_URL;*/

export const usePublicationsStore = defineStore('publicationsStore', {
    state: () => ({
        publications: [],
        loading: false,
        error: null,
        currentPage: 1,
        hasMorePages: false,
    }),
    actions: {
        async fetchPublications(page = 1) {
            try {
                this.loading = true;
                this.error = null;
                const response = await axios.get(`${API_URL}/articles/`, {
                    params: { page: page || 1 },
                });

        this.publications = response.data.data
        this.currentPage = page
        const { total, per_page } = response.data
        const totalPages = Math.ceil(total / per_page)
        this.hasMorePages = page < totalPages
      } catch {
        this.error = 'Momentanemente no se puede acceder a las noticias. Disculpe'
      } finally {
        this.loading = false
      }
    },
  },
})
