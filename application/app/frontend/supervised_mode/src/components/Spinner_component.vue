<template>
    <div class="modal_back">
        <img src="../assets/img/pngegg.png" alt="bell" class="spinner_img">
    </div>
</template>

<script>

export default {

    name: "Spinner_component",

    props:{

    },

    methods: {},

    data(){return{}},

}

</script>

<style scoped>

    .modal-back{
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .spinner_img{
        max-height: 25%;
        transform-origin: 50% 70%;
        animation-name: rotate;
        animation-duration: 2s;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
    }

    @keyframes rotate {
        0% {transform: rotate(0deg);}
        25% {transform: rotate(90deg);}
        50% {transform: rotate(180deg);}
        75% {transform: rotate(270deg);}
        100% {transform: rotate(360deg);}
    }

</style>