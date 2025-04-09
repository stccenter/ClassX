import React from 'react';
import { EditOutlined, EllipsisOutlined, SettingOutlined } from '@ant-design/icons';
import { Avatar, Card } from 'antd';
import styled from "@emotion/styled";
import { Link } from "react-router-dom";

const { Meta } = Card;
const DomainCard = ({ data }) => {
    console.log("research field data:", data)

    const setting = () => {
        console.log("Setting")
    }
    // switchResearchField use to switch research field
    return (
        <Link to="/dashboard/images"
            style={{
                cursor: "pointer",
                width: "24%",
                height: "50%",
                margin: "3px",
            }}
            state={{ data: data }}
            >
            <Card
                style={{
                    width: "100%",
                    height: "100%",
                }}
                cover={
                    <Background css={{
                        background: `url(${data.src}) no-repeat center center / cover`
                    }}>

                    </Background>
                }
                actions={[
                    <SettingOutlined key="setting" />,
                    <EditOutlined key="edit" />,
                    <EllipsisOutlined key="ellipsis" />,
                ]}
            >

                <Meta
                    title={data.name}
                />
            </Card>
        </Link>
    );
}

const Background = styled.div`
    height: 100px;
    @media screen and (min-height: 800px){
        height: 230px;
    }
`
export default DomainCard;