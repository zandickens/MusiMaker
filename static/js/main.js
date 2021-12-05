new Vue({
  el: "#app",
  delimiters: ["${", "}"],
  data: {
    dropFiles: null,
  },
  methods: {
    deleteDropFile() {
      this.dropFiles = null;
    },
    uploadFile() {
      console.log(this.dropFiles);
    },
  },
});
