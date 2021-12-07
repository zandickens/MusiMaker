new Vue({
  el: "#app",
  delimiters: ["${", "}"],
  data: {
    dropFiles: null,
    isLoading: false,
    isFullPage: true
  },
  methods: {
    deleteDropFile() {
      this.dropFiles = null;
    },
    uploadFile() { 
      console.log(this.dropFiles);
      var xhr=new XMLHttpRequest();
      xhr.open('post','/upload_song',true);
      const form = new FormData();
      form.append('file',this.dropFiles);
      xhr.send(form);
      xhr.onreadystatechange = function()
      {
          if (xhr.readyState == 4 && xhr.status == 200)
          {
              console.log("Redirecting.")
              window.location.href = xhr.responseURL;
          }
      };
    },
    openLoading() {
      console.log("hello world");
      this.isLoading = true
      setTimeout(() => {
          this.isLoading = false
      }, 10 * 1000)
    }
  },
});
