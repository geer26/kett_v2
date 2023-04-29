<template>

    <div class="result_container">

        <div class="name_container">
            <h1>{{ this.result.name }}</h1>
        </div>
        
        <div class="results">
            <table>
                <tr>
                    <th>EXERCISE</th>
                    <th>TIME ELAPSED</th>
                    <th>WORKING WEIGHT</th>
                    <th>REPS</th>
                </tr>
                <tr v-for="res in this.result.results" v-bind:value="{name: res.exercise}" :key="res.exercise">
                    <td>{{ res.exercise }}</td>
                    <td>{{ res.time }}</td>
                    <td>{{ res.weight }}</td>
                    <td>{{ res.reps }}</td>
                </tr>
            </table>
        </div>

        <div class="buttons-container">
            <a 
            class="btn red_btn"
            @click="this.$emit('close_results')"
            >
                <p>close</p>
            </a>
        </div>

    </div>

</template>

<script>
    export default {
        name: "Result_component",

        props: {
            result: {},
        },

        mounted(){
            this.save_result()
        },

        methods: {
            save_result(){
                let csv_header = 'exercise, time elapsed, working weight, reps\n'
                this.result.results.forEach( res => {
                    const row = `${res.exercise},${res.time},${res.weight},${res.reps}\n`
                    csv_header += row
                })
                console.log("RES TO SAVE:\n"+csv_header)
                
                let filename = `${this.result.name}.csv`
                let element = document.createElement('a')
                element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_header))
                element.setAttribute('download', filename);
                element.style.display = 'none'
                document.body.appendChild(element)
                element.click()
                document.body.removeChild(element)
            },
        },

        data(){return{
            csvdata: null,
            href: null
        }}

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
        backdrop-filter: blur(10px);
        background-color: var(--light_gray_70);
        z-index: 2;
        color: var(--dark_gray);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .name_container {
        width: 90%;
        max-height: 10%;
    }

    .results{
        height: 80%;
        width: 90%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        overflow: auto;
    }

    .buttons-container {
        display: flex;
        justify-content: space-around;
        width: 90%;
        max-height: 10%;
        padding: 10px;
    }

    .btn_base {
        font-weight: 600;
        font-size: 1.3rem;
        width: 20%;
        margin: 10px;
    }

    table {
        border-collapse: collapse;
        width: 100%;
    }

    th {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 8px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 600;
    }

    td {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 8px;
        text-align: center;
        font-size: 1.6rem;
    }

    tr:nth-child(even) {
        background-color: #dddddd;
    }

</style>