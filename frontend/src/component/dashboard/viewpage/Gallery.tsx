import React, { useState, useEffect } from 'react'
import styled from '@emotion/styled'
import { Pagination } from 'antd';
import useChunkArrayInGroups from '../../../hooks/useChunkArrayInGroups'
import useConvertObjToArr from '../../../hooks/useConvertObjToArr';
import GalleryContainer from './GalleryContainer';

export default function ViewGallery({ title, cardNum, cropData, orgData, segData, labelData, labelMap }) {
    console.log("cropData:", cropData)
    console.log("orgData:", orgData)
    console.log("labelMap:", labelMap)
    const [curPage, setCurPage] = useState(1);

    const cardContainers = useChunkArrayInGroups(useConvertObjToArr(cropData), 10).map((group, index) => {
        // console.log("creating container")
        return (
            <GalleryContainer key={index} data={group} page={index + 1} curPage={curPage} orgImageList={orgData} segImages={segData} labelImages={labelData} labelMap={labelMap} />
        )
    });

    const pageUpdate = (page) => {
        setCurPage(page);
    }

    return (
        <Container>

            <div className="title">
                {title}
            </div>
            <div className="body">
                {cardContainers}
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


