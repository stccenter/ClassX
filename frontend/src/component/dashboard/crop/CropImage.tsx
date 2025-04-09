import React, { useRef, useEffect, useState } from 'react'
import styled from "@emotion/styled"
import { Button, Form, Slider, notification, Spin } from 'antd';
import axios from 'axios'


notification.config({
    placement: 'topRight',
    duration: 3,
});

export default function CropImage(props) {
    // get variables from props
    const { originalImage, winSize, reloadData, finishLoad } = props

    // REF
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const canvasZoomRef = useRef<HTMLCanvasElement>(null);
    // STATES
    const [cropImageResizeFactor, setCropImageResizeFactor] = useState(0.72)
    const [imageData, setImageData] = useState(null)
    const [xVal, setXVal] = useState(0)
    const [yVal, setYVal] = useState(0)
    const [zoomValue, setZoomValue] = useState(256)
    const [spin, setspin] = useState(true)

    // Get mouse position
    const getMousePos = (canvas, evt) => {
        let canvasCoords = canvas.getBoundingClientRect();
        return {
            x: evt.clientX - parseInt(canvasCoords.left),
            y: evt.clientY - parseInt(canvasCoords.top)
        };
    }

    // when original image is clicked, 
    //  1. put a square on image
    //  2. show crop image prew
    const setPreviewPosition = (evt) => {
        console.log("setPreviewPosition")
        console.log("evt", evt)
        if(!imageData) return;

        // get canvas of original image 
        const canvas = canvasRef.current;
        if(!canvas) return;

        let ctx = canvas.getContext("2d");
        // get canvas of zoom in window
        const canvasZoom = canvasZoomRef.current;
        if(!canvasZoom) return;

        let ctx1 = canvasZoom.getContext('2d');

        if(!ctx || !ctx1) return;

        // get mouse position on canvas of original image
        let mousePos = getMousePos(canvas, evt);
        let displayVal = getMousePos(canvas, evt);
        // delete canvas content of original image
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        // set width and height for original image(TODO set screen height 900 for temp)
        let canvas_rescaleHeight = parseFloat((winSize.height * cropImageResizeFactor).toFixed(1));
        let canvas_rescaleWidth = canvas_rescaleHeight * (imageData.width / imageData.height);
        // resize original image based on screen size
        let resizeFactor = canvas_rescaleHeight / imageData.height;
        // reverse resized data base to original data
        let resizeFactorNav = imageData.height / canvas_rescaleHeight;
        // draw new canvas content with new zoom square
        ctx.drawImage(imageData, 0, 0, imageData.width, imageData.height, 0, 0, canvas_rescaleWidth, canvas_rescaleHeight);
        // set zoom square
        ctx.beginPath();
        ctx.lineWidth = 1;
        // get zoom value 
        let zoomVal = zoomValue;
        let lenVal = parseFloat((zoomVal * resizeFactor).toFixed(1));
        //prevent box from going off the image
        let zoomClickVal = parseFloat((zoomVal * resizeFactor).toFixed(1));
        if (mousePos.x > (canvas_rescaleWidth - zoomClickVal)) {
            mousePos.x = canvas_rescaleWidth - zoomClickVal;
            displayVal.x = canvas_rescaleWidth - zoomClickVal;

        }
        if (mousePos.y > (canvas_rescaleHeight - zoomClickVal)) {
            mousePos.y = canvas_rescaleHeight - zoomClickVal;
            displayVal.y = canvas_rescaleHeight - zoomClickVal;
        }
        // TODO set x and y slider value
        setXVal(mousePos.x * resizeFactorNav);
        setYVal(mousePos.y * resizeFactorNav);

        let strokeColor = '#00FF00';
        ctx.strokeStyle = strokeColor;
        ctx.rect(mousePos.x, mousePos.y, lenVal, lenVal);
        ctx.stroke();

        ctx1.clearRect(0, 0, ctx1.canvas.width, ctx1.canvas.height);

        //zoomVal = parseInt(zoomVal)
        canvasZoom.width = zoomVal;
        canvasZoom.height = zoomVal;
        ctx1.drawImage(imageData, mousePos.x * resizeFactorNav, mousePos.y * resizeFactorNav, zoomVal, zoomVal, 0, 0, canvasZoom.width, canvasZoom.height);
    }

    // when move slider, update xVal and yVal
    const NavChange = (xval, yval) => {
        let winHeight = winSize.height;
        let canvas_rescaleHeight = (winHeight * cropImageResizeFactor).toFixed(1);
        let canvas_rescaleWidth = canvas_rescaleHeight * (imageData.width / imageData.height);
        // resize original image based on screen size
        let resizeFactor = canvas_rescaleHeight / imageData.height;
        // reverse resized data base to original data
        let resizeFactorNav = imageData.height / canvas_rescaleHeight;
        let y = (yVal * resizeFactor).toFixed(2);
        let x = (xVal * resizeFactor).toFixed(2);
        // set zoomVal as 256 for now
        let zoomVal = zoomValue * resizeFactor;

        if (y > (canvas_rescaleHeight - zoomVal)) {
            y = canvas_rescaleHeight - zoomVal;
            setYVal(imageData.height - (zoomVal * resizeFactorNav));
        }
        else {
            setYVal(yval);
        }
        if (x > (canvas_rescaleWidth - zoomVal)) {
            x = canvas_rescaleWidth - zoomVal;
            setXVal(imageData.width - (zoomVal * resizeFactorNav))
        } else {
            setXVal(xval)
        }
        const canvas = canvasRef.current;
        let ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

        ctx.drawImage(imageData, 0, 0, imageData.width, imageData.height, 0, 0, canvas_rescaleWidth, canvas_rescaleHeight);
        ctx.beginPath();
        ctx.lineWidth = "1";
        ctx.strokeStyle = '#00FF00';
        ctx.rect(x, y, zoomVal, zoomVal);
        ctx.stroke();
    }

    // update square when zoom slider change
    const rangeZoomChange = () => {
        let winHeight = winSize.height;
        // set width and height for original image
        let canvas_rescaleHeight = (winHeight * cropImageResizeFactor).toFixed(1);
        let canvas_rescaleWidth = canvas_rescaleHeight * (imageData.width / imageData.height);
        // resize original image based on screen size
        let resizeFactor = canvas_rescaleHeight / imageData.height;
        // reverse resized data base to original data
        let resizeFactorNav = imageData.height / canvas_rescaleHeight;

        let zoomVal = (zoomValue * resizeFactor).toFixed(1);
        let x = (xVal * resizeFactor).toFixed(2);
        let y = (yVal * resizeFactor).toFixed(2);
        const canvas = canvasRef.current;
        let ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.drawImage(imageData, 0, 0, imageData.width, imageData.height, 0, 0, canvas_rescaleWidth, canvas_rescaleHeight);
        ctx.beginPath();
        ctx.lineWidth = "1";
        ctx.strokeStyle = '#00FF00';
        ctx.rect(x, y, zoomVal, zoomVal);
        ctx.stroke();
    }

    // update preview canvas when zoom slider change
    const setZoomPreview = () => {
        const canvasZoom = canvasZoomRef.current;
        let ctx1 = canvasZoom.getContext("2d");
        canvasZoom.width = zoomValue;
        canvasZoom.height = zoomValue;
        ctx1.clearRect(0, 0, ctx1.canvas.width, ctx1.canvas.height);
        ctx1.drawImage(imageData, xVal, yVal, zoomValue, zoomValue, 0, 0, canvasZoom.width, canvasZoom.height);
    }

    const setDefaultZoom = (id) => {
        let winHeight = winSize.height;
        let canvas_rescaleHeight = (winHeight * cropImageResizeFactor).toFixed(1);
        let canvas_rescaleWidth = canvas_rescaleHeight * (imageData.width / imageData.height);
        // resize original image based on screen size
        let resizeFactor = canvas_rescaleHeight / imageData.height;
        // reverse resized data base to original data
        let resizeFactorNav = imageData.height / canvas_rescaleHeight;
        let y = (yVal * resizeFactor).toFixed(2);
        let x = (xVal * resizeFactor).toFixed(2);
        setZoomValue(256);
        let zoomVal = (256 * resizeFactor).toFixed(1);
        const canvas = canvasRef.current;
        const canvasZoom = canvasZoomRef.current;
        let ctx1 = canvasZoom.getContext("2d");
        const ctx = canvas.getContext('2d');
        ctx.beginPath();
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.drawImage(imageData, 0, 0, imageData.width, imageData.height, 0, 0, imageData.width * resizeFactor, imageData.height * resizeFactor);
        ctx.lineWidth = "1";
        //the preview
        ctx1.clearRect(0, 0, ctx1.canvas.width, ctx1.canvas.height);
        ctx.strokeStyle = '#00FF00';
        ctx.rect(x, y, zoomVal, zoomVal);
        ctx.stroke();
        canvasZoom.width = 256;
        canvasZoom.height = 256;
        ctx1.clearRect(0, 0, ctx1.canvas.width, ctx1.canvas.height);
        ctx1.drawImage(imageData, xVal, yVal, 256, 256, 0, 0, canvasZoom.width, canvasZoom.height);
    }

    // render preview image when slider update
    const setImagePreview = () => {

        let zoomVal = zoomValue;
        if (xVal > ((imageData.width) - zoomVal)) {
            setXVal((imageData.width) - zoomVal);
        }
        if (yVal > ((imageData.height) - zoomVal)) {
            setYVal((imageData.height) - zoomVal);

        }
        const canvasZoom = canvasZoomRef.current;
        let ctx1 = canvasZoom.getContext("2d");
        canvasZoom.width = zoomVal;
        canvasZoom.height = zoomVal;
        ctx1.clearRect(0, 0, ctx1.canvas.width, ctx1.canvas.height);
        ctx1.drawImage(imageData, xVal, yVal, zoomVal, zoomVal, 0, 0, canvasZoom.width, canvasZoom.height);
    }

    // on Crop Image button click
    const onFinish = () => {
        notification.info({
            message: 'Cropping Image Processing',
        })
        const form = new FormData();
        form.append("x", parseInt(xVal));
        form.append("y", parseInt(yVal));
        form.append("zoom", zoomValue);
        form.append("name", "jiakangliu1997@gmail.com");
        form.append("id", originalImage.id);
        form.append("crop_size", 256);


        axios({
            // Endpoint to send files
            url: "/api/saveCropImage/",
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            // Attaching the form data
            data: form,
        })
            // Handle the response from backend here
            .then((res) => {
                console.log("submit res:", res)
                notification.success({
                    message: `Image successfully cropped and store to backend.`,
                })
                reloadData()
            })
            // Catch errors if any
            .catch((err) => { console.log(err) });
    };

    const onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
    };

    // update y value when:
    //  1. slider update
    //  2. square on original image update 
    const updateYValue = (value) => {
        setYVal(value)
        NavChange(xVal, value)
        setImagePreview()
    }

    // update x value when:
    //  1. slider update
    //  2. square on original image update 
    const updateXValue = (value) => {
        setXVal(value)
        NavChange(value, yVal)
        setImagePreview()
    }

    const updateZoomVal = (value) => {
        setZoomValue(value)
        rangeZoomChange()
        setZoomPreview()
    }


    useEffect(() => {
        setspin(true)
        console.log("1")
        const canvas = canvasRef.current;
        const canvasZoom = canvasZoomRef.current;
        let ctx1 = canvasZoom.getContext("2d");
        let zoomVal = 256;
        const context = canvas.getContext('2d');
        let image = new Image();
        image.src = `${import.meta.env.VITE_SRC_URL}/${originalImage.visualization_path}`;
        // image.src = `http://localhost:5000/static/${originalImage.visualization_path}`;
        image.onload = drawImageActualSize;
        console.log("2")
        console.log(image)
        console.log("3")
        function drawImageActualSize() {
            console.log("4")
            setImageData(this);
            // calculate width and height for original image based on screen size (TODO set screen height 900 for temp)
            let canvas_rescaleHeight = (winSize.height * cropImageResizeFactor).toFixed(1);
            let canvas_rescaleWidth = (canvas_rescaleHeight * (originalImage.width / originalImage.height)).toFixed(1);
            // TODO: set range bar length of x-axis and y-axis 

            // set canvas width and height
            canvas.width = canvas_rescaleWidth;
            canvas.height = canvas_rescaleHeight;
            // cut entire original image and put on canvas
            context.drawImage(this, 0, 0, this.width, this.height, 0, 0, canvas_rescaleWidth, canvas_rescaleHeight);
            context.beginPath();
            context.lineWidth = "1";
            // set preview canvas
            canvasZoom.width = zoomVal;
            canvasZoom.height = zoomVal;
            ctx1.clearRect(0, 0, ctx1.canvas.width, ctx1.canvas.height);
            console.log("5")
            ctx1.drawImage(this, xVal, yVal, zoomVal, zoomVal, 0, 0, canvasZoom.width, canvasZoom.height);
            console.log("6")
            setspin(false)
        }
    }, [])


    return (
        <Spin tip="loading" size="large" spinning={spin}>
            <Form
                name="basic"
                wrapperCol={{
                    span: 10,
                }}
                initialValues={{
                    remember: true,
                }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
                style={{ display: "flex" }}
            >
                <div>
                    <div style={{
                        display: "flex",
                        height: `${(winSize.height * 0.72).toFixed(1)}px`,
                    }}>
                        <Form.Item
                            label="Y"
                            name="y"
                            rules={[
                                {
                                    // required: true,
                                    message: 'Please input your username!',
                                },
                            ]}
                            labelCol={{ span: 8 }}
                        >
                            <div style={{
                                display: 'inline-block',
                                height: `${(winSize.height * 0.72).toFixed(1)}px`,
                                marginRight: 10
                            }}>
                                <Slider vertical onChange={updateYValue} value={typeof yVal === 'number' ? yVal : 0} reverse={true} min={0} max={originalImage.height} />
                            </div>

                        </Form.Item>
                        <Container>
                            <canvas ref={canvasRef} onClick={setPreviewPosition} />
                            <div style={{
                                marginLeft: '9rem',
                                marginTop: '13rem',
                            }}>
                                <canvas ref={canvasZoomRef} style={{ width: 256, height: 256 }} />
                                <Form.Item
                                    wrapperCol={{
                                        offset: 8,
                                        span: 16,
                                    }}
                                >
                                    <Button type="primary" htmlType="submit">
                                        Crop Image
                                    </Button>
                                </Form.Item>
                            </div>
                        </Container>
                    </div>

                    <Form.Item
                        label="X"
                        name="x"
                        labelCol={{ span: 1 }}
                        rules={[
                            {
                                // required: true,
                                message: 'Please input your password!',
                            },
                        ]}
                    >
                        <div style={{
                            display: 'inline-block',
                            width: `${(winSize.height * 0.72 * originalImage.width / originalImage.height).toFixed(1)}px`,
                        }}>
                            <Slider onChange={updateXValue} value={typeof xVal === 'number' ? xVal : 0} defaultValue={0} min={0} max={originalImage.width} />
                        </div>
                    </Form.Item>
                    <Form.Item
                        label="Zoom"
                        name="zoom"
                        labelCol={{ span: 1 }}
                        style={{
                            margin: 0
                        }}
                    >
                        <div style={{
                            display: 'flex',
                            width: 300,
                        }}>
                            <Slider onChange={updateZoomVal} style={{ width: 300 }} value={typeof zoomValue === 'number' ? zoomValue : 0} step={256} defaultValue={0} min={0} max={3000} />
                            <Button onClick={setDefaultZoom}>Default</Button>
                        </div>
                    </Form.Item>
                </div>
            </Form>
        </Spin>
    )
}


const Container = styled.div`
    display: flex;
    justify-content: space-between;
`
