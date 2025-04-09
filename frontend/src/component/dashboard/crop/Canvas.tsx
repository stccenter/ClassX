import { useRef, useEffect } from 'react'



export default function Canvas(props) {
    console.log("props: ", props)
    const canvasRef = useRef<HTMLCanvasElement>(null);


    useEffect(() => {
        console.log("Canvas on effect")
        const canvas = canvasRef.current!;
        const context = canvas.getContext('2d')!;

        console.log("originalImage: ", props.originalImage)
        let image = new Image();
        image.src = `${import.meta.env.VITE_SRC_URL}/${props.originalImage.thumbnail_path}`;
        image.onload = drawImageActualSize;
        console.log(image)
        function drawImageActualSize() {
            console.log("openModel-drawImageActualSize")
            let x = props.source.width;
            let y = props.source.height;
            let OG_width = props.originalImage.width;
            let OG_height = props.originalImage.height;
            let crop_size = props.source.crop_size;
            canvas.width = OG_width / 10;
            canvas.height = OG_height / 10;


            context.fillStyle = 'red';
            context.fillRect(20, 20, 350, 100);
            // @ts-expect-error TODO: Look into a better type for this but it works
            context.drawImage(this, 0, 0, canvas.width, canvas.height);
            let rectX = (x - crop_size) / 10;
            let rectY = (y - crop_size) / 10;
            let rectWidth = crop_size / 10;
            let rectHeight = crop_size / 10;

            context.beginPath();
            context.lineWidth = 2;
            context.strokeStyle = "red";
            context.rect(rectX, rectY, rectWidth, rectHeight);
            context.stroke();
        }
    }, [])

    return (
        <canvas style={{ width: 400 }} ref={canvasRef} />
    )
}
