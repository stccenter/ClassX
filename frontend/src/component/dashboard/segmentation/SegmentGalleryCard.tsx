import React, { useState, useEffect } from 'react';
import { EditOutlined, AimOutlined, InfoCircleOutlined, CheckCircleTwoTone, CloseCircleTwoTone } from '@ant-design/icons';
import { Card, Popover, Button, Modal } from 'antd';
import styled from "@emotion/styled";
import { Link } from "react-router-dom";
import useWindowDimensions from '../../../hooks/userWindowDimensions';
import SegmentLabel from "../segmentation/SegmentLabel"

const { Meta } = Card;
const SegmentGalleryCard = ({ source }) => {
    console.log("SegmentGalleryCard sourse:", source)
    const [name, setName] = useState(source.name.replace(/[^0-9|_]/g, '').split('_'))
    const [method, setMethod] = useState('')
    const [param1, setparam1] = useState({ name: "", value: 0 })
    const [param2, setparam2] = useState({ name: "", value: 0 })
    const [param3, setparam3] = useState({ name: "", value: 0 })
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [colorCluster, setColorCluster] = useState({ used: false, method: "", value: 0 })
    const [lightAdjustment, setLightAdjustment] = useState("default")
    const [winSize, setWinSize] = useState(useWindowDimensions())
    const setting = () => {
        console.log("Setting")
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

    useEffect(() => {

        if (source.segment_method == 1) { // Watershed
            setMethod("Watershed")
            setparam1({ name: "Gauss Sigma", value: source.param1 })
            setparam2({ name: "", value: source.param2 });
            setparam3({ name: "Feature Separation", value: source.param3 });
        } else if (source.segment_method == 2) { // SLIC
            setMethod("SLIC")
            setparam1({ name: "Segmentation Level", value: source.param1 });
            setparam2({ name: "Compacting", value: source.param2 });
            setparam3({ name: "Gauss Sigma", value: source.param3 });
        } else if (source.segment_method == 3) { // Quickshift
            setMethod("Quickshift")
            setparam1({ name: "Kernal Size", value: source.param1 });
            setparam2({ name: "Max Distance", value: source.param2 });
            setparam3({ name: "Gauss Sigma", value: source.param3 });
        } else if (source.segment_method == 4) { // Felzenswlb
            setMethod("Felzenswlb")
            setparam1({ name: "Gauss Sigma", value: source.param1 });
            setparam2({ name: "Scale", value: source.param2 });
            setparam3({ name: "Minimum Size", value: source.param3 });
        }

        if (source.color_method != 0) {
            setColorCluster({ used: true, method: source.color_method == 1 ? "adaptive" : "K-means", value: source.color_clusters })
        }
        if (source.light_method != 0) {
            setLightAdjustment(source.light_method == 1 ? "Histogram" : source.light_method == 2 ? "Adaptive Equalization" : "CLANE")
        }
    }, [])
    return (
        <>
            <Card
                style={{
                    cursor: "pointer",
                    width: "19%",
                    height: "50%",
                    marginRight: "10px",
                    marginBottom: "10px",
                }}
                hoverable
                cover={
                    <Background css={{
                        background: `url(${import.meta.env.VITE_SRC_URL}/${source.marked_image_path}) no-repeat center center / contain`,
                        // background: `url(http://localhost:5000/static/${source.marked_image_path}) no-repeat center center / contain`,
                        marginTop: "1rem"
                    }} />
                }
                actions={[
                    <Button type="primary" onClick={showModal}>Label Image</Button>,
                    <Popover key={"info" + source.id} placement="topRight" title="Segmentation Setting"
                        content={<ul>
                            <li> <Key>{param1.name}</Key> : <Value>{param1.value}</Value></li>
                            <li><Key>{param2.name}</Key> : <Value>{param2.value}</Value></li>
                            <li><Key>{param3.name}</Key> : <Value>{param3.value}</Value></li>
                            {colorCluster.used ?
                                <div>
                                    <li><Key>Color Cluster</Key> : <Value><CheckCircleTwoTone twoToneColor="green" /></Value></li>
                                    <li><Key>Color Cluster Method</Key> : <Value>{colorCluster.method}</Value></li>
                                    <li><Key>Color Cluster Value</Key> : <Value>{colorCluster.value}</Value></li>
                                </div>
                                :
                                <li><Key>Color Cluster</Key> : <Value><CloseCircleTwoTone twoToneColor="red" /></Value></li>}
                            <li><Key>Light Adjustment Method</Key> : <Value>{lightAdjustment}</Value></li>
                            <li><Key>Contract Stretch</Key> : <Value>{source.contrast_method == 1 ? <CheckCircleTwoTone twoToneColor="green" /> : <CloseCircleTwoTone twoToneColor="red" />}</Value></li>
                            {source.small_rem_method == 1 ?
                                <div>
                                    <li><Key>Small Feature Region</Key> : <Value><CheckCircleTwoTone twoToneColor="green" /></Value></li>
                                    <li><Key>Small Feature Region Value</Key> : <Value>{source.small_rem_threshold}</Value></li>
                                </div>
                                :
                                <li><Key>Small Feature Region</Key> : <Value><CloseCircleTwoTone twoToneColor="red" /></Value></li>}
                            {source.region_merge_method != 0 ?
                                <div>
                                    <li><Key>Region Merge</Key> : <Value><CheckCircleTwoTone twoToneColor="green" /></Value></li>
                                    <li><Key>Region Merge Method</Key> : <Value>{source.region_merge_method == 1 ? "Threshhold Cut" : source.region_merge_method == 2 ? "Normalized Cut" : "MergeHierachical"}</Value></li>
                                    <li><Key>Region Merge Value</Key> : <Value>{source.region_merge_threshold}</Value></li>
                                </div>
                                :
                                <li><Key>Region Merge</Key> : <Value><CloseCircleTwoTone twoToneColor="red" /></Value></li>}

                        </ul>
                        }><InfoCircleOutlined key="edit" /></Popover>,
                ]}
            >
                <Meta
                    title={<div style={{ position: "relative" }}>
                        {method}
                        <span style={{ position: "absolute", right: 0, bottom: 0, fontSize: "small" }}>{name[2] + '-' + name[0] + "-" + name[1]}</span>
                    </div>}
                />
            </Card >
            <Modal title="Label Image" open={isModalOpen} onOk={handleOk} onCancel={handleCancel} width={winSize.width * 0.9} destroyOnClose={true}>
                <SegmentLabel data={source} />
            </Modal>
        </>
    );
}

const Background = styled.div`
    height: 100px;
    @media screen and (min-height: 800px){
        height: 200px;
    }
`
const Key = styled.div`
    display: inline-block;
`
const Value = styled.div`
   display: inline-block;
`


export default SegmentGalleryCard;
