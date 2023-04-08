//https://www.w3schools.com/howto/howto_js_trigger_button_enter.asp

// Get modal container and button elements
const modalContainer = document.querySelector('.modal-container');
const modalBtn = document.querySelector('#settings-button');

// Add event listener to button to toggle modal display
modalBtn.addEventListener('click', function() {
    modalContainer.style.display = 'block';
});

// Add event listener to modal container to hide modal when clicked outside of content
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
//DrawOnEnter Convexity Defect?
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
// Create a new image element and load the image from the URL
    var image = new Image();
    image.src = imageUrl; 

// Wait for the image to load
    image.onload = function() {
        // Get a reference to the canvas element and its context
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        var existingImage = document.getElementById('lfa_image');

        // Set the canvas size to match the image size
        existingWidth = existingImage.width;
        existingHeight = existingImage.height;

        canvas.width = existingWidth
        canvas.height = existingHeight

        // Draw the image on the canvas
        context.drawImage(image, 0, 0, existingWidth, existingHeight);

        // CIRCLEDRAW?
        area = document.getElementById('min_area').value;
        radius = Math.sqrt(area / Math.PI)
        //Is linewidth wierd? changes size of circle?
        drawCircle(context, centerX, centerY, radius)
        
        //LINEDRAW?
        maxDist = document.getElementById('max_dist').value;
        drawLineFromPoint(context, centerX, centerY, parseInt(maxDist))
        

            
        // Replace the image with the modified canvas
        existingImage.src = canvas.toDataURL();

    };
}

function addDrawOnEnter(input) {
    // Execute a function when the user presses a key on the keyboard
    input.addEventListener("keypress", function(event) {
        // If the user presses the "Enter" key on the keyboard
        if (event.key === "Enter") {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
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
    //data:image/png;base64,{{ inputImage }}
    