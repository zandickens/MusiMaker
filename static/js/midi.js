new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
      drumFiles: null,
      melodyFiles: null,
      isLoading: false,
      isFullPage: true
    },
    methods: {
      deleteDrumFile() {
        this.drumFiles = null;
      },
      deleteMelodyFile() {
        this.melodyFiles = null;
      },
      uploadMelodyFile() { 
        console.log(this.melodyFiles);
        var xhr=new XMLHttpRequest();
        xhr.open('post','/midi_melody_upload',true);
        const form = new FormData();
        form.append('file',this.melodyFiles);
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
      uploadDrumFile() { 
        console.log(this.drumFiles);
        var xhr=new XMLHttpRequest();
        xhr.open('post','/midi_drum_upload',true);
        const form = new FormData();
        form.append('file',this.drumFiles);
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
        //console.log("hello world");
        this.isLoading = true
        setTimeout(() => {
            this.isLoading = false
        }, 10 * 1000)
      }
    },
  });
  