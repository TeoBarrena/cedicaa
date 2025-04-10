<script setup>
import WelcomeItem from './WelcomeItem.vue'
import HorseIcon from './icons/IconHorse.vue'
</script>

<template>
  <WelcomeItem>
    <template #icon>
      <HorseIcon />
    </template>
    <template #heading>Nosotros</template>

    Somos una Asociación Civil sin Fines de Lucro, fundada en 1994 en la ciudad de La Plata,
    Provincia de Buenos Aires.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <HorseIcon />
    </template>
    <template #heading>Misión</template>

    Nuestra misión es la INCLUSIÓN SOCIAL: trabajamos con la finalidad de igualar oportunidades en
    procura de la reinserción familiar, el logro de la escolaridad, la integración laboral y la
    mejora integral de la calidad de vida de nuestros alumnos y alumnas.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <HorseIcon />
    </template>
    <template #heading>Actividad</template>

    La actividad que realizamos se denomina internacionalmente Rehabilitación Ecuestre y es una
    terapia integral que apunta a la recuperación de la persona en sus dimensiones biológica,
    psíquica y social. La Rehabilitación Ecuestre utiliza al caballo de manera terapéutica,
    aprovechando las características de su naturaleza innata y de su medio ambiente como
    facilitadores del proceso rehabilitador.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <HorseIcon />
    </template>
    <template #heading>Alumnos/as</template>

    Los alumnos y alumnas del CEDICA son personas con distintos niveles de discapacidad física y/o
    mental, que pueden presentar patologías asociadas, así como individuos en situaciones de riesgo
    y vulnerabilidad social. Provienen de Institutos de Menores, Hospitales y Centros de Salud,
    otras ONG’s, barrios carenciados y/o familias vulnerables.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <HorseIcon />
    </template>
    <template #heading>Ubicación</template>
    La fundación se ecuentra en las instalaciones cedidas por el Hipódromo de La Plata, en donde
    contamos no sólo con una Nueva Pista de Actividades Ecuestres, Oficina y Salón de Capacitación,
    sino también con el alojamiento de nuestros caballos, también gracias a la generosidad de la
    Escuela de Jockeys.

    <a
      href="https://www.google.com.ar/maps/place/Hipodromo+Club+de+Tenis/@-34.9043312,-57.9504676,17.25z/data=!4m6!3m5!1s0x95a2e655273b7bb3:0xf3e488bec0a28e76!8m2!3d-34.9041378!4d-57.948066!16s%2Fg%2F1tmgdm0y?entry=ttu&g_ep=EgoyMDI0MTExMy4xIKXMDSoASAFQAw%3D%3D"
      target="_blank"
      rel="noopener"
      >Calle 44 y 115 (1900) La Plata, La Plata, B 1900, Argentina</a
    >.
  </WelcomeItem>
</template>
