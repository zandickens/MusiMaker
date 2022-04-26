// This is used to turn span items in b-table into images
// there is probably a way to do this through Vue.js but it is hard and idk how to do it

function generate_img(){
    let album_urls = document.querySelectorAll("[data-label='Album Cover']");
    if(album_urls.length === 0) {
        album_urls = document.querySelectorAll("[data-label='Cover']");
    }
    console.log(album_urls)

    for(i = 0; i <= album_urls.length; i++) {
        let link = album_urls[i].children[0].innerText;
        album_urls[i].innerHTML = ''
        
        let album_img = document.createElement('img')
        album_img.src = link;
        album_img.height = 50
        album_img.width = 50

        album_urls[i].appendChild(album_img)
    }
}

function changeForm() {
    document.getElementById('spotify_form').action = '/spotify_' + document.querySelector('input[name="selection"]:checked').id
}