<template>
    <h1 class="time">{{ this.Time_formatter }}</h1>
</template>

<script>

export default {
  name: "Timer_component",

  props: {
    time: Number,
  },

  mounted() {
  },

  computed: {
    Time_formatter(){
      let rem = this.time
      if (this.time == 0){
        return "00:00:00"
      }
      let hour = Math.floor(rem/3600) > 10 ? Math.floor(rem/3600) : "0" + Math.floor(rem/3600) 
      rem = rem%3600
      let min = Math.floor(rem/60) > 10 ? Math.floor(rem/60) : "0" + Math.floor(rem/60)
      rem = rem%60
      let sec = rem > 10 ? rem : "0" + rem
      return `${hour}:${min}:${sec}`
    }
  },
  
  methods: {
  },

  data(){return{
  }}

}

</script>

<style scoped>

.time{
  font-size: 35vh;
}

</style>