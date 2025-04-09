/*
Gallery Component 
attribute
    - title 
    - cardList
    - card component   
*/
import React, { useState, useEffect } from 'react'
import styled from '@emotion/styled'
import { Pagination, Empty } from 'antd';
import useChunkArrayInGroups from '../../../hooks/useChunkArrayInGroups'
import useConvertObjToArr from '../../../hooks/useConvertObjToArr';


export interface GalleryProps {
    title: string;
    Card: any;
    cardNum: number;
    CardContainer: any;
    data: any;
    originalImage: any;
    display: any;
    researchFieldData: any;
}

export default function Gallery({ title, Card, cardNum, CardContainer, data, originalImage, display, researchFieldData }: GalleryProps) {
    // console.log("This is Gallery")
    console.log("Gallery data: ", data.length);
    // console.log("Gallery cardNum: ", cardNum);
    // console.log("Gallery originalImage: ", originalImage);
    // display();

    const [curPage, setCurPage] = useState(1);

    const cardContainers = useChunkArrayInGroups(useConvertObjToArr(data), 10).map((group, index) => {
        // console.log("creating container")
        return (
            <CardContainer key={index} data={group} page={index + 1} curPage={curPage} Card={Card} originalImage={originalImage} researchFieldData={researchFieldData} />
        )
    });

    const pageUpdate = (page: number) => {
        setCurPage(page);
    }

    return (
        <Container>

            <div className="title">
                {title}
            </div>
            <div className="body">
                {data.length != 0 ? cardContainers : <Empty />}
            </div>
            <Pagination align="center" defaultCurrent={1} defaultPageSize={10} total={cardNum} onChange={pageUpdate} />

        </Container>
    )
}

const Container = styled.div`
    padding: 1.5rem;
    height: 100%;
    width: 100%;
    /* background: red; */
    .title{
        padding-left: 2rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
        margin-bottom: 1rem;
        font-size: 2rem;
        border-bottom: 2px solid #C9C9C9;
        
    } 
    .body{
        width: 100%;
        height:80%;
        margin-bottom: 1rem;
    }

    @media screen and (max-height: 800px){
            padding: 1rem;
            .title{
                padding-left: 2rem;
                padding-top: 0.5rem;
                margin-bottom: 1rem;
                font-size: 2rem;
            }    
        }
`


