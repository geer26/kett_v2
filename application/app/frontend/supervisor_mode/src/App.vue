<template>

  <Room_selector v-if="!this.connected" @connect_to_room="this.connect_to_room"/>

  <div></div>

</template>

<script>

import Room_selector from './components/Room_selector_component.vue'

export default {

  name: 'App',

  components: {
    Room_selector
  },

  methods: {
    connect_to_room(data){
      // TODO try connection
      data
      this.connected = true
    }
  },

  data(){return{
    room: null,
    connected: false,
  }}

}
</script>

<style>
</style>
