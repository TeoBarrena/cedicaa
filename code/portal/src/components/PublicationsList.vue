<template>
  <div class="publications">
    <h2 class="title">Noticias</h2>
    <p v-if="loading">Cargando...</p>
    <p v-if="error">{{ error }}</p>

    <!-- Listado de publicaciones -->
    <div v-if="!loading && publications.length" class="publications-list">
      <div v-for="publication in publications" :key="publication.id" class="publication-card">
        <h3>{{ publication.title }}</h3>
        <p class="date">{{ formatDate(publication.published_at) }}</p>
        <p>{{ publication.summary }}</p>
        <button @click="goToDetail(publication.id)">Ver más</button>
      </div>
    </div>
    <p v-if="!loading && !publications.length && !error">No hay publicaciones para mostrar.</p>

    <!-- Paginador -->
    <div v-if="!loading && publications.length" class="pagination">
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">Anterior</button>
      <span>Página {{ currentPage }}</span>
      <button :disabled="!hasMorePages" @click="changePage(currentPage + 1)">Siguiente</button>
    </div>
  </div>
</template>

<script setup>
import { usePublicationsStore } from '../stores/publications'
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const store = usePublicationsStore()
const { publications, loading, error } = storeToRefs(store)

// Rutas
const router = useRouter()

// Estados para el paginador
const currentPage = computed(() => store.currentPage)
const hasMorePages = computed(() => store.hasMorePages)

const fetchPublications = async (page = 1) => {
  try {
    await store.fetchPublications(page)
  } catch (error) {
    console.error(error)
  }
}

// Cambiar de página
const changePage = (page) => {
  fetchPublications(page)
}

// Formatear fecha
const formatDate = (date) => {
  if (!date) return 'Sin publicar'
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(date).toLocaleDateString('es-ES', options)
}

// Redirigir al detalle (sin implementar aún)
const goToDetail = (id) => {
  router.push({ name: 'publication', params: { id } })
}

onMounted(() => {
  fetchPublications()
})
</script>

<style scoped>
.publications {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.publications-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.publication-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.publication-card h3 {
  margin: 0 0 10px;
}

.publication-card .date {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 12px;
}

.publication-card button {
  padding: 8px 16px;
  border: none;
  background-color: #007bff;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

.publication-card button:hover {
  background-color: #0056b3;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 16px;
  border: none;
  background-color: #007bff;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination span {
  font-weight: bold;
}

/* Agregar un borde decorativo azul en la parte inferior */
.title {
  font-size: 2.5rem;
  font-weight: 700;
  color: rgb(35, 62, 134); /* Texto blanco */
  text-align: center; /* Centrado */
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 20px;
  font-family: 'Arial', sans-serif;
  position: relative;
  padding-bottom: 3px; /* Espacio para el subrayado */
}

/* Subrayado azul */
.title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 50%;
  height: 4px;
  background-color: rgb(35, 62, 134); /* Azul */
}

/* Animación para el título */
@keyframes slideIn {
  0% {
    transform: translateX(-30px);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

.title {
  animation: slideIn 0.8s ease-out;
}
</style>
