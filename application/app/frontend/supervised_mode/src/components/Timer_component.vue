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
      let hour = Math.floor(rem/3600) >= 9 ? Math.floor(rem/3600) : "0" + Math.floor(rem/3600) 
      if (Math.floor(rem/3600) == 9) {hour = "09"}
      rem = rem%3600
      let min = Math.floor(rem/60) >=9 ? Math.floor(rem/60) : "0" + Math.floor(rem/60)
      if (Math.floor(rem/60) == 9) {min = "09"}
      rem = rem%60
      let sec = rem >=9 ? rem : "0" + rem
      if (rem == 9) {sec = "09"}
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
  font-size: 30vh;
}

</style>