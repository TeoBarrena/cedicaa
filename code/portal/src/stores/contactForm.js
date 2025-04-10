import { defineStore } from 'pinia'
import { API_URL } from '@/constants/constants'

export const useContactFormStore = defineStore('contactForm', {
  state: () => ({
    title: '',
    email: '',
    name: '',
    body: '',
    errors: {},
    isSubmitted: false,
    loading: false,
    gcaptchaLoaded: false,
    captchaToken: '',
    siteKey: 'bf96ea32-8928-4c5e-a322-3d0ec0d28e08',
  }),
  actions: {
    initializeHCaptcha() {
      const container = document.getElementById('hcaptcha-container');
      if (!container) return

      const script = document.createElement('script');
      script.src = 'https://js.hcaptcha.com/1/api.js';
      script.async = true;
      script.defer = true;

      script.onload = () => {
        window.hcaptcha.render(container, {
          sitekey: this.siteKey,
          callback: (token) => {
            this.captchaToken = token;
            this.gcaptchaLoaded = true;
          },
        })
      }

      document.head.appendChild(script);
    },
    validateForm() {
      this.errors = {}

      if (!this.title.trim()) this.errors.title = 'El título es requerido.';
      if (!this.email.trim() || !/\S+@\S+\.\S+/.test(this.email)) {
        this.errors.email = 'Debes proporcionar un email válido.';
      }
      if (!this.name.trim()) this.errors.name = 'El nombre es requerido.';
      if (!this.body.trim() || this.body.length < 11) {
        this.errors.body = 'El mensaje debe tener al menos 11 caracteres.';
      }
      if (!this.captchaToken) {
        this.errors.captcha = 'Debes completar el captcha.';
      }

      return Object.keys(this.errors).length === 0;
    },
    async submitForm(captchaToken) {
      this.captchaToken = captchaToken;

      if (!this.validateForm()) return

      this.loading = true

      try {
        if (!this.gcaptchaLoaded) {
          this.errors.captcha = 'CAPTCHA no está disponible. Intenta recargar la página.';
          this.loading = false;
          return
        }

        const formData = {
          title: this.title,
          email: this.email,
          name: this.name,
          body: this.body,
          captcha: this.captchaToken,
        }

        const response = await fetch(`${API_URL}/messages/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        })

        const result = await response.json();
        console.log(result);
        if (response.status === 201) {
          this.isSubmitted = true;
          this.resetForm();
        }
      } catch (error) {
        console.error('Error:', error);
        this.errors.captcha = 'Ocurrió un error al enviar el formulario.';
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.title = '';
      this.email = '';
      this.name = '';
      this.body = '';
      this.errors = {};
      this.loading = false;
      this.captchaToken = '';
    },
  },
})
