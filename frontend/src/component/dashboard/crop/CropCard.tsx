import React, { useRef, useEffect } from 'react';
import { EditOutlined, AimOutlined } from '@ant-design/icons';
import { Card, Popover } from 'antd';
import styled from "@emotion/styled";
import { Link } from "react-router-dom";
import Canvas from "./Canvas"

const { Meta } = Card;

export interface CropCardProps {
    source: any;
    title: string;
    originalImage: any;
    researchFieldData: any;
}

const CropCard = ({ source, title, originalImage, researchFieldData }: CropCardProps) => {
    // console.log("originalImage:", originalImage)
    console.log("source:", source)



    return (
        <Link to="/dashboard/segment"
            state={{ id: source.id, o_id: source.original_image_id, researchFieldData: researchFieldData }}
            style={{
                cursor: "pointer",
                width: "19%",
                height: "50%",
                marginRight: "10px",
                marginBottom: "10px"
            }}>
            <Card
                style={{
                    paddingTop: 30,
                    width: "100%",
                    height: "100%",
                }}
                hoverable
                cover={
                    <Background css={{
                        background: `url(${import.meta.env.VITE_SRC_URL}/${source.visualization_path}) no-repeat center center / contain`
                        // background: `url(http://localhost:5000/static/${source.visualization_path}) no-repeat center center / contain`
                    }}>

                    </Background>
                }
                actions={[
                    <Popover placement="topLeft" title="Crop Image Location" content={
                        <Canvas source={source} originalImage={originalImage} />
                    }><AimOutlined key="setting" /></Popover>,
                    <EditOutlined key="edit" />,
                    // <EllipsisOutlined key="ellipsis" />,
                ]}
            >

                <Meta
                    title={title}
                />
            </Card >
        </Link >
    );
}

const Background = styled.div`
    height: 100px;
    @media screen and (min-height: 800px){
        height: 200px;
    }
`
export default CropCard;
