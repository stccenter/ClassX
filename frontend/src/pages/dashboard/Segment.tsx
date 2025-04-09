import React, { useState, useRef, useEffect } from 'react'
import { useOutletContext, useLocation } from "react-router-dom";
import { Modal, Spin, notification } from 'antd';
import axios from 'axios'
import styled from "@emotion/styled"
import { SegmentForm } from '../../component'
import SegmentGallery from '../../component/dashboard/segmentation/SegmentGallery';
import useWindowDimensions from '../../hooks/userWindowDimensions';
import useConvertToBreadcrumb from '../../hooks/useConvertToBreadcrumb';

notification.config({
    placement: 'topRight',
    duration: 2,
});

export default function Segment() {

    const dataFromCrop = useLocation()
    const cropImageID = dataFromCrop.state.id;
    const originalImageID = dataFromCrop.state.o_id;
    const researchFieldData = dataFromCrop.state.researchFieldData;
    const [breadcrumb, setBreadcrumb] = useOutletContext()
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [dataForm, setDataForm] = useState([]);
    const [lightAdjustment, setLightAdjustment] = useState(false)
    const [segmentImages, setSegmentImages] = useState([])
    const [winSize, setWinSize] = useState(useWindowDimensions())
    const [reload, setReload] = useState(false)
    const [spin, setSpin] = useState(true)
    const canvasRef0 = useRef(null);
    const canvasRef1 = useRef(null);
    const canvasRef2 = useRef(null);
    const canvasRef3 = useRef(null);

    const handleOk = () => {
        // console.log("dataform:", dataForm)
        setIsModalOpen(false);
        axios({
            // Endpoint to send files
            url: '/api/saveSegmentImage/',
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            // Attaching the form data
            data: dataForm,
        })
            // Handle the response from backend here
            .then((res) => {
                console.log("submit res:", res)
                setReload(!reload)
            })
            // Catch errors if any
            .catch((err) => { console.log(err) });

    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const setHistMethod = (id) => {
        let updated = false;
        let data = [...dataForm]
        data.forEach(item => {
            if (item.name === "hist_method") {
                updated = true;
                item.value = id;
            }
        })
        // console.log("id: ", id);
        // console.log("dataForm: ", dataForm);
        if (updated) {
            setDataForm(data)
        } else {
            setDataForm([...dataForm, { name: "hist_method", value: id }])
        }
    }

    const previewData = (form, LAflag) => {
        // console.log("preview Data form:", form)
        setSpin(true)
        setLightAdjustment(LAflag);
        setDataForm(form)
        setIsModalOpen(true);
        axios({
            // Endpoint to send files
            url: '/api/previewSegmentImage/',
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            // Attaching the form data
            data: form,
        }).then((res) => {
            console.log("submit res:", res)
            setSpin(false)
            const canvas0 = canvasRef0.current;
            const canvas1 = canvasRef1.current;
            const canvas2 = canvasRef2.current;
            const canvas3 = canvasRef3.current;
            let canvasRefList = [canvas0, canvas1, canvas2, canvas3,];


            res.data.forEach((item, index) => {
                // console.log("index:", index)
                // console.log("item.")
                const context = canvasRefList[index].getContext('2d');
                let img = new Image();
                img.src = `data:image/png;base64,${item.image}`
                img.onload = () => {
                    console.log("img.width", img.width)
                    console.log("img.height", img.height)
                    console.log("canvasRefList[index].width", canvasRefList[index].width)
                    console.log("canvasRefList[index].height", canvasRefList[index].height)

                    context.drawImage(img, 0, 0, img.width, img.height, 0, 0, canvasRefList[index].width, canvasRefList[index].height);
                }
            })

        }).catch((err) => { console.log(err) });
    }


    useEffect(() => {
        // set up breadcrumb
        console.log("segment breadcrumb crop ID:", cropImageID)
        setBreadcrumb(useConvertToBreadcrumb([{ name: "Research Field", url: "/dashboard/" }, { name: researchFieldData.name, url: "/dashboard/images", state: { data: researchFieldData } }, { name: "Crop Image", url: "/dashboard/crop", state: { id: originalImageID, data: researchFieldData } }, { name: "Image Segmentation", url: "/dashboard/segment" }]))
        // fetch data from backend
        axios({
            url: "/api/getSegmentImages/",
            method: "GET",
            responseType: 'json',
            headers: { 'Content-Type': 'application/json' },
            params: { "crop_image_id": cropImageID, }
        }).then((res) => {
            // console.log("res:", res)
            // console.log("res:", res.data)
            setSegmentImages(res.data)
        }).catch((err) => {
            console.log(err)
        });
    }, [reload])
    return (

        <div style={{ display: "flex", height: '92vh' }}>
            <SegmentForm previewData={previewData} cropImageID={cropImageID} />
            <Modal title="Segmented Image Preview" open={isModalOpen} onOk={handleOk} onCancel={handleCancel} width={winSize.width * 0.3} style={{ textAlign: "center" }}>
                <Spin tip="Loading..." spinning={spin} size="large">
                    <LAItem onClick={() => {
                        notification.info({
                            message: 'Default Light Adjustment is selected.',
                        })
                    }}>
                        <div>Default</div>
                        <canvas ref={canvasRef0} onClick={() => { setHistMethod(0) }} style={{ height: 256, width: 256 }} />
                    </LAItem>
                    <div style={{ display: lightAdjustment ? "block" : "none" }}>
                        <LAItem onClick={() => {
                            notification.info({
                                message: 'Histogram Equalization Light Adjustment is selected.',
                            })
                        }}>
                            <div>Histogram Equalization</div>
                            <canvas ref={canvasRef1} onClick={() => { setHistMethod(1) }} style={{ height: 256, width: 256 }} />
                        </LAItem>
                        <LAItem onClick={() => {
                            notification.info({
                                message: 'Adaptive Equalization Light Adjustment is selected.',
                            })
                        }}>
                            <div>Adaptive Equalization</div>
                            <canvas ref={canvasRef2} onClick={() => { setHistMethod(2) }} style={{ height: 256, width: 256 }} />
                        </LAItem>
                        <LAItem onClick={() => {
                            notification.info({
                                message: 'CLAHE Light Adjustment is selected.',
                            })
                        }}>
                            <div>CLAHE</div>
                            <canvas ref={canvasRef3} onClick={() => { setHistMethod(3) }} style={{ height: 256, width: 256 }} />
                        </LAItem>
                    </div>
                </Spin>
            </Modal>
            <SegmentGallery title={"Segmentation Image Library"} cardNum={segmentImages.length} data={segmentImages} />
        </div>


    )
}

const LAItem = styled.div`
    cursor: pointer;
    :hover{
        background: #c1c1c1;
    }
    
`
