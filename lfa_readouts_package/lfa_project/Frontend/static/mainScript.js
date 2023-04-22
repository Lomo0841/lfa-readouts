const modalContainer = document.querySelector('.modal-container');
const modalBtn = document.querySelector('#settings-button');

modalBtn.addEventListener('click', function() {
    modalContainer.style.display = 'block';
});

modalContainer.addEventListener('click', function(event) {
    if (event.target === modalContainer) {
        modalContainer.style.display = 'none';
    }
});

fileInput = document.getElementById('file_input')
if (fileInput){
    fileInput.addEventListener('change', function(){
            document.getElementById('load_form').submit();
    });
}

addDrawOnEnter(document.getElementById("center_x"))
addDrawOnEnter(document.getElementById("center_y"))
addDrawOnEnter(document.getElementById("min_area"))
addDrawOnEnter(document.getElementById("max_dist"))

document.getElementById("max_defect").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();            
    }
});

document.getElementById("kernel_size").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();            
    }
});

            
var image = document.getElementById('lfa_image');
if(image){
    image.addEventListener('click', function(event) {
        var x = event.offsetX;
        var y = event.offsetY;

        document.getElementById('center_x').value = x;
        document.getElementById('center_y').value = y;
        drawOnImage("data:image/png;base64," + inputImage, x, y);
    });
}


function drawOnImage(imageUrl, centerX, centerY) {
    var image = new Image();
    image.src = imageUrl; 

    image.onload = function() {
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        var existingImage = document.getElementById('lfa_image');

        existingWidth = existingImage.width;
        existingHeight = existingImage.height;

        canvas.width = existingWidth
        canvas.height = existingHeight

        context.drawImage(image, 0, 0, existingWidth, existingHeight);

        area = document.getElementById('min_area').value;
        radius = Math.sqrt(area / Math.PI)
        
        drawCircle(context, centerX, centerY, radius)
        
        maxDist = document.getElementById('max_dist').value;
        drawLineFromPoint(context, centerX, centerY, parseInt(maxDist))
        
        existingImage.src = canvas.toDataURL();

    };
}

function addDrawOnEnter(input) {
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            drawOnImage("data:image/png;base64," + inputImage, parseInt(document.getElementById('center_x').value), parseInt(document.getElementById('center_y').value))
        }
    });
}

function drawCircle(context, x, y, radius) {
    context.beginPath();
        context.arc(x, y, radius, 0, 2 * Math.PI, false);
        context.strokeStyle = `rgb(0,255,0)`;
        context.lineWidth = 3;    
        context.stroke();
}

function drawLineFromPoint(context, startX, startY, length) {
    endX = startX + length;
    context.beginPath();
    context.moveTo(startX, startY);
    context.lineTo(endX, startY);
    context.stroke();
}
    