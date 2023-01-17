// Just some JS to have some fun
// I believe this doesn't count towards the mark but I'll comment it anyway

changeColor(); // change color of text when page loads using this function

setInterval(() => { // Interval that runs the code in it every 600ms to change the color again
    changeColor(); // change color of text
}, 600)

function changeColor() { // this function simply sets the "style" attribute of the body to a RGB combination of 3 different numbers
    document.querySelector("body").setAttribute("style", `color: rgb(${randomNumber()}, ${randomNumber()},${randomNumber()})`)
}

function randomNumber() { // generate a random number between 0 and 254 (I believe it can never reach 255 but I also don't really care))
    return Math.floor(Math.random() * (255));
}