<template>
    <div class="popup">
        <div class="popup-inner">
            <h1>Edit List</h1>
            <h6>Select The List</h6>
            <select v-model="this.EditedList.old_name" class="form-select" aria-label="Default select example">
                <option v-for="names in a" :key="names">{{ names.lname }}</option>
            </select>
            <label>New List Name</label>
            <input type="text" v-model="EditedList.new_name">
            <br>
            <label>New Description</label>
            <input type="text" v-model="EditedList.new_description">
            <button class="btn btn-light" @click.prevent="ListEdit">Make Changes</button>
            <button class="btn btn-secondary" @click="viewchange2">Close</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ListEditPopup',
    props: { user: Number },
    data() {
        return {
            a: [{ lname: "updating" }],
            b: { a: false, SelectedList: "" },
            EditedList: { old_name: "", new_name: "", new_description: "" }
        }
    },
    async created() {
        await fetch("http://127.0.0.1:5000/" + this.user,
        {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                }
            }).then((response) => response.json()).then(data => this.a = data).catch((error) => { console.log(error) })
    },
    methods: {
        viewchange2(event) {
            this.$emit("viewchange", this.b.a)
        },
        async ListEdit() {
            await fetch('http://127.0.0.1:5000/' + this.user, {
                method: 'PATCH',
                credentials: 'include',
                body: JSON.stringify(this.EditedList),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then((json) => console.log(json)).catch((err) => console.log(err));

            this.reloadpage()

        },
        reloadpage() {
            var delayInMilliseconds = 0;

            setTimeout(function () {
                window.location.reload()
            }, delayInMilliseconds)

        },

    }
};
</script>

<style lang="scss" scoped>
.popup {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 99;
    background-color: rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
}

.popup-inner {
    background: #FFF;
    padding: 32px;
}
</style>