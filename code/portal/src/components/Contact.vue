<template>
  <!-- Spinner -->
  <div v-if="contactForm.loading" class="custom-spinner">
    <div class="spinner"></div>
  </div>

  <!-- Contenido principal -->
  <div v-else class="contact">
    <!-- Formulario de contacto -->
    <form v-if="!contactForm.isSubmitted" @submit.prevent="handleSubmit" id="contactForm">
      <div>
        <label for="title">Título*:</label>
        <input id="title" v-model="contactForm.title" type="text" placeholder="Escribe un título" />
        <p v-if="contactForm.errors.title" class="error">{{ contactForm.errors.title }}</p>
      </div>

      <div>
        <label for="email">Email*:</label>
        <input id="email" v-model="contactForm.email" type="email" placeholder="Escribe tu email" />
        <p v-if="contactForm.errors.email" class="error">{{ contactForm.errors.email }}</p>
      </div>

      <div>
        <label for="name">Nombre*:</label>
        <input id="name" v-model="contactForm.name" type="text" placeholder="Escribe tu nombre" />
        <p v-if="contactForm.errors.name" class="error">{{ contactForm.errors.name }}</p>
      </div>

      <div>
        <label for="body">Mensaje*:</label>
        <textarea id="body" v-model="contactForm.body" placeholder="Escribe tu mensaje"></textarea>
        <p v-if="contactForm.errors.body" class="error">{{ contactForm.errors.body }}</p>
      </div>

      <!-- Contenedor de hCaptcha -->
      <div id="hcaptcha-container"></div>
      <p v-if="contactForm.errors.captcha" class="error">{{ contactForm.errors.captcha }}</p>

      <button type="submit" :disabled="!contactForm.gcaptchaLoaded">Enviar</button>
    </form>

    <!-- Mensaje de agradecimiento -->
    <div v-else class="thank-you-message">
      <h2>¡Gracias por comunicarte con nosotros!</h2>
      <p>En breves enviaremos una respuesta.</p>
    </div>
  </div>
</template>


<script>
import { onMounted } from 'vue'
import { useContactFormStore } from '@/stores/contactForm'

export default {
  setup() {
    const contactForm = useContactFormStore()

    onMounted(() => {
      contactForm.initializeHCaptcha() // Inicializa hCaptcha al montar el componente
    })

    const handleSubmit = () => {
      contactForm.submitForm(contactForm.captchaToken)
    }

    return { contactForm, handleSubmit }
  },
}
</script>
<style src="../assets/form.css"></style>
