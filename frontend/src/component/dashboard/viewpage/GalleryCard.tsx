import React, { useState, useEffect, ReactNode } from 'react';
import { EditOutlined, AimOutlined, InfoCircleOutlined, CheckCircleTwoTone, CloseCircleTwoTone } from '@ant-design/icons';
import { Card, Popover, Button, Modal, Timeline } from 'antd';
import styled from "@emotion/styled";
import useWindowDimensions from '../../../hooks/userWindowDimensions';
import Canvas from "./Canvas"
import ImagePage from './ImagePage'
import { CroppedImage, ImageObject } from '../../util/api';
import CropImageLocation from '../../ui/CropImageLocation';
const { Meta } = Card;

// TODO: Not make these any
interface GalleryCardProps {
    source: CroppedImage
    orgImage: ImageObject[]
    segImage: any

    labelImages: any
    labelMap: any
}

const GalleryCard = ({ source, orgImage, segImage, labelImages, labelMap }: GalleryCardProps) => {
    console.log("sourse:", source)
    console.log("orgImage:", orgImage)
    console.log("segImage:", segImage)
    console.log("labelImages:", labelImages)
    console.log("labelMap:", labelMap)
    const [createDate, setCreateDate] = useState(orgImage[0].creation_date)
    const [modifiedDate, setModifiedDate] = useState(source.last_modified_date)
    const [labelImage, setLabelImage] = useState([])
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [winSize, setWinSize] = useState(useWindowDimensions())

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    useEffect(() => {
        // set created date and modified date
        const tempCreateDate = new Date(createDate);
        const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
        setCreateDate(tempCreateDate.toLocaleDateString('en-US', options))
        const tempModifiedDate = new Date(modifiedDate);
        setModifiedDate(tempModifiedDate.toLocaleDateString('en-US', options))
        // get label image 
        let tempLabelImage = labelImages.filter(image => {
            return image.segment_image_id == segImage[0].id;
        })
        setLabelImage(tempLabelImage)
    }, [])

    return (
        <Container>
            <Card
                style={{

                }}
                hoverable
                cover={
                    <Background css={{
                        background: `url(${import.meta.env.VITE_SRC_URL}/${source.visualization_path}) no-repeat center center / contain`,
                        // background: `url(http://localhost:5000/static/${source.visualization_path}) no-repeat center center / contain`,
                        marginTop: "1rem"
                    }} />
                }
                actions={[
                    <Button type="primary" onClick={showModal}>Detail</Button>,
                    <Popover placement="topLeft" title="Crop Image Location" content={
                        <CropImageLocation
                            imageUrl={`${import.meta.env.VITE_SRC_URL}/${orgImage[0].visualization_path}`}
                            size={400}
                            bottomRightX={source.width}
                            bottomRightY={source.height}
                            boxWidth={source.crop_size/2}
                            boxHeight={source.crop_size/2}
                            boxColor="#00FF00"
                            boxLineWidth={3}
                        />}>
                    <AimOutlined key="setting" /></Popover>,
                ]}
            >
                <Meta
                    title={

                        <Timeline
                            items={[
                                {
                                    children: `Image created at ${createDate}`,
                                },
                                {
                                    children: `Last modified date at ${modifiedDate}`,
                                    color: 'green'
                                },
                            ]}
                        />
                    }
                />
            </Card >
            <Modal title="View Detail" open={isModalOpen} onOk={handleOk} onCancel={handleCancel} width={winSize.width * 0.9} destroyOnClose={true}>
                <ImagePage data={source} labelImage={labelImage[0]} labelMap={labelMap} />
            </Modal>
        </Container>
    );
}

const Background = styled.div`
    height: 100px;
    @media screen and (min-height: 800px){
        height: 200px;
    }
`
const Container = styled.div`
    cursor: pointer;
    width: fit-content;
    height: 50%;
    margin-right: 10px;
    margin-bottom: 10px;
    .ant-card-body{
        padding:0;
        padding-left: 24px;
        .ant-card-meta-detail{
            margin-top:10px;
            .ant-timeline-item{
                margin-top:4px;
                padding-bottom: 10px;
            }
            .ant-timeline-item-last{
                .ant-timeline-item-content{
                    min-height:0;
                }
            }
        }
    }
`


export default GalleryCard;
