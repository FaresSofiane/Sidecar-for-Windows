
const canvas = document.querySelectorAll('canvas')[0]
const context = canvas.getContext('2d')
let lineWidth = 0
let isMousedown = false
let points = []

const img = document.getElementById('image')

document.addEventListener('DOMContentLoaded', function () {



  const socket = io('http://192.168.1.78:5000');
  const lastPoint = {x: null, y: null}



canvas.addEventListener('pointermove', (e) => {

  socket.emit('pencil', {x: e.clientX*2, y: e.clientY*2, lineWidth: lineWidth, isMousedown: isMousedown})
    lastPoint.x = e.clientX*2
    lastPoint.y = e.clientY*2


});

canvas.addEventListener('pointerenter', (e) => {
    isMousedown = true
        socket.emit('click', {x: e.clientX*2, y: e.clientY*2, lineWidth: lineWidth, isMousedown: isMousedown})




});





canvas.width = img.width
  setTimeout(() => {
        canvas.height = img.height

  }, 1000)


});