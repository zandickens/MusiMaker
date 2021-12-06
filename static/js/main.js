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
      fetch("/upload_song", {
        method: "POST",
        body: JSON.stringify({
          filename: this.dropFiles.name,
          data: this.dropFiles,
        }),
      });
    },
  },
});
