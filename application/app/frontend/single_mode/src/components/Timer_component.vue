<template>
    <h1 class="time">{{ this.time }}</h1>
</template>

<script>

export default {
  name: "Timer_component",

  props: {
    time: Number,
  },

  mounted() {
  },
  
  methods: {
  },

  data(){return{
  }}

}

</script>

<style scoped>

.time{
  font-size: 35vh;;
}

</style>