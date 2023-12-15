document.addEventListener('DOMContentLoaded', (event) => {
    const webcamElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('canvas');
    const canvas = canvasElement.getContext('2d');

    // Check if the browser supports getUserMedia
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                // Assign the video stream to the video element source
                webcamElement.srcObject = stream;

                // Use TensorFlow.js to load the COCO-SSD model
                cocoSsd.load()
                    .then(model => detectFrame(model));

                function detectFrame(model) {
                    // Execute detection on each frame
                    model.detect(webcamElement)
                        .then(predictions => {
                            // Draw bounding boxes on the canvas
                            canvas.clearRect(0, 0, canvasElement.width, canvasElement.height);
                            predictions.forEach(prediction => {
                                canvas.beginPath();
                                canvas.rect(prediction.bbox[0], prediction.bbox[1], prediction.bbox[2], prediction.bbox[3]);
                                canvas.lineWidth = 2;
                                canvas.strokeStyle = 'red';
                                canvas.fillStyle = 'red';
                                canvas.stroke();
                                canvas.fillText(`${prediction.class} (${Math.round(prediction.score * 100)}%)`, prediction.bbox[0], prediction.bbox[1] > 10 ? prediction.bbox[1] - 5 : 10);
                            });
                        })
                        .finally(() => requestAnimationFrame(() => detectFrame(model)));
                }
            })
            .catch((error) => {
                console.error('Error accessing the webcam:', error);
            });
    } else {
        console.error('getUserMedia is not supported by this browser');
    }
});
