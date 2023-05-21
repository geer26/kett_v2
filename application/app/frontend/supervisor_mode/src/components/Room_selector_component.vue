<template>
    <div class="modal_background">
        
        <div class="modal glassmorphism_gray"> 

            <v-text-field
              clearable
              label="Event name"
              v-model="this.room"
              :disabled="!this.conn"
              class="room_input"
              ></v-text-field>
            
            <div class="room_selection" v-if="this.room !== ''">
                <p style="color:#F57C00">JOIN</p>
                <v-switch
                  v-model="this.new_room"
                  hide-details
                  ripple="true"
                ></v-switch>
                <p style="color:#1976d2">CREATE</p>
            </div>
            
            <v-btn
              prepend-icon="fas fa-hammer"
              v-ripple
              v-if="this.new_room && this.room !== ''"
              @click="this.create_room"
              color="blue-darken-2">
              create
            </v-btn>

            <v-btn
              prepend-icon="fas fa-right-to-bracket"
              v-ripple
              v-if="!this.new_room && this.room !== ''"
              @click="this.join_room"
              color="orange-darken-2">
              join
            </v-btn>
        
        </div>

    </div>
</template>

<script>

import { socket, state  } from "@/socket"

export default {

name: "Room_selector",

mounted(){
  socket.on('room_confirmed', (data) => {
    if (data.status == 1){
      this.$emit('connect_to_room', {room_name: this.room, nemaspace: data.namespace})
      return
    } else {
      this.$emit("raise_alert", {message: data.message})
    }

  })
},

props: {
  
},

computed: {
    conn() {
      return state.connected
    }
  },

methods: {

  create_room(){
    if(!this.conn){
      this.$emit("raise_alert", {message: "Server is unavailable!"})
      return
    }
    if(this.room == "") {
      this.$emit("raise_alert", {message: "Event name must be specified!"})
      return
    }

    socket.emit('createroom', {room_name: this.room, super: true, new_room: this.new_room, station_name: 'SUPERVISOR'})
    return
  },

  join_room(){
    if(!this.conn){
      this.$emit("raise_alert", {message: "Server is unavailable!"})
      return
    }
    if(this.room == "") {
      this.$emit("raise_alert", {message: "Event name must be specified!"})
      return
    }

    socket.emit('joinroom', {room_name: this.room, super: true, new_room: this.new_room, station_name: 'SUPERVISOR'})
    return
  },

},

data(){return{
    room: "",
    new_room: true,
    state: state,
}},

}

</script>

<style scoped>


.modal_background{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    backdrop-filter: blur(5px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.modal{
    position: relative;
    width: 20%;
    padding: 10px;
    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.room_input {
        font-size: 1rem;
        font-weight: 700;
        width: 90%;
        color: var(--light_gray);
        text-align: center;
        margin: 10px;
        padding: 5px;
    }


.room_selection{
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content:space-between;
    align-items: center;
    margin: 20px;
}

.room_selection p{
  margin: 10px;
}
 
</style>