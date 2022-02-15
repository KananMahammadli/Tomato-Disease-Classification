$(document).ready(function () {

    const dropArea = document.querySelector("#drop-area");
    const uploadImage = document.querySelector(".uploadImage");
    const input = document.querySelector("input");
    const submitForm = document.querySelector('#submitForm');
    const form = document.querySelector('#customForm');
    const burgerButton = document.querySelector('.burgerButton');

    let file;
    let loaded = 0;
    let total = 0;
    let percent = 0;

    const openFileSelection = async() => {
        await input.click();
    }


    $(".burgerButtonHolder").click(()=>{
        console.log("salam")
        $(".burgerButtonHolder").toggleClass("openedNav")
        $(".mobileNavigation").slideToggle()
    })

    $(".cancelUpload").click(()=>{
        refreshUploadField()
    })

    uploadImage.onclick = () => {
        openFileSelection()
        
        input.onchange = function(){
            file = (form[0].files)[0]
            console.log(file)
            sendImage(file)
            uploadProcess()
        }

    }

    const uploadProcess = () => {
        $('.imageHolder').attr('src', "../static/images/loading.svg")
        $('.texts').css({"display":"none"})
        $('.loadingArea').slideDown()
        $('.uploadImage').css({ 'display': 'none' })
        $('.predict').css({ 'display': 'inherit' })
    }

    const refreshUploadField = ()=>{
        $('.imageHolder').attr('src', "../static/images/drag_drop.svg")
        $('.texts').css({"display":"block"})
        $('.loadingArea').slideUp()
        $('.uploadImage').css({ 'display': 'inherit' })
        $('.predict').css({ 'display': 'none' })
    }


    dropArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropArea.classList.add("active");
        console.log('sag ol')
    });


    dropArea.addEventListener("dragleave", () => {
        dropArea.classList.remove("active");
    });


    dropArea.addEventListener("drop", (event) => {
        event.preventDefault();
        file = event.dataTransfer.files[0];
        sendImage(file)
        uploadProcess()
    });

    $('.predict').click(()=>{
        $(".loadingArea").css({"display":"none"})
        $(".resultArea").slideDown()
        $(".predict").css({"display":"none"})
        $(".uploadImage").css({"display":"inherit"})
    })


    const sendImage = (file) => {

        var formData = new FormData();
        formData.append('file', file)

        const config = {
            onUploadProgress: progressEvent => {
                console.log(progressEvent)
                loaded = Math.round((progressEvent.loaded / (1024 * 1024) + Number.EPSILON) * 100) / 100;
                total = Math.round((progressEvent.total / (1024 * 1024) + Number.EPSILON) * 100) / 100;
                percent = Math.floor((loaded / total) * 100);
                $(".loadingArea .imageName .name").html(file.name)
                $(".loadingArea .imageSize .size").html(`${loaded} of ${total}MB `)
                $(".loadingArea .imageSize .percent").html(`${percent}%`)
                $(".loadingArea .loadingBar .loadingStatus").animate({ 'width': `${percent}%` })

                if(percent === 100){
                    showFile()
                }

            }
        }

        console.log(percent)


        axios.post('/predict', formData, config).then(response => {

            $('.predict').css({ 'display': 'inherit' })

            if (response.status === 200) {
                $("#result").text(response.data.label)
                $("#confidenceScore").text(response.data["confidence score"])
                $('.loadingStateForButton').removeClass('loadingStateForButton')
            }
            else {
                toastr.error('Error has occured. Please try again!')
            }
        })
    }







    function showFile(){
      let fileType = file.type;
      let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
      if(validExtensions.includes(fileType)){ 
        let fileReader = new FileReader();
        fileReader.onload = ()=>{
          let fileURL = fileReader.result;
          $(".imageHolder").attr('src',fileURL) = imgTag;
        }
        fileReader.readAsDataURL(file);
      }else{
        toastr.error('Please choose image format!')
      }
    }




})