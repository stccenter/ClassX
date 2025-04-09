import React, { useState, useEffect } from 'react'
import { useOutletContext } from "react-router-dom";
import { Button, Modal } from 'antd';
import styled from "@emotion/styled"
import axios from 'axios'
import { useLocation } from 'react-router-dom';
import Gallery from '../../component/dashboard/crop/Gallery'
import { CropCard, CropCardContainer, CropImage } from '../../component'
import useWindowDimensions from '../../hooks/userWindowDimensions';
import useConvertToBreadcrumb from '../../hooks/useConvertToBreadcrumb';


export default function Crop() {

    const dataFromTable = useLocation()
    const originalImageID = dataFromTable.state.id;
    const researchFieldData = dataFromTable.state.data;
    console.log("researchField:", researchFieldData)
    const [breadcrumb, setBreadcrumb] = useOutletContext()
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [cardNum, setCardNum] = useState(0)
    const [data, setData] = useState([]);
    const [originalImage, setOriginalImage] = useState(null)
    const [winSize, setWinSize] = useState(useWindowDimensions())
    const [reload, setReload] = useState(false)

    useEffect(() => {
        // set up breadcrumb
        setBreadcrumb(useConvertToBreadcrumb([{ name: "Research Field", url: "/dashboard/" }, { name: researchFieldData.name, url: "/dashboard/images", state: { data: researchFieldData } }, { name: "Crop Image", url: "/dashboard/images" }]))
        axios({
            // Endpoint to send files
            url: `/api/dashboard/crop?id=${originalImageID}`,
            method: "GET",
            headers: {},
            // Attaching the form data
            data: "",
        })
            // Handle the response from backend here
            .then((res) => {
                console.log(`/api/dashboard/${originalImageID}/crop res:`, res.data)
                setData({ ...res.data.crop_image })
                setOriginalImage(res.data.original_image)
                setCardNum(res.data.crop_image.length);
                // displayCurrentStates();
            })
            // Catch errors if any
            .catch((err) => { console.log(err) });
    }, [reload])

    const reloadData = () => {
        setReload(!reload);
    }
    const showModal = () => {
        setIsModalOpen(true);

    };

    const handleOk = () => {
        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };



    const displayCurrentStates = () => {
        console.log("crop data:", data);
        // console.log("crop data[0]:", data?.at(0));
        console.log("crop cardNum:", cardNum);
        console.log("crop originalImage:", originalImage);
    }
    return (
        <Container>
            <Button type="primary" onClick={showModal} style={{
                position: "absolute",
                top: "4rem",
                right: "3rem",
            }}>
                Crop New Image
            </Button>
            <Modal title="Crop New Image" open={isModalOpen} onOk={handleOk} onCancel={handleCancel} width={winSize.width * 0.9} style={{ top: 30 }}>

                <CropImage originalImage={originalImage} winSize={winSize} reloadData={reloadData} />

            </Modal>
            <Gallery title="Crop Image Library" Card={CropCard} cardNum={cardNum} CardContainer={CropCardContainer} data={data} originalImage={originalImage} display={displayCurrentStates} researchFieldData={researchFieldData} />
        </Container>
    )
}

const Container = styled.div`
    position:relative;
    height: 92vh;
    width: 100%;
`
