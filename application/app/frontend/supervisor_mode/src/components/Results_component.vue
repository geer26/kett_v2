<template>
    <div class="result_container glassmorphism_gray">
        <h1>SHOW RESULTS!</h1>
        <button @click="this.$emit('close_results')">CLOSE</button>
    </div>
</template>

<script>

    export default{

        name: 'Results_component',

        mounted(){},

        props: {
            result: {}
        },

        computed: {},

        methods: {},

        data(){return{}},
    
    }

</script>

<style scoped>

.result_container{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    padding: 5px;
    /*backdrop-filter: blur(10px);
    background-color: var(--light_gray_70);*/
    z-index: 2;
    color: var(--dark_gray);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

</style>