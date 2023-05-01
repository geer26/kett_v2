<template>

  <Room_selector v-if="!this.room"/>

  <div></div>

</template>

<script>

import Room_selector from './components/Room_selector_component.vue'

export default {
  name: 'App',
  components: {
    Room_selector
  },
  data(){return{
    room: null,
  }}
}
</script>

<style>
</style>
