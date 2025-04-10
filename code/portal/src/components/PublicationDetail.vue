<template>
  <div class="publication-detail-card" v-if="publication">
    <div class="card">
      <div class="card-body">
        <h1 class="card-title">{{ publication.title }}</h1>
        <p class="date">{{ formatDate(publication.published_at) }}</p>
        <p class="card-text summary">{{ publication.summary }}</p>
        <div class="card-text content" v-html="publication.content"></div>
        <button @click="goBack" class="btn btn-primary mt-3">Volver</button>
      </div>
    </div>
  </div>
  <p v-else-if="loading">Cargando...</p>
  <p v-else class="error">{{ error }}</p>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePublicationsStore } from '../stores/publications'

const route = useRoute()
const router = useRouter()
const store = usePublicationsStore()

// Estados
const loading = ref(false)
const error = ref(null)

// Obtén el ID de la publicación desde la URL
const publicationId = computed(() => route.params.id)

// Filtra la publicación de la lista de publicaciones
const publication = computed(() => {
  return store.publications.find((pub) => pub.id === parseInt(publicationId.value))
})

// Manejo de errores si no se encuentra la publicación
onMounted(() => {
  if (!publication.value) {
    error.value = 'Publicación no encontrada. Asegúrate de que la publicación exista.'
  }
})

// Navegar de regreso a la lista de publicaciones
const goBack = () => {
  router.push('/publications')
}

// Formatear fecha
const formatDate = (date) => {
  if (!date) return 'Sin publicar'
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(date).toLocaleDateString('es-ES', options)
}
</script>

<style scoped>
.publication-detail-card {
  max-width: 800px;
  margin: 20px auto;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 16px;
  background-color: #f9f9f9;
}

.card-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.date {
  color: gray;
  font-size: 0.9rem;
  margin-bottom: 20px;
}

.card-text {
  font-size: 1rem;
}

.content {
  margin-top: 20px;
}

.btn-primary {
  padding: 10px 20px;
  font-size: 1rem;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
