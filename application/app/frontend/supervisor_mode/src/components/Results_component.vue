<template>
    <div class="result_container glassmorphism_gray">

        <div class="results">
            <div v-for="res in this.sorted_result" v-bind:value="{name: res.mate_name}" :key="res.mate_name">
                <div class="result_names">
                    <p>{{ res.mate_name }}</p>
                    <p>:</p>
                    <p style="color: var(--red)">{{ res.result.name }}</p>
                </div>
                <table>
                    <tr>
                        <th>EXERCISE</th>
                        <th>WORKING WEIGHT</th>
                        <th>REPS</th>
                    </tr>
                    <tr v-for="r in res.result.results" v-bind:value="{n: r.exercise}" :key="r.exercise">
                        <td>{{ r.exercise }}</td>
                        <td class="centered">{{ r.weight }}kg</td>
                        <td class="centered">{{ r.reps }}</td>
                    </tr>
                </table>
            </div>

        </div>

        <div class="buttons-container">
            <a 
            class="btn red_btn"
            @click="this.$emit('close_results')"
            >
                <p>close</p>
            </a>

            <a class="btn green_btn" @click="this.save_result">
                <p>save result</p>
            </a>
        </div>

    </div>
</template>

<script>

    export default{

        name: 'Results_component',

        mounted(){
            console.log("all results: ", this.result)
        },

        props: {
            result: []
        },

        computed: {
            sorted_result(){
                let list = this.result
                list.sort((a,b) => a.mate_name.localeCompare(b.mate_name))
                return list
            }
        },

        methods: {

            save_result(){
                let csv = ""
                this.result.forEach(res => {
                    csv += `${res.mate_name},${res.result.name}\n`
                    csv += 'exercise, time elapsed, working weight, reps\n'
                    res.result.results.forEach(r => {
                        const row = `${r.exercise},${r.time},${r.weight},${r.reps}\n`
                        csv += row
                    })
                })
                
                let filename = "kett_result.csv"
                let element = document.createElement('a')
                element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv))
                element.setAttribute('download', filename);
                element.style.display = 'none'
                document.body.appendChild(element)
                element.click()
                document.body.removeChild(element)
            },
            
        },

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

.results{
    height: 90%;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: flex-start;
    flex-wrap: wrap;
    overflow: auto;
    font-size: 80%;
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

.result_names{
    position: relative;
    display:flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    background-color: var(--light_gray);
}

.result_names p{
    font-size: 110%;
    margin: 0;
    margin-right: 10px;
    padding-left: 10px;
}

table{
    background-color: var(--light_gray);
    padding: 10px;
}

th{
    text-align: left;
    border: 1px solid var(--dark_gray);
    padding: 5px;
}

td{
    text-align: left;
    border: 1px solid var(--dark_gray);
    padding: 5px;
}

.centered{
    text-align: center;
}

</style>